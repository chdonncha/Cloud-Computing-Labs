import httplib
import boto

conn = httplib.HTTPConnection("ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81")
conn.request("GET", "/key")

r1 = conn.getresponse().read().split(":")
print(r1[0])
print(r1[1])
print(boto.Version) 	
