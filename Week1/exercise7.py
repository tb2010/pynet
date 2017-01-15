#!/usr/bin/env python

# Example 7 - read Yaml and JSON files and pretty print contents
import yaml
import json
from pprint import pprint

with open("my-list.yml") as f:
    pprint(yaml.load(f))

with open("my-list.json") as f:
    pprint(json.load(f))

