import json
import re
import requests
from bs4 import BeautifulSoup


def fetch_rates():
    url = "https://www.fenegosida.org/"
    headers = {
        "User-Group": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text()

        # Regex patterns to find prices following the labels
        # Looking for numbers like 287,100 or 4,590 after the currency symbol/text
        gold_match = re.search(
            r"FINE GOLD\s*\(9999\)\s*per 1 tola\s*(?:रु\s*)?([\d,]+)",
            text_content,
            re.IGNORECASE,
        )
        silver_match = re.search(
            r"SILVER\s*per 1 tola\s*(?:रु\s*)?([\d,]+)",
            text_content,
            re.IGNORECASE,
        )

        # Fallback to general data extraction if specific layout regex matches fail
        gold_price = gold_match.group(1).strip() if gold_match else "Not Found"
        silver_price = (
            silver_match.group(1).strip() if silver_match else "Not Found"
        )

        # Create JSON structure
        data = {
            "source": "FENEGOSIDA",
            "currency": "NPR",
            "unit": "1 tola",
            "rates": {
                "fine_gold_9999": gold_price,
                "silver": silver_price,
            },
        }

        # Convert to JSON string
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        print(json_data)

        # Save to a file so GitHub Actions can save/commit it
        with open("rates.json", "w", encoding="utf-8") as f:
            f.write(json_data)

    except Exception as e:
        error_json = json.dumps({"error": str(e)})
        print(error_json)
        with open("rates.json", "w") as f:
            f.write(error_json)


if __name__ == "__main__":
    fetch_rates()
