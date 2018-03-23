import unittest
import boto3
import dynamodb_helper
from botocore.exceptions import ClientError
from mock import patch
from moto import mock_dynamodb2

class dynamodb_helper_test(unittest.TestCase):

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
        self.assertEqual(self.existing_id,dynamodb_helper.query_for_one(self.table_name,self.id_name,self.existing_id)[self.id_name])
        self.assertEqual(None,dynamodb_helper.query_for_one(self.table_name,self.id_name,self.nonexistent_id))
        self.assertEqual(None,dynamodb_helper.query_for_one(self.table_name,'bad_id',self.nonexistent_id))
        with self.assertRaises(Exception):            
            result = dynamodb_helper.query_for_one('bad_table',self.id_name,self.nonexistent_id)

    @patch('os.environ', {
    'AWS_ACCESS_KEY_ID': '123',\
    'AWS_SECRET_ACCESS_KEY':'123',\
    'AWS_DEFAULT_REGION':'us-east-1',})
    @mock_dynamodb2
    def test_put_item(self):
        dynamodb = boto3.resource('dynamodb')        
        dynamodb.create_table(AttributeDefinitions=self.attribute_defs, KeySchema=self.key_schema, TableName=self.table_name,ProvisionedThroughput=self.provisioned_throughput)
        with self.assertRaises(Exception):
            dynamodb_helper.put_item('bad_table',{'id':self.nonexistent_id})
        dynamodb_helper.put_item(self.table_name,{'id':self.nonexistent_id})
        self.assertEqual(self.nonexistent_id,dynamodb_helper.query_for_one(self.table_name,self.id_name,self.nonexistent_id)[self.id_name])        
        # TODO
        #empty item
        #item has no id
        #item is not json
        #ok item
        #timestamp
        #item contains empty items
        