import json
import boto3
from boto3.dynamodb.conditions import Key

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': json.dumps({ 'message': err}) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*',
        },
    }

def respond_token(token):
    return {
        'statusCode': 200,
        'body': json.dumps({"token" : {"authenticationToken": token}}),
        'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin":"*"}
    } 
    
def redirect(location):
    return {
        "statusCode": 302,
        "headers": {
            "Location": location
        }
    }     

def query_for_one(table, id_name, id):
    try: 
        dynamodb = boto3.resource('dynamodb')
        result = dynamodb.Table(table).query(KeyConditionExpression=Key(id_name).eq(id))
        if len(result['Items']) == 1:
            return result['Items'][0]
        return None
    except Exception as err:
        print("EXCEPTION: query_for_one")
        print(err)
        raise(err)