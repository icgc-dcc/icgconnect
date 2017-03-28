
import requests
import json
import subprocess
import os
import csv
import hashlib
from icgconnect.utils import file_utils

COLLAB_URL = "https://meta.icgc.org"

def entities_get(gnos_id):
    if len(requests.get(COLLAB_URL+'/entities?gnosId='+gnos_id).json().get('content')) == 0: return None
    return requests.get(COLLAB_URL+'/entities?gnosId='+gnos_id).json().get('content')

def entities_post(id_service_token, gnos_id, filename, project_code):
    if not entities_get(gnos_id) == None:
        raise Exception("Entity already exists in collaboratory: "+gnos_id)

    headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + id_service_token}
    body = {"gnosId": gnos_id,"fileName": filename,"projectCode": project_code,"access": "controlled"}
    r = requests.post(COLLAB_URL+'/entities', data=json.dumps(body), headers=headers)
    return r

def entities_get_post(gnos_id, id_service_token, filename, project_code):
    if entities_get(gnos_id) == None:
        entities_post(id_service_token, gnos_id, filename, project_code)
    return entities_get(gnos_id)

def entities_get_entity_id(gnos_id):
    return entities_get(gnos_id).get('id')

def entities_exists(gnos_id):
    return len(requests.get(COLLAB_URL+'/entities?gnosId='+gnos_id).json().get('content')) > 0

def filename_get_id(gnos_id, filename):
    if filename_get(gnos_id, filename) == None:
        return
    return filename_get(gnos_id, filename)['id']

def filename_get(gnos_id, filename):
    for _file in entities_get(gnos_id):
        if filename == _file['fileName']:
            return _file
    return None

def filename_post(gnos_id, id_service_token, filename, project_code):
    if not filename_get_id(gnos_id, filename) == None:
        raise Exception("Filename already exists in collaboratory: "+gnos_id+" - "+filename)

    headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + id_service_token}
    body = {"gnosId": gnos_id,"fileName": filename,"projectCode": project_code,"access": "controlled"}
    r = requests.post(COLLAB_URL+'/entities', data=json.dumps(body), headers=headers)
    return r

def filename_get_post(gnos_id, id_service_token, filename, project_code):
    if filename_get_id(gnos_id, filename) == None:
        filename_post(gnos_id, id_service_token, filename, project_code)
    return filename_get(gnos_id, filename)

def upload(manifest_file):
    subprocess.call(['icgc-storage-client ','--profile','collab','upload','--manifest',manifest_file])

def quick_upload(id_service_token, gnos_id, files):
    manifest_file = gnos_id+".txt"
    with open(manifest_file,"w") as f:
        f.write("object_id\tfile_name\tmd5\n")
        for _f in files:
            file_path = os.path.join(os.path.dirname(os.path.abspath(_f['file_name'])),_f['file_name'])

            if not file_utils.get_file_md5(file_path) == _f['file_md5sum']:
                raise Exception(file_path+" does not match md5")    

            f.write(_f['object_id']+"\t"+file_path+"\t"+_f['file_md5sum']+"\n")

    subprocess.call(['icgc-storage-client/bin/icgc-storage-client','--profile','collab','upload','--manifest',manifest_file])
    with open(manifest_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            os.remove(row['file_name'])
    os.remove(manifest_file)
