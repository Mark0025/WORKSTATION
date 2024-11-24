from dotenv import load_dotenv
import os
from openai import OpenAI
from loguru import logger

# Load environment variables
load_dotenv()

def test_openai():
    """Simple test of OpenAI API using latest client format"""
    try:
        # Initialize the client with ONLY the API key, no org ID
        client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            organization=None  # Explicitly set to None to override any default
        )
        
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a quick joke about programming"}
            ]
        )
        
        # Get the response content
        joke = response.choices[0].message.content
        
        logger.success("✅ OpenAI API key is working!")
        print(f"Response from API: {joke}")
        return True
        
    except Exception as e:
        logger.error(f"❌ OpenAI API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Testing OpenAI API key...")
    test_openai()