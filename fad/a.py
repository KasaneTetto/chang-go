import requests

headers = {
    "cookie": "honoka=e2X1_dmWstz7E0va8Xg6zH-JU-R0vixTmiF12OQYVnG3chpTBI6vSetsH-htVyhGrqyOWYNUwqU-MHQdPj6HX4wtvxGCdErIHLwKKpbAIV4eVUGVSQM-FuwSqB8YGnno;",
}

# a.txt: 각 줄에 IPv4 대역(CIDR 형식)이 있다고 가정
with open("a.txt", "r", encoding="utf-8") as f:
    ip_lines = [line.strip() for line in f if line.strip()]
        
# b.txt: 각 줄에 "오류있는 IPv4대역 - 텍스트" 형태라고 가정
with open("b.txt", "r", encoding="utf-8") as f:
    note_lines = [line.strip() for line in f if line.strip()]
        
# 두 파일의 줄 수 중 더 적은 줄만큼 처리
total_lines = min(len(ip_lines), len(note_lines))

for i in range(total_lines):
    ip_value = ip_lines[i]
    note_line = note_lines[i]
    
    # note 텍스트 추출: '-' 문자가 있다면 그 이후 부분, 없으면 전체 문자열 사용
    note_text = note_line.split("-", 1)[1].strip() if "-" in note_line else note_line

    # API 요청
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
