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
	return _get_obj_xml(os.path.join(project_folder,dataset_accession,'xmls','dataset',dataset_accession+".dataset.xml"), 'DATASET','dataset_xml')

def get_runs_xml(project_folder, dataset_accession, ega_run_accession):
	return _get_obj_xml(os.path.join(project_folder,dataset_accession,'xmls','runs',ega_run_accession+".run.xml"), 'RUN_SET','runs_xml')

def get_experiments_xml(project_folder, dataset_accession, ega_experiment_accession):
	return _get_obj_xml(os.path.join(project_folder,dataset_accession,'xmls','experiments',ega_experiment_accession+".experiment.xml"), 'EXPERIMENT_SET','experiments_xml')

def get_samples_xml(project_folder, dataset_accession, sample_accession):
	return _get_obj_xml(os.path.join(project_folder,dataset_accession,'xmls','samples',sample_accession+".sample.xml"), 'SAMPLE_SET','sample_xml')

def get_study_xml(project_folder, dataset_accession, study_accession):
	return _get_obj_xml(os.path.join(project_folder,dataset_accession,'xmls','study',study_accession+".study.xml"), 'STUDY_SET','study_xml')

def quick_generate(project_folder, output_file,dataset_accession=None, sample_accession=None, study_accession=None, ega_run_accession=None, experiment_accession=None):
	dataset_xml = get_dataset_xml(project_folder, dataset_accession)
	runs_xml = get_runs_xml(project_folder, dataset_accession, ega_run_accession)
	experiments_xml = get_experiments_xml(project_folder, dataset_accession, experiment_accession)
	samples_xml = get_samples_xml(project_folder, dataset_accession, sample_accession)
	study_xml = get_study_xml(project_folder, dataset_accession, study_accession)

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
		reload(sys)
		sys.setdefaultencoding('utf-8')
		elem = minidom.parseString(xml).firstChild
		doc.firstChild.appendChild(elem)

	fh = open(output_file, "wb")
	doc.writexml(fh)
	fh.close()
