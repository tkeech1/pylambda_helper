import unittest
import json
import lambda_helper

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

