# main_chatbot.py (fully refactored and cleaner version)

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

# 2. Initialize vector store once for given video ID

def init_vector_store(video_id: str):
    if video_id in vector_store_cache:
        return vector_store_cache[video_id]

    chunks = get_video_transcript_chunks(video_id)
    if not chunks:
        vector_store_cache[video_id] = None
        return None

    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embedding)
    vector_store_cache[video_id] = vector_store
    return vector_store

# 3. Retrieve context

def get_context_text(question: str, vector_store, k=4):
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
            "You are a helpful assistant specialized in answering questions based on provided transcripts.\n"
            "Use the following context to answer the user's question as accurately and completely as possible.\n"
            "If the answer is partially present, use reasoning to combine information.\n"
            "If the context does not contain enough information, respond with: 'I'm sorry, I do not have sufficient information from the transcript to answer that.'\n\n"
            "Transcript context:\n{context}"
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
    model = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)
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

def chat(session_id: str, question: str, vector_store):
    context = get_context_text(question, vector_store)
    chain = build_chain()
    response = chain.invoke(
        {"current_message": question, "context": context},
        config={"configurable": {"session_id": session_id}}
    )
    return response

# Entry point
##if __name__ == "__main__":
##    video_id = input("Enter YouTube video ID: ").strip()
##    session_id = "user1"
##
##    vector_store = init_vector_store(video_id)
##    if vector_store is None:
##        print("Transcript not available or failed to build vector store.")
##    else:
##        while True:
##            user_input = input("You: ")
##            if user_input.lower() in ['exit', 'quit']:
##                print(vector_store_cache)
##                print(store)
##                break
##            answer = chat(session_id, user_input, vector_store)
##            print(f"Bot: {answer}\n")
