#!/usr/bin/python3
import boto3
from boto3.dynamodb.conditions import Key
import json
from decimal import Decimal
import sys

# Return a dictionary {docid: tfidf} for all docs that mention this term
def term_tfidf(term, table):
    res = {}
    response = table.query(KeyConditionExpression=Key('term').eq(term))
    for item in response['Items']:
        doc_id = item['docid']
        tfidf = item['value']
        res[doc_id] = float(tfidf)
    return res

def mergeSum(dict1, dict2):
    dict3 = {}
    for key, value in dict1.items():
        if key in dict2:
            dict3[key] = dict1[key] + dict2[key]
        else:
            dict3[key] = dict1[key]
    for key, value in dict2.items():
        if key not in dict1:
            dict3[key] = dict2[key]
    return dict3

def compute(terms):
    client = boto3.resource('dynamodb')
    table = client.Table('tfidf')
    docs = {}
    for term in terms:
        docs = mergeSum(docs, term_tfidf(term, table))
    tuples = [(k, v) for k, v in docs.items()]
    tuples = filter(lambda t: t[1] > 0, tuples)
    return sorted(tuples, key=lambda x: x[1], reverse=True)

def termify(l):
    words = l.strip().split()
    terms = []
    for word in words:
        lowered = word.lower()
        term = ''.join(list(filter(lambda c: 97 <= ord(c) <= 122, lowered)))
        if len(term) > 0:
            terms.append(term)
    return terms

def dowords(words):
    results = compute(words)
    retval = []
    for i in range(0, min(5, len(results))):
        r = results[i]
        retval.append({'doc_id': r[0], 'score': int(r[1]*10000000)})
    return retval

def dosearch():
    while (True):
        sys.stdout.write("Query: ")
        iline = input()
        results = dowords(termify(iline))
        for i in range(0, min(5, len(results))):
            r = results[i]
            #print("{0}. {1} -- {2}".format(i+1, r[0], int(r[1]*10000000)))
            print(r)


if __name__== "__main__":
  dosearch()



