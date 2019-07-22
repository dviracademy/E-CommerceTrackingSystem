import boto3
from elasticsearch import Elasticsearch
import geocoder
from datetime import datetime as dt


msg_id = 0
# Receive messages from sqs
sqs = boto3.resource('sqs',region_name='eu-west-1')
queue = sqs.get_queue_by_name(QueueName='tracker')
es = Elasticsearch([{'host': '192.168.99.100', 'port': 9200}])

mappings = {
    "mappings": {
        "properties": {
            "phone": {"type": "text"},
            "price": {"type": "integer"},
            "usage": {"type": "text"},
            "pro_type": {"type": "text"},
            "currency": {"type": "text"},
            "product": {"type": "text"},
            "origin_ip": {"type": "ip"},
            "created": {"type": "date"},
            "location": {"type": "geo_point"}
        }
    }
}

index_name = 'entry_log'
try:
    es.indices.create(index=index_name, body=mappings)
except:
    print('Index already exists, proceeding as usual')

while True:
    print("Waiting for new product...")

    for message in queue.receive_messages(MaxNumberOfMessages=1, VisibilityTimeout=5, WaitTimeSeconds=20,MessageAttributeNames=['type', 'price', 'usage', 'currency', 'product','origin_ip']):
        pro_type = message.message_attributes.get('type').get('StringValue')
        price = message.message_attributes.get('price').get('StringValue')
        usage = message.message_attributes.get('usage').get('StringValue')
        currency = message.message_attributes.get('currency').get('StringValue')
        product = message.message_attributes.get('product').get('StringValue')
        origin_ip = message.message_attributes.get('origin_ip').get('StringValue')
        data = ("pro_type:"+ pro_type, "price:"+price, "usage:"+usage, "currency:"+currency, "product:"+product, "origin_ip:"+origin_ip)
        print("Found new product: ", data)

        # Generating IP to Longitude and Latitude geolocation
        g = geocoder.ip('me')
        long = g.lng
        lat = g.lat

        # Insert Data to Elasticearch
        if msg_id != message.message_id:

            print(es)

            p1={
                "pro_type":pro_type,
                "price":price,
                "usage": usage,
                "currency": currency,
                "product": product,
                "origin_ip":origin_ip,
                "location": "%s,%s" % (lat, long),
                'created': dt.now()
            }

            es.index(index=index_name, body=p1)
            msg_id = message.message_id
            message.delete()
