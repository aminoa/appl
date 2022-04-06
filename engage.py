import requests
from datetime import datetime
import json
from bs4 import BeautifulSoup 

"""
scrapes NYU events, returns JSON object

"""
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

    return simple_events 

def get_organizations(num_orgs="10"):
    formatted_date = datetime.now().strftime("%Y-%m-%dT%H:%M-%S")
    request_url = requests.get(
        f'https://engage.nyu.edu/api/discovery/search/organizations?'
        f'orderBy[0]=UpperName%20asc&'
        f'top={num_orgs}&'
        f'filter=&'
        f'query=&'
        f'skip=0')

    request_json = request_url.json()
    request_orgs = request_json['value']
    simple_events = {}

    for org in request_orgs:
        simple_events[org['Id']] = {
           "name": org['Name'],
           "short_name": org['ShortName'],
           "description": org['Description'],
           "summary": org['Summary'],
           "status": org['Status'],
           "category_names": org['CategoryNames']
        }   

    return simple_events

def get_news(num_news=10):
    request_url = requests.get(
        f'https://engage.nyu.edu/api/discovery/article/search?'
        f'take={num_news}&'
        f'search=&'
        f'skip=0&'
        f'orderByField=LastUpdatedOn&'
        f'orderByDirection=descending')
    
    request_json = request_url.json()
    request_orgs = request_json['items']
    simple_events = {}

    for org in request_orgs:
        simple_events[org['id']] = {
           "title": org['title'],
           "summary": org['summary'],
           "story": org['story'], #same as summary with html
           "author": org['author']['firstName'] + " " + org['author']['lastName'],
           "image_url": org['image']['fullUrl'],
           "image_caption": org['imageCaption'],
           "creation_date": org['createdOn'],
           "updated_date": org['updatedOn']
        }   

    return simple_events

