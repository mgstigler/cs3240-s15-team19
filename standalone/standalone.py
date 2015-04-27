import urllib3, getpass, json

def run_program(http):
    # response = http.request('GET', 'http://127.0.0.1:8000/json_test/')
    # print(response.data.decode('utf-8'))
    # json_object = json.loads(response.data.decode('utf-8'))
    # print(json_object)
    base_url = input("Please enter base url: ")

    while True:
        json_user = check_user_login(http, base_url)
        if json_user:
            break
        option = input("Invalid username/password. Try again? [Yn]")
        if option != 'Y':
            exit()

def check_user_login(http, base_url):
    login_url = base_url + '/json_login/'
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    fields = {
        'username': username,
        'password': password,
    }
    response = http.request_encode_body(method='POST', url=login_url, fields=fields)

    json_object = json.loads(response.data.decode('utf-8'))

    if json_object['status'] == 'success':
        return json_object['user']
    else:
        return None

if __name__ == "__main__":
    http = urllib3.PoolManager()

    run_program(http)