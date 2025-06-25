from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser 
import os

from langchain_core.chat_history import InMemoryChatMessageHistory   # in this particular class they have defined on list (so the entire conversation we record insidt that particular list(and we can manage the differrent different conversations as well)(means 2 different persons chat history we can manage in this(in similar manner chat gpt)))
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


from langchain_core.runnables import RunnableParallel,RunnablePassthrough,RunnableLambda


from extract_video2 import get_video_transcript_chunks


from retriever import get_context_text
context_text=get_context_text()   # we have the give the question here 

from prompt_template import get_default_prompt
prompt=get_default_prompt()



load_dotenv()

model= ChatOpenAI(model='gpt-4o-mini',temperature=0)








parser=StrOutputParser()
store={}  # this is my dictionary




def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]

 # here i create configuration id's

chain=prompt| model|parser
chain_with_memory=RunnableWithMessageHistory(chain,
                                             get_session_history,
                                             input_messages_key="current_message",
                                             history_messages_key="history",
                                             
)   # model and particular method in this function RunnableWithMessageHistory





# To invoke the chain with session ID and input message:
def chat(session_id: str, user_message: str):
    config = {"configurable": {"session_id": session_id}}

    response = chain_with_memory.invoke(
        {"current_message": user_message,
         "context":context_text},
        config=config
    )
    return response


print(store)






















if __name__ == "__main__":
    video="DB9mjd-65gw"
    session_id = "my_first_chat"
    print("Chatbot started! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = chat(session_id, user_input)
        print("Assistant:", response)

print(store)

















# in streamlit api integration