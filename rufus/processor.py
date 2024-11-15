from typing import List, Dict
from openai import OpenAI
import logging
import json
from .utils import chunk_text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_extraction_prompt(self, content: str, instructions: str) -> str:
        return f"""
        Given the following web content and instructions, extract and structure the relevant information.
        Create a well-organized document that can be used for RAG applications.

        Instructions: {instructions}

        Content:
        {content}

        Return the content in the following JSON format:
        {{
            "title": "Brief title describing the content",
            "summary": "Brief summary of the key points",
            "content": "Main extracted content, relevant to the instructions",
            "metadata": {{
                "topics": ["relevant", "topics", "covered"],
                "relevance_score": 0-1 score indicating relevance to instructions
            }}
        }}
        """

    def process_chunk(self, chunk: str, instructions: str) -> Dict:
    # """Process a single chunk of content using GPT."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Changed from gpt-4-turbo-preview
                messages=[{
                    "role": "system",
                    "content": "You are a content extraction AI that processes web content into structured documents for RAG systems."
                }, {
                    "role": "user",
                    "content": self.generate_extraction_prompt(chunk, instructions)
                }],
                temperature=0.3
            )

            try:
                content = response.choices[0].message.content
                return json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse GPT response as JSON: {e}")
                return None

        except Exception as e:
            logger.error(f"Error processing chunk: {str(e)}")
            return None

    def process(self, pages: List[Dict], instructions: str = None) -> List[Dict]:
        processed_documents = []

        for page in pages:
            try:
                chunks = chunk_text(page['content'], max_length=4000)

                for chunk in chunks:
                    processed = self.process_chunk(chunk, instructions)
                    if processed:
                        if 'metadata' in processed:
                            processed['metadata']['source_url'] = page['url']
                        processed_documents.append(processed)
                    else:
                        logger.warning(f"Failed to process chunk from {page['url']}")

            except Exception as e:
                logger.error(f"Error processing page {page['url']}: {str(e)}")
                continue

        return processed_documents
