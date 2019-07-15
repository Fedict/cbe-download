import argparse
import bs4
import requests
import urllib3

cbesite = 'https://kbopub.economie.fgov.be'

'''
Download open data CBE zip file, requires a valid username and password
'''
def download(session):
    try:
        content = session.get(cbesite + '/kbo-open-data/affiliation/xml?form=')
        soup = bs4.BeautifulSoup(content.text, 'html.parser')
        link = soup.select("table[id='row'] tr:last-child td:nth-of-type(2) a")[0]['href']
        data = session.get(cbesite + '/kbo-open-data/affiliation/xml/' + link)
        open('kbo.zip', 'wb').write(data.content)
    except urllib3.exceptions.NewConnectionError:
        print('Connection failed')

def login(session, user, password):
    url = cbesite + '/kbo-open-data/login'
    try:
        content = session.get(url)
        soup = bs4.BeautifulSoup(content.text, 'html.parser')
        action = soup.form['action']
        fields = {'j_username': user, 'j_password': password }
        content = session.post(cbesite + action, fields)
    except urllib3.exceptions.NewConnectionError:
        print('Connection failed')

def main(args):
    with requests.Session() as session:
        login(session, args.user, args.password)
        download(session)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Download CBE data')
    parser.add_argument('user', help='user name')
    parser.add_argument('password', help='password')
    args = parser.parse_args()
    main(args)
