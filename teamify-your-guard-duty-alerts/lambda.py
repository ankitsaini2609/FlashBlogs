import json
import requests
import os

def send_message(findingID, findingType, resourceType, resourceDetails, severity, firstSeen, lastSeen, count):
    TEAM_WEBHOOK_URL = os.getenv('TEAM_WEBHOOK_URL')
    data = {
    "@type": "MessageCard",
    "@context": "http://schema.org/extensions",
    "themeColor": "0076D7",
    "summary": "New Guard Duty Finding Alert",
    "sections": [{
        "activityTitle": "New Guard duty finding alert",
        "activitySubtitle": "",
        "activityImage": "https://awsvideocatalog.com/images/aws/png/PNG%20Light/Security,%20Identity,%20&%20Compliance/Amazon-GuardDuty.png",
        "facts": [{
            "name": "Finding ID",
            "value": "{}".format(findingID)
        }, {
            "name": "Finding Type",
            "value": "{}".format(findingType)
        }, {
            "name": "Resource Type",
            "value": "{}".format(resourceType)
        }, {
            "name": "Resource Details",
            "value": "```" + json.dumps(resourceDetails, indent=4)
        }, {
            "name": "Severity",
            "value": "{}".format(severity)
        }, {
            "name": "First Seen",
            "value": "{}".format(firstSeen)
        }, {
            "name": "Last Seen",
            "value": "{}".format(lastSeen)
        }, {
            "name": "Count",
            "value": "{}".format(count)
        }],
        "markdown": True,
    }]
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(TEAM_WEBHOOK_URL, json=data, headers=headers)
    print(res.json())
    if res.status_code != 200:
        print("Unable to send the alert for findingID: {0}".format(findingID))

def lambda_handler(event, context):
    if event is not None:
        severity = event['detail']['severity']
        findingType = event['detail']['type']
        resourceType = event['detail']['resource']['resourceType']
        resourceDetails = ""
        findingID = event['id']
        firstSeen = event['detail']['service']['eventFirstSeen']
        lastSeen = event['detail']['service']['eventLastSeen']
        count = event['detail']['service']['count']
        for resource in event['detail']['resource'].keys():
            if 'details' in resource.lower():
                resourceDetails = event['detail']['resource'][resource]
        send_message(findingID, findingType, resourceType, resourceDetails, severity, firstSeen, lastSeen, count)
    return {
        'statusCode': 200
    }
