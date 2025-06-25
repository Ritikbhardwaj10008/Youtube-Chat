from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder







#def get_default_prompt():
#    prompt = ChatPromptTemplate.from_messages(
#        [
#            ('system', 'You are a helpful assistant. Answer Only from the provided transcript context.If the context is insufficient just say you donot know'),
#            MessagesPlaceholder(variable_name="history"),
#            ('human',"{current_message}")
#            
#        ]
#    )
#    return prompt


def get_default_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            # Use context explicitly in the system message
            ('system', (
                "You are a helpful assistant. Use only the information provided in the context below to answer questions. "
                "If the context is insufficient or does not contain the answer, say you don't know.\n\n"
                "Context:\n{context}"
            )),
            MessagesPlaceholder(variable_name="history"),
            ('human', "{current_message}")
        ]
    )
    return prompt





