
import subprocess


def download(object_id, icgc_storage_client, output_dir,force=True):
    if force:
        subprocess.call([icgc_storage_client, '--profile','aws','download','--object-id',object_id,'--index=false','--output-dir',output_dir,'--force'])
    else:
        subprocess.call([icgc_storage_client, '--profile','aws','download','--object-id',object_id,'--index=false','--output-dir',output_dir])