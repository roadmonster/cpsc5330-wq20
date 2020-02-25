#!/usr/bin/python3
import boto3
from smart_open import open
from decimal import Decimal

def create_table():
    ddb = boto3.client('dynamodb')
    table = ddb.create_table(
        TableName='tfidf',
        KeySchema=[
            { 'AttributeName': 'term',  'KeyType': 'HASH' },
            { 'AttributeName': 'doc_id', 'KeyType': 'RANGE' }],
        AttributeDefinitions=[
            { 'AttributeName': 'term', 'AttributeType': 'S'},
            { 'AttributeName': 'doc_id', 'AttributeType': 'S'}],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10000
        })
    # Wait for the table to exist before exiting
    print('Waiting')
    waiter = ddb.get_waiter('table_exists')
    waiter.wait(TableName='tfidf')
    print('Done')

def add_tfidf_records(s3_filename = 's3://hanks-bda-2020-01/data-output/tfidf/000000_0'):
    res = boto3.resource('dynamodb')
    table = res.Table('tfidf')
    create_table()
    with open(s3_filename, 'rb') as fin:
        i = 1
        for line in fin:
            strvalue = line.decode('utf-8').strip()
            doc_id, term, value = strvalue.split('\x01')
            table.put_item(Item={ 'term': term, 'doc_id': doc_id, 'value': Decimal(value) })
            if (i % 1000) == 0:
                print(f"I {i}")
            i += 1

