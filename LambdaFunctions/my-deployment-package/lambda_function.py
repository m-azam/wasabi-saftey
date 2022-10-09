import os
from twilio.rest import Client


def lambda_handler(event, context):
    account_sid = 'ACfc53f045e8503f2e912aaeb501d138a1'
    auth_token = '2816c3130a038980d85e8058d9fdc40d'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Domestic abuse SOS!",
        from_='+13857071705',
        to='+14256154385'
    )

    print(message.sid)
