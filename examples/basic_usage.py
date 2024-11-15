from rufus import RufusClient
import json

def main():
    client = RufusClient()
    documents = client.scrape(
        "https://www.sfgov.com",
        instructions="Find information about HR policies and employee benefits"
    )

    if documents:
        print("\nExtracted Documents:")
        for doc in documents:
            print(f"\nTitle: {doc['metadata']['title']}")
            print(f"Text: {doc['text'][:200]}...")
            print(f"Topics: {', '.join(doc['metadata']['topics'])}")
            print(f"Type: {doc['metadata']['chunk_type']}")
            print(f"Source: {doc['metadata']['source_url']}")
            print(f"Relevance: {doc['metadata']['relevance_score']}")
            print("-" * 50)
    else:
        print("No documents were extracted")

if __name__ == "__main__":
    main()
