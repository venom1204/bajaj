import streamlit as st
import requests
import pandas as pd

# YOUR API URL (Change this to your Render URL later)
API_URL = "https://bajaj-opwg.onrender.com"

st.title("🧾 AI Bill Extractor")
st.write("Paste an image URL below to extract line items automatically.")

# 1. Input Box
url_input = st.text_input("Image URL", "https://ocr.space/Content/Images/receipt-ocr-original.jpg")

if st.button("Extract Data"):
    with st.spinner("Analyzing Bill..."):
        try:
            # 2. Call your API
            response = requests.post(API_URL, json={"document": url_input})
            result = response.json()

            if result.get("is_success"):
                data = result["data"]
                items = data["pagewise_line_items"][0]["bill_items"]
                total = data["reconciled_amount"]

                # 3. Display Totals
                col1, col2 = st.columns(2)
                col1.metric("Total Items", len(items))
                col2.metric("Total Amount", f"${total}")

                # 4. Display Table
                df = pd.DataFrame(items)
                # Clean up the dataframe for display
                df_display = df[["item_name", "item_amount", "item_quantity"]]
                df_display.columns = ["Item", "Price", "Qty"]
                
                st.table(df_display)
                
                st.success("Extraction Complete!")
            else:
                st.error(f"Error: {result.get('error')}")

        except Exception as e:
            st.error(f"Connection Failed: {e}")