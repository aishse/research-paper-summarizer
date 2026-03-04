import base64
import io
import json
import os
import requests
import hashlib
import pypdfium2 as pdfium
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()


nvai_url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.environ.get('NGC_API_KEY')}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
def get_cache_path(file_path):
    with open(file_path, "rb") as f:
        hash = hashlib.md5(f.read()).hexdigest()
    return f".cache/{hash}.txt"


def summarize(full_text): 
    inputs = {
        "model": "nvidia/nvidia-nemotron-nano-9b-v2",
        "messages": [
            {
                "role": "user",
                "content": f"""{os.environ.get('SUMMARY_PROMPT')}\n\n{full_text}""",
            }
        ],
        "max_tokens": 1024,
    }
    try:
        response = requests.post(nvai_url, headers=headers, json=inputs)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Summarization error: {e}")
        return None

def parse_pdf(file_path):
    cache_path = get_cache_path(file_path)
    if os.path.exists(cache_path):
        print("Using cached extraction...")
        with open(cache_path) as f:
            return f.read()

    pdf = pdfium.PdfDocument(file_path)
    total = len(pdf)

    print("Rendering pages...")
    page_images = []
    for i, page in enumerate(pdf):
        image = page.render(scale=2).to_pil()
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        page_images.append((i, image_data, total))

    pdf.close()  # close PDF before threading

    all_text = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_page, args): args[0] for args in page_images}

        for future in as_completed(futures):
            i = futures[future]
            try:
                result = future.result()
                all_text[i] = result if result else "<No text found>"
            except Exception as e:
                print(f"Error processing page {i+1}: {e}")
                all_text[i] = ""

    os.makedirs(".cache", exist_ok=True)
    with open(cache_path, "w") as f:
        f.write("\n\n".join(all_text[i] for i in sorted(all_text)))

    return "\n\n".join(all_text[i] for i in sorted(all_text))

def process_page(args):
        i, image_data, total = args
        print(f"Processing page {i+1}/{total}...")
        
        inputs = {
            "model": "nvidia/nemotron-parse",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"},
                        }
                    ],
                }
            ],
            "max_tokens": 8192,
        }

        try:
            response = requests.post(nvai_url, headers=headers, json=inputs)
            response.raise_for_status()
            data = response.json()
            tool_call = data["choices"][0]["message"]["tool_calls"][0]
            blocks = json.loads(tool_call["function"]["arguments"])

            # extract just the text from each block, preserving order
            page_text = "\n".join(block["text"] for block in blocks[0] if "text" in block)
            return page_text

        except requests.exceptions.RequestException as e:
            print(f"Error on page {i+1}: {e}")
            print(response.json())
            return ""

if __name__ == "__main__":
    extracted_text = parse_pdf("europa.pdf")
    if extracted_text:
        print("Extracted text successfully. Now summarizing...")
        summary = summarize(extracted_text)
        if summary:
            print("dumping summary to summary.md")
            with open("summary.md", "w") as f:
                f.write(summary)
    else:
        print("An error occurred during text extraction. Summary not generated.")
