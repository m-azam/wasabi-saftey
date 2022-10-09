import json
import boto3
import datetime


def lambda_handler(event, context):
    print(type(event))
    print("body>> ", event)
    event = json.dumps(event)
    print("Event json %s" % json.dumps(event["body"]))
    print("Context %s" % context)
    client = boto3.resource('dynamodb')
    table = client.Table('IncidentReport')
    eventDateTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

    if event["httpMethod"] == "POST":
        response = table.put_item(
            Item={
                'id': event['id'],
                'theat-level': event['threatLevel'],
                'threat-type': event['threatType'],
                'name': event['name'],
                'location': event['location'],
                'createdAt': eventDateTime,
                'updatedAt': eventDateTime
            }
        )
        return {
            'statusCode': 200
        }
    elif event["httpMethod"] == "PUT":
        response = table.put_item(
            Item={
                'id': event['id'],
                'theat-level': event['threatLevel'],
                'threat-type': event['threatType'],
                'name': event['name'],
                'location': event['location'],
                'createdAt': eventDateTime,
                'updatedAt': eventDateTime
            }
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': 'Record ' + context.aws_request_id + ' added'
        }
    elif event["httpMethod"] == "GET":
        response = table.get_item(
            Key={
                'id': event['id']
            }
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': response
        }
    elif event['httpMethod'] == "DELETE":
        response = table.delete_item(
            Key={
                'id': event['id']
            }
        )
        return {
            'statusCode': '204',
            'body': 'Tutorial Deleted successfully'
        }

