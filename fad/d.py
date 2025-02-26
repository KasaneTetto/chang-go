import requests
import time
import csv

def fetch_vpn_ips():
    url = "https://www.vpngate.net/api/iphone"
    response = requests.get(url)
    if response.status_code != 200:
        print("[Error] Failed to fetch VPN data.")
        return []
    
    data = response.text.splitlines()
    csv_data = [line for line in data if not line.startswith("#")]
    reader = csv.reader(csv_data)
    
    ip_list = [row[1] for row in reader if len(row) > 1]  # Extracting only the 'IP' column
    return set(ip_list)

def notify_aclgroup(ip_value):
    url = "https://haneul.wiki/aclgroup"
    body = {
        "group": "b17c9924-1293-4586-897e-a9071dca4610",
        "mode": "ip",
        "ip": ip_value,
        "note": "VPNGate 우회 수단 대역 | 로그인 후 활동하시길 바랍니다.",
        "duration": 0,
        "hidelog": "N"
    }
    headers = {
    "cookie": "honoka=e2X1_dmWstz7E0va8Xg6zH-JU-R0vixTmiF12OQYVnG3chpTBI6vSetsH-htVyhGrqyOWYNUwqU-MHQdPj6HX4wtvxGCdErIHLwKKpbAIV4eVUGVSQM-FuwSqB8YGnno;",
}
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 204:
        print(f"[Success] Notified ACL group for IP: {ip_value}")
    else:
        print(f"[Error] Failed to notify ACL group for IP: {ip_value}")

def main():
    previous_ips = fetch_vpn_ips()
    
    if previous_ips:
        print("[Info] Initial VPN IPs detected. Notifying ACL group...")
        for ip in previous_ips:
            notify_aclgroup(ip)
    
    while True:
        current_ips = fetch_vpn_ips()
        
        if current_ips:
            if previous_ips and current_ips != previous_ips:
                print("[Info] VPN IPs changed. Notifying ACL group...")
                for ip in current_ips:
                    notify_aclgroup(ip)
            else:
                print("[Info] No changes detected.")
            
            previous_ips = current_ips  # Save the current IPs for the next iteration
        
        time.sleep(90)  # Wait for 5 minutes

if __name__ == "__main__":
    main()
