# Rufus - Intelligent Web Scraper for RAG Systems

Rufus is an intelligent web scraping tool designed to prepare data for Retrieval-Augmented Generation (RAG) systems. It combines advanced web crawling capabilities with AI-powered content processing to extract and structure relevant information from websites.

---

## Features

- **Intelligent web crawling** with dynamic content support  
- **AI-driven content extraction and structuring**  
- **RAG-optimized document output**  
- **Asynchronous processing** for improved performance  
- **Rich metadata and content classification**  
- **JSONL export** for seamless RAG integration  

---

## Prerequisites

- Python 3.8+  
- OpenAI API key  

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/rufus.git
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Install Playwright browsers
   ```bash
   playwright install chromium
   ```
5. Set up environment variables
   ```bash
   cp .env.example .env
   ```
   Edit .env and add your OpenAI API key:
   ```
   RUFUS_API_KEY=your-openai-api-key
   ```
6. Install the package in development mode from the project root:
   ```
   pip install -e .
   ```
   This makes the rufus package importable while allowing you to modify the code. Run this from the directory containing setup.py.

---
## Usage
### Basic Example
#### Note: The basic example is as per the instruction provided in the task file
```bash
from rufus import RufusClient

client = RufusClient()
documents = client.scrape(
    "https://www.sfgov.com",
    instructions = "We're making a chatbot for the HR in San Francisco."
)
```
### Running the Demo
Run the following command:
```bash
python examples/basic_usage.py
```
Output will be saved in **output/scraped_content.jsonl**.

### Example Output
```bash
Processing pages:   0%|                                                                                     | 0/1 [00:00<?, ?it/s]INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Processing pages: 100%|█████████████████████████████████████████████████████████████████████████████| 1/1 [00:02<00:00,  2.75s/it]

Documents saved to: output/scraped_content.jsonl

Extracted Documents Preview:

Title: Chatbot for HR in San Francisco
Text: sfgov.com sfgov.com 2024 Copyright. All Rights Reserved. Privacy Policy...
Topics: privacy policy, copyright
Type: policy
Relevance: 0.8
```
output/scraped_content.jsonl
```json
{
  "id": "58f37f8c-9b44-42ef-bdd1-9c60720e5132",
  "text": "sfgov.com sfgov.com 2024 Copyright. All Rights Reserved. Privacy Policy",
  "metadata": {
    "title": "Chatbot for HR in San Francisco",
    "source_url": "https://www.sfgov.com",
    "chunk_type": "policy",
    "timestamp": "2024-11-15T13:49:37.555420",
    "topics": [
      "privacy policy",
      "copyright"
    ],
    "context": "Creating a chatbot for HR in San Francisco",
    "relevance_score": 0.8
  }
}

```

---

## Output Format
Documents are structured to optimize for RAG systems:
```json
{
    "id": "unique-id",
    "text": "Main content for embedding",
    "metadata": {
        "title": "Content title",
        "source_url": "Source URL",
        "chunk_type": "Content type",
        "timestamp": "ISO timestamp",
        "topics": ["topic1", "topic2"],
        "context": "Additional context",
        "relevance_score": 0.95
    }
}
```
---

## Configuration
Rufus supports the following configurable parameters:

| Parameter        | Description                  | Default |
|------------------|------------------------------|---------|
| `max_depth`      | Maximum crawling depth       | 3       |
| `max_pages`      | Maximum pages to crawl       | 100     |
| `timeout`        | Request timeout in seconds   | 30      |
| `max_concurrent` | Maximum concurrent requests  | 5       |

---

## Error Handling
- **Network errors are logged and skipped**: Handles timeouts, unreachable servers, or connection issues gracefully. These errors are logged and skipped.
- **Invalid content is filtered out**: Automatically filters out invalid or non-parsable content, ensuring only relevant data is processed.
- **Rate limiting is managed automatically**: Manages rate limits from web servers and APIs by implementing retry logic with exponential backoff.

---

## Common Issues
- **OpenAI API Error:** Check your API key in ```.env```.
- **No Content Extracted:** Verify the URL's accessibility.
- **Timeout Errors:** Adjust the timeout settings.
- **Memory Issues:** Reduce ```max_pages``` or ```max_concurrent```.

---

## Project Structure
```
rufus/
├── rufus/
│   ├── __init__.py
│   ├── client.py
│   ├── scraper.py
│   ├── processor.py
│   └── utils.py
├── examples/
│   └── basic_usage.py
├── tests/
│   └── test_rufus.py
├── .env.example
├── requirements.txt
└── README.md
```
### Description of Folders and Files

- **`rufus/`**: Main package containing the core logic of the project.
  - `__init__.py`: Initializes the package.
  - `client.py`: Module for client-related functionality.
  - `scraper.py`: Contains web scraping methods and classes.
  - `processor.py`: Handles data processing tasks.
  - `utils.py`: Helper functions shared across modules.

- **`examples/`**: Contains usage examples for understanding and testing the project.

- **`tests/`**: Unit tests to ensure the code behaves as expected.

- **`.env.example`**: Template for environment variables required for configuration.

- **`requirements.txt`**: Specifies Python dependencies for the project.

- **`README.md`**: Main documentation file for the project.

### Notes

- Ensure to create a `.env` file based on `.env.example` for local configuration.
- Run tests in the `tests/` directory before deploying or extending functionality.

---

## To Contribute to this repository:
- Fork the repository
- Create a feature branch
- Submit a pull request

---
## Author
[Kunal Shah](kunaljshah03@gmail.com)
