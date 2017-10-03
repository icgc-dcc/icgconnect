"""

Wrapper functions to integrate some aws functions to python

This package contains functions to communicate with aws through ICGC. You might need
to communicate with aws especially for downloading or for uploading files.

"""


import subprocess


def download(object_id, icgc_storage_client, output_dir,force=True):
    """
    Download an ICGC file stored in aws using the object id. Make sure that you have the 
    icgc-storage-client (http://docs.icgc.org/cloud/guide/) installed on your computer before using this function.
    If you are not able to download a file using the this function or the ICGC-Storage cliengt, make sure
    that you have a valid token that allows you aws download access.
    
    An explanation
    :param object_id:           The object if od the file you want to download
    :param icgc_storage_client: The path of the icgc-storage client on your computer
    :param output_dir:          The output directory where the file will be downloaded
    :param force:               True overwrites an existing output file with the same name
    """
    if force:
        subprocess.call([icgc_storage_client, '--profile','aws','download','--object-id',object_id,'--index=false','--output-dir',output_dir,'--force'])
    else:
        subprocess.call([icgc_storage_client, '--profile','aws','download','--object-id',object_id,'--index=false','--output-dir',output_dir])