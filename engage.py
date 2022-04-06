import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup 

def get_events(num_events="15", search=""):
    formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M-%S")
    request_url = requests.get(
        f'https://engage.nyu.edu/api/discovery/event/search?'
        f'endsAfter={formatted_date}-04:00&'
        f'orderByField=endsOn&'
        f'orderByDirection=ascending&'
        f'status=Approved&take={num_events}&'
        f'query={search}')

    request_json = request_url.json()

    request_events = request_json['value']
    simple_events = {}

    for event in request_events:
        description_html = description_text = event['description']

        # cleanup with beautiful soup
        if description_text != None:
            description_text = description_text.replace("\r", "").replace("\n", "").replace("\t", "")
            soup = BeautifulSoup(description_text, "html.parser")
            description_text = soup.get_text()
        else:
            description_text = "None"

        simple_events[event['id']] = {
           "name": event['name'],
           "organization_name": event['organizationName'],
           "description_text": description_text,
           "description_html": description_html,
           "start_time": event['startsOn'],
           "end_time": event['endsOn'],
           "location": event['location'], 
           "status": event['status'],
           "theme": event['theme'],
           "benefit_names": event['benefitNames'],
           "category_names": event['categoryNames']
        }   

    print(simple_events) 
    
get_events();