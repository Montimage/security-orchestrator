#!/bin/bash

# Tested environment:
#
# [Thu Dec 26 13:48:50] mmt@mmt:hspl_tosca$ uname -a
# Linux mmt 5.15.0-124-generic #134-Ubuntu SMP Fri Sep 27 20:20:17 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
# [Thu Dec 26 13:48:58] mmt@mmt:hspl_tosca$ lsb_release -a
# No LSB modules are available.
# Distributor ID:	Ubuntu
# Description:	Ubuntu 22.04.5 LTS
# Release:	22.04
# Codename:	jammy


# exit immediate when gotting error
set -e

# start virtual environment
virtualenv -p python3 .
source bin/activate

# install requirements
# A NumPy version >=1.17.3 and <1.25.0
pip install numpy==1.22.0
#pip install -U pip setuptools wheel
pip install spacy==2.3.9
pip install spacy-lookups-data==1.0.0
pip install nltk==3.5
pip install pyyaml==6.0.2

#bash

echo "

=> Setup successfully the virtual environment.
  
  - To enter the environment: 
      source bin/activate
  - To exit the environment (once entered)
       deactivate
"