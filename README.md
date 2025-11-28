# 🧾 AI-Powered Bill Data Extraction Pipeline

This project is a sophisticated document intelligence solution designed to automatically extract line items from bills, invoices, and receipts. It utilizes **Google Gemini 2.0 Flash** (Multimodal LLM) to accurately parse unstructured image data into structured JSON.

The system is engineered to handle specific accounting challenges, such as **excluding subtotals/taxes** to prevent double-counting and performing **mathematical reconciliation** to verify invoice accuracy.

## 🚀 Key Features

* **Multimodal Extraction:** Accepts image URLs of bills and receipts and processes them using Computer Vision + LLM.
* **Intelligent Parsing:** Strictly distinguishes between actual product line items and summary lines (Subtotal, Tax, VAT).
* **Auto-Reconciliation:** Python logic manually recalculates the total sum of extracted items to ensure the math adds up.
* **Dual Interface:**
    * **Streamlit Frontend:** A modern, interactive web UI for easy testing and visualization.
    * **FastAPI Backend:** A robust, production-ready REST API.

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **AI Model:** Google Gemini 2.0 Flash (via `google-generativeai`)
* **Backend Framework:** FastAPI (`uvicorn`)
* **Frontend UI:** Streamlit
* **Image Processing:** PIL (Pillow) & Requests

## 📂 Project Structure

```text
├── main.py             # The FastAPI Backend (The Brain)
├── app.py              # The Streamlit Web App (The User Interface)
├── client.py           # Python script to test the API programmatically
├── requirements.txt    # List of project dependencies
├── .env                # API Keys (Not included in version control)
└── README.md           # Project Documentation



## ⚙️ Setup & Installation
* Follow these steps to set up the project locally.

1. Clone the Repository

```
git clone <REPO_LINK_HERE>
cd bill-extractor
```

2. Create a Virtual Environment
* It is recommended to use a virtual environment to manage dependencies.
```
# Create the environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Configure Environment Variables
* Create a file named .env in the root directory. Add your Google Gemini API key:
```
GEMINI_API_KEY=AIzaSy...YourKeyHere...
```

## 🧪 How to Test the Application

*You can test the application using three different methods. Note: For the Streamlit App and Client Script to work, the Backend Server must be running first.

Step 1: Start the Backend Server
Open your terminal and run:
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Wait until you see the message: Uvicorn running on http://0.0.0.0:8000

Step 2: Choose a Testing Method
### 🟢 Method A: The Visual Web Interface (Streamlit)

Best for: Visualizing the data in a table and testing quickly.

Keep the server running in the first terminal.

Open a new terminal and run:
```
streamlit run app.py
```

The app will open in your browser automatically.

Paste a receipt URL (e.g., https://ocr.space/Content/Images/receipt-ocr-original.jpg) and click "Extract Data".

### 🟡 Method B: The Python Client Script

Best for: Simulating how another Python program would interact with your API.

Keep the server running.
In a new terminal, run:
```
python client.py
```

The script will send a request and print the extracted receipt data in the terminal.

### 🔵 Method C: Direct API Request (cURL)

Best for: Testing raw JSON endpoints.
```
curl -X POST [http://127.0.0.1:8000/extract-bill-data](http://127.0.0.1:8000/extract-bill-data) \
-H "Content-Type: application/json" \
-d '{"document": "[https://templates.invoicehome.com/invoice-template-us-neat-750px.png](https://templates.invoicehome.com/invoice-template-us-neat-750px.png)"}'
```