from setuptools import setup

setup(name='icgconnect',
      version='0.0.1',
      description='Library of functions to communicate with genome related databases.',
      url='https://github.com/baminou/icgconnect.git',
      author='Brice Aminou',
      author_email='brice.aminou@oicr.on.ca',
      license='MIT',
      packages=['icgconnect','icgconnect.collab','icgconnect.ega','icgconnect.icgc','icgconnect.utils','icgconnect.xml_audit','icgconnect.aws',
                'icgconnect.icgc.song'],
      install_requires=[
            'requests',
            'pysam'
      ],
      zip_safe=True,
      test_suite='nose.collector',
      tests_require=['nose'])
