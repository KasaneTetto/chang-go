import requests

headers = {
    "cookie": "honoka=e2X1_dmWstz7E0va8Xg6zH-JU-R0vixTmiF12OQYVnG3chpTBI6vSetsH-htVyhGrqyOWYNUwqU-MHQdPj6HX4wtvxGCdErIHLwKKpbAIV4eVUGVSQM-FuwSqB8YGnno;",
}

with open("block.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for line in lines:
    ip_value, note_text = line.split(" - ", 1)

    url = "https://haneul.wiki/aclgroup"

    body = {
        "group": "b17c9924-1293-4586-897e-a9071dca4610",
        "mode": "ip",
        "ip": ip_value.strip(),
        "note": note_text.strip(),
        "duration": 0,
        "hidelog": "N"
    }

    print(f"{body}")

    response = requests.post(url, headers=headers, data=body)
    print(f"Status Code: {response.status_code}")
    print(response.text)