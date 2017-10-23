
This library contains Python functions to send and access accessible data from Collaboratory and EGA servers. The functions in the library contain wrapper to EGA and Collaboratory API.

# How to Install

Make sure that you have python 2.7 and pip (https://pypi.python.org/pypi/pip) installed.

Clone this repository and install the package using pip:

```bash
$ git clone https://github.com/icgc-dcc/icgconnect.git
$ cd icgconnect
$ pip install .
```

ICGConnect contains many helpful functions to communicate with different servers:
* EGA - https://ega-archive.org/submission/programmatic-submissions
* Collaboratory - http://docs.icgc.org/cloud/guide/
* ICGC - http://docs.icgc.org/portal/api/

# Help
You can access the list of functions and definitions using pydoc - https://docs.python.org/2/library/pydoc.html
## EGA
Wrapper functions for EGA submission and downloand API
### EGA Submission
```bash
pydoc icgconnect.ega.submission
```
### EGA Download
```bash
pydoc icgconnect.ega.download
```
