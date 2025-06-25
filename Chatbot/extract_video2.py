from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_video_transcript_chunks(video_id: str, language: str = "en", chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Fetches transcript from YouTube video and splits it into text chunks.
    
    Args:
        video_id (str): YouTube video ID
        language (str): Preferred transcript language code (default: "en")
        chunk_size (int): Max characters per chunk
        chunk_overlap (int): Overlap between chunks

    Returns:
        List of LangChain Document chunks (text + metadata)
    """
    
    try:
        # Get the transcript in the specified language
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)

    except NoTranscriptFound:
        print(f"No transcript found in language '{language}' for video {video_id}")
        return []
    except TranscriptsDisabled:
        print("Captions are disabled for this video.")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

    # Split the transcript into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.create_documents([transcript])
    
    return chunks
