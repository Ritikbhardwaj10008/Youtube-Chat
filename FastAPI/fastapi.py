
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()


from Chatbot.file4 import init_vector_store, chat, vector_store_cache

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    video_id: str
    question: str

@app.get("/")
def Hello():
    return {'message':'Youtube Chat'}

@app.get('/about')
def About():
    return {'message':'A fully fuctional API chatbot to chat with youtube video'}

@app.post("/chat")
def chat_api(req: ChatRequest):
    if req.video_id not in vector_store_cache:
        init_vector_store(req.video_id)
    
    vector_store = vector_store_cache.get(req.video_id)
    if vector_store is None:
        raise HTTPException(status_code=404, detail="Transcript not available.")
    
    answer = chat(req.session_id, req.question, vector_store)
    return {"answer": answer}