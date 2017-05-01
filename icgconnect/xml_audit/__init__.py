from xml.dom import minidom
import os
import sys
import urllib
import requests


def get_dataset(project_folder, project_name, dataset_accession):
	
    url_path = get_dataset_file_path(project_folder, project_name, dataset_accession)
    return _get_obj_xml(url_path, 'DATASET', 'dataset_xml')

def get_runs(project_folder,project_name, dataset_accession, ega_run_accession):
    url_path = get_run_file_path(project_folder, project_name, dataset_accession, ega_run_accession)
    return _get_obj_xml(url_path,'RUN_SET', 'runs_xml')

def _get_obj_xml(file_path, tag_name,root_name):
	obj_xml = minidom.getDOMImplementation().createDocument(None,root_name,None)

	reload(sys)
	sys.setdefaultencoding('utf-8')
	elem =  minidom.parseString(minidom.parse(urllib.urlopen(file_path)).getElementsByTagName(tag_name)[0].toxml()).firstChild

	obj_xml.firstChild.appendChild(elem)
	return obj_xml.toxml()

def get_experiments(project_folder, project_name, dataset_accession, ega_experiment_accession):
	url_path = get_experiment_file_path(project_folder,project_name, dataset_accession, ega_experiment_accession)
	return _get_obj_xml(url_path, 'EXPERIMENT_SET', 'experiments_xml')

def get_samples(project_folder, project_name, dataset_accession, sample_accession):
	url_path = get_sample_file_path(project_folder, project_name, dataset_accession, sample_accession)
	return _get_obj_xml(url_path,'SAMPLE_SET', 'sample_xml')

def get_study(project_folder, project_name, dataset_accession, study_accession):
	url_path = get_study_file_path(project_folder, project_name, dataset_accession, study_accession)
	return _get_obj_xml(url_path, 'STUDY_SET', 'study_xml')

def get_dataset_file_path(project_folder, project_name, dataset_accession):
	return _get_object_file_path(project_folder, project_name, dataset_accession, dataset_accession, 'dataset','dataset.xml')

def get_run_file_path(project_folder, project_name, dataset_accession, ega_run_accession):
	return _get_object_file_path(project_folder, project_name, dataset_accession, ega_run_accession, 'runs', 'run.xml')

def get_experiment_file_path(project_folder, project_name, dataset_accession, ega_experiment_accession):
	return _get_object_file_path(project_folder, project_name, dataset_accession, ega_experiment_accession, 'experiments','experiment.xml')

def get_sample_file_path(project_folder, project_name, dataset_accession, sample_accession):
	return  _get_object_file_path(project_folder, project_name, dataset_accession, sample_accession,'samples', 'sample.xml')

def get_study_file_path(project_folder, project_name, dataset_accession, study_accession):
	return  _get_object_file_path(project_folder, project_name, dataset_accession, study_accession,'study', 'study.xml')

def _get_object_file_path(project_folder, project_name, dataset_accession, object_accession, object_folder,extension):
	return  os.path.join(project_folder, project_name, dataset_accession, 'xmls', object_folder, object_accession +"."+extension)

def dataset_exists(project_folder, project_name, dataset_accession):
	return _object_exists(project_folder, project_name, dataset_accession, dataset_accession, 'dataset', 'dataset.xml')

def run_exists(project_folder, project_name, dataset_accession,run_accession):
	return _object_exists(project_folder, project_name, dataset_accession, run_accession, 'runs','run.xml')

def experiment_exists(project_folder, project_name, dataset_accession, experiment_accession):
	return _object_exists(project_folder, project_name, dataset_accession, experiment_accession, 'experiments', 'experiment.xml')

def sample_exists(project_folder, project_name, dataset_accession, sample_accession):
	return _object_exists(project_folder, project_name, dataset_accession, sample_accession, 'samples', 'sample.xml')

def study_exists(project_folder, project_name, dataset_accession, study_accession):
	return _object_exists(project_folder, project_name, dataset_accession, study_accession, 'study', 'study.xml')

def project_exists(project_folder):
	return _url_exists(project_folder)

def _object_exists(project_folder, project_name, dataset_accession, object_accession, object_folder, extension):
	return _url_exists(_get_object_file_path(project_folder, project_name, dataset_accession, object_accession,object_folder, extension))

def _url_exists(url_path):
	return requests.get(url_path).status_code == 200

def quick_generate(project_folder, project_name, output_file,dataset_accession, sample_accession=None, study_accession=None, ega_run_accession=None, experiment_accession=None):
	dataset_xml = None
	runs_xml = None
	experiments_xml = None
	samples_xml = None
	study_xml = None

	if not dataset_accession == None:
		dataset_xml = get_dataset(project_folder, project_name, dataset_accession)

	if not sample_accession == None:
		samples_xml = get_samples(project_folder, project_name, dataset_accession, sample_accession)

	if not study_accession == None:
		study_xml = get_study(project_folder, project_name, dataset_accession, study_accession)

	if not ega_run_accession == None:
		runs_xml = get_runs(project_folder, project_name, dataset_accession, ega_run_accession)

	if not experiment_accession == None:
		experiments_xml = get_experiments(project_folder, project_name, dataset_accession, experiment_accession)

	write(output_file, dataset_xml, runs_xml, experiments_xml, samples_xml, study_xml)

def write(output_file, *xmls):
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
