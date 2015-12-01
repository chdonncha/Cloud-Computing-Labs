# This script created a queue
#
# Author - Paul Doyle Nov 2015
#
#
import httplib
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys

keys = httplib.HTTPConnection("ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81")
keys.request("GET", "/key")

r1 = keys.getresponse().read().split(":")

# Get the keys from a specific url and then use them to connect to AWS Service 
access_key_id = r1[0]
secret_access_key = r1[1]

# Set up a connection to the AWS service. 

conn = boto.sqs.connect_to_region(
	"eu-west-1",
	aws_access_key_id=access_key_id,
	aws_secret_access_key=secret_access_key
)


# Get a list of the queues that exists and then print the list out
# Do not use / or " in the name
q = conn.get_queue("D14123580-%s" % sys.argv[1])

messages = q.get_messages()

for i in range(0, len(messages)):
	print("Message read = %s" % messages[i].get_body())
