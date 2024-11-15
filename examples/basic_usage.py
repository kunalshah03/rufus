from rufus import RufusClient

def main():
    # Initialize client
    client = RufusClient()

    # Example: Scraping HR information
    documents = client.scrape(
    "https://www.sfgov.com",  # Government site as mentioned in case study
    instructions="Find information about HR policies and employee benefits"
)

    # Print results
    for doc in documents:
        print(f"\nTitle: {doc['title']}")
        print(f"Summary: {doc['summary']}")
        print(f"Topics: {', '.join(doc['metadata']['topics'])}")
        print(f"Relevance: {doc['metadata']['relevance_score']}")

if __name__ == "__main__":
    main()
