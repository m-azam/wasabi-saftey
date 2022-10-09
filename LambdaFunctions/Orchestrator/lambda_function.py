import json
import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    # TODO implement
    event = json.loads(event.get('body'))
    print('event',event.get('body'))
    sentimentEngineReq = {
        "trigger": event['trigger']
    }

    responseFromSentimentEngine = client.invoke(FunctionName="arn:aws:lambda:us-east-1:591179928505:function:sentimentEngine", InvocationType="RequestResponse", Payload=json.dumps(sentimentEngineReq))


    sentimentResponseJson = json.load(responseFromSentimentEngine['Payload'])
    print("Sentiment Engine response: ",sentimentResponseJson)
    craftMessageReq = {"latitude": event['latitude'],
            "longitude": event['longitude'],
            "userName": event['userName'],
            "threatType": sentimentResponseJson['threatType'],
            "threatLevel": sentimentResponseJson['threatLevel']
    }
    print(craftMessageReq)
    responseFromCraftMessage = client.invoke(FunctionName="arn:aws:lambda:us-east-1:591179928505:function:createMessage", InvocationType="RequestResponse", Payload=json.dumps(craftMessageReq))
    craftMessageJson = json.load(responseFromCraftMessage['Payload'])
    print(craftMessageJson)
    sosMessage = craftMessageJson['message']


    smsServiceReq = {
        "phone": "+14256154385",
        "message": sosMessage
    }

    responseFromSmsService = client.invoke(FunctionName="arn:aws:lambda:us-east-1:591179928505:function:sms-service", InvocationType="RequestResponse", Payload=json.dumps(smsServiceReq))

    responseJsonSms = json.load(responseFromSmsService['Payload'])
    print("Sms service response: ", responseJsonSms)

    return responseJsonSms