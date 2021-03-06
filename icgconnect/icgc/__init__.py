import requests
import json
import re
import os
import subprocess

ICGC_ID_SERVICE_URL_TEST = "http://hetl2-dcc.res.oicr.on.ca:9000" # dry run uses this
ICGC_ID_SERVICE_URL_PROD = "https://id.icgc.org" # submit uses this

ICGC_API_BASEURL = "https://dcc.icgc.org/api"

ICGC_ID_SERVICE_ENDPOINTS = {
    "id": {
        "donor": {
            "path": "donor/id",
            "params": ["submittedProjectId", "submittedDonorId"]
        },
        "specimen": {
            "path": "specimen/id",
            "params": ["submittedProjectId", "submittedSpecimenId"]
        },
        "sample": {
            "path": "sample/id",
            "params": ["submittedProjectId", "submittedSampleId"]
        }
    }
}

def index_donors():
    return requests.get(ICGC_API_BASEURL+'/v1/donors').text

def donors_pql():
    return requests.get(ICGC_API_BASEURL+'/v1/donors/pql').text

def get_donor(donor_id):
    return json.loads(requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id).text)

def get_donor_genes(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/genes').text

def get_donor_genes_count(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/genes/count').text

def get_donor_genes_counts(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/genes/counts').text

def get_donor_mutations_count_by_gene(donor_id, gene_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/genes/'+gene_id+'/mutations/count').text

def get_donor_mutations_counts_by_gene(donor_id, gene_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/genes/'+gene_id+'/mutations/counts').text

def get_donor_mutations(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/mutations').text

def get_donor_mutations_count(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/mutations/count').text

def get_donor_mutations_counts(donor_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/mutations/counts').text

def get_donor_genes_count_by_mutation(donor_id, mutation_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/mutations/'+mutation_id+'/genes/count').text

def get_donor_genes_counts_by_mutation(donor_id, mutation_id):
    return requests.get(ICGC_API_BASEURL+'/v1/donors/'+donor_id+'/mutations/'+mutation_id+'/genes/counts').text

def get_donor_id_from_submitted_donor_id(project_id, submitted_donor_id):
    for line in get_samples_from_project(project_id).split('\n'):
        if line.split('\t')[5] == submitted_donor_id:
            return line.split('\t')[4]

def get_gender_from_donor_id(donor_id):
    return get_donor(donor_id).get('gender')

def get_submitter_donor_id_from_donor_id(donor_id):
    return get_donor(donor_id).get('submittedDonorId')

def get_samples_from_project(project_id):
    return requests.get(ICGC_API_BASEURL+'/v1/projects/'+project_id+'/samples').text

def get_project_id_from_donor_id(donor_id):
    return get_donor(donor_id).get('projectId')

def get_submitted_sample_id_from_donor_id(donor_id):
    return _get_donor_dict(donor_id).get('submitted_sample_id')

def get_submitted_specimen_id_from_donor_id(donor_id):
    return _get_donor_dict(donor_id).get('submitted_specimen_id')

def get_specimen_type_from_donor_id(donor_id):
    return _get_donor_dict(donor_id).get('specimen_type')

def get_specimen_class_from_donor_id(donor_id):
    specimen_type = get_specimen_type_from_donor_id(donor_id)
    if "normal" in specimen_type.lower(): return "Normal"
    if "tumour" in specimen_type.lower(): return "Tumour"
    raise ValueError("The specimen class could not be determined")

def get_sample_submitter_id_from_donor_id(donor_id):
    return _get_donor_dict(donor_id).get('icgc_sample_id')

def get_library_strategy_from_donor_id(donor_id):
    return _get_donor_dict(donor_id).get('sequencing_strategy')

def _get_donor_dict(donor_id):
    project_id = get_project_id_from_donor_id(donor_id)
    _keys = get_samples_from_project(project_id).split('\n')[0].split('\t')
    for line in get_samples_from_project(project_id).split('\n'):
        if line.split('\t')[4] == donor_id:
            _line = line.split('\t')
            return dict(zip(_keys,_line))

def id_service(icgc_token, type_, project_code, submitter_id, create=True, is_test=False):
    """
    ICGC ID Service
    """

    if not type_ in ('donor', 'specimen', 'sample'):
        raise Exception('Unsupported entity type: %s' % type_)

    project_code = str(project_code)
    submitter_id = str(submitter_id)

    url = ICGC_ID_SERVICE_URL_TEST if is_test else ICGC_ID_SERVICE_URL_PROD
    path = ICGC_ID_SERVICE_ENDPOINTS['id'][type_]['path']

    project_param = '='.join([
                                ICGC_ID_SERVICE_ENDPOINTS['id'][type_]['params'][0],
                                project_code
                            ])
    submitter_id_param = '='.join([
                                    ICGC_ID_SERVICE_ENDPOINTS['id'][type_]['params'][1],
                                    submitter_id
                                ])
    create_param = '='.join(['create', 'true' if create else 'false'])

    try:
        full_url = "%s/%s?%s&%s&%s" % (url, path, project_param, submitter_id_param, create_param)

        r = requests.get(full_url,
                       headers={
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer %s' % icgc_token
                                }
                    )
    except:
        raise Exception("Failed calling ICGC ID service with: %s" % full_url)

    if "error" in r.text:
        res = re.sub(r'"error_description":".*"', '"error_description":""', r.text) if 'invalid_token' in r.text else r.text
        raise Exception("Failed calling ICGC ID serivce with: %s. Server response: %s" % (full_url, res))

    return r.text

