# we are using FAISS vector store
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from extract_video2 import get_video_transcript_chunks

##transcript=get_video_transcript_chunks(video_id)
##embedding=OpenAIEmbeddings(model="text-embedding-3-small")
##
##vector_store=FAISS.from_documents(transcript,embedding)





def create_vector_store():
    """Create and return a FAISS vector store from video transcript."""
    chunks=get_video_transcript_chunks()
    
    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embedding)
    return vector_store
# this sotre every chunk with different ids

#print(transcript)
#ids=vector_store.index_to_docstore_id
#print(ids)
#print(vector_store.get_by_ids([ids[0]]))
