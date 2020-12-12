import subprocess
import requests
import json
import time
import sys
import yaml
from nfvo.orchestrator import Orchestrator
with open(sys.argv[1]) as f:
    nfvo=Orchestrator("osm","vim-emu","nfvi")
    nfvo.deploy_security_network(sys.argv[1])
