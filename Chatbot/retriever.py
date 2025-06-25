from convert_chunks_to_vectors import create_vector_store

##vector_store=create_vector_store()
##retriever=vector_store.as_retriever(search_type="similarity",search_kwargs={"k":4})
### retriever khud mai ek runnable function hota hai to uspr invoke function hota hai 
##
##retrieved_doc=retriever.invoke(question)
##
##context_text="\n\n".join(doc.page_content for doc in retrieved_doc)





def get_context_text( question, k=4):
    """Get context text from video transcript."""
    vector_store = create_vector_store()
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    retrieved_doc = retriever.invoke(question)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_doc)
    return context_text

#hii=retriever.invoke("what is deepmind")
#print(hii)