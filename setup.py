import os
from setuptools import setup, find_packages


version = "1.0.0"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
long_description = read('README.md')
    
setup(name='DatasetRawseeds',
      version=version,
      author="Andrea Censi",
      author_email="andrea@cds.caltech.edu",
      url='http://github.com/AndreaCensi/dataset_rawseeds',
      description=""" Dataset Rawseeds""",
      long_description=long_description,
      keywords="statistics",
      license="LGPL",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],

      download_url='http://github.com/AndreaCensi/dataset_rawseeds/tarball/%s' % version,
      
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[ ],
      tests_require=['nose'],
      entry_points={},
)

