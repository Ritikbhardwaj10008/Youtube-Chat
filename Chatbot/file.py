# main_chatbot.py

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from paddleocr import PaddleOCR
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import layoutparser as lp
import fitz
import cv2
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

store = {}  # session memory store

# 1. Extract transcript from video and chunk it
def get_video_transcript_chunks(video_id: str, language: str = "en", chunk_size: int = 1000, chunk_overlap: int = 200):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        print(f"Transcript error: {e}")
        return []

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents([transcript])

# 2. Create FAISS vector store from chunks
def create_vector_store(video_id: str):
    chunks = get_video_transcript_chunks(video_id)
    if not chunks:
        return None
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embedding)

# 3. Retrieve context using similarity search
def get_context_text(video_id: str, question: str, k=4):
    vector_store = create_vector_store(video_id)
    if vector_store is None:
        return ""
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    retrieved_doc = retriever.invoke(question)
    return "\n\n".join(doc.page_content for doc in retrieved_doc)

# 4. Prompt template
def get_default_prompt():
    return ChatPromptTemplate.from_messages([
        ('system', (
            "You are a helpful assistant. Use only the information provided in the context below to answer questions. "
            "If the context is insufficient or does not contain the answer, say you don't know.\n\n"
            "Context:\n{context}"
        )),
        MessagesPlaceholder(variable_name="history"),
        ('human', "{current_message}")
    ])

# 5. Session memory

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 6. Chain creation
def build_chain():
    model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    parser = StrOutputParser()
    prompt = get_default_prompt()
    chain = prompt | model | parser
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="current_message",
        history_messages_key="history"
    )

# 7. Chat function

def chat(video_id: str, session_id: str, question: str):
    context = get_context_text(video_id, question)
    chain = build_chain()
    response = chain.invoke(
        {"current_message": question, "context": context},
        config={"configurable": {"session_id": session_id}}
    )
    return response

# Example usage:
if __name__ == "__main__":
    video_id = input("Enter YouTube video ID: ").strip()
    session_id = "user1"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        answer = chat(video_id, session_id, user_input)
        print(f"Bot: {answer}\n")
