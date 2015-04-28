import urllib3, getpass, json

def run_program(http):
    # response = http.request('GET', 'http://127.0.0.1:8000/json_test/')
    # print(response.data.decode('utf-8'))
    # json_object = json.loads(response.data.decode('utf-8'))
    # print(json_object)
    base_url = input("Please enter base url: ")
    base_url = 'http://127.0.0.1:8000'
    json_user = None
    # Loop for user login
    while True:
        json_user = check_user_login(http, base_url)
        if json_user:
            print("Welcome " + json_user['username'])
            break
        option = input("Invalid username/password. Try again? [Yn]")
        if option != 'Y':
            exit()

    # Pre-load data for the user
    json_report_list = get_report_list(base_url, json_user['id'])

    # Program control loop
    while True:
        command = input(">>> Please enter a command: ")
        # exit
        if command == "-1":
            print("Thank you")
            exit()
        # list reports
        elif command == 'ls':
            print("Reports:")
            for json_report in json_report_list:
                print(json_report['short'])
            print()
        # show report details
        elif command.startswith('show'):
            command_split = command.split()
            report_name = command_split[1]

            report_found = False
            for json_report in json_report_list:
                if json_report['short'] == report_name:
                    show_report_details(json_report)
                    report_found = True
                    break

            if not report_found:
                print("Report not found")
        # download encrypted file
        elif command.startswith('download'):
            command_split = command.split()
            media_name = command_split[1]
            response = download_file(base_url, media_name)

            with open(media_name, 'wb') as out_file:
                out_file.write(response.data)

            response.release_conn()

def download_file(base_url, media_name):
    url = base_url + '/json_file_download/' + media_name + '/'
    response = http.request('GET', url)
    return response

def show_report_details(json_report):
    # Print all fields that are not lists
    for key in json_report:
        if key != 'file_list':
            print(key + ": " + str(json_report[key]))
    print("Files:")
    for file in json_report['file_list']:
        print(json_report['file_list'][file])
    print()

def get_report_list(base_url, user_id):
    url = base_url + '/json_report_list/' + str(user_id) + '/'
    response = http.request('GET', url)
    return json.loads(response.data.decode('utf-8'))['report_list']


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