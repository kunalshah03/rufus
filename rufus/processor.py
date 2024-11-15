import json
import logging
import uuid
from datetime import datetime
from time import sleep
from typing import Dict, List, Optional
from tqdm import tqdm
from openai import OpenAI
import nltk
from nltk.tokenize import sent_tokenize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.rate_limit_delay = 1
        nltk.download('punkt', quiet=True)

    def preprocess_content(self, content: str, max_length: int = 4000) -> List[str]:
        sentences = sent_tokenize(content)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) > max_length:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence)

        if current_chunk:
            chunks.append(' '.join(current_chunk))
        return chunks

    def generate_rag_prompt(self, content: str, instructions: str, metadata: Dict) -> str:
        return f"""
        Process this content for RAG system integration.
        Instructions: {instructions}
        Source URL: {metadata.get('url', 'Unknown')}
        Content: {content}

        Return strictly valid JSON matching this structure:
        {{
            "text": "Main content for embedding",
            "title": "Descriptive section title",
            "source_url": "Origin URL",
            "chunk_type": "policy|procedure|faq|general",
            "topics": ["topic1", "topic2"],
            "context": "Additional retrieval context",
            "relevance_score": 0.0 to 1.0
        }}
        """

    def process_chunk(self, chunk: str, instructions: str, metadata: Dict) -> Optional[Dict]:
        try:
            sleep(self.rate_limit_delay)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "You are a RAG content processor. Return only valid JSON."
                }, {
                    "role": "user",
                    "content": self.generate_rag_prompt(chunk, instructions, metadata)
                }],
                temperature=0.3,
                max_tokens=1000
            )

            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]

            result = json.loads(content)

            if result.get('relevance_score', 0) < 0.5:
                return None

            return {
                "id": str(uuid.uuid4()),
                "text": result["text"],
                "metadata": {
                    "title": result["title"],
                    "source_url": result["source_url"],
                    "chunk_type": result["chunk_type"],
                    "timestamp": datetime.now().isoformat(),
                    "topics": result["topics"],
                    "context": result["context"],
                    "relevance_score": result["relevance_score"]
                }
            }

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return None

    def process(self, pages: List[Dict], instructions: str = None) -> List[Dict]:
        processed_documents = []

        for page in tqdm(pages, desc="Processing pages"):
            try:
                chunks = self.preprocess_content(page['content'])
                metadata = {
                    "url": page['url'],
                    "title": page['title'],
                    "structured_data": page.get('structured_data', {})
                }

                for chunk in chunks:
                    doc = self.process_chunk(chunk, instructions, metadata)
                    if doc:
                        processed_documents.append(doc)

            except Exception as e:
                logger.error(f"Error processing page {page['url']}: {str(e)}")
                continue

        return processed_documents

    def save_to_jsonl(self, documents: List[Dict], output_file: str):
        """Save documents in JSONL format for RAG systems."""
        with open(output_file, 'w', encoding='utf-8') as f:
            for doc in documents:
                f.write(json.dumps(doc) + '\n')
