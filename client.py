import requests
import json

# 1. The URL of your API
url = "http://127.0.0.1:8000/extract-bill-data"

# 2. The Image we want to read (Walmart Receipt)
payload = {
    "document": "https://ocr.space/Content/Images/receipt-ocr-original.jpg"
}

print("Scanning Bill...")

# 3. Send the request
try:
    response = requests.post(url, json=payload)
    result = response.json()

    # 4. Extract and Print the Info Nicely
    if result.get("is_success"):
        data = result["data"]
        items = data["pagewise_line_items"][0]["bill_items"]
        total = data["reconciled_amount"]

        print("\n" + "="*30)
        print("       RECEIPT EXTRACTOR       ")
        print("="*30)
        print(f"{'ITEM NAME':<20} | {'PRICE'}")
        print("-" * 30)

        # Loop through the list to extract items
        for item in items:
            name = item["item_name"]
            price = item["item_amount"]
            print(f"{name:<20} | ${price:.2f}")

        print("-" * 30)
        print(f"{'TOTAL CALCULATION':<20} | ${total:.2f}")
        print("="*30)
    else:
        print("Error:", result.get("error"))

except Exception as e:
    print("Connection Failed. Is the server running?")
    print(e)
