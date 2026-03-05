# Research Paper Summarizer

An intelligent PDF extraction and summarization tool that leverages NVIDIA's API models to extract text from research papers and generate concise summaries.

## Features

- **Intelligent PDF Text Extraction**: Uses NVIDIA's Nemotron Parse model to extract text from PDF pages with tool calling
- **Concurrent Processing**: Processes multiple pages in parallel (5 concurrent workers) for faster extraction
- **Smart Caching**: Caches extracted text based on PDF file hash to avoid redundant API calls
- **AI-Powered Summarization**: Generates summaries using NVIDIA's Nemotron Nano 9B model
- **Structured Block Parsing**: Extracts and preserves text blocks from document structure

## Requirements

- Python 3.7+
- NVIDIA API key (`NGC_API_KEY`)
- Prompt
- PDF file to process

## Installation

1. Install dependencies:
```bash
pip install requests pypdfium2 python-dotenv
```

2. Create a `.env` file in the project root:
```
NGC_API_KEY=your_nvidia_api_key_here
```

## Usage

Run the summarizer:

```bash
python main.py
```

The tool will:
1. Read and process `europa.pdf` (or modify the filename in `main.py`)
2. Extract text from all pages using parallel processing
3. Cache the extracted text in `.cache/`
4. Generate a summary and save it to `summary.md`

## Architecture

### PDF Processing Pipeline

```
PDF File → Page Rendering (2x scale) → Base64 Encoding → Parallel Processing
                                                              ↓
                                                    NVIDIA Nemotron Parse API
                                                              ↓
                                                    Tool Call Response (JSON)
                                                              ↓
                                                    Block Extraction & Joining
                                                              ↓
                                                    Cached Text Storage
```

### Text Extraction
- Converts each PDF page to a high-resolution PNG image (2x rendering scale)
- Encodes images as base64 for API transmission
- Uses NVIDIA Nemotron Parse's tool calling to extract structured text blocks
- Processes up to 5 pages concurrently for efficiency

### Caching System
- Generates MD5 hash of the source PDF file for unique identification
- Stores extracted text in `.cache/{hash}.txt`
- On subsequent runs, reuses cached extraction (skips API calls entirely)

### Summarization
- Combines all extracted text from the document
- Uses NVIDIA's Nemotron Nano 9B v2 model for summarization
- Applies custom summary prompt from environment variables
- Outputs final summary to `summary.md`

## API Models

- **Text Extraction**: `nvidia/nemotron-parse` - Advanced OCR and document parsing with tool calling
- **Summarization**: `nvidia/nvidia-nemotron-nano-9b-v2` - Efficient text summarization (1024 token limit)

## Environment Variables

- `NGC_API_KEY`: Your NVIDIA API key for authentication

## Output Files

- `summary.md` - Generated summary of the research paper
- `.cache/{hash}.txt` - Cached extracted text (not committed to git)

## Error Handling

- Gracefully handles API failures and missing responses
- Continues processing remaining pages if one fails
- Marks failed pages with `<No text found>` placeholder
- Returns empty summary if text extraction fails

## Configuration

To adjust performance or behavior:

- **Change concurrency**: Modify `max_workers` in `ThreadPoolExecutor` (default: 5)
- **Control extraction quality**: Adjust `render(scale=2)` value (higher = better quality, slower)
- **Limit summary length**: Change `max_tokens` in the summarize function (default: 4096)
- **Process different PDFs**: Update the filename in the `if __name__ == "__main__"` block

## Notes

- The tool expects PDFs with extractable text; scanned images may require OCR preprocessing
- NVIDIA API usage incurs costs based on your account plan
- Caching significantly reduces API calls for repeated processing of the same document