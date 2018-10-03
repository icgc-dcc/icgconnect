
import requests
import json
import subprocess
import os
import csv
import hashlib
from icgconnect.utils import file_utils
from pkg_resources import resource_string

_COLLAB_URL = "https://meta.icgc.org"

def entities_get(gnos_id):
    """ The information about an entity

        Args:
            gnos_id (str):  An existing entity's id from GNOS

        Returns:
            str:    The requested entity

        Raises:
            ValueError: Id does not exists in the records
    """
    response = requests.get(_COLLAB_URL+'/entities?gnosId='+gnos_id).json().get('content')
    if len(response) == 0:
        raise ValueError("GNOS id does not exist in the records: "+gnos_id)
    return response

def entities_post(id_service_token, gnos_id, filename, project_code):
    """ Create a new entity

        Args:
            id_service_token:   A valid ICGC token
            gnos_id:            The GNOS ID entity to create
            filename:           A filename to associate to the GNOS id
            project_code:       The code to associate the project with

        Returns:
            dict:    The server response

        Raises:
            ValueError: The entity already exists in the record
            ValueError: The ICGC token is invalid
    """
    #try:
    #    entities_get(gnos_id)
    #    raise ValueError("Entity already exists in collaboratory: "+gnos_id)
    #except ValueError, err:
    #    pass
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + id_service_token}
    body = {"gnosId": gnos_id,"fileName": filename,"projectCode": project_code,"access": "controlled"}
    r = requests.post(_COLLAB_URL+'/entities', data=json.dumps(body), headers=headers)
    print(r.text)

    if r.status_code == 401:
        raise ValueError("ICGC server error response: "+json.loads(r.text).get('error'))
    return r.text

def entities_get_post(gnos_id, id_service_token, filename, project_code):
    """ Retrieves an entity and creates if does not already exist

        Args:
            gnos_id (str):              An existing entity's id from GNOS
            id_service_token (str):     A valid ICGC token
            filename:                   A filename to associate with the entity
            project_code:               The project to associate the entity

        Returns:
            dict:   The retrieved entity

        Raises:
            ValueError: The entity cannot be created because of invalid informations
    """
    if not entities_exists(gnos_id):
        entities_post(id_service_token, gnos_id, filename, project_code)

    try:
        return entities_get(gnos_id)
    except ValueError as err:
        raise ValueError("Entity cannot be created. Please verify the provided information. GNOS id: "+gnos_id+", service token: "+id_service_token+", filename: "+filename+", project code: "+project_code)

def entities_exists(gnos_id):
    """ Check if entity exists in the records

        Args:
            gnos_id (str):  An existing entity's id from GNOS
    """
    return len(requests.get(_COLLAB_URL+'/entities?gnosId='+gnos_id).json().get('content')) > 0

def filename_exists(gnos_id, filename):
    try:
        filename_get(gnos_id, filename)
        return True
    except ValueError:
        return False

def filename_get_id(gnos_id, filename):
    """ Retrieve the object id of a filename

        Args:
            gnos_id (str):  An existing entity's id from GNOS
            filename:       The requested file name

        Returns:
            str:    The related object id
    """
    if not filename_exists(gnos_id, filename):
        raise ValueError("The requested filename does not exist: "+filename)
    return filename_get(gnos_id, filename)['id']

def filename_get(gnos_id, filename):
    """ Retrieve a file associated to a GNOS id

        Args:
            gnos_id (str):  An existing entity's id from GNOS
            filename (str): The filename to retrieve from the records

        Returns:
            dict:   The retrieved file

        Raises:
            ValueError: The filename is not found
    """
    for _file in entities_get(gnos_id):
        if filename == _file['fileName']:
            return _file
    raise ValueError("The requested file does not exist in the records, GNOS id: "+gnos_id+", filename: "+filename)

def filename_post(gnos_id, id_service_token, filename, project_code):
    """ Add a filename to an entity. It creates the entity if it does not already exist

        Args:
            gnos_id (str):              An existing entity's id from GNOS
            id_service_token (str):     A valid ICGC token
            filename (str):             A filename to add to the entity
            project_code (str):         The project code to add the file

        Returns:
            dict:   The server response

        Raises:
            ValueError: The filename already exists in collaboratory
            ValueError: The file cannot be added because of invalid informations
    """
    try:
        _file = filename_get_id(gnos_id, filename)
        return _file
    except ValueError:
        pass

    headers = {'Content-Type': 'application/json','Authorization': 'Bearer ' + id_service_token}
    body = {"gnosId": gnos_id,"fileName": filename,"projectCode": project_code,"access": "controlled"}
    r = requests.post(_COLLAB_URL+'/entities', data=json.dumps(body), headers=headers)

    if r.status_code == 401:
        raise ValueError("ICGC server error response: "+json.loads(r.text).get('error'))
    return r.text

def filename_get_post(gnos_id, id_service_token, filename, project_code):
    if not filename_exists(gnos_id, filename):
        filename_post(gnos_id, id_service_token, filename, project_code)
    return filename_get(gnos_id, filename)

def upload(manifest_file, icgc_storage_client, force):
    """ Upload files listed in a manifest file to Collaboratory

        Args:
            manifest_file (str):    The local path of a manifest file
    """
    #_validate_manifest_file(manifest_file)
    try:
        if force == True:
            subprocess.check_output([icgc_storage_client,'--profile','collab','upload','--manifest',manifest_file,'--force'])
        else:
            subprocess.check_output([icgc_storage_client,'--profile','collab','upload','--manifest',manifest_file])
    except subprocess.CalledProcessError as err:
        raise Exception("Upload to collab failed: "+str(err))

def _validate_manifest_file(manifest_file):
    """ Validates if the manifest file for collaboratory upload has the required format

        Args:
            manifest_file (str):    The local path of a manifest_file file

        Raises:
            ValueError: The manifest_file does not exist
            ValueError: Manifest file not in appropriate format
            ValueError: object_id is not the title of the first column
            ValueError: file_name is not the title of the second column
            ValueError: md5 is not the title of the third column
    """
    if not os.path.isfile(manifest_file):
        raise ValueError("The manifest file does not exist: "+manifest_file)

    with open(manifest_file,'r') as f:
        first_line = f.readline().split()
        
        if len(first_line) !=3:
            raise ValueError("Manifest file not in appropriate format: "+manifest_file)

        if not 'object_id' == first_line[0]:
            raise ValueError("First column must be object_id in manifest file: "+manifest_file)

        if not any('file_name' in s for s in first_line):
            raise ValueError("Second column must be file_name in manifest file: "+manifest_file)

        if not any('md5' in s for s in first_line):
            raise ValueError("Third column must be md5 in manifest file: "+manifest_file)

def _validate_file_to_upload(gnos_id, filename, md5, object_id):
    """ Validate a file to upload to collaboratory

        Args:
            gnos_id (str):      An existing entity's id from GNOS
            filename (str):     A file path in the local system
            md5 (str):          The MD5 sumf of corresponding to the file
            object_id (str):    The object id related to the file to upload

        Raises:
            ValueError: The filename is missing in the parameters
            ValueError: The filename does not exist in the filesystem
            ValueError: The GNOS id is missing in the parameters
            ValueError: The md5 sum is missing in the parameters
            ValueError: The object_id is missing in the parameters
            ValueError: The md5 sum required does not match the computed md5sum
            ValueError: No entity has been created for the file to upload
    """
    if filename == None:
        raise ValueError("The filename is missing.")

    if not os.path.isfile(filename):
        raise ValueError("The file does not exist: "+filename)

    if gnos_id == None:
        raise ValueError("The gnos id is missing for this file: "+filename)

    if md5 == None:
        raise ValueError("The MD5 sum is missing for this file: "+filename)

    if object_id == None:
        raise ValueError("The object id is missing for this file: "+filename)

    if not file_utils.get_file_md5(filename) == md5:
        raise ValueError("MD5 sum of the file is not matching: "+filename)

    #if not filename_exists(gnos_id, filename):
    #    raise ValueError("A related entity has not been created yet: GNOS id: "+gnos_id+", filename: "+filename)


def validate_manifest_file(gnos_id, manifest_file):
    """ Check if the manifest file has valid informations to upload to Collaboratory

        Args:
            gnos_id (str):          An existing entity's id from GNOS
            manifest_file (str):    A manifest_file containing upload informations

        Returns:
            bool:   True if the validation succeeded

        Raises:
            ValueError: The manifest file is invalid
    """
    _validate_manifest_file(manifest_file)

    with open(manifest_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            try:
                _validate_file_to_upload(gnos_id, row['file_name'],row['md5'],row['object_id'])
            except ValueError as err:
                raise ValueError("Manifest file validation failed. Reason: "+str(err))
    return True

def generate_manifest_file(output_file, files=None):
    """ Generate a manifest file for Collaboratory

        Args:
            output_file (str):  The name of the file to output the manifest
            files (list):       A list of dictionaries containing object_id, file_md5sum and file_name keys

        Returns:
            bool: True if the file has been generated

        Raises:
            KeyError: The object_id key is missing
            KeyError: The file_md5sum key is missing
            KeyError: The file_name key is missing
    """
    if not files == None:
        for _f in files:
            if not 'object_id' in _f:
                raise KeyError("object_id key missing from files array")
            if not 'file_name' in _f:
                raise KeyError("file_name key missing from files array: "+_f['file_name'])
            if not 'file_md5sum' in _f:
                raise ValueError("file_md5sum key missing from files array: "+_f['file_name'])

    with open(output_file,"w") as f:
        f.write("object_id\tfile_name\tmd5\n")
        if not files == None:
            for _f in files:
                file_path = os.path.join(os.path.dirname(os.path.abspath(_f['file_name'])),_f['file_name'])
                f.write(_f['object_id']+"\t"+file_path+"\t"+_f['file_md5sum']+"\n")
    return True

def delete_manifest_file(manifest_file, related_files=False):
    """ Delete a manifest file

        Args:
            manifest_file (str):    Path of the manifest file
            related_files (bool):   True if the files referenced in the manifest file have to be deleted

        Returns:
            bool:   True if the file has been successfully deleted
    """
    if related_files == True:
        _validate_manifest_file(manifest_file)
        with open(manifest_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                file_utils.delete_file(row['file_name'])
    file_utils.delete_file(manifest_file)
    return True

def add_to_manifest_file(manifest_file, object_id, filename, md5):
    """ Add an entry to the manifest file

        Args:
            manifest_file (str):    Path to the manifest file
            object_id (str):        Object id of ICGC client
            filename (str):         Name of the file to be added
            md5 (str):              MD5 sum of the file to be added
    """
    with open(manifest_file, "a") as f:
        f.write(object_id+"\t"+filename+"\t"+md5+"\n")

def quick_upload(gnos_id, files, icgc_storage_client, force=True):
    manifest_file = gnos_id+".txt"
    generate_manifest_file(manifest_file, files)
    validate_manifest_file(gnos_id, manifest_file)
    upload(manifest_file, icgc_storage_client, force)
    delete_manifest_file(manifest_file, True)

def download(object_id, icgc_storage_client, output_dir,force=True, skip_validation=False):
    args = ""
    if force:
        args = args + " --force"

    if skip_validation:
        args = args + " --validate=false"

    subprocess.call([icgc_storage_client, '--profile', 'collab', 'download', '--object-id', object_id, '--index=false',
                     '--output-dir', output_dir, args])