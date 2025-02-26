import requests
import csv

def fetch_asn_data(asn, token):
    """
    주어진 ASN(예: AS198375)과 토큰으로 IPinfo API에서 정보를 조회합니다.
    """
    url = f"https://ipinfo.io/{asn}?token={token}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API 요청 실패: 상태 코드 {response.status_code}")
    return response.json()

def process_asn(asn_str, token):
    """
    하나의 ASN에 대해 API 조회 및 결과 문자열 목록을 생성합니다.
    단, API 응답의 type 값이 "hosting"인 경우에만 결과를 반환하며,
    아니면 빈 리스트를 반환합니다.
    """
    try:
        data = fetch_asn_data(asn_str, token)
    except Exception as e:
        print(f"{asn_str} 데이터 조회 실패: {e}")
        return []

    # type 값이 'hosting'이 아닌 경우 건너뜁니다.
    if data.get("type") != "hosting":
        print(f"{asn_str}의 type이 hosting이 아니므로 저장하지 않습니다.")
        return []

    # 상위 레벨의 'name'과 'country' 값 추출
    company_name = data.get("name", "Unknown")
    country = data.get("country", "XX")
    
    # prefixes와 prefixes6 내부의 'netblock' 값 추출
    prefixes = data.get("prefixes", [])
    netblocks = [prefix.get("netblock") for prefix in prefixes if prefix.get("netblock")]
    
    prefixes6 = data.get("prefixes6", [])
    netblocks6 = [prefix.get("netblock") for prefix in prefixes6 if prefix.get("netblock")]
    
    all_netblocks = netblocks + netblocks6
    if not all_netblocks:
        print(f"{asn_str}에 대한 netblock 정보가 없습니다.")
        return []
    
    # 지정한 형식의 문자열 생성
    lines = []
    for netblock in all_netblocks:
        line = f"{netblock} - IP 위치: {country}, [{asn_str}] - [{company_name}] 우회 수단 IP | 로그인 후 활동하시길 바랍니다.\n"
        lines.append(line)
    
    return lines

def main():
    token = "257a054309c07f"  # 실제 발급받은 토큰으로 교체하세요.
    output_lines = []
    
    # asn-list.txt 파일을 CSV 형식으로 읽습니다.
    with open("asn-list.txt", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row or len(row) < 1:
                continue
            # 첫 번째 값(ASN 번호)을 좌우 공백 제거 후 추출
            asn_number = row[0].strip()
            if not asn_number:
                continue
            # ASN 번호 앞에 "AS"를 붙여 형식화 (예: AS198375)
            asn_str = f"AS{asn_number}"
            # 각 ASN에 대해 결과 문자열 리스트를 반환받아 누적
            lines = process_asn(asn_str, token)
            output_lines.extend(lines)
    
    # 누적된 결과가 있을 경우 block-list.txt 파일에 기록
    if output_lines:
        with open("block-list.txt", "w", encoding="utf-8") as f:
            for line in output_lines:
                f.write(line)
        print("block-list.txt 파일에 결과가 저장되었습니다.")
    else:
        print("저장할 결과가 없습니다.")

if __name__ == "__main__":
    main()
