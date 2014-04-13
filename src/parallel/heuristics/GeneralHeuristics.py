'''
Created on Apr 4, 2014

@author: ezulkosk
'''
from common import Common, API, Options
from common.Common import mAnd
from parallel.heuristics.SAP import random_unique_service_random_server
from visitors import CreateBracketedConstraints
import itertools
import operator
import random
import sys
from z3 import Or, And




def no_split(z3inst, module, num_split):
    return [True for _ in range(num_split)]
    

def condense(products, num_split): 
    currIndex = 0
    while len(products) > num_split:
        lastCon = products.pop()
        products[currIndex] = products[currIndex] + lastCon
        currIndex = currIndex + 1
        if currIndex == num_split:
            currIndex = 0
    products = [Or(*i) for i in products]
    return products

def random_xor_gcard_clafer_toggle(z3inst, module,  num_split):
    '''
    only considers clafers with gcard = [0,1], AND numInstances = 1
    '''
    xors = []
    for i in z3inst.z3_sorts:
        claferSort = z3inst.z3_sorts[i]
        lowerGCard = claferSort.lowerGCard
        upperGCard = claferSort.upperGCard
        if lowerGCard == 1 and upperGCard == 1 and claferSort.numInstances == 1 and not claferSort.element.isAbstract:
            bad = False
            for j in claferSort.fields:
                if j.numInstances != 1:
                    bad = True
                    break
            if not bad and len(claferSort.fields) > 1:
                xors.append((claferSort, len(claferSort.fields)))
    xors.sort(key=operator.itemgetter(1))
    constraints = [True for i in range(num_split)]
    try:
        curr_count = 1
        splitters = []
        for i in xors:
            (claferSort, num_fields) = i
            splitters.append(claferSort)
            curr_count = curr_count * num_fields
            if curr_count >= num_split:
                break
        if curr_count < num_split:
            raise Exception
        else:
            ranges = []
            for i in splitters:
                curr_range = []
                for j in i.fields:
                    curr_range.append(j.instances[0] == 0)
                if i.lowerCardConstraint == 0 and i.upperCardConstraint == 1 and i.numInstances == 1:
                    # the xor parent is off
                    curr_range.append(i.instances[0] == 1)
                ranges.append(curr_range)
            products = list(itertools.product(*ranges))
            products = [[And(*list(i))] for i in products]
            products = condense(products, num_split)
            return products
        
            
    except Exception as e:
        print(e)
        return safe_raise_heuristic_failure_exception("Not enough xor options for heuristic random_xor_gcard_clafer_toggle#" + str(num_split)) 
        
    return constraints


def optional_clafer_toggle(z3inst, module,  num_split, order="random"):
    '''
    only considers clafers with card = [0,1], AND numInstances = 1
    num_split must be a power of 2
    '''
    assert(Common.is_power2(num_split))
    opts = []
    for i in z3inst.z3_sorts:
        claferSort = z3inst.z3_sorts[i]
        lowerCard = claferSort.lowerCardConstraint
        upperCard = claferSort.upperCardConstraint
        if lowerCard == 0 and upperCard == 1 and claferSort.numInstances == 1 and not claferSort.element.isAbstract:
            opts.append(claferSort)
    if order == "random":
        random.shuffle(opts)
    else:
        pairs = []
        for i in opts:
            pairs.append((i, len(i.parentStack)))
        pairs.sort(key=operator.itemgetter(1))
        if order == "top":
            pairs.reverse()
        opts = [i for (i, _) in pairs]
    constraints = [True]
    try:
        while num_split != 1:
            num_split = num_split // 2
            currSort = opts.pop(0)
            newConstraints = []
            for i in constraints:
                newConstraints.append(mAnd(i, currSort.instances[0] == 0))
            for i in constraints:
                newConstraints.append(mAnd(i, currSort.instances[0] == 1))
            constraints = newConstraints
    except:
        return safe_raise_heuristic_failure_exception("Not enough optionals clafers for heuristic optional_clafer_toggle") 
        
    return constraints


def range_split(z3inst, module, num_split, order="biggest"):
    #only consider ranges of top level abstracts that are referring to the same type of concretes
    pairs = []
    for i in z3inst.z3_sorts.values():
        glCardRange = i.numInstances - i.element.glCard[0].value + 1
        pairs.append((i, glCardRange))
    if order == "random":
        random.shuffle(pairs)
    else:
        pairs.sort(key=operator.itemgetter(1))
        if order == "biggest":
            pairs.reverse()
    constraints = []
    
    splitters = []
    curr_count = 0
    for i in pairs:
        (claferSort, card_range) = i
        splitters.append(claferSort)
        curr_count = curr_count + card_range
        if curr_count >= num_split:
            break
    if curr_count < num_split:
        raise Exception
    else:
        ranges = []
        for i in splitters:
            curr_range = []
            for j in range(i.element.glCard[0].value, i.numInstances + 1):
                left = API.createCard(API.createArg(i.element.uid, i))
                right = API.createInteger(j)
                bc = CreateBracketedConstraints.CreateBracketedConstraints(z3inst, True)
                constraint = bc.generatedConstraintVisit(API.createEquals(left, right))
                curr_range.append(constraint)
            ranges.append(curr_range)
        products = list(itertools.product(*ranges))
        products = [[And(*list(i))] for i in products]
        products = condense(products, num_split)
        return products
    
    return safe_raise_heuristic_failure_exception("biggest_range_split failed")
    
def divide_biggest_ranges_in_two(z3inst, module, num_split):
    sys.exit("INCOMPLETE: need to figure out what to do when run out of splits")
    
heuristics = {
              "NO_SPLIT" : no_split,
              "random_optional_clafer_toggle" : lambda z, m, n: optional_clafer_toggle(z,m,n,order="random"),
              "top_optional_clafer_toggle" : lambda z, m, n: optional_clafer_toggle(z,m,n,order="top"),
              "bottom_optional_clafer_toggle" : lambda z, m, n: optional_clafer_toggle(z,m,n,order="bottom"),
              "random_xor_gcard_clafer_toggle" : random_xor_gcard_clafer_toggle,
              "biggest_range_split" : lambda z, m, n: range_split(z,m,n,order="biggest"),
              "smallest_range_split" : lambda z, m, n: range_split(z,m,n,order="smallest"),
              "random_range_split" : lambda z, m, n: range_split(z,m,n,order="random"),
              "divide_biggest_ranges_in_two" : divide_biggest_ranges_in_two
             }

def safe_raise_heuristic_failure_exception(msg):
    '''
    Do not want to raise this exception on sharcnet.
    '''
    if Options.LEARNING_ENVIRONMENT == "sharcnet":
        return []
    else:
        raise HeuristicFailureException(msg)

class HeuristicFailureException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
        