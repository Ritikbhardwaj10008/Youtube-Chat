#What is no sql data base
##### we can store or retrieve the data without a sql language(and no need to store the data in the tabular format without that i can store the data and retrieve the data and dont use the sql language for any kindo of storeage or any kind of retrieval)
#TYPES OF NO-SQL databases
#1) Document databases:store data in documnet similar to JSON objects.Each document contains pairs off fields and values .Example include MongoDB and CouchDB
#2)Key value store:Every single item in the database is stored as an attribute name(or'key') together with its value.Example( Redis and DynamoDB)

#3)Wide Column store: store data in tables , rows and dynamic columns.They are optimized over queries over large datasets,and columnar storage allows for efficient data compression and dast data retrieval.Examples (Apache Cassandra and Google Bigtable)

#4) Graph databases: Designed to store and navigate relationships.They have structures comprising nodes (entities)edges(relationships),and properties .Examplse(Neo4j and amazon neptune)

####################Advantages of No-SQL DATABASES################################'
#1)scalability
#2)Distributed architecture
#3)Manage larger volumes
#4)Flexible Schema   # means on the run time we can change the schema
#5)High performance
#6)High availability and replication
#7)Development speed




################################---VECTOR DB---##################################################
# DATA IS 2TYPES   -> sturctured -> tabular data (categorical col ,numerical col)
# and unstructured data -> text ,images audio
# when we are talking about NoSQL DATABASE it is for both type of data 



### VECTOR db is designed to handle vector data -> particularly for the similarity search
## Vector data refers to data represented as high dimensional vectors ,which are often derived from complex data such as text, images or audio using feature extraction technieques.
 

# CHARACTERSTICS OT VECTOR DB
#1)sTORAGE OF High dimensional vectors
#2)Efficient Similarity search
#3)Indexing Mechanism
#4)Advanced indexing mechanism (KD-trees or ball trees,hashing based methods locality Sensitive Hashing (LHS) ,or even neural network based approaches)  


#Example for vector db
#chroma,pinecone,weaviate,milvus,faiss,Qdrant,vald,vectorflow,opensearch,pgvector,open-source vector databasse,Closed-source vector database




#combine solun(NoSQL+VectorDB)
# in real time data will be very huge 
