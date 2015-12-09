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


@app.route("/queues", methods=["POST"])
def queue_create():
	"""
	Create a new queue
	curl -X POST -H 'Content-Type: application/json' http://localhost:5000/queue -d '{"name":"my-queue"}'
	"""

	conn = get_conn()
	body = request.get_json(force=True)

	myqueue = conn.create_queue("D14123580-%s" % body['name'])

	resp = {"id":myqueue.id}

	return Response(response=json.dumps(resp),mimetype="application/json")

@app.route("/queues/<queue>", methods=["DELETE"])
def queue_delete(queue):
	"""
	Delete Queue
	curl -X DELETE -H 'Content-Type: application/json' http://localhost:5000/queue/<mytestqueue>
	"""

	conn = get_conn()

	q = conn.get_queue("D14123580-%s" % queue)

	resp = {}

	if q != None:	
		r = conn.delete_queue(q)
		resp["id"] = q.id
		resp["status"] = "Queue is deleted"
	else:
		resp["status"] = "Queue is not deleted"

	return Response(response=json.dumps(resp),mimetype="application/json")


@app.route("/queues/<queue>/msgs/count", methods=["GET"])
def queue_msgcount(queue):
	"""
	Counts the number of messages in the queue

	curl -X GET -H 'Content-Type: application/json' http://localhost:5000/queues/<mytestqueue>/msgs/count
	"""

	conn = get_conn()

	q = conn.get_queue("D14123580-%s" % queue)

	resp = {}

	if q != None:
		resp["id"] = q.id
		resp["count"] = q.count()
	else:
		resp["status"] = "Not Found"

	return Response(response=json.dumps(resp), mimetype="application/json")

@app.route("/queues/<queue>/msgs", methods=["POST"])
def queue_msgwrite(queue):
	"""
	Writes a message to the queue

	curl -X POST -H 'Content-Type: application/json' http://localhost:5000/queues/<mytestqueue>/msgs -d '{"content":"message"}'
	"""
	conn = get_conn()
	body = request.get_json(force=True)

	q = conn.get_queue("D14123580-%s" % queue)

	resp = {}

	if q != None:
		m = Message()
		m.set_body(body["content"])
		q.write(m)
		resp["id"] = q.id
		resp["message"] = m.get_body()
	else:
		resp["status"] = "Not Found"

	return Response(response=json.dumps(resp), mimetype="application/json")

@app.route("/queues/<queue>/msgs", methods=["DELETE"])
def queue_msgreaddelete(queue):
	"""
	Reads a message to the queue

	curl -X DELETE -H 'Content-Type: application/json' http://localhost:5000/queues/<mytestqueue>/msgs
	"""
	conn = get_conn()

	q = conn.get_queue("D14123580-%s" % queue)

	resp = {}

	m = q.read(60)

	if (m != None):
		resp["id"] = q.id
		resp["message"] = m.get_body()
		q.delete_message(m)
	else:
		resp["status"] = "Not Found"

	return Response(response=json.dumps(resp),mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
