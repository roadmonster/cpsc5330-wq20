#!/usr/bin/python

import sys

#  Read the tfidf dictionary  in from disk -- we want to get rid of this
def ingest():
    tfidfs = {}
    with open("tfidf.txt") as f:
        for line in f:
            doc_id, term, tfidf = line.strip().split('\x01')
            tdict = tfidfs.get(term, {})
            tdict[doc_id] = float(tfidf)
            tfidfs[term] = tdict
    return tfidfs

# Second argument is the dictionary:  term -> {{docid -> value}}
# We need to get a retrieve from dynamodb to look like this same dictionary.
# Cheat code below
 
def compute(terms, tfidfs):
    docs = {}
    for term in terms:
        docs = mergeSum(docs, tfidfs.get(term, {}))
    tuples = [(k, v) for k, v in docs.items()]
    tuples = filter(lambda t: t[1] > 0, tuples)
    return sorted(tuples, key=lambda x: x[1], reverse=True)

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

def termify(line):
    terms = []
    for word in line.strip().split():
        lowered = word.lower()
        term = filter(lambda c: 97 <= ord(c) <= 122, lowered)
        if len(term) > 0:
            terms.append(term)
    return terms

def dosearch():
    tfidfs = ingest()
    while (True):
        sys.stdout.write("Query: ")
        iline = raw_input()
        results = compute(termify(iline), tfidfs)
        for i in range(0, min(5, len(results))):
            r = results[i]
            print("{0}. {1} -- {2}".format(i+1, r[0], int(r[1]*10000000)))

    
if __name__== "__main__":
  dosearch()

'''
 client = boto3.resource('dynamodb')
    table = client.Table('tfidf')
def term_tfidf(term, table):
    res = {}
    response = table.query(KeyConditionExpression=Key('term').eq(term))
    for item in response['Items']:
        doc_id = item['doc_id']
        tfidf = item['value']
        res[doc_id] = float(tfidf)
    return res
'''