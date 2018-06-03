from warrant.aws_srp import AWSSRP
import time

from warrant import Cognito

USERNAME='ridwaan2'
PASSWORD='yXY2Z2mH'
POOL_ID='us-east-1_AgAJAlp74'
CLIENT_ID = '7mic2g4j3tkve6sn2hns91uk91'
POOL_REGION = 'us-east-1'

IDENTITYPOOLID = 'us-east-1:e1a2e785-6445-4a73-8b2c-e4395ec34a09'




# athenticate user using SRP and time it 

Mastertic = time.time()
tic = time.time() 
aws = AWSSRP(username=USERNAME, password=PASSWORD, pool_id=POOL_ID,
             client_id=CLIENT_ID, pool_region = POOL_REGION)
tokens = aws.authenticate_user()
toc = time.time() 
print ("time to authenticate the user in pool", toc - tic)

id_token = tokens['AuthenticationResult']['IdToken']
refresh_token = tokens['AuthenticationResult']['RefreshToken']
access_token = tokens['AuthenticationResult']['AccessToken']
token_type = tokens['AuthenticationResult']['TokenType']

print id_token

#federate user and time it 

import boto3

client = boto3.client('cognito-identity', region_name = POOL_REGION)

tic = time.time() 
response = client.get_id( 
    IdentityPoolId=IDENTITYPOOLID,
    Logins={
        'cognito-idp.us-east-1.amazonaws.com/'+POOL_ID: id_token
    }
)

response2 = client.get_credentials_for_identity(
    IdentityId= response['IdentityId'],
    Logins={
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_AgAJAlp74': id_token
    },
    
)
Mastertoc = time.time() 
toc = time.time() 

print ("time to federate the user in Federated Identities ", toc - tic)
print ("Total time ", Mastertoc - Mastertic)

print response2

#print response2





