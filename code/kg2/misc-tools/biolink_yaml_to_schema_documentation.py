#!/usr/bin/env python3
'''Generates markdown documentation of the Translator Knowledge Graph from the Biolink model

   Usage:  ./biolink_yaml_to_schema_documentation.py biolink-model.yaml (NOT FINISHED YET)
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import io
import json
import jsonschema2md
import yaml


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description='biolink_yaml_to_schema_documentation.py: analyzes the biolink-model.yaml file to generate a JSON representation of the Biolink KG schema.')
    arg_parser.add_argument('biolinkModelYamlLocalFile', type=str)
    return arg_parser


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


def safe_load_yaml_from_string(yaml_string: str):
    return yaml.safe_load(io.StringIO(yaml_string))


args = make_arg_parser().parse_args()
biolink_model_file_name = args.biolinkModelYamlLocalFile

biolink_model = safe_load_yaml_from_string(read_file_to_string(biolink_model_file_name))
classes_info = biolink_model['classes']
node_slot_names = classes_info['entity']['slots']
edge_slot_names = classes_info['association']['slots']
top_types = biolink_model['types']

master_schema = "http://json-schema.org/draft-07/schema#"

node_required = []

node_properties = dict()
schema_nodes = {'$schema': master_schema,
                'title': 'Node',
                'description': 'Biolink knowledge graph node',
                'properties': node_properties,
                'required': node_required}

edge_properties = dict()
schema_edges = {'$schema': master_schema,
                'title': 'Edge',
                'description': 'Biolink knowledge graph edge',
                'properties': edge_properties}

js2md_parser = jsonschema2md.Parser()

slot_info_all = biolink_model['slots']
for node_slot_name in node_slot_names:
    slot_info = slot_info_all[node_slot_name]
    description = slot_info.get('description', '').replace('\n * ', '')
    slot_uri = slot_info.get('slot_uri', "")
    multivalued = slot_info.get('multivalued', False)
    required = slot_info.get('required', False)
    if slot_info.get('identifier', False):
        slot_range_type_print = "uriorcurie"
    elif slot_info.get('slot_uri', None) is not None:
        slot_range_type_print = "string"
    else:
        slot_range_type = slot_info['range']
        if top_types.get(slot_range_type, None) is not None:
            slot_range_type_print = top_types[slot_range_type]['typeof']
        elif classes_info.get(slot_range_type, None) is not None:
            if classes_info[slot_range_type].get('values_from', None) is not None:
                slot_range_type_print = classes_info[slot_range_type]['values_from']
            else:
                slot_range_type_print = slot_range_type
        else:
            slot_range_type_print = 'unknown'
    if multivalued:
        type_arrayified = [slot_range_type_print]
    else:
        type_arrayified = slot_range_type_print
    name = node_slot_name.replace(' ', '_')
    node_properties[name] = {'type': type_arrayified,
                             'description': description + '; **required: ' + str(required) + '**'}
    if required:
        node_required.append(name)

json.dump(schema_nodes, open('kg-schema.json', 'w'))
