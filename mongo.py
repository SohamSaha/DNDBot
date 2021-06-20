import os
import pymongo
from pymongo.common import SERVER_SELECTION_TIMEOUT

conn_str = os.environ['CONNECTION_STRING']

client = pymongo.MongoClient(conn_str, SERVER_SELECTION_TIMEOUT-5000)

def get_value(collection, query_key, query_value, db_key):
    col = client[os.environ['DND_DATABASE']][collection]
    query = { query_key : query_value }
    doc = col.find(query, {'_id': 0, db_key: 1})
    for value in doc:
        return (value)

def update_record(collection, query_key, query_value, component, value):
    col = client[os.environ['DND_DATABASE']][collection]
    col.update_one({query_key : query_value}, {"$set": { component : value }})

def get_collection_length(collection):
    col = client[os.environ['DND_DATABASE']][collection]
    return (col.count_documents({}))

def get_campaign_users():
    index = 1
    user_string = ''
    while index <= get_collection_length('Campaign 1 Users'): 
        received_name = get_value('Campaign 1 Users', 'index', str(index), 'value')
        formatted_name = received_name['value']
        user_string += '<@' + formatted_name + '> '
        index += 1
    return (user_string)