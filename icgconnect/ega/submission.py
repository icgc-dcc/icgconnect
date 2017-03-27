
import requests, json

api_access_url = "https://ega.crg.eu/submitterportal/v1"


def login(username, password):
	""" Login to the ega submission api

		Args:
			username:	username of the ega-box
			password:	password for the username

		Returns:
			str: The return value. A session token

		Exceptions:
			ValueError: Authentication error if username and pasword do not match
	"""
	payload = {
		"username": username,
		"password": password,
		"loginType": "submitter"
	}

	return _result_from_response(requests.post(_api_access_endpoint('/login'), data=payload))[0]['session']['sessionToken']

def logout(session_token):
	""" Logout form the ega api

		Args:
			session_token:	A valid session token

		Returns:
			dict: Logout server response
	"""
	_validate_session_token(session_token)
	return _result_from_response(requests.delete(_api_access_endpoint('/logout'),headers=_session_headers(session_token)))[0]['session'] == None

def studies_index(session_token,status=None):
	""" Index all accessible studies

		Args:
			session_token:	A valid session token
			status:			The status of the studies

		Returns:
			dict:	All accessible studies
	"""
	return _objects_index(session_token,'studies',status)

def studies_get(session_token,id_type,id, submission_id=None):
	""" Retrieve a study

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			submission_id:	A submission id as filter

		Returns:
			dict:	The study found
	"""
	return _objects_get(session_token,'studies',id_type,id, submission_id)

def samples_index(session_token, status=None):
	""" Index all samples

		Args:
			session_token:	A valid session token
			status:			A status for the sample

		Returns:
			dict:	A list of samples
	"""
	return _objects_index(session_token,'samples',status)

def samples_get(session_token, id_type, id, submission_id=None):
	""" Retrive a sample

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the sample
			submission_id:	A submission id as filter

		Returns:
			dict:	The corresponding sample
	"""
	return _objects_get(session_token,'samples',id_type,id, submission_id)

def datasets_index(session_token, status=None):
	""" Index all datasets

		Args:
			session_token:	A valid session token
			status:			The status of the datasets

		Returns:
			dict:	All corresponding datasets
	"""
	return _objects_index(session_token,'datasets',status)

def datasets_get(session_token, id_type, id, submission_id=None):
	""" Retrive a dataset

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the dataset to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	A dataset
	"""
	return _objects_get(session_token,'datasets',id_type,id, submission_id=None)

def experiments_index(session_token, status=None):
	""" Index all experiments

		Args:
			session_token:	A valid session token
			status:			Status of the experiments to retrieve

		Returns:
			dict:	An experiment
	"""
	return _objects_index(session_token,'experiments',status)

def experiments_get(session_token, id_type, id, submission_id=None):
	"""	Retrive an experiment

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the experiment to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding experiment
	"""
	return _objects_get(session_token,'experiments',id_type,id, submission_id=None)

def analyses_index(session_token, status=None):
	""" Index all analyses

		Args:
			session_token:	A valid session token
			status:			A status to filter the analyses

		Returns:
			dict:	Index of accessible analyses
	"""
	return _objects_index(session_token,'analyses',status)

def analyses_get(session_token, id_type, id, submission_id=None):
	""" Retrive an analysis

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the analysis to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding analysis
	"""
	return _objects_get(session_token,'analyses',id_type,id, submission_id=None)

def dacs_index(session_token, status=None):
	""" Index all dacs

		Args:
			session_token:	A valid session token
			status:			A status to filter the dacs

		Returns:
			dict:	Index all dacs
	"""
	return _objects_index(session_token,'dacs',status)

def dacs_get(session_token, id_type, id, submission_id=None):
	""" Retrieve a dac

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the dac to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding dac
	"""
	return _objects_get(session_token,'dacs',id_type,id, submission_id=None)

def policies_index(session_token, status=None):
	""" Index all policies

		Args:
			session_token: 	A valid session token
			status:			A status to filter the policies

		Returns:
			dict:	Index all policies
	"""
	return _objects_index(session_token,'policies',status)

def policies_get(session_token, id_type, id, submission_id=None):
	""" Retrieve a policy

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the policy to retrive
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding policy
	"""
	return _objects_get(session_token,'policies',id_type,id, submission_id=None)

def runs_index(session_token, status=None):
	""" Index all runs

		Args:
			session_token:	A valid session token
			status:			A status to filter the runs

		Returns:
			dict:	Index all runs
	"""
	return _objects_index(session_token,'runs',status)

def runs_get(session_token, id_type, id, submission_id=None):
	""" Retrieve a run

		Args:
			session_token: 	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the run to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding run
	"""
	return _objects_get(session_token,'runs',id_type,id, submission_id=None)

def submissions_index(session_token, status=None):
	""" Index all submissions

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the submission to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding submission
	"""
	return _objects_index(session_token,'submissions',status, submission_id=None)

def submissions_get(session_token, id_type, id, submission_id=None):
	""" Retrieve a submission

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the submission to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The corresponding submission
	"""
	return _objects_get(session_token,'submissions',id_type,id, submission_id=None)

def enum_analysis_file_types():
	""" Enumeration of analysis file types

		Returns:
			dict:	List of analysis file types
	"""
	return _get_enum('analysis_file_types')

def enum_analysis_types():
	""" Enumeration of analysis types

		Returns:
			dict:	List of analysis types
	"""
	return _get_enum('analysis_types')

def enum_case_control():
	""" Enumeration of case or control

		Returns:
			dict:	List case or control
	"""
	return _get_enum('case_control')

def enum_dataset_types():
	""" Enumeration of dataset types

		Returns:
			dict:	List dataset types
	"""
	return _get_enum('experiment_types')

def enum_experiment_types():
	""" Enumeration of experiment types

		Returns:
			dict:	List experiment types
	"""
	return _get_enum('experiment_types')

def enum_file_types():
	""" Enumeration of file types

		Returns:
			dict:	List file types
	"""
	return _get_enum('file_types')

def enum_genders():
	""" Enumeration of genders

		Returns:
			dict:	List of genders
	"""
	return _get_enum('genders')

def enum_instrument_models():
	""" Enumeration of instrument models

		Returns:
			dict:	List of instrument models
	"""
	return _get_enum('instrument_models')

def enum_library_selections():
	""" Enumeration of library selections

		Returns:
			dict:	List of library selections
	"""
	return _get_enum('library_selections')

def enum_library_sources():
	""" Enumeration of library sources

		Returns:
			dict: List of library sources
	"""
	return _get_enum('library_sources')

def enum_library_strategies():
	""" Enumeration of library strategies

		Returns:
			dict: List of library strategies
	"""
	return _get_enum('library_strategies')

def enum_reference_chromosomes():
	""" Enumeration of reference chromosomes

		Returns:
			dict:	List of reference chromosomes
	"""
	return _get_enum('reference_chromosomes')

def enum_reference_genomes():
	""" Enumeration of reference genomes

		Returns:
			dict:	List of reference genomes
	"""
	return _get_enum('reference_genomes')

def enum_study_types():
	""" Enumeration of study types

		Returns:
			dict:	List of study types
	"""
	return _get_enum('study_types')

def _get_enum(_type):
	""" Return a specific enumeration - Generic

		Args:
			_type:	The name of the enumeration

		Raises:
			ValueError: The _type has to be in the available list

		Returns:
			dict:	List an enumeration
	"""
	enums = ['analysis_file_types','analysis_types','case_control','dataset_types','experiment_types','file_types','genders','instrument_models','library_selections','library_sources','library_strategies',
	'reference_chromosomes','reference_genomes','study_types']
	
	if not _type in enums:
		raise ValueError("Invalid enum: "+', '.join(enums))

	return _result_from_response(requests.get(_api_access_endpoint('/enums/'+_type)))


def _objects_index(session_token, object_type,status=None, submission_id=None):
	""" The index of available objects - Generic

		Args:
			session_token: 	A valid session token
			object_type:	The type of object to index
			status:			A status to filter the index
			submission_id:	A submission id for filtering

		Raises:
			ValueError:	An invalid session token
			ValueError:	An invalid object type

		Returns:
			dict:	The index of requested object type available
	"""
	_validate_session_token(session_token)
	url = '/'

	if submission_id!=None:
		url = '/submissions/'+submission_id+"/"

	object_types = ['studies','samples','submissions','datasets','experiments','analyses','dacs','policies','runs']

	if not object_type in object_types:
		raise ValueError("Object "+object_type+" is not valid. "+', '.join(object_types))
	if status == None:
		r = _result_from_response(requests.get(_api_access_endpoint(url+object_type), headers=_session_headers(session_token)))
		if(len(r)>0):
			return r[0]['json']
	else:
		r = _result_from_response(requests.get(_api_access_endpoint(url+object_type+'?status='+status.upper()), headers=_session_headers(session_token)))
		if(len(r)>0):
			return r[0]['json']

def _objects_get(session_token,object_type,id_type,id, submission_id=None):
	""" Retrieve a specific object - Generic

		Args:
			session_token:	A valid session token
			object_type:	The type of the object to retrieve
			id_type:		Type of id ega_stable_id or ALIAS
			id:				Id of the object to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The requested object
	"""
	_validate_session_token(session_token)
	validate_id_type(id_type)
	return _result_from_response(requests.get(_api_access_endpoint('/'+object_type+'/'+id+'?idtype='+id_type), headers=_session_headers(session_token)))[0]['json']

def _session_headers(session_token):
	""" Generate the session header with the session token

		Args:
			session_token:	A valid session token

		Returns:
			str:	A header for the request
	"""
	return {'Content-Type': 'application/json','X-Token': session_token}

def _validate_status(status):
	""" Check if a status exists

		Args:
			status:	A status to validate

		Raises:
			ValueError:	An invalid status
	"""
	if not status in ['DRAFT','VALIDATED','VALIDATED_WITH_ERRORS','PARTIALLY_SUBMITTED','SUBMITTED']:
		raise ValueError("Status must be either DRAFT, VALIDATED, VALIDATED_WITH_ERRORS, PARTIALLY_SUBMITTED, SUBMITTED")

def validate_id_type(id_type):
	""" Check if the id_type exists

		Args:
			id_type:	An id type to validate

		Raises:
			ValueError:	An invalid id type
	"""
	if not id_type in ['ega_stable_id','ALIAS']:
		raise ValueError("ID type must be either ega_stable_id or ALIAS")

def _api_access_endpoint(endpoint,session_token=None):
	""" Generate the api access endpoint

		Args:
			endpoint:		A valid endpoint path
			session_token:	A valid session token

		Returns:
			str:	The api url
	"""
	if session_token == None:
		return api_access_url+endpoint
	return api_access_url+endpoint+"?session="+session_token

def _result_from_response(raw_response):
	""" Get result of server response

		Args:
			raw_response:	A response from EGA server

		Returns:
			str:	The result
	"""
	r = json.loads(raw_response.text)
	_validate_response(r)
	return r['response']['result']

def _validate_response(json_response):
	""" Validate the EGA server response

		Args:
			json_response:	A json response from EGA

		Raises:
			ValueError:	An invalid json response
	"""
	if json_response['header']['code'] != "200":
		raise ValueError(json_response['header']['userMessage'])

def _validate_session_token(session_token):
	""" Validate a session token

		Args:
			session_token:	A session token generated by EGA

		Raises:
			ValueError:	An invalid session token
	"""
	if session_token == None:
		raise ValueError("EGA session token is empty")
