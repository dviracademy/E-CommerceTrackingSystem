import boto3
from flask import Flask, request
from requests import get
import os


# Making the listener using flask
app = Flask(__name__)
# Example URL: www.example.com/tracking?type=phone&product=iphone&usage=personal&price=200&currency=usd

@app.route('/tracking', methods=['GET'])
def producer():
    # Requests for information about the attributes in the url using request
    product_type = request.args.get('type')
    product = request.args.get('product')
    usage = request.args.get('usage')
    price = request.args.get('price')
    currency = request.args.get('currency')
    ip_address = get('https://api.ipify.org').text

    # Making the json with all the parameters to be send
    json = {
        'type': {
            'DataType': 'String',
            'StringValue': product_type
        },
        'product': {
            'DataType': 'String',
            'StringValue': product
        },

        'usage':{
            'DataType': 'String',
            'StringValue': usage
        },
        'price':  {
            'DataType': 'Number',
            'StringValue': price
        },
        'currency': {
            'DataType': 'String',
            'StringValue': currency
        },
        'origin_ip': {
            'DataType': 'String',
            'StringValue': ip_address
        }
    }
    # Sending the data to SQS queue with boto3
    sqs_queue_url = os.environ['SQS_URL']
    #sqs_queue_url = 'https://sqs.eu-west-1.amazonaws.com/362954016127/tracker'
    sqs = boto3.client('sqs',region_name='eu-west-1')
    try:
        msg_id = sqs.send_message(QueueUrl=sqs_queue_url, MessageBody=product_type, MessageAttributes=json)
        msg_id = msg_id["MessageId"]
    except Exception as e:
        return {"error": 'There was an error handling the message: %s' %e}

    return ('Sent message to sqs with data: '
            + product_type + ", " + product +  ", " + usage + ", " + price +  ", " + currency +
            ". From ip address: "+ ip_address +'. The SQS message ID: ' + msg_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)





