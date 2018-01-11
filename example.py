import os
import requests
import tempfile

def get_headers(host, client_id, client_secret, user_name, user_password):
    url = 'https://{host}/oauth/token'.format(host = host)
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    data = {'grant_type':'password', 'client_id': client_id, 'client_secret': client_secret,
              'username': user_name, 'password': user_password}

    response = requests.post(url, data = data)
    return  {'Authorization': 'Bearer {access_token}'.format(access_token = response.json()['access_token'])}

def post_file_to_share(host, headers, folder_id):
    #create a temp file as an example
    fh, filepath = tempfile.mkstemp()
    with open(filepath, 'wb') as write_obj:
        write_obj.write(b'example text')
    # create a post request to get URL
    response_iniital = requests.post(url= 'https://{host}/sf/v3/Items({folder_id})/Upload2'.format(folder_id = folder_id, host = host), 
            data = {"Method":"Method", "Raw": False }, headers = headers,
            )
    # Create files dict
    files = {'File1': ('new_file_name_on_share.txt', open(filepath, 'rb'), 'text/plain')}
    # post the file
    response_files = requests.post(url = response_iniital.json()['ChunkUri'], files = files )
    # response can be 200 and still not really be successful
    if response_files.status_code < 300 and response_files.text != "OK":
        sys.stderr.write("Some error occurred: {error}\n".format(error = response_files.text))
    elif response_files.status_code > 200:
        sys.stderr.write('Error: {status}\n'.format(response_files.status_code))
    else:
        print("Success!")

if __name__ == '__main__':
    headers = get_headers(host = os.environ['HOST'],
            client_id = os.environ['CLIENT_ID'],
            client_secret = os.environ['CLIENT_SECRET'],
            user_name = os.environ['USER_NAME'],
            user_password = os.environ['USER_PASSWORD'],
            )
    post_file_to_share(os.environ['HOST'], headers, os.environ['FOLDER_ID'])
