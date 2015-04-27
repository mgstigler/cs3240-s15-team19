import urllib3, getpass, json

def run_program(http):
    # response = http.request('GET', 'http://127.0.0.1:8000/json_test/')
    # print(response.data.decode('utf-8'))
    # json_object = json.loads(response.data.decode('utf-8'))
    # print(json_object)

    while True:
        if check_user_login(http):
            break
        option = input("Invalid username/password. Try again? [Yn]")
        if option != 'Y':
            exit()

def check_user_login(http):
    login_url = 'http://127.0.0.1:8000/json_login/'
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    fields = {
        'username': username,
        'password': password,
    }
    response = http.request_encode_body(method='POST', url=login_url, fields=fields)

    json_object = json.loads(response.data.decode('utf-8'))

    return json_object['status'] == 'success'

if __name__ == "__main__":
    http = urllib3.PoolManager()

    run_program(http)