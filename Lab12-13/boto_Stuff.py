import httplib
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
import os
import json
from flask import Flask, request, redirect, url_for, Response

app = Flask(__name__)

@app.route("/")
def index():
    return """
Available API endpoints:

GET	/queues				List all queues
POST	/queues				Create a new queue
DELETE	/queues/<qid>			Delete a specific queue
GET	/queues/<qid>/msgs		Get a message, return it to the user
GET	/queues/<qid>/msgs/count	Return the number of messages in a queue
POST	/queues/<qid>/msgs		Write a new message to a queue
DELETE	/queues/<qid>/msgs		Get and delete a message from the queue

"""

@app.route ('/getKeys', methods=['GET'] )
def get_conn():

	keys = httplib.HTTPConnection("ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81") 
	keys.request("GET", "/key")

	r1 = keys.getresponse().read().split(":")

	access_key_id = r1[0]
	secret_access_key = r1[1]

	return boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

@app.route("/queues", methods=["GET"])
def queues_index():
	"""
	List all queues
	curl -s -X GET -H 'Accept: application/json' http://localhost:5000/queues | python -mjson.tool
	"""
	all = []
	conn = get_conn()

	for q in conn.get_all_queues():
		all.append(q.name)

	resp = json.dumps(all)
	return Response(response=resp, mimetype="application/json")


@app.route("/queues", methods=["GET"])
def queues_index():
        """
        Create Queue
        curl -s -X GET -H 'Accept: application/json' http://localhost:5000/queues | python -mjson.tool
        """

	access_key_id = r1[0]
	secret_access_key = r1[1]

	myqueue = conn.create_queue("D14123580-%s" % sys.argv[1])

	print(myqueue.id)

	"""
	rs = conn.get_all_queues()
	for q in rs:
        	print q.id
	"""



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
