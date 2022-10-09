import json
import boto3
import os

db = boto3.client('dynamodb')


def lambda_handler(event, context):
    trigger = event['trigger']
    try:
        db_response = get_db_response(trigger)
    except:
        print('emergency undefined')
    threat_type = check_trigger_type(trigger)
    sentiment_response = formulate_response(db_response, threat_type)
    return sentiment_response


def check_trigger_type(trigger):
    list = ['rock', 'jazz', 'pop']
    if trigger in list:
        return 'domestic abuse'
    else:
        return 'emergency'


def get_db_response(trigger):
    return db.get_item(
        TableName='ThreatMap',
        Key={
            'UserInput': {'S': trigger}
        }
    )


def formulate_response(db_response, threat_type):
    if threat_type == 'emergency':
        return {
            'threatType': threat_type,
            'threatLevel': '2'
        }
    item = db_response['Item']

    threat_level = item['MappedThreat']['N']

    return {
        'threatType': threat_type,
        'threatLevel': threat_level
    }