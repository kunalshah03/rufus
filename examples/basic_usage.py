from rufus import RufusClient
import logging
import os

def main():
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   try:
       output_dir = "output"
       os.makedirs(output_dir, exist_ok=True)
       output_file = os.path.join(output_dir, "scraped_content.jsonl")

       client = RufusClient()
       documents = client.scrape(
           "https://www.example.com",
           instructions="Extract main content and information"
       )

       if documents:
           # Save using built-in method
           client.processor.save_to_jsonl(documents, output_file)
           print(f"\nDocuments saved to: {output_file}")

           print("\nExtracted Documents Preview:")
           for doc in documents:
               print(f"\nTitle: {doc['metadata']['title']}")
               print(f"Text: {doc['text'][:200]}...")
               print(f"Topics: {', '.join(doc['metadata']['topics'])}")
               print(f"Type: {doc['metadata']['chunk_type']}")
               print(f"Relevance: {doc['metadata']['relevance_score']}")
               print("-" * 50)
       else:
           print("No documents were extracted")

   except Exception as e:
       logger.error(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
   main()
