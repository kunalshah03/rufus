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
   cd rufus
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
   # Edit .env and add your OpenAI API key:
   RUFUS_API_KEY=your-openai-api-key
   ```
   
