from __future__ import print_function
import datetime
import pickle
import os
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import scrapeSC as sc

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events'] # read/write access to events

month = { 
    'jan' : '01',
    'feb' : '02',
    'mar' : '03',
    'apr' : '04',
    'maj' : '05',
    'jun' : '06',
    'jul' : '07',
    'aug' : '08',
    'sep' : '09',
    'okt' : '10',
    'nov' : '11',
    'dec' : '12',
}

def create_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # Set $GOOGLE_CRED to access credentials
    if(os.environ['GOOGLE_CRED']):
        credJson = os.environ['GOOGLE_CRED']
    else:
        print("Please point out the credentials.json file!\n")
        print("Set enf variable $GOOGLE_CRED to credentials folder\n")

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credJson + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds) # returns service

def write_upcoming_events(nrEventsMax, service):
    # Call the Calendar API

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming %i events'% nrEventsMax)

    events_result = service.events().list(calendarId='primary',
                                        timeMin=now,
                                        maxResults=nrEventsMax,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def create_event(match, team):

    comp_info = "" 
    for pl in team["players"]:
        info = team["players"][pl]
        comp_info +=  'name : ' + pl + '\n'
        comp_info += 'phone : ' + info["phone"] + '\n'
        comp_info += 'mail : ' + info["mail"] + '\n'

    start = '2020-' + month[match['date'][1]] + '-'+ match['date'][0] + 'T20:00:00+02:00'
    end = '2020-' + month[match['date'][1]] + '-' + match['date'][0] + 'T21:30:00+02:00'

    eventDict = {
        'summary': 'Game against : ' + team["teamName"],
        'location': 'Platensgatan 8, 582 20 Linköping',
        'description':  match["teams"][0] + ' vs. '+  match["teams"][1] +'\n'
        + 'Teaminfo: \n'
        + comp_info + '\n',

        'start': {
            'dateTime': start,
            'timeZone': 'GMT+2:00'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'GMT+2:00'
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
            {'email': 'skantedal@gmail.com'},
        ],
        'reminders': {
            'useDefault': True,
        },
    }


    return eventDict



def main():
    service = create_service()
    moi, toi = sc.get_all_matches_for_team()
    for i, m in enumerate(moi):
        event =  create_event(m, toi[i])
        t = service.events().insert(calendarId='primary', body=event).execute()

    write_upcoming_events(10, service)

if __name__ == '__main__':
    main()
