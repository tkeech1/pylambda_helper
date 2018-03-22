import unittest
import json
import lambda_helper
import boto3
from botocore.exceptions import ClientError
from mock import patch
from moto import mock_dynamodb2

class lambda_helper_test(unittest.TestCase):
    
    def test_response_200_json(self): 
        testVal = {'test':'resp'}
        self.assertEqual(
            {
                'statusCode': '200',
                'body': json.dumps(testVal),
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*',},
            }
            ,lambda_helper.respond(None,testVal))

    def test_response_200_string(self): 
        testVal = 'test'
        self.assertEqual(
            {
                'statusCode': '200',
                'body': json.dumps(testVal),
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*',},
            }
            ,lambda_helper.respond(None,testVal)
        )

    def test_response_400(self):    
        testVal = 'An error'
        self.assertEqual(
            {
                'statusCode': '400',
                'body': json.dumps({ 'message' : testVal}),
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*',},
            }
            ,lambda_helper.respond(testVal,None))

    def test_response_both_values(self):    
        testVal = 'An error'
        self.assertEqual(
            {
                'statusCode': '400',
                'body': json.dumps({ 'message' : testVal}),
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*',},
            }
            ,lambda_helper.respond(testVal,testVal))    

    def test_response_only_error_value(self):    
        testVal = 'An error'
        self.assertEqual(
            {
                'statusCode': '400',
                'body': json.dumps({ 'message' : testVal}),
                'headers': {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*',},
            }
            ,lambda_helper.respond(testVal))               

    def test_respond_token(self):    
        testVal = 'test'
        self.assertEqual( 
            {
            'statusCode': 200,
            'body': json.dumps({'token' : {'authenticationToken': testVal}}),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin":"*"}
            }
        , lambda_helper.respond_token(testVal))    
        self.assertEqual( 
            {
            'statusCode': 200,
            'body': json.dumps({'token' : {'authenticationToken': None}}),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin":"*"}
            }
        , lambda_helper.respond_token(None)) 

    def test_redirect(self):    
        testVal = 'test'
        self.assertEqual( 
            {
            'statusCode': 302,
            'headers': {"Location": testVal},
            }
        , lambda_helper.redirect(testVal))   
        self.assertEqual( 
            {
            'statusCode': 302,
            'headers': {"Location": None},
            }
        , lambda_helper.redirect(None))


class lambda_helper_db_test(unittest.TestCase):

    def setUp(self):
        self.table_name = 'test'
        self.existing_id = '732'
        self.id_name = 'id'
        self.nonexistent_id = '324'  
        self.attribute_defs = [{
                'AttributeName': self.id_name,
                'AttributeType': 'S'
            }]
        self.key_schema = [{
                'AttributeName': self.id_name,
                'KeyType': 'HASH'
            }]
        self.provisioned_throughput = {
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }           
    
    def tearDown(self):
        pass

    @patch('os.environ', {
    'AWS_ACCESS_KEY_ID': '123',\
    'AWS_SECRET_ACCESS_KEY':'123',\
    'AWS_DEFAULT_REGION':'us-east-1',})
    @mock_dynamodb2
    def test_query_for_one(self):       
        dynamodb = boto3.resource('dynamodb')        
        dynamodb.create_table(AttributeDefinitions=self.attribute_defs, KeySchema=self.key_schema, TableName=self.table_name,ProvisionedThroughput=self.provisioned_throughput)
        dynamodb.Table(self.table_name).put_item(Item={self.id_name:self.existing_id})
        self.assertEqual(self.existing_id,lambda_helper.query_for_one(self.table_name,self.id_name,self.existing_id)[self.id_name])
        self.assertEqual(None,lambda_helper.query_for_one(self.table_name,self.id_name,self.nonexistent_id))
        self.assertRaises(Exception, lambda_helper.query_for_one(self.table_name,'bad_id',self.nonexistent_id))
        #self.assertRaises(ClientError, lambda_helper.query_for_one('bad_table',self.id_name,self.nonexistent_id))
