from xml.dom import minidom
import os
import sys
import urllib
import requests


def get_dataset(project_folder, project_name, dataset_accession):
	"""
	Get xml file of a dataset
	:param project_folder: 		A folder containing datasets related to a project
	:param project_name: 		The project name of the project in the project folder
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:return: An xml string related to the dataset
	"""
	url_path = get_dataset_file_path(project_folder, project_name, dataset_accession)
	return _get_obj_xml(url_path, 'DATASET', 'dataset_xml')

def get_runs(project_folder,project_name, dataset_accession, ega_run_accession):
	"""
	Get xml file of a run
	:param project_folder: 		A folder containing datasets related to a project
	:param project_name: 		The project name in the project folder
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:param ega_run_accession: 	The run EGA accession (EGAR)
	:return: An xml string related to the run
	"""
	url_path = get_run_file_path(project_folder, project_name, dataset_accession, ega_run_accession)
	return _get_obj_xml(url_path,'RUN_SET', 'runs_xml')

def get_experiments(project_folder, project_name, dataset_accession, ega_experiment_accession):
	"""
	Get xml file of an experiment
	:param project_folder: 				A folder containing datasets related to a project
	:param project_name: 				A project name in the project folder
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param ega_experiment_accession: 	The experiment EGA accession (EGAX...)
	:return:  An xml string related to the experiment
	"""
	url_path = get_experiment_file_path(project_folder,project_name, dataset_accession, ega_experiment_accession)
	return _get_obj_xml(url_path, 'EXPERIMENT_SET', 'experiments_xml')

def get_analyses(project_folder, project_name, dataset_accession, ega_analysis_accession):
	"""
	Get xml file of an analysis
	:param project_folder: 				A folder containing datasets related to a project
	:param project_name: 				A project name in the project folder
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param ega_analysis_accession: 		The analysis EGA accession (EGAZ...)
	:return:  An xml string related to the analysis
	"""
	url_path = get_analysis_file_path(project_folder,project_name, dataset_accession, ega_analysis_accession)
	return _get_obj_xml(url_path, 'ANALYSIS_SET', 'analyses_xml')

def get_samples(project_folder, project_name, dataset_accession, sample_accession):
	"""
	Get xml file of a sample
	:param project_folder:			A folder containing datasets related to a project
	:param project_name: 			A project name in the project folder
	:param dataset_accession: 		The dataset EGA accession (EGAD...)
	:param sample_accession: 		The sample EGA accession (EGAN...)
	:return:  An xml string related to the sample
	"""
	url_path = get_sample_file_path(project_folder, project_name, dataset_accession, sample_accession)
	return _get_obj_xml(url_path,'SAMPLE_SET', 'sample_xml')

def get_study(project_folder, project_name, dataset_accession, study_accession):
	"""
	Get xml file of a study
	:param project_folder: 			A folder containing datasets related to a project
	:param project_name: 			A project name in the project folder
	:param dataset_accession: 		The dataset EGA accession (EGAD...)
	:param study_accession: 		The sample EGA accession (EGAN...)
	:return:  An xml string related to the study
	"""
	url_path = get_study_file_path(project_folder, project_name, dataset_accession, study_accession)
	return _get_obj_xml(url_path, 'STUDY_SET', 'study_xml')

def get_dataset_file_path(project_folder, project_name, dataset_accession):
	"""
	Generate the path of a dataset in the project folder
	:param project_folder: 		The project folder
	:param project_name: 		The project name where the dataset is
	:param dataset_accession: 	The dataset EGA accession
	:return: The full path of the dataset in a project folder
	"""
	return _get_object_file_path(project_folder, project_name, dataset_accession, dataset_accession, 'dataset','dataset.xml')

def get_run_file_path(project_folder, project_name, dataset_accession, ega_run_accession):
	"""
	Generate the path of a run in the project folder
	:param project_folder: 		The project folder
	:param project_name: 		The project name where the run is
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:param ega_run_accession: 	The run EGA accession (EGAR...)
	:return: The full path of the run in a project folder
	"""
	return _get_object_file_path(project_folder, project_name, dataset_accession, ega_run_accession, 'runs', 'run.xml')

def get_experiment_file_path(project_folder, project_name, dataset_accession, ega_experiment_accession):
	"""
	Generate the path of an experiment in the project folder
	:param project_folder: 				The project folder
	:param project_name: 				The project name where the experiment is
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param ega_experiment_accession: 	The experiment EGA accession (EGAR...)
	:return: The full path of the experiment in a project folder
	"""
	return _get_object_file_path(project_folder, project_name, dataset_accession, ega_experiment_accession, 'experiments','experiment.xml')

def get_analysis_file_path(project_folder, project_name, dataset_accession, ega_analysis_accession):
	"""
	Generate the path of an analysis in the project folder
	:param project_folder: 				The project folder
	:param project_name: 				The project name where the experiment is
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param ega_analysis_accession: 		The analysis EGA accession (EGAR...)
	:return: The full path of the experiment in a project folder
	"""
	return _get_object_file_path(project_folder, project_name, dataset_accession, ega_analysis_accession, 'analysis','analysis.xml')

def get_sample_file_path(project_folder, project_name, dataset_accession, sample_accession):
	"""
	Generate the path of a sample in the project folder
	:param project_folder: 				The project folder
	:param project_name: 				The project name where the sample is
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param sample_accession: 			The sample EGA accession (EGAN...)
	:return: The full path of the sample in a project folder
	"""
	return  _get_object_file_path(project_folder, project_name, dataset_accession, sample_accession,'samples', 'sample.xml')

def get_study_file_path(project_folder, project_name, dataset_accession, study_accession):
	"""
	Generate the path of a study in the project folder
	:param project_folder: 				The project folder
	:param project_name: 				The project name where the study is
	:param dataset_accession: 			The dataset EGA accession (EGAD...)
	:param study_accession: 			The sample EGA accession (EGAN....)
	:return: The full path of the study in a project folder
	"""
	return  _get_object_file_path(project_folder, project_name, dataset_accession, study_accession,'study', 'study.xml')

def dataset_exists(project_folder, project_name, dataset_accession):
	"""
	Check if a dataset xml file exists in the project folder
	:param project_folder: 		The project folder
	:param project_name: 		The name of the project
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, dataset_accession, 'dataset', 'dataset.xml')

def run_exists(project_folder, project_name, dataset_accession,run_accession):
	"""
	Check if a run xml file exists in the project folder
	:param project_folder: 		The project folder
	:param project_name: 		The name of the project
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:param run_accession: 		The run EGA accession (EGAR...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, run_accession, 'runs','run.xml')

def experiment_exists(project_folder, project_name, dataset_accession, experiment_accession):
	"""
	Check if an experiment xml file exists in the project folder
	:param project_folder: 			The project folder
	:param project_name: 			The name of the project
	:param dataset_accession: 		The dataset EGA accession (EGAD...)
	:param experiment_accession: 	The experiment EGA accession (EGAX...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, experiment_accession, 'experiments', 'experiment.xml')

def analysis_exists(project_folder, project_name, dataset_accession, analysis_accession):
	"""
	Check if an analysis xml file exists in the project folder
	:param project_folder: 			The project folder
	:param project_name: 			The name of the project
	:param dataset_accession: 		The dataset EGA accession (EGAD...)
	:param analysis_accession: 		The analysis EGA accession (EGAZ...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, analysis_accession, 'analysis', 'analysis.xml')

def sample_exists(project_folder, project_name, dataset_accession, sample_accession):
	"""
	Check if a sample xml file exists in the project folder
	:param project_folder:		The project folder 
	:param project_name: 		The name of the project
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:param sample_accession: 	The sample EGA accession (EGAN...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, sample_accession, 'samples', 'sample.xml')

def study_exists(project_folder, project_name, dataset_accession, study_accession):
	"""
	Check if the study xml file exists in the project folder
	:param project_folder: 		The project folder
	:param project_name: 		The name of the project
	:param dataset_accession: 	The dataset EGA accession (EGAD...)
	:param study_accession: 	The study EGA accession (EGAS...)
	:return: True if the xml file exists, False otherwise
	"""
	return _object_exists(project_folder, project_name, dataset_accession, study_accession, 'study', 'study.xml')

def _get_obj_xml(file_path, tag_name,root_name):
	"""
	Generic function to generate an xml file
	:param file_path: 	Full path of the object to transfer
	:param tag_name: 	XML tag that contains the information to extract
	:param root_name: 	XML root tag of the document
	:return: 	The XML object corresponding to the object
	"""
	obj_xml = minidom.getDOMImplementation().createDocument(None,root_name,None)

	reload(sys)
	sys.setdefaultencoding('utf-8')
	print(file_path)
	elem =  minidom.parseString(minidom.parse(urllib.urlopen(file_path)).getElementsByTagName(tag_name)[0].toxml()).firstChild

	obj_xml.firstChild.appendChild(elem)
	return obj_xml.toxml()

def _get_object_file_path(project_folder, project_name, dataset_accession, object_accession, object_folder,extension):
	"""
	Generate the file path of the object
	:param project_folder: 		The project folder path
	:param project_name: 		The project name
	:param dataset_accession: 	The dataset file EGA accession (EGAD...)
	:param object_accession: 	The object file EGA accession (EGA...)
	:param object_folder: 		The object folder type in the tree structure under the project folder
	:param extension: 			The extension of the file to retrieve
	:return: 	The file path of the requested object file
	"""
	return  os.path.join(project_folder, project_name, dataset_accession, 'xmls', object_folder, object_accession +"."+extension)


def project_exists(project_folder):
	"""
	Check if a project folder exists
	:param project_folder: 	The full path of the project to check
	:return: True if the project exists, False otherwise
	"""
	return _url_exists(project_folder)

def _object_exists(project_folder, project_name, dataset_accession, object_accession, object_folder, extension):
	"""
	Generic function to check if an object exsists
	:param project_folder: 		Full path of the project 
	:param project_name: 		The project name
	:param dataset_accession: 	The dataset EGA file accession (EGAD...)
	:param object_accession: 	The object EGA file accession (EGAF...)
	:param object_folder: 		The obbject folder name
	:param extension: 			The file extension the object to retrieve
	:return: True if the object is found, False otherwise
	"""
	return _url_exists(_get_object_file_path(project_folder, project_name, dataset_accession, object_accession,object_folder, extension))

def _url_exists(url_path):
	"""
	Check if an url exists
	:param url_path: 	The URL to check
	:return: True if the URL exists, False otherwise
	"""
	return requests.get(url_path).status_code == 200

def quick_generate(project_folder, project_name, output_file,dataset_accession, sample_accession=None, study_accession=None, ega_run_accession=None, experiment_accession=None, analysis_accession=None,include_dataset=True):
	"""
	Generates the combination of xmls requested
	:param project_folder: 			The folder containing all the projects
	:param project_name: 			The project name
	:param output_file: 			The output xml file name
	:param dataset_accession: 		The dataset EGA file accession (EGAD...)
	:param sample_accession: 		The sample EGA file accession (EGAN...)
	:param study_accession: 		The study EGA file accession (EGAS...)
	:param ega_run_accession: 		The run EGA file accession (EGAR...)
	:param experiment_accession: 	The experiment EGA file accession (EGAX...)
	:param analysis_accession:	 	The analysis EGA file accession (EGAZ...)
	:return: None
	"""
	dataset_xml = None
	runs_xml = None
	experiments_xml = None
	samples_xml = None
	study_xml = None
	analysis_xml = None

	if include_dataset and not dataset_accession=='':
		dataset_xml = get_dataset(project_folder, project_name, dataset_accession)

	if not sample_accession == None and not sample_accession=='':
		samples_xml = get_samples(project_folder, project_name, dataset_accession, sample_accession)

	if not study_accession == None and not study_accession=='':
		study_xml = get_study(project_folder, project_name, dataset_accession, study_accession)

	if not ega_run_accession == None and not ega_run_accession=='':
		runs_xml = get_runs(project_folder, project_name, dataset_accession, ega_run_accession)

	if not experiment_accession == None and not experiment_accession=='':
		experiments_xml = get_experiments(project_folder, project_name, dataset_accession, experiment_accession)

	if not analysis_accession == None and not analysis_accession=='':
		analysis_xml = get_analyses(project_folder, project_name, dataset_accession, analysis_accession)

	write(output_file, dataset_xml, runs_xml, experiments_xml, analysis_xml,samples_xml, study_xml)

def write(output_file, *xmls):
	"""
	Combine multiple xml files into an output file
	:param output_file: 	The path of the output file
	:param xmls: 			The array of xml files
	:return: 				None
	"""
	impl = minidom.getDOMImplementation()
	doc = impl.createDocument(None, "root", None)

	for xml in xmls:
		if not xml == None:
			reload(sys)
			sys.setdefaultencoding('utf-8')
			elem = minidom.parseString(xml).firstChild
			doc.firstChild.appendChild(elem)

	fh = open(output_file, "wb")
	doc.writexml(fh)
	fh.close()
