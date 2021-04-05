#!/bin/env python3
from datetime import datetime, timedelta
import json
import os
import pathlib
import sys
import urllib.request
import expand_utilities as eu
from typing import List
from collections import defaultdict
from itertools import product

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")  # ARAXQuery directory
from ARAX_response import ARAXResponse
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../UI/OpenAPI/python-flask-server/")
from openapi_server.models.query_graph import QueryGraph


class Director:

    def __init__(self, log: ARAXResponse, all_kps: List[str]):
        self.meta_map_path = f"{os.path.dirname(os.path.abspath(__file__))}/meta_map.json"
        self.log = log
        self.all_kps = all_kps
        # Check if it's time to update the local copy of the meta_map
        if self._need_to_regenerate_meta_map():
            self._regenerate_meta_map()
        # Load our map now that we know it's up to date
        with open(self.meta_map_path) as map_file:
            self.meta_map = json.load(map_file)

    def get_kps_for_single_hop_qg(self, qg: QueryGraph) -> List[str]:
        # confirm that the qg is one hop
        if len(qg.edges) > 1:
            self.log.error(f"Query graph can only have one edge, but instead has {len(qg.edges)}.", error_code="UnexpectedQG")
            return
        # isolate possible subject predicate object from qg
        qedge = list(qg.edges.values())[0]
        sub_category_list = eu.convert_to_list(qg.nodes[qedge.subject].category)
        obj_category_list = eu.convert_to_list(qg.nodes[qedge.object].category)
        predicate_list = eu.convert_to_list(qedge.predicate)
        
        # use metamap to check kp for predicate triple
        kps_to_return = []
        for kp, predicates_dict in self.meta_map.items():
            if self._triple_is_in_predicates_response(predicates_dict, sub_category_list, predicate_list, obj_category_list):
                kps_to_return.append(kp)
        return kps_to_return
    
    # returns True if at least one possible triple exists in the predicates endpoint response
    @staticmethod
    def _triple_is_in_predicates_response(self, predicates_dict: dict, subject_list: list, predicate_list: list, object_list: list)  -> bool:
        # handle potential emptiness of sub, obj, predicate lists
        if not subject_list: # any subject
            subject_list = list(predicates_dict.keys())
        if not object_list: # any object
            object_set = set()
            _ = [object_set.add(obj) for obj_dict in predicates_dict.values() for obj in obj_dict.keys()]
            object_list = list(object_set)
        any_predicate = False if predicate_list else True

        # handle combinations of subject and objects using cross product
        qg_sub_obj_dict = defaultdict(lambda: set())
        for sub, obj in list(product(subject_list, object_list)):
            qg_sub_obj_dict[sub].add(obj)

        # check for subjects
        kp_allowed_subs = set(predicates_dict.keys())
        accepted_subs = kp_allowed_subs.intersection(set(qg_sub_obj_dict.keys()))

        # check for objects
        for sub in accepted_subs:
            kp_allowed_objs = set(predicates_dict[sub].keys())
            accepted_objs = kp_allowed_objs.intersection(qg_sub_obj_dict[sub])
            if len(accepted_objs) > 0:
                # check predicates
                for obj in accepted_objs:
                    if any_predicate or set(predicate_list).intersection(set(predicates_dict[sub][obj])):
                        return True
        return False

    def _need_to_regenerate_meta_map(self) -> bool:
        # Check if file doesn't exist or if it hasn't been modified in the last day
        meta_map_file = pathlib.Path(self.meta_map_path)
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        if not meta_map_file.exists() or datetime.fromtimestamp(meta_map_file.stat().st_mtime) < twenty_four_hours_ago:
            self.log.debug(f"Local copy of meta map either doesn't exist or needs to be refreshed")
            return True
        else:
            return False

    def _regenerate_meta_map(self):
        # Create an up to date version of the meta map
        self.log.debug(f"Regenerating combined meta map for all KPs")
        self.meta_map = dict()
        for kp in self.all_kps:
            # get predicates dictionary from KP
            kp_endpoint = eu.get_kp_endpoint_url(kp)
            if kp_endpoint is None:
                self.log.debug(f"No endpoint for {kp}. Skipping for now.")
                continue
            kp_predicates_response = urllib.request.urlopen(f"{kp_endpoint}/predicates")
            if kp_predicates_response.status != 200:
                self.log.warning(f"Unable to access {kp}'s predicates endpoint "
                             f"(returned status of {kp_predicates_response.status})")
                continue
            predicates_dict = json.loads(kp_predicates_response.read())
            self.meta_map[kp] = predicates_dict
        # Save our big combined metamap to a local json file
        with open(self.meta_map_path, "w+") as map_file:
            json.dump(self.meta_map, map_file)

    def _get_non_api_kps_meta_info(self):
        # TODO: Hardcode info for our KPs that don't have APIs here... (then include when building meta map)
        # Need to hardcode DTD and NGD
        # For NGD, should we just use KG2's predicate info?
        # For DTD, my best guess is subjects = Drug, ChemicalSubstance, objects = Disease, but that feels likely incomplete
        pass
