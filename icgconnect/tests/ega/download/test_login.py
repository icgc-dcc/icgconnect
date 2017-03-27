import pytest

from icgconnect.ega.download import login

def test_is_valid_email():
	with pytest.raises(ValueError):
		login('test','test')
	
