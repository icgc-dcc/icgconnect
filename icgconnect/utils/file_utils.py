import hashlib
import os
from shutil import copyfile
import pysam

def get_file_md5(fname):
	if not os.path.isfile(fname):
		raise ValueError("The file does not exist: "+fname)
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def get_file_size(fname):
	if not os.path.isfile(fname):
		raise ValueError("The file does not exist: "+fname)
	return os.path.getsize(fname)

def delete_file(filename):
	""" Delete a file in the local system

		Args:
			filename (str):	Path of the file name

		Raises:
			ValueError:	The file does not exist
	"""
	if not os.path.isfile(filename):
		raise ValueError("The file does not exist: "+ filename)
	os.remove(filename)

def generate_bai_from_bam(bam_file_path, file_output):
	""" Generate a bai file from a bam file

		Args:
			bam_file_path (str):	Path of the bam file
			file_output (str):		Path to create the bai file

		Raises:
			ValueError:	Bam file does not exist
			ValueError: Output file already exists
			ValueError: Input same as output file
	"""
	if not os.path.isfile(bam_file_path):
		raise ValueError("Bam file does not exist: "+bam_file_path)

	if os.path.isfile(file_output):
		raise ValueError("The output file already exists: "+file_output)

	if bam_file_path == file_output:
		raise ValueError("The input file cannot be the same as the output file: "+bam_file_path)

	pysam.index(bam_file_path)
	if not bam_file_path+".bai" == file_output:
		copyfile(bam_file_path+".bai",file_output)
