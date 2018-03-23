import json

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

