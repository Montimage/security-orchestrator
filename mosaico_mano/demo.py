import subprocess
import requests
import json
import time
import sys
import yaml
from nfvo.orchestrator import Orchestrator
with open(sys.argv[1]) as f:
    nfvo=Orchestrator("osm","vim-emu",None)
    nfvo.deploy_security_ns(sys.argv[1])
