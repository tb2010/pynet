#!/usr/bin/env python

# Example 6 - Create Yaml and JSON files from list object.
import yaml
import json

my_list = [
    'item1',
    'item2',
    {
        'name': 'test',
        'info': 'Yes we need more',
    },
]

with open("my-list.yml", "w") as f:
    f.write(yaml.dump(my_list, default_flow_style=False))

with open("my-list.json", "w") as f:
    json.dump(my_list, f)

