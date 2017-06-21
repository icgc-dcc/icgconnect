
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

	return str(_result_from_response(requests.post(_api_access_endpoint('/login'), data=payload))[0]['session']['sessionToken'])

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
	studies = _objects_index(session_token,'studies',status)
	output = []

	for i in xrange(0, len(studies)):
		tags = []
		for j in xrange(0,len(studies[i].get('customTags'))):
			tags.append({'tag':studies[i].get('customTags')[j].get('tag'),
						 'value': studies[i].get('customTags')[j].get('value')})

		output.append({'alias': studies[i].get('alias'),
						'id':studies[i].get('id'),
					   'study_type_id':studies[i].get('studyTypeId'),
					   'short_name':studies[i].get('shortName'),
					   'title': studies[i].get('title'),
					   'study_abstract': studies[i].get('studyAbstract'),
					   'own_term': studies[i].get('ownTerm'),
					   'pubmed_ids': studies[i].get('pubmedIds'),
					   'custom_tags': tags})

	return output

def studies_get(session_token,id_type,id, submission_id=None):
	""" Retrieve a study

		Args:
			session_token:	A valid session token
			id_type:		Type of id ega_stable_id or ALIAS
			submission_id:	A submission id as filter

		Returns:
			dict:	The study found
	"""
	study = _objects_get(session_token,'studies',id_type,id, submission_id)

	tags = []
	for j in xrange(0, len(study.get('customTags'))):
		tags.append({'tag': study.get('customTags')[j].get('tag'),
					 'value': study.get('customTags')[j].get('value')})

	return {'alias':study.get('alias'),
			'id': study.get('id'),
			'study_type_id': study.get('studyTypeId'),
			'short_name': study.get('shortName'),
			'title': study.get('title'),
			'study_abstract': study.get('studyAbstract'),
			'own_term': study.get('ownTerm'),
			'pub_med_ids':study.get('pubMedIds'),
			'custom_tags': study.get('customTags')}

def studies_post(session_token, submission_id, alias=None, study_type_id=None, short_name=None, title=None, study_abastract=None, own_term=None,
				 pub_med_ids=[],custom_tags=[]):

	"""
	Create a study on EGA submission
	:param session_token: 	A valid session token
	:param submission_id: 	A valid subimssion id
	:param alias: 			The alias assigned to the study
	:param study_type_id: 	The type of study from the study types list
	:param short_name: 		The short name of the study
	:param title: 			The title assigned to the study
	:param study_abastract: The abastract
	:param own_term: 		The own term
	:param pub_med_ids: 	Array of pubmed ids
	:param custom_tags: 	An array of custom tags
	:return: dict:			The created study
	"""

	data = {}
	data['alias'] = alias
	data['studyTypeId'] = study_type_id
	data['shortName'] = short_name
	data['title'] = title
	data['studyAbstract'] = study_abastract
	data['ownTerm'] = own_term
	data['pubMedIds'] = pub_med_ids
	data['customTags'] = []

	for tag in custom_tags:
		data['customTags'].append({'tag':tag['tag'], 'value':tag['value']})

	return _objects_post(session_token, 'studies',submission_id,data)

def samples_index(session_token, status=None):
	""" Index all samples

		Args:
			session_token:	A valid session token
			status:			A status for the sample

		Returns:
			dict:	A list of samples
	"""
	samples = _objects_index(session_token,'samples',status)
	output = []

	for sample in samples:
		attributes = []
		for attribute in sample.get('attributes'):
			attributes.append({'tag': attribute.get('tag'), 'value': attribute.get('value')})
		output.append({'id': sample.get('id'),
					   'alias': sample.get('alias'),
					   'description': sample.get('description'),
					   'case_or_control-id': sample.get('caseOrControlId'),
					   'gender_id': sample.get('genderId'),
					   'organism_part': sample.get('organismPart'),
					   'cell_line': sample.get('cellLine'),
					   'region': sample.get('region'),
					   'phenotype': sample.get('phenotype'),
					   'subject_id': sample.get('subjectId'),
					   'anonymized_name': sample.get('anonymizedName'),
					   'biosample_id': sample.get('biosampleId'),
					   'sample_age': sample.get('sampleAge'),
					   'sample_detail': sample.get('sampleDetail'),
					   'attributes': attributes})

	return  output

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
	sample = _objects_get(session_token,'samples',id_type,id, submission_id)
	attributes = []
	for attribute in sample.get('attributes'):
		attributes.append({'tag': attribute.get('tag'), 'value': attribute.get('value')})
	return {'id': sample.get('id'),
			'alias': sample.get('alias'),
			'description': sample.get('description'),
			'case_or_control-id': sample.get('caseOrControlId'),
			'gender_id': sample.get('genderId'),
			'organism_part': sample.get('organismPart'),
			'cell_line': sample.get('cellLine'),
			'region': sample.get('region'),
			'phenotype': sample.get('phenotype'),
			'subject_id': sample.get('subjectId'),
			'anonymized_name': sample.get('anonymizedName'),
			'biosample_id': sample.get('biosampleId'),
			'sample_age': sample.get('sampleAge'),
			'sample_detail': sample.get('sampleDetail'),
			'attributes': attributes
			}

def samples_post(session_token, submission_id,alias=None, title=None, description=None, case_or_control_id=None,
				 gender_id=None, organism_part=None, cell_line=None, region=None, phenotype=None, subject_id=None,
				 anonymized_name=None, bio_sample_id=None, sample_age=None, sample_detail=None, attributes=[]):
	data = {}
	data['alias'] = alias
	data['title'] = title
	data['description'] = description
	data['caseOrControlId'] = case_or_control_id
	data['genderId'] = gender_id
	data['organismPart'] = organism_part
	data['cellLine'] = cell_line
	data['region'] = region
	data['phenotype'] = phenotype
	data['subjectId'] = subject_id
	data['anonymizedName'] = anonymized_name
	data['bioSampleId'] = bio_sample_id
	data['sampleAge'] = sample_age
	data['sampleDetail'] = sample_detail
	data['attributes'] = []

	for attribute in attributes:
		data['attributes'].append({'tag':attribute['tag'],'value':attribute['value']})

	return _objects_post(session_token,'samples',submission_id,data)

def samples_put(session_token, id, alias=None, title=None, description=None, case_or_control_id=None, gender_id=None,
				organism_part=None, cell_line=None, region=None, phenotype=None, subject_id=None, anonymized_name=None,
				bio_sample_id=None, sample_age=None, sample_detail=None, attributes=[]):
	data = {}
	data['alias'] = alias
	data['title'] = title
	data['description'] = description
	data['caseOrControlId'] = case_or_control_id
	data['genderId'] = gender_id
	data['organismPart'] = organism_part
	data['cellLine'] = cell_line
	data['region'] = region
	data['phenotype'] = phenotype
	data['subjectId'] = subject_id
	data['anonymizedName'] = anonymized_name
	data['bioSampleId'] = bio_sample_id
	data['sampleAge'] = sample_age
	data['sampleDetail'] = sample_detail
	data['attributes'] = attributes

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

def datasets_post(session_token, submission_id, alias, dataset_type_ids=[], policy_id=None, runs_references = None, analysis_references=[],title=None, dataset_links=[], attributes=[]):
	data = {}
	data['alias'] = alias
	data['datasetTypeIds'] = dataset_type_ids
	data['policyId'] = policy_id
	data['runsReferences'] = runs_references
	data['analysisReferences'] = analysis_references
	data['title'] = title
	data['datasetLinks'] = []
	data['attributes'] = []

	for link in dataset_links:
		data['datasetLinks'].append({'tag':link['label'], 'url':link['url']})

	for attribute in attributes:
		data['attributes'].append({'tag':attribute['tag'],'value':attribute['value']})

	return _objects_post(session_token, 'datasets',submission_id,data)


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

def experiments_post(session_token, submission_id, alias, title=None, instrument_model_id=None,
					 library_source_id=None, library_selection_id=None, library_strategy_id=None,
					 design_description=None, library_name=None, library_construction_protocol=None,
					 library_layout_id=None,paired_nominal_length=0, paired_nominal_sdev=0, sample_id=None, study_id=None):

	data = {}
	data['alias'] = alias
	data['title'] = title
	data['instrumentModelId'] = instrument_model_id
	data['librarySourceId'] = library_source_id
	data['librarySelectionId'] = library_selection_id
	data['libraryStrategyId'] = library_strategy_id
	data['designDescription'] = design_description
	data['libraryName'] = library_name
	data['libraryConstructionProtocol'] = library_construction_protocol
	data['libraryLayoutId'] = library_layout_id
	data['pairedNominalLength'] = paired_nominal_length
	data['pairedNominalSdev'] = paired_nominal_sdev
	data['sampleId'] = sample_id
	data['studyId'] = study_id

	return  _objects_post(session_token,'experiments',submission_id,data)

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

def analyses_post(session_token, submission_id, alias=None, title=None, description=None, study_id=None, sample_references=[],
				  analysis_center=None, analysis_date=None, analysis_type_id=None, files=[],
				  attributes=[], genome_id=None, chromosome_references=[],experiment_type_id=[],platform=None):
	data = {}
	data['alias'] = alias
	data['title'] = title
	data['description'] = description
	data['studyId'] = study_id
	data['analysisCenter'] = analysis_center
	data['analysisDate'] = analysis_date
	data['analysisTypeId'] = analysis_type_id
	data['genomeId'] = genome_id
	data['experimentTypeId'] = experiment_type_id
	data['platform'] = platform

	data['sampleReferences'] = []
	data['files'] = []
	data['attributes'] = []
	data['chromosomeReferences'] = []

	for reference in sample_references:
		data['sampleReferences'].append({'value':reference['value'],'label':reference['label']})

	for _file in files:
		data['files'].append({'fileId':_file['file_id'],'fileName':_file['file_name'],'checksum':_file['checksum'],
		'unencryptedChecksum':_file['unencrypted_checksum'],'fileTypeId':_file['file_type_id']})

	for attribute in attributes:
		data['attribtues'].append({'tag':attribute['tag'], 'value':attribute['value'],'unit':attribute['unit']})

	for reference in chromosome_references:
		data['chromosomeReferences'].append({'value':reference['value'],'label':reference['label']})

	return _objects_post(session_token,'analyses',submission_id,data)

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

def dacs_post(session_token, submission_id, alias=None, title=None, contacts=[]):
	data = {}
	data['alias'] = alias
	data['title'] = title
	data['contacts'] = contacts

	return _objects_post(session_token,'dacs',submission_id, data)

def dacs_put(session_token, id, alias=None, title=None, contacts=[]):
	data = {}
	data['alias'] = alias
	data['title'] = title
	data['contacts'] = contacts

	return _objects_put(session_token, 'dacs',id,data)

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

def policies_post(session_token, submission_id, alias, dac_id=None, title=None, policy_text=None, _url=None):
	data = {}
	data['alias'] = alias
	data['dacId'] = dac_id
	data['title'] = title
	data['policyText'] = policy_text
	data['url'] = _url
	data = json.dumps(data)
	return _objects_post(session_token, 'policies', submission_id, data)

def policies_put(session_token, policy_id, alias, dac_id, title, policy_text, _url):
	data = {}
	data['alias'] = alias
	data['dacId'] = dac_id
	data['title'] = title
	data['policyText'] = policy_text
	data['url'] = _url

	data = json.dumps(data)
	return _objects_put(session_token, 'samples',policy_id, data)


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

def runs_post(session_token, submission_id,alias=None, sample_id=None, run_file_type_id=None, experiment_id=None, files=[]):
	data = {}
	data['alias'] = alias
	data['sampleId'] = sample_id
	data['runFileTypeId'] = run_file_type_id
	data['experimentId'] = experiment_id
	data['files'] = []
	for _file in files:
		data['files'].append({'fileId':_file['file_id'],
							  'fileName':_file['file_name'],
							  'checksum':_file['checksum'],
							  'unencryptedChecksum':_file['unencrypted_checksum'],
							  'checksumMethod':_file['checksum_method']})

	return _objects_post(session_token, 'runs',submission_id,data)

def runs_put(session_token, sample_id, alias=None, run_file_type_id=None, experiment_id=None, files=[]):
	data = {}
	data['alias'] = alias
	data['sampleId'] = sample_id
	data['runFileTypeId'] = run_file_type_id
	data['experimentId'] = experiment_id
	data['files'] = []
	for _file in files:
		data['files'].append({'fileId': _file['file_id'],
							  'fileName': _file['file_name'],
							  'checksum': _file['checksum'],
							  'unencryptedChecksum': _file['unencrypted_checksum'],
							  'checksumMethod': _file['checksum_method']})

	return _objects_put(session_token, 'runs', sample_id, data)

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

def submissions_post(session_token, title=None, description=None, analysis_ids=None, dac_ids=None, dataset_ids=None,
					 experiment_ids=None, policy_ids=None, run_ids=None, sample_ids=None, study_ids=None):
	data = {}
	data['title'] = title
	data['description'] = description

	data['submissionSubset'] = {}
	data['submissionSubset']['analysisIds'] = analysis_ids
	data['submissionSubset']['dacIds'] = dac_ids
	data['submissionSubset']['datasetIds'] = dataset_ids
	data['submissionSubset']['experimentIds'] = experiment_ids
	data['submissionSubset']['policyIds'] = policy_ids
	data['submissionSubset']['runIds'] = run_ids
	data['submissionSubset']['sampleIds'] = sample_ids
	if not study_ids == None:
		data['submissionSubset']['studtyIds'] = study_ids

	return _objects_post(session_token, None, None, data)

def submissions_put(session_token, submission_id, title=None, description=None, analysis_ids=None, dac_ids=None, dataset_ids=None,
					experiment_ids=None, policy_ids=None, run_ids=None, sample_ids=None, study_ids=None):
	data = {}
	data['title'] = title
	data['description'] = description

	data['submissionSubset'] = {}
	data['submissionSubset']['analysisIds'] = analysis_ids
	data['submissionSubset']['dacIds'] = dac_ids
	data['submissionSubset']['datasetIds'] = dataset_ids
	data['submissionSubset']['experimentIds'] = experiment_ids
	data['submissionSubset']['policyIds'] = policy_ids
	data['submissionSubset']['runIds'] = run_ids
	data['submissionSubset']['sampleIds'] = sample_ids
	if not study_ids == None:
		data['submissionSubset']['studtyIds'] = study_ids

	return _objects_put(session_token, 'submissions', submission_id, data)

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

	objects = []
	if status == None:
		r = _result_from_response(requests.get(_api_access_endpoint(url+object_type), headers=_session_headers(session_token)))
		if(len(r)>0):
			for tmp_r in r:
				objects.append(json.loads(tmp_r['json']))
			return objects
	else:
		r = _result_from_response(requests.get(_api_access_endpoint(url+object_type+'?status='+status.upper()), headers=_session_headers(session_token)))
		if(len(r)>0):
			for tmp_r in r:
				objects.append(json.loads(tmp_r['json']))
			return objects

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
	return json.loads(_result_from_response(requests.get(_api_access_endpoint('/'+object_type+'/'+id+'?idtype='+id_type), headers=_session_headers(session_token)))[0]['json'])

def _objects_post(session_token,object_type,submission_id, json_data):
	""" Save a specific object - Generic

		Args:
			session_token:	A valid session token
			object_type:	The type of the object to retrieve
			submission_id:	A submission id for filtering

		Returns:
			dict:	The requested object
	"""
	_validate_session_token(session_token)

	url_string = '/submissions'

	if not object_type == None:
		url_string = url_string + "/" + submission_id + "/" + object_type

	return _result_from_response(requests.post(_api_access_endpoint(url_string), json=json_data, headers=_session_headers(session_token)))[0]

def _objects_put(session_token, object_type, object_id, json_data):
	_validate_session_token(session_token);

	url_string = '/'+object_type+"/"+object_id+"?action=EDIT"

	return _result_from_response(requests.put(_api_access_endpoint(url_string),json=json_data, headers=_session_headers(session_token)))[0]

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
