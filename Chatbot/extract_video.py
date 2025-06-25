#pip install -q youtube-transcript-api langchain-community langchain-openai \
#               faiss-cpu tiktoken python-dotenv
 
from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

video_id="DB9mjd-65gw"
try:
    # if you dont care which language ,this results the best one
    transcript_list=YouTubeTranscriptApi.get_transcript(video_id,languages=["en"])
    # Youtube transcript api give transcript sentence by sentence in one frame (so in next line we join the transcript at all)
    # flattent it to plain text
    transcript=" ".join(chunk["text"] for chunk in transcript_list)
    print(transcript)

except TranscriptsDisabled:
    print("No captions available for this video")


# Now text splitting
splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks=splitter.create_documents([transcript])


