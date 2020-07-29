from gauth_module import setup_gmail_api_auth

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    service = setup_gmail_api_auth(SCOPES)

    # Call the Gmail API watch
    request = {
    'labelIds': ['INBOX'],
    'topicName': 'projects/gnotifier-1595882123710/topics/mygmailtopic'
    }
    
    resp = service.users().watch(userId='me', body=request).execute()
    print(resp)



if __name__ == '__main__':
    main()
