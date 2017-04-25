from xml.dom import minidom
import os
import sys

def _get_obj_xml(file_path, tag_name,root_name):
	obj_xml = minidom.getDOMImplementation().createDocument(None,root_name,None)

	reload(sys)
	sys.setdefaultencoding('utf-8')

	elem = minidom.parseString(minidom.parse(file_path).getElementsByTagName(tag_name)[0].toxml()).firstChild

	obj_xml.firstChild.appendChild(elem)
	return obj_xml.toxml()

def get_dataset_xml(project_folder, dataset_accession):
	return _get_obj_xml(get_dataset_xml_file_path(project_folder, dataset_accession), 'DATASET','dataset_xml')

def get_runs_xml(project_folder, dataset_accession, ega_run_accession):
	return _get_obj_xml(get_run_xml_file_path(project_folder, dataset_accession, ega_run_accession), 'RUN_SET','runs_xml')

def get_experiments_xml(project_folder, dataset_accession, ega_experiment_accession):
	return _get_obj_xml(get_experiment_xml_file_path(project_folder,dataset_accession,ega_experiment_accession), 'EXPERIMENT_SET','experiments_xml')

def get_samples_xml(project_folder, dataset_accession, sample_accession):
	return _get_obj_xml(get_sample_xml_file_path(project_folder,dataset_accession,sample_accession), 'SAMPLE_SET','sample_xml')

def get_study_xml(project_folder, dataset_accession, study_accession):
	return _get_obj_xml(get_study_xml_file_path(project_folder,dataset_accession,study_accession), 'STUDY_SET','study_xml')


def get_dataset_xml_file_path(project_folder, dataset_accession):
	return _get_object_xml_file_path(project_folder, dataset_accession, dataset_accession, 'dataset','dataset')

def get_run_xml_file_path(project_folder, dataset_accession, ega_run_accession):
	return _get_object_xml_file_path(project_folder, dataset_accession, ega_run_accession, 'runs', 'run')

def get_experiment_xml_file_path(project_folder, dataset_accession, ega_experiment_accession):
	return _get_object_xml_file_path(project_folder, dataset_accession, ega_experiment_accession, 'experiments','experiment')

def get_sample_xml_file_path(project_folder, dataset_accession, sample_accession):
	return  _get_object_xml_file_path(project_folder, dataset_accession, sample_accession,'samples', 'sample')

def get_study_xml_file_path(project_folder, dataset_accession, study_accession):
	return  _get_object_xml_file_path(project_folder, dataset_accession, study_accession,'study', 'study')

def _get_object_xml_file_path(project_folder, dataset_accession, object_accession, object_folder,type):
	return os.path.join(project_folder, dataset_accession, 'xmls',object_folder,object_accession+"."+type+".xml")


def quick_generate(project_folder, output_file,dataset_accession=None, sample_accession=None, study_accession=None, ega_run_accession=None, experiment_accession=None):
	dataset_xml = None
	runs_xml = None
	experiments_xml = None
	samples_xml = None
	study_xml = None

	if not dataset_accession == None:
		dataset_xml = get_dataset_xml(project_folder, dataset_accession)

	if not sample_accession == None:
		samples_xml = get_samples_xml(project_folder, dataset_accession, sample_accession)

	if not study_accession == None:
		study_xml = get_study_xml(project_folder, dataset_accession, study_accession)

	if not ega_run_accession == None:
		runs_xml = get_runs_xml(project_folder, dataset_accession, ega_run_accession)

	if not experiment_accession == None:
		experiments_xml = get_experiments_xml(project_folder, dataset_accession, experiment_accession)

	write(output_file, dataset_xml, runs_xml, experiments_xml, samples_xml, study_xml)

def combine(*xmls):
	impl = minidom.getDOMImplementation()
	doc = impl.createDocument(None, "root", None)

	for xml in xmls:
		reload(sys)
		sys.setdefaultencoding('utf-8')
		elem = minidom.parseString(xml).firstChild
		doc.firstChild.appendChild(elem)

	return doc.toxml()

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
