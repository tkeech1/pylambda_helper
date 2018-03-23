import boto3
import datetime
from boto3.dynamodb.conditions import Key

def get_timestamp():
    return datetime.datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S:%f')

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

def put_item(table, item):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table)
        # remove empty items
        item = dict((k, v) for k, v in item.items() if v)
        item['last_update_gmt'] = get_timestamp()
        update = table.put_item( Item=item )

    except Exception as err:
        print("EXCEPTION: put_item")
        print(err)
        raise(err)