# E-CommerceTrackingSystem
Tracking for E-Commerce system 

Hello, 
This is a E-Commerce project made by dvir.

The proccess of the project:
REST API service that has single GET enpoint on "/tracker" --> "Producer" container produce json text with the parameters --> send it to SQS queue --> "Consumer" container listen to SQS queue and send it to Elasticsearch container --> Kibana container stores the data and present road map of ip geo location.

Instructions:
1. Build your own queue named 'tracker' in Ireland eu-west-1

2. To build "Producer" image run (files: requirements.txt,Producer.py,Dockerfile): 
docker build -t producer . 

3. To run "Producer" container run (With your access key & secret access key):
docker run -e AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID> -e AWS_SECRET_ACCESS_KEY=<YOUR_ACCESS_KEY> -e SQS_URL=<YOUR_SQS_URL> --name producer -p 5000:5000 -d -it producerr

4. To build "Consumer" image run (files: requirements.txt,Consumer.py,Dockerfile): 
docker build -t consumer .

5. To run consumer container run:
docker run -e AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY_ID> -e AWS_SECRET_ACCESS_KEY=<YOUR_ACCESS_KEY> -p 1234:1234 --name consumer -d -it consumer 

6. To pull elasticsearch container run (optional):
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.2.0

7. To run elasticsearch container run:
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e network.host=0.0.0.0 -e START_DAEMON=TRUE --name elasticsearch -d -it docker.elastic.co/elasticsearch/elasticsearch:7.2.0

8. To pull Kibana container run (optional): 
docker pull docker.elastic.co/kibana/kibana:7.2.0

9. To run Kibana container run:
docker run -d -p 5601:5601 -h kibana --name kibana --link elasticsearch:elasticsearch docker.elastic.co/kibana/kibana:7.2.0

Done :)
