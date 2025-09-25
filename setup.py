'''
The setup file is required for the packaging and also for the metadata, requirements, dependencies. 
It is used by setuptools

'''

from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    '''This function will retuen the requirements list'''
    requirement_list:List[str]=[]
    try:
        with open('requirements.txt','r') as f:
            #read lines from the file
            lines=f.readlines()
            ## process each line
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!= '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. Please ensure it exists in the project root.")
    return requirement_list

setup(
    name="MLENEProject",
    version="0.0.1",
    author="Mani Allada",
    author_email="maniallada28@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
