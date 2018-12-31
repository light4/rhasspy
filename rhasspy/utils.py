import os
import re
import logging
import math
import itertools
import collections
from typing import Mapping, List, Iterable, Optional, Any

# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------

def read_dict(dict_file: Iterable[str],
              word_dict: Optional[Mapping[str, List[str]]] = None):
    '''
    Loads a CMU word dictionary, optionally into an existing Python dictionary.
    '''
    if word_dict is None:
        word_dict = {}

    for line in dict_file:
        line = line.strip()
        if len(line) == 0:
            continue

        word, pronounce = re.split('\s+', line, maxsplit=1)
        idx = word.find('(')
        if idx > 0:
            word = word[:idx]

        pronounce = pronounce.strip()
        if word in word_dict:
            word_dict[word].append(pronounce)
        else:
            word_dict[word] = [pronounce]

    return word_dict

# -----------------------------------------------------------------------------

def lcm(*nums):
    '''Returns the least common multiple of the given integers'''
    if len(nums) == 0:
        return 1

    nums_lcm = nums[0]
    for n in nums[1:]:
        nums_lcm = (nums_lcm*n) // math.gcd(nums_lcm, n)

    return nums_lcm

# -----------------------------------------------------------------------------

def recursive_update(base_dict: Mapping[Any, Any], new_dict: Mapping[Any, Any]):
    '''Recursively overwrites values in base dictionary with values from new dictionary'''
    for k, v in new_dict.items():
        if isinstance(v, collections.Mapping) and (k in base_dict):
            recursive_update(base_dict[k], v)
        else:
            base_dict[k] = v