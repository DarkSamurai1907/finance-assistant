import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Config:
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')
    COHERE_API_KEY: str = os.environ.get('COHERE_API_KEY', '')
    FINLIGHT_API_KEY: str = os.environ.get('FINLIGHT_API_KEY', '')
    TAVILY_API_KEY: Optional[str] = os.environ.get('TAVILY_API_KEY', None)
    
    # LangSmith Configuration
    LANGSMITH_TRACING: bool = os.environ.get('LANGSMITH_TRACING', 'false').lower() == 'true'
    LANGSMITH_ENDPOINT: str = os.environ.get('LANGSMITH_ENDPOINT', 'https://api.smith.langchain.com')
    LANGSMITH_API_KEY: str = os.environ.get('LANGSMITH_API_KEY', '')
    LANGSMITH_PROJECT: str = os.environ.get('LANGSMITH_PROJECT', 'finance-assistant')
    
    @classmethod
    def validate(cls) -> bool:
        required_vars = ['OPENAI_API_KEY', 'COHERE_API_KEY', 'FINLIGHT_API_KEY']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        return True

config = Config()