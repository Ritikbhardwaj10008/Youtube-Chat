# main_chatbot.py (fully corrected and production-ready)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Memory store for sessions
store = {}
vector_store_cache = {}  # Cache vector stores by video_id

# 1. Extract transcript and chunk

def get_video_transcript_chunks(video_id: str, language: str = "en", chunk_size: int = 1000, chunk_overlap: int = 200):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)
    except (NoTranscriptFound, TranscriptsDisabled, Exception) as e:
        print(f"Transcript error: {e}")
        return []

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents([transcript])

# 2. Build vector store

def create_vector_store(video_id: str):
    chunks = get_video_transcript_chunks(video_id)
    if not chunks:
        return None
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(chunks, embedding)

# 3. Retrieve context

def get_context_text(video_id: str, question: str, k=4):
    if video_id not in vector_store_cache:
        vector_store_cache[video_id] = create_vector_store(video_id)
    vector_store = vector_store_cache[video_id]
    if vector_store is None:
        return ""

    docs = vector_store.similarity_search(question, k=k)

    if not docs:
        return "No relevant context found."

    return "\n\n".join(doc.page_content for doc in docs)

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

# 6. Build chain with memory

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

# 7. Full chat function

def chat(video_id: str, session_id: str, question: str):
    context = get_context_text(video_id, question)
    chain = build_chain()
    response = chain.invoke(
        {"current_message": question, "context": context},
        config={"configurable": {"session_id": session_id}}
    )
    return response

# Entry point
if __name__ == "__main__":
    video_id = input("Enter YouTube video ID: ").strip()
    session_id = "user1"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        answer = chat(video_id, session_id, user_input)
        print(f"Bot: {answer}\n")