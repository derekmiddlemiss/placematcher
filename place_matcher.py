#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 23:21:41 2021

@author: del
"""
import re
import math
import string
from itertools import groupby
from Levenshtein import distance

class PlaceMatcher:
    
    any_letter = re.compile(r"[^{}0-9]".format(string.punctuation))
    
    @staticmethod
    def _name_to_scoring(name):
        name = str.lower(str.strip(name))
        name = name.translate(str.maketrans("", "", string.punctuation))
        return name    
    
    @staticmethod
    def _name_to_ref(name):
        return str.strip(name)
    
    def __init__(self, places, use_first = False, unknown_thresh = None):
        self._get_names(places)
        self._use_first = use_first
        if unknown_thresh is None:
            self._unknown_thresh = math.inf
        else:
            self._unknown_thresh = unknown_thresh
        if self._use_first:
            self._split_names()
        
        
    def _get_names(self, places):
        try:
            names = places['name'].to_list()
        except KeyError as err:
            raise KeyError("dict or DataFrame input to 'places' must have 'name' key.") from err
        except AttributeError:
            names = places['name']
        except TypeError:
            names = places
        if type(names) != list: names = [names]
        
        self._ref_names = list(map(PlaceMatcher._name_to_ref, names))
        self._scoring_names = list(map(PlaceMatcher._name_to_scoring, names))
    
    def _split_names(self):        
        self._scoring_names = {lett: list(names)
            for lett, names in groupby(self._scoring_names, 
            key=lambda name: PlaceMatcher.any_letter.search(name).group())}

        self._ref_names = {lett: list(names)
            for lett, names in groupby(self._ref_names, 
            key=lambda name: str.lower(PlaceMatcher.any_letter.search(name).group()))}
        
    def match(self, to_match):
        to_match = PlaceMatcher._name_to_scoring(to_match)

        if self._use_first:
            key = self.any_letter.search(to_match).group()
            scoring_names = self._scoring_names.get(key, None)
            if scoring_names is None: return "Unknown"
        else:
            scoring_names = self._scoring_names
            
        lowest_score = math.inf
        lowest_score_unique = True
        for index, name in enumerate(scoring_names):
            score = distance(to_match, name)
            if score < lowest_score:
                lowest_score = score
                lowest_score_unique = True
                if self._use_first:
                    lowest_pos = {"key": key, "index": index}
                else:
                    lowest_pos = {"index": index}
            elif score == lowest_score:
                lowest_score_unique = False
        
        if not lowest_score_unique or lowest_score >= self._unknown_thresh:
            return "Unknown"
        else:
            if self._use_first:
                return self._ref_names[lowest_pos["key"]][lowest_pos["index"]]
            else:
                return self._ref_names[lowest_pos["index"]]
                
                    
            
        
            
        
            
        
        
