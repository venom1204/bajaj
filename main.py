from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import requests
from PIL import Image
from io import BytesIO

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Fallback for safety
    api_key = os.getenv("OPENAI_API_KEY") 

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

app = FastAPI()

# --- STRICT RESPONSE MODELS (As per Assignment) ---

class TokenUsage(BaseModel):
    total_tokens: int
    input_tokens: int
    output_tokens: int

class BillItem(BaseModel):
    item_name: str
    item_amount: float
    item_rate: float
    item_quantity: float # Assignment asked for float, not int

class PageItem(BaseModel):
    page_no: str
    page_type: str # "Bill Detail | Final Bill | Pharmacy"
    bill_items: List[BillItem]

class DataBlock(BaseModel):
    pagewise_line_items: List[PageItem]
    total_item_count: int

class FinalResponse(BaseModel):
    is_success: bool
    token_usage: TokenUsage
    data: DataBlock

class BillRequest(BaseModel):
    document: str

# --- CORE LOGIC ---

def analyze_image_with_gemini(image_url: str):
    # A. Download Image
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()
        image_data = Image.open(BytesIO(response.content))
    except Exception as e:
        return None, f"Download Error: {str(e)}"

    # B. The Strict Prompt
    prompt = """
    Analyze this bill image. Extract line items strictly.
    
    1. Identify the 'page_type': choose exactly one of ["Bill Detail", "Final Bill", "Pharmacy"].
    2. Extract line items (name, rate, quantity, amount).
    3. Rules: 
       - Do NOT include Subtotals or Tax in the item list.
       - If quantity is missing, assume 1.
    4. Return valid JSON only. Format:
    {
        "page_type": "...",
        "items": [
            {"item_name": "...", "item_rate": 0.0, "item_quantity": 1.0, "item_amount": 0.0}
        ]
    }
    """
    
    # C. Call Gemini
    try:
        response = model.generate_content([prompt, image_data])
        
        # Extract Token Usage (Gemini provides this object)
        usage = response.usage_metadata
        token_data = {
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count
        }

        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text), token_data

    except Exception as e:
        # Fallback if parsing fails
        return None, str(e)

# --- API ENDPOINT ---

@app.post("/extract-bill-data", response_model=FinalResponse)
async def extract_bill(request: BillRequest):
    ai_json, metadata_or_error = analyze_image_with_gemini(request.document)
    
    # Handle Errors
    if ai_json is None:
        return {
            "is_success": False,
            "token_usage": {"total_tokens":0, "input_tokens":0, "output_tokens":0},
            "data": {"pagewise_line_items": [], "total_item_count": 0}
        }

    # Format Data exactly as requested
    items_list = []
    for item in ai_json.get("items", []):
        items_list.append({
            "item_name": str(item.get("item_name", "Unknown")),
            "item_amount": float(str(item.get("item_amount", 0)).replace(',', '')),
            "item_rate": float(str(item.get("item_rate", 0)).replace(',', '')),
            "item_quantity": float(str(item.get("item_quantity", 1)))
        })

    # Construct the final structure
    response_payload = {
        "is_success": True,
        "token_usage": metadata_or_error, # This contains the token counts
        "data": {
            "pagewise_line_items": [
                {
                    "page_no": "1", # Assuming single image per URL for now
                    "page_type": ai_json.get("page_type", "Bill Detail"),
                    "bill_items": items_list
                }
            ],
            "total_item_count": len(items_list)
        }
    }
    
    return response_payload