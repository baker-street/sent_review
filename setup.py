"""
sentreview Copyright (C) 2015  Steven Cutting
"""


from setuptools import setup, find_packages

with open("README.md") as fp:
    THE_LONG_DESCRIPTION = fp.read()

PACKAGES = ['sentreview']


setup(
    name="sentreview",
    version="0.1.0",
    license='GNU GPL v3+',
    description="NLP library",   # UPDATE INFO
    long_description=THE_LONG_DESCRIPTION,
    classifiers=['Topic :: NLP',
                 'Topic :: Text processing',
                 'Topic :: text munging',
                 'Topic :: data munging',
                 'Topic :: feature engineering',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Data Scientists',
                 'Operating System :: GNU Linux',
                 'Operating System :: OSX :: MacOS :: MacOS X',
                 'Operating System :: POSIX',
                 'Development Status :: 3 - Alpha',
                 'Programming Language :: Python :: 2.7',
                 'License :: GNU GPL v3+',
                 'Status :: ' + "pre-alpha",
                 ],
    keywords='nlp text',
    author='Steven Cutting',
    author_email='steven.e.cutting@linux.com',
    packages=find_packages(exclude=('scripts', 'tests')),
    # zip_safe=False,
    )
