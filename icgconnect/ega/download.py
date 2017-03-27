
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import json
import subprocess
import hashlib
import os

api_access_url = "https://ega.ebi.ac.uk/ega/rest/access/v2"
api_download_url = "http://ega.ebi.ac.uk/ega/rest/ds/v2"

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def login(email, password):
	""" Login to the ega api

		Args:
			email (str): 		Email of the user to login
			password (str): 	Password of the user

		Returns:
			str: The return value. A session token

		Raises:
			ValueError: If `email` format is not a valid email
	"""

	# Email must be a valid email
	if not re.match("[^@]+@[^@]+\.[^@]+", email):
		raise ValueError(email+" is not a valid email")

	print _api_access_endpoint("/users/"+email+"?pass="+password, None)

	return result_from_response(requests.get(_api_access_endpoint("/users/"+email+"?pass="+password, None), verify=False))[1]

def logout(session_token):
	""" Logout from the ega api

		Args:
			session_token: A valid session token

		Return:
			dict: Logout server response

	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/users/logout",session_token), verify=False))[0]

def datasets_index(session_token):
	""" List the dataset ids

		Args:
			session_token: A valid session token

		Return:
			dict: List of dataset ids
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/datasets",session_token), verify=False))

def files_index(session_token, dataset):
	""" List files in a dataset

		Args:
			session_token: A valid session token
			dataset: ID of the dataset

		Return:
			dict: List of files in the dataset
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/datasets/"+dataset+"/files",session_token), verify=False))

def files_get(session_token, file_id):
	""" Informations about one file

		Args:
			session_token: A valid session token
			file_id: A file id to access

		Return:
			dict: Informations about the requested file
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/files/"+file_id,session_token), verify=True))

def requests_index(session_token):
	""" List of indexes

		Args:
			session_token: A valid session token

		Return:
			dict: All opened requests in the account
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/requests",session_token), verify=False))

def requests_get(session_token, request_label):
	""" Informations about a request

		Args:
			session_token: A valid session token

		Return:
			dict: The informations about the requested request
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/requests/"+request_label,session_token), verify=False))

def requests_delete(session_token, request_label):
	""" Delete an existing request

		Args:
			session_token: A valid session token

		Return:
			dict: The deletion status
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/requests/delete/"+request_label, session_token), verify=False))

def requests_create(session_token, object_id, type, encryption_key, request_label):
	"""  Delete an existing request 

		Args:
			session_token: A valid session token
			object_id: The id of the object to download
			type: Type of data to download
			encryption_key: Encrypt key to use for encryption
			request_lable: A label name for the request

		Return:
			dict: The informations about the created request

		Raises:
			ValueError: The type has to be either files or datasets
			ValueError: An error from the ega server
	"""
	validate_session_token(session_token)

	if not type.lower() in ['datasets','files']:
		raise ValueError("Request can be created only on files or datasets")

	downloadrequest = {'downloadrequest':'{"rekey":'+encryption_key+',"downloadType":"STREAM","descriptor":'+request_label+'}'}
	response = requests.post("https://ega.ebi.ac.uk/ega/rest/access/v2/requests/new/"+type+"/"+object_id+"?session="+session_token,data=downloadrequest,headers={'Accept':'application/json'}, verify=False)
	if response.status_code != 200:
		raise ValueError(json.loads(response)['header']['userMessage'])

	return requests_get(session_token,request_label)[0]

def tickets_get(session_token, ticket_id):
	""" Informations about a ticket

		Args:
			session_token: A valid session token
			ticket_id: The id of an existing ticket

		Return:
			dict: The informations about the existing ticket
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/requests/ticket/"+ticket_id,session_token), verify=False))

def tickets_delete(session_token, ticket_id):
	""" Delete an existing ticket

		Args:
			session_token: A valid session token
			ticket_id: The id of an existing ticket

		Return:
			dict: The EGA response after deletion
	"""
	validate_session_token(session_token)
	return result_from_response(requests.get(_api_access_endpoint("/requests/ticket/delete/"+ticket_id,session_token), verify=False))

def results(ticket_id):
	r = requests.get(api_download_url+"/results/"+ticket_id, verify=False)
	return r.text

def _api_access_endpoint(endpoint,session_token=None):
	""" Create the endpoint to call

		Args:
			endpoint: Parameter of the endpoint (/example)
			session_token: A valid session token

		Return:
			The endpoint URL to use
	"""
	if session_token == None:
		return api_access_url+endpoint
	return api_access_url+endpoint+"?session="+session_token

def validate_session_token(session_token):
	""" Check if the session token is valid

		Args:
			session_token:	A session token

		Raises:
			ValueError: The session token is empty
	"""
	if session_token == None:
		raise ValueError("EGA session token is empty")

def validate_response(json_response):
	""" Check if the response code is 200

		Args:
			json_response:	A json response from server request result

		Raises:
			ValueError: An error from the server
	"""
	if json_response['header']['code'] != "200":
		raise ValueError(json_response['header']['userMessage'])

def result_from_response(raw_response):
	""" Retrieve the result from server response

		Args:
			raw_response:	A response from the server
	"""
	r = json.loads(raw_response.text)
	validate_response(r)
	return r['response']['result']

def download_request(email, password, request_label,type, output_folder, streams=7):
	if not type.lower() in ['datasets','files']:
		raise ValueError("Request can be created only on files or datasets")

	if type == "files":
		subprocess.call(['java','-jar','EgaDemoClient.jar','-p',email,password,'-dr',request_label,'-path',output_folder,'-nt',str(streams)])
		#r = requests.get(api_download_url+"/downloads/"+ticket_id,headers={'Accept': 'application/octet-stream'}, stream=True)
		#with open(output_file,"wb") as f:
		#	for chunk in r.iter_content(chunk_size=1024):
		#		if chunk:
		#			f.write(chunk)

def decrypt_encrypted_file(email,password,_file,decryption_key):
	""" Decrypt an ega encrypted file

		Args:
			email (str): 		Email of the user to login
			password (str): 	Password of the user
			_file:				The path of the file to be decrypted
			decryption_key:		A valid key to decrypt the file
	"""
	# Email must be a valid email
	if not re.match("[^@]+@[^@]+\.[^@]+", email):
		raise ValueError(email+" is not a valid email")

	subprocess.call(['java','-jar','EgaDemoClient.jar','-p',email,password,'-dc',_file,'-dck',decryption_key])


