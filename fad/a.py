import requests

headers = {
    "cookie": "honoka=e2X1_dmWstz7E0va8Xg6zH-JU-R0vixTmiF12OQYVnG3chpTBI6vSetsH-htVyhGrqyOWYNUwqU-MHQdPj6HX4wtvxGCdErIHLwKKpbAIV4eVUGVSQM-FuwSqB8YGnno;",
}

with open("a.txt", "r", encoding="utf-8") as f:
    ip_lines = [line.strip() for line in f if line.strip()]
        
with open("b.txt", "r", encoding="utf-8") as f:
    note_lines = [line.strip() for line in f if line.strip()]
        
total_lines = min(len(ip_lines), len(note_lines))

for i in range(total_lines):
    ip_value = ip_lines[i]
    note_line = note_lines[i]
    
    note_text = note_line.split("-", 1)[1].strip() if "-" in note_line else note_line

    url = "https://haneul.wiki/aclgroup"

    body = {
        "group": "b17c9924-1293-4586-897e-a9071dca4610",
        "mode": "ip",
        "ip": f"{ip_value}",
        "note": f"{note_text}",
        "duration": 0,
        "hidelog": "N"
    }
    
    print(f"Sending request for IP: {ip_value} with Note: {note_text}")
    
    response = requests.post(url, headers=headers, data=body) 
    print(f"Status Code: {response.status_code}")
    print(response.text)
