import argparse
import requests
from decouple import config
from google import Google
from pyvirtualdisplay import Display

def set_session(dologin):
    g = Google(dologin)
    if (g.browser):
        g.browser.close()

    session = requests.Session()
    for cookie in g.cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return g, session

def drive_info(drive_id, dologin):
    key = config('KEY')
    origin = 'https://drive.google.com'
    fields = 'id,name,quotaInfo(quotaBytesUsed,individualQuotaBytesTotal),permissionsSummary'
    url = 'https://clients6.google.com/drive/v2internal/teamdrives/{drive_id}?fields={fields}&key={key}'.format(drive_id=drive_id, fields=fields, key=key)
    g, session = set_session(dologin)

    headers = {}
    headers['Authorization'] = "SAPISIDHASH "+g.SAPISID_hash(origin)
    headers['Origin'] = origin
    session.headers = headers

    response = session.get(url)

    return response.text

def drive_adduser(drive_id, user, dologin):
    key = config('KEY')
    origin = 'https://drive.google.com'
    fields = 'emailAddress'
    url = 'https://clients6.google.com/drive/v2internal/files/{drive_id}/permissions?fields={fields}&supportsTeamDrives=true&key={key}'.format(drive_id=drive_id, fields=fields, key=key)

    g, session = set_session(dologin)

    headers = {}
    headers['Authorization'] = "SAPISIDHASH "+g.SAPISID_hash(origin)
    headers['Origin'] = origin
    session.headers = headers

    data = {}
    # TODO needs to verify API's roles
    data['role'] = 'fileOrganizer'
    data['type'] = 'user'
    data['value'] = user

    response = session.post(url, data=str(data))

    return response.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="debug")
    parser.add_argument("-l", "--login", action='store_true', help="faz login")
    parser.add_argument("-a", "--add", metavar='email', help="email do usuário a ser adicionado")
    parser.add_argument("drive_id", help="id do drive")

    args = parser.parse_args()

    if (not args.debug):
        display = Display()
        display.start()

    drive_id = args.drive_id
    dologin = args.login
    if (args.add):
        user = args.add
        print(drive_adduser(drive_id, user, dologin))
    else:
        print(drive_info(drive_id, dologin))

    if (not args.debug):
        display.stop()

if __name__ == "__main__":
    main()
