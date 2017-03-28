import pytest
import httpretty
import requests
import json

from icgconnect.ega.download import login

def test_is_valid_email():
	with pytest.raises(ValueError):
		login('test','test')

def test_valid_credentials():
	httpretty.enable()
	httpretty.register_uri(httpretty.GET, "https://ega.ebi.ac.uk/ega/rest/access/v2/users/test@gmail.com",
               body='{"header":{"apiVersion":"v2","code":"200","errorCode":"200","userMessage":"OK"},"response":{"numTotalResults":2,"result":["success","90ac5f7c-b180-4420-9bbc-f4924f44a897"]}}')
	login('test@gmail.com','test')
	httpretty.disable()