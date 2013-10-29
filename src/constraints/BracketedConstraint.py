'''
Created on Apr 29, 2013

@author: ezulkosk
'''
from common import Common
from common.Common import mOr, mAnd
from constraints import Constraints
from constraints.Constraints import GenericConstraints
from lxml.builder import basestring
from structures.ExprArg import ExprArg, IntArg, BoolArg, Mask, JoinArg
from z3 import If, Not, Sum, Implies, And, Xor, Or
import sys


#FIX ME
def joinWithSuper(sort, mask):
    '''
    :param sort:
    :type sort: :class:`~common.ClaferSort`
    :returns: (:class:`~common.ClaferSort`, [Int()]) 
    
    Maps each instance of the subclafer **sort** to the corresponding super instance. Returns the super sort and its instances.
    '''
    newMask = Mask()
    for i in mask.keys():
        #ClaferSort.addSubSort(self, sub), is somewhat related 
        newMask.put(i + sort.indexInSuper,
                    If(mask.get(i) != sort.parentInstances, 
                       sort.superSort.instances[i + sort.indexInSuper], 
                       sort.superSort.parentInstances))
    return(sort.superSort, newMask)


def joinFilter(index, keys, joinSorts):
    if not Common.BREAK:
        return []
    newKeys = []
    currKeys = [index]
    for i in joinSorts:
        newCurrKeys = set([])
        for j in currKeys:
            #get extraAbsenceConstraint correct....
            if j == i.numInstances:
                continue
            (low,high,_) = i.instanceRanges[j]
            if low <= j and j <= high:
                for k in range(low,high+1):
                    newCurrKeys.add(k)
        currKeys = list(newCurrKeys)        
    return currKeys

def joinHelper(left, right, zeroedVal):
    '''
    :param leftSort:
    :type leftSort: :class:`~common.ClaferSort`
    :param rightSort:
    :type rightSort: :class:`~common.ClaferSort`
    :param linstances:
    :type linstances: [Int()]
    :param rinstances:
    :type rinstances: [Int()]
    :param zeroedVal: the number of parentInstances of rightSort, or zero if rightSort is "int"
    :type zeroedVal: int
    :returns: Z3-function(int, int) 
    
    Creates a Z3-function that ranges over len(rinstances). For each index in rinstances, 
    returns the instance if its corresponding instance in linstances is on
    , else the instances is *masked* to be zeroedVal. ::
    
    >>> zeroedVal = 3
    >>> leftSort.parentInstances = 1
    >>> linst = [0,0,1]
    >>> rinst = [0,1,1,2,2,3]
    >>> join([0,0,1], [0,1,1,2,2,3]) 
    >>>    => [mask(0), mask(1), mask(1), mask(2), mask(2), mask(3]]
    >>>    => [0,1,1,3,3,3]
    
    Here, since linst[2] = leftSort.parentInstances, any instance in rinstances that points to linst[2] is *zeroed*. 
    The other instances remain the same.
    '''
    leftJoinPoint = left.joinSorts[-1]
    rightJoinPoint = right.joinSorts[0]
    
    #get the instanceSorts associated with the join point.
    for i in left.instanceSorts:
        (left_sort, left_mask) = i
        if isinstance(left_sort, basestring) or left_sort == leftJoinPoint:
            break
    for i in right.instanceSorts:
        (right_sort, right_mask) = i #FIXME
        if isinstance(right_sort, basestring) or right_sort == rightJoinPoint:
            break
        
    '''
    for i in range(len(left_mask)):
        if left_mask[i]:
            condList.append(left.instances[count] != leftJoinPoint.parentInstances)
            onInstancesList.append(i) 
            count = count + 1
    '''
    #should be very fine-grained for the solver, but might bog down translation, not sure yet
    newMask = Mask()
    ''' new '''
    if Common.BREAK:
        for i in left_mask.keys():
            joinRange = joinFilter(i, right_mask.keys(), right.joinSorts)
            for j in joinRange:
                if j in right_mask.keys():
                    prevClause = newMask.get(j)
                    newMask.put(j, mOr(prevClause, And(left_mask.get(i) != left_sort.parentInstances, 
                                                    rightJoinPoint.instances[j] == i)))
        for i in newMask.keys():
            newMask.put(i, If(newMask.get(i), right_mask.get(i) , zeroedVal))
        for i in newMask.values():
            print(i)
            print()
        return newMask
    ''' end '''
    for i in right_mask.keys():
        (lower, upper, _) = rightJoinPoint.instanceRanges[i]
        for j in range(lower, upper + 1): 
            #only possibly join with things that are in left
            if left_mask.get(j):
                prevClause = newMask.get(i)
                newMask.put(i, mOr(prevClause, And(left_mask.get(j) != left_sort.parentInstances, 
                                                rightJoinPoint.instances[i] == j)))#right_mask.get(i) == j)))
        #if leftJoinInstances:
        #   newMaskList.append(i)
        #   condList.append(mOr(*[And(left_mask.get(k) != leftJoinPoint.parentInstances, rightJoinPoint.instances[i] == k) for k in leftJoinInstances]))
    for i in newMask.keys():
        newMask.put(i, If(newMask.get(i), right_mask.get(i) , zeroedVal))
    return newMask
    '''
    (sort, mask) = left.instanceSorts[0]
    newMask = Mask()
    for i in mask.keys():
        (lower,upper,_) = sort.instanceRanges[i]
        for j in range(lower, upper + 1):
            prevClause = newMask.get(j)
            newMask.put(j, mOr(prevClause, mask.get(i) == j))
    
    funcID = str(Common.getFunctionUID())
    functionName = "f" + funcID + "_" + leftJoinPoint.element.nonUniqueID() + "." + rightJoinPoint.element.nonUniqueID()
    joinFunction = Function(functionName, IntSort(), IntSort())
    joinHelperFunction = Function("h" + functionName , IntSort(), IntSort())
    constraints = []
    for i in range(len(left.instances)):
        constraints.append(joinHelperFunction(i) == left.instances[i]) 
    constraints.append(joinHelperFunction(len(left.instances)) == leftJoinPoint.parentInstances)
    for i in range(len(right.instances)):  #rinstance[i] in joinHelperFunction arg
        constraints.append(joinFunction(i) == If(joinHelperFunction(rightJoinPoint.instances[i]) != leftJoinPoint.parentInstances, right.instances[i], zeroedVal))
    constraints.append(joinFunction(len(right.instances)) == zeroedVal)
    leftJoinPoint.z3.join_constraints.addAll(constraints)
    return joinFunction
    '''

#can optimize this.parent
#need to range newInstances over ALL sorts in instanceSorts (don't have a test case yet)
#   for example, leftJoinPoint.parentInstances CHANGES if there are multiple sorts here
#XXX
def op_join(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns the join of left and right, using the join function created in createJoinFunction().
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return JoinArg(left, right)


    '''
    NOTHING BENEATH IS USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    '''
    
    leftJoinPoint = left.joinSorts[-1]
    rightJoinPoint = right.joinSorts[0]
    if isinstance(rightJoinPoint, basestring):
        if rightJoinPoint == "parent":
            joinSorts = left.joinSorts + [leftJoinPoint.parent] +  [right.joinSorts[i] for i in range(1, len(right.joinSorts))]
            (sort, mask) = left.instanceSorts[0]
            newMask = Mask()
            for i in mask.keys():
                (lower,upper,_) = sort.instanceRanges[i]
                for j in range(lower, upper + 1):
                    if j == leftJoinPoint.parentInstances:
                        break
                    prevClause = newMask.get(j)
                    newMask.put(j, mOr(prevClause, mask.get(i) == j))
                    #*[j == i for j in left.instances])
                #newInstances.append(If(clause, leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
            for i in newMask.keys():
                newMask.put(i, If(newMask.get(i), leftJoinPoint.parent.instances[i], leftJoinPoint.parent.parentInstances))
            return ExprArg(joinSorts, [(leftJoinPoint.parent, newMask)])
        elif rightJoinPoint == "ref":
            if isinstance(leftJoinPoint.refSort, basestring):
                if leftJoinPoint.refSort == "integer":
                    mask = left.getInstanceMask(leftJoinPoint)
                    newMask = Mask()
                    for i in mask.keys():
                        newMask.put(i, If(mask.get(i) != leftJoinPoint.parentInstances, leftJoinPoint.refs[i], 0))
                    return(ExprArg(left.joinSorts + ["int"], 
                                   [("int", newMask)] ))   
                elif leftJoinPoint.refSort == "string":
                    #obviously needs to change, just pretend strings are ints for now
                    mask = left.getInstanceMask(leftJoinPoint)
                    newMask = Mask()
                    for i in mask.keys():
                        newMask.put(i, If(mask.get(i) != leftJoinPoint.parentInstances, leftJoinPoint.refs[i], 0))
                    return(ExprArg(left.joinSorts + ["int"], 
                                   [("int", newMask)] ))   
                    
                else:
                    print("Error on: " + leftJoinPoint.refSort + ", refs other than int (e.g. double) unimplemented")
                    sys.exit()
            else: 
                #join on ref sort
                joinSorts = left.joinSorts + [leftJoinPoint.refSort] +  [right.joinSorts[i] for i in range(1, len(right.joinSorts))]
                #needs to be more robust for multiple instanceSorts
                (sort, mask) = left.instanceSorts[0]
                tempRefs = []
                newMask = Mask()
                for i in mask.keys():
                    # **** the "else" used to be refSort.parentInstances, but i think this is right
                    tempRefs.append(If(mask.get(i) != leftJoinPoint.parentInstances,
                                       leftJoinPoint.refs[i], leftJoinPoint.refSort.numInstances))
                for i in range(leftJoinPoint.refSort.numInstances):
                    clause = mOr(*[j == i for j in tempRefs])
                    newMask.put(i, If(clause, leftJoinPoint.refSort.instances[i], leftJoinPoint.refSort.parentInstances))
                newInstanceSorts = [(leftJoinPoint.refSort, newMask)]
                return(ExprArg(joinSorts, newInstanceSorts))
                '''
                for j in range(sort.numInstances):
                    if mask[j]:
                        tempRefs.append(If(left.instances[count] != leftJoinPoint.parentInstances
                                           , leftJoinPoint.refs[j], leftJoinPoint.refSort.parentInstances))
                        count = count + 1
                for i in range(leftJoinPoint.refSort.numInstances):
                    
                    clause = mOr(*[j == i for j in tempRefs])
                    newInstances.append(If(clause, leftJoinPoint.refSort.instances[i], leftJoinPoint.refSort.parentInstances))
                return(ExprArg(joinSorts, [(leftJoinPoint.refSort, newMask)]))
                '''
    else:
        #Make more robust
        instanceSort = left.instanceSorts[0]
        (leftJoinPoint, leftMask) = instanceSort
        while not(rightJoinPoint in leftJoinPoint.fields):
            (leftJoinPoint, leftMask) = joinWithSuper(leftJoinPoint, leftMask)
            #(leftJoinPoint, leftInstances) = joinWithSuper(leftJoinPoint, leftInstances)
        instanceSorts = right.instanceSorts
        (sort, mask) = instanceSorts[0]
        if(isinstance(sort,basestring) and sort == "int"):
            zeroedVal = 0
        else:
            zeroedVal = sort.parentInstances
        newJoinSorts = left.joinSorts[:]
        newJoinSorts.append(leftJoinPoint)
        newLeft = ExprArg(newJoinSorts, [(leftJoinPoint, leftMask)])
        newInstanceSorts = [(sort, joinHelper(newLeft, right, zeroedVal))]
        joinSorts = newLeft.joinSorts + right.joinSorts
        return(ExprArg(joinSorts, newInstanceSorts))

def op_card(arg):
    '''
    :param arg:
    :type left: :class:`~arg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns the number of instances that are *on* in arg.
    '''
    assert isinstance(arg, ExprArg)
    instances = []
    for i in arg.getInstanceSorts():
        (sort, mask) = i
        for j in mask.values():
            instances.append(If(j != sort.parentInstances, 1, 0))  
    return IntArg([Sum(instances)])

def op_add(left,right):
    '''
    :param left:
    :type left: :class:`~IntArg`
    :param right:
    :type right: :class:`~IntArg`
    :returns: :class:`~IntArg` 
    
    Returns left + right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval + rval])

def op_sub(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left - right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval - rval])

def op_mul(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left * right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval * rval])

#integer division
def op_div(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Returns left / right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return IntArg([lval / rval]
                   if((not isinstance(lval, int)) or (not isinstance(rval, int)))
                             else [lval // rval])
    
    
def op_un_minus(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Negates arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.getInstanceSort(0)
    val = mask.pop_value()
    return IntArg([-(val)])
    

def op_not(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Boolean negation of arg.
    '''
    assert isinstance(arg, ExprArg)
    (_, mask) = arg.getInstanceSort(0)
    val = mask.pop_value()
    return BoolArg([Not(val)])
    
#need to iterate over all instancesorts, maybe not
def op_eq(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left = right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    
    #integer equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if (isinstance(left_sort, basestring) and left_sort == "int") or \
        (isinstance(right_sort, basestring) and right_sort == "int"):
        
        return BoolArg([sum(*[left_mask.values() for (_, left_mask) in left.getInstanceSorts()]) 
                        == sum(*[right_mask.values() for (_, right_mask) in right.getInstanceSorts()])])
    #clafer-set equality case
    else:
        cond = []
        while True:
            nextSorts = getNextInstanceSort(sortedL, sortedR)
            if not nextSorts:
                break
            if len(nextSorts) == 1:
                (_, (sort, l)) = nextSorts[0]
                #if only one side of the equation has elements a sort,
                #make sure none are on.
                for i in l.values():
                    cond.append(i == sort.parentInstances)
                    
            else:
                (_, (sort, l)) = nextSorts[0]
                (_, (_, r)) = nextSorts[1]
                for i in l.difference(r.getTree()):
                    cond.append(l.get(i) == sort.parentInstances)
                for i in r.difference(l.getTree()):
                    cond.append(r.get(i) == sort.parentInstances)
                for i in l.intersection(r.getTree()):
                    cond.append(mAnd(Implies(l.get(i) != sort.parentInstances,
                                              r.get(i) != sort.parentInstances),
                                          Implies(l.get(i) == sort.parentInstances,
                                              r.get(i) == sort.parentInstances)))
        return BoolArg([And(*cond)])
    
def op_ne(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left != right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_eq(left, right)
    for i in expr.getInstanceSorts():
        (_, mask) = i
        for j in mask.keys():
            mask.put(j, Not(mask.get(j)))
    return expr
    
def op_lt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left < right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([lval < rval])  
        
def op_le(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left <= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([lval <= rval])  

def op_gt(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left > right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_lt(right, left)

def op_ge(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that the left >= right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return op_le(right, left)

def op_and(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean conjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([mAnd(lval, rval)])  

def op_or(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean disjunction of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([mOr(lval, rval)])  

def op_xor(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Computes the boolean XOR of the left and right instances.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (_, left_mask) = left.getInstanceSort(0)
    (_, right_mask) = right.getInstanceSort(0)
    lval = left_mask.pop_value()
    rval = right_mask.pop_value()
    return BoolArg([Xor(lval, rval)])  

def op_implies(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensure that if instance *i* of left is on, so is instance *i* of right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    
    #integer equality case
    (left_sort, left_mask) = left.getInstanceSort(0)
    (right_sort, right_mask) = right.getInstanceSort(0)
    if (isinstance(left_sort, basestring) and left_sort == "bool") or \
        (isinstance(right_sort, basestring) and right_sort == "bool"):
        
        return BoolArg([Implies(left_mask.pop_value(), right_mask.pop_value())])
    #clafer-set equality case
    else:
        cond = []
        while True:
            nextSorts = getNextInstanceSort(sortedL, sortedR)
            if not nextSorts:
                break
            if len(nextSorts) == 1:
                (side, (sort, l)) = nextSorts[0]
                #if only left side of the equation has elements of a sort,
                #make sure none are on.
                if side == "l":
                    for i in l.values():
                        cond.append(i == sort.parentInstances)
                    
            else:
                (_, (sort, l)) = nextSorts[0]
                (_, (_, r)) = nextSorts[1]
                for i in l.difference(r.getTree()):
                    cond.append(l.get(i) == sort.parentInstances)
                for i in l.intersection(r.getTree()):
                    cond.append(Implies(l.get(i) != sort.parentInstances,
                                              r.get(i) != sort.parentInstances))
        return BoolArg([And(*cond)])
    #return BoolArg([mAnd(*[Implies(i,j) for i,j in zip(left.instances, right.instances)])])

def op_equivalence(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that an element of left is *on* iff it is *on* in right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    return BoolArg([And(op_implies(left, right), op_implies(right,left))])
    #return BoolArg([mAnd(*[mAnd(Implies(i,j), Implies(j,i)) for i,j in zip(left.instances, right.instances)])])
    
def op_ifthenelse(cond, ifExpr, elseExpr):
    '''
    :param cond:
    :type cond: :class:`~ExprArg`
    :param ifExpr:
    :type ifExpr: :class:`~ExprArg`
    :param elseExpr:
    :type elseExpr: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Returns the corresponding Z3 If-construct over the instances of the arguments.
    '''
    assert isinstance(cond, ExprArg)
    assert isinstance(ifExpr, ExprArg)
    assert isinstance(elseExpr, ExprArg)
    
    (_, cond_mask) = cond.getInstanceSort(0)
    (_, if_mask) = ifExpr.getInstanceSort(0)
    (_, else_mask) = elseExpr.getInstanceSort(0)
    
    return BoolArg([If(cond_mask.pop_value(), if_mask.pop_value(), else_mask.pop_value())])

def getNextInstanceSort(left, right):
    if left or right:
        if left and right:
            if left[0][0] < right[0][0]:
                return [("l", left.pop(0))]
            elif left[0][0] > right[0][0]:
                return [("r", right.pop(0))]
            else:
                return [("l", left.pop(0)), ("r", right.pop(0))]
        elif left:
            return [("l", left.pop(0))]
        else:
            return [("r", right.pop(0))]
    else: 
        return []

def op_union(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set union (left ++ right)
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (_, nextInstanceSort) = nextSorts[0]
            newInstanceSorts.append(nextInstanceSort)
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.difference(r.getTree()):
                newMask.put(i, l.get(i))
            for i in r.difference(l.getTree()):
                newMask.put(i, r.get(i))
            for i in l.intersection(r.keys()):
                newMask.put(i, Common.min2(l.get(0), r.get(0)))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(newInstanceSorts)
                
  
def op_intersection(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set intersection (left & right)
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            continue
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.intersection(r.keys()):
                newMask.put(i, Common.max2(l.get(0), r.get(0)))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)
    
    
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    (extendedL, extendedR) = set_extend(left,right)
    finalInstances = []
    for i in extendedL.instanceSorts:
        for _ in range(i.numInstances):
            finalInstances.append(Common.max2(extendedL.instances.pop(0), extendedR.instances.pop(0)))
    return ExprArg(extendedR.joinSorts, extendedR.instanceSorts, finalInstances)
    '''

def op_difference(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Computes the set difference (left - - right)
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    newInstanceSorts = []
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (side, nextInstanceSort) = nextSorts[0]
            if(side == "l"):
                newInstanceSorts.append(nextInstanceSort)
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            newMask = Mask()
            for i in l.difference(r.getTree()):
                newMask.put(i, l.get(i))
            for i in l.intersection(r.keys()):
                newMask.put(i, If(r.get(i) != sort.parentInstances
                                     , l.get(i)
                                     , sort.parentInstances))
            newInstanceSorts.append((sort, newMask))
    return ExprArg(left.joinSorts, newInstanceSorts)
    
def getMatch(key, list):
    '''
    returns the items in list with the same sort as key,
    along with the index of the instances in the supersort
    '''
    matches = []
    for i in list:
        (sort, _) = i
        if key == sort:
            matches.append((0,i))
        else:
            totalIndexInSuper = 0
            tempKey = key
            while tempKey.superSort:
                totalIndexInSuper = totalIndexInSuper + tempKey.indexInSuper
                tempKey = tempKey.superSort
                if tempKey == sort:
                    matches.append((totalIndexInSuper, i))
                    break
    return matches
                
def op_in(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~BoolArg` 
    
    Ensures that left is a subset of right.
    '''
    sortedL = sorted([(sort, mask.copy()) for (sort,mask) in left.getInstanceSorts()])
    sortedR = sorted([(sort, mask.copy()) for (sort,mask) in right.getInstanceSorts()])
    cond = []
    for i in sortedL:
        (left_sort, left_mask) = i
        matches = getMatch(left_sort, sortedR)
        for j in matches:
            (transform, (right_sort,right_mask)) = j
            for k in left_mask.keys():
                if not right_mask.get(k + transform):
                    cond.append(left_mask.get(k) == left_sort.parentInstances)
                else:
                    cond.append(Implies(left_mask.get(k) != left_sort.parentInstances,
                                        right_mask.get(k + transform) != right_sort.parentInstances))
    return BoolArg([And(*cond)])
    '''
    while True:
        nextSorts = getNextInstanceSort(sortedL, sortedR)
        if not nextSorts:
            break
        if len(nextSorts) == 1:
            (side, (sort, l)) = nextSorts[0]
            if side == "l":
                #make sure nothing on the left is on, since it cant be in the right
                for i in l.values():
                    cond.append(i == sort.parentInstances)
                
        else:
            (_, (sort, l)) = nextSorts[0]
            (_, (_, r)) = nextSorts[1]
            for i in l.difference(r.getTree()):
                cond.append(l.get(i) == sort.parentInstances)
            for i in l.intersection(r.getTree()):
                cond.append(Implies(l.get(i) != sort.parentInstances,
                                          r.get(i) != sort.parentInstances))
    return BoolArg([And(*cond)])
    '''
def op_nin(left,right):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Ensures that left is not a subset of right.
    '''
    assert isinstance(left, ExprArg)
    assert isinstance(right, ExprArg)
    expr = op_in(left,right)
    return BoolArg([expr.pop_value()])

def op_domain_restriction(l,r):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    No idea what this does.
    '''
    pass

def op_range_restriction(l,r):
    '''
    :param left:
    :type left: :class:`~ExprArg`
    :param right:
    :type right: :class:`~ExprArg`
    :returns: :class:`~ExprArg` 
    
    Nope.
    '''
    pass

def op_sum(arg):
    '''
    :param arg:
    :type arg: :class:`~ExprArg`
    :returns: :class:`~IntArg` 
    
    Computes the sum of all integer instances in arg. May not match the semantics of the Alloy backend.
    '''
    assert isinstance(arg, ExprArg)
    instances = []
    for i in arg.getInstanceSorts():
        (_, mask) = i
        for j in mask.values():
            instances.append(j)
    return IntArg([Sum(instances)])

'''
    Map used to convert Clafer operations to Z3 operations
    keys: operation(str) returned by Clafer Python generator
    values: pairs:
        1. arity
        2. function associated with the operator
'''
ClaferToZ3OperationsMap = {
                           #Unary Ops
                           "!"           : (1, op_not),
                           "UNARY_MINUS" : (1, op_un_minus),
                           "#"           : (1, op_card),
                           "max"         : (1, "TODO"),
                           "min"         : (1, "TODO"),
                           "sum"         : (1, op_sum),    
                           #Binary Ops
                           "<=>"         : (2, op_equivalence),
                           "=>"          : (2, op_implies),
                           "||"          : (2, op_or),
                           "xor"         : (2, op_xor),
                           "&&"          : (2, op_and),
                           "<"           : (2, op_lt),
                           ">"           : (2, op_gt),
                           "<="          : (2, op_le),
                           ">="          : (2, op_ge),
                           "="           : (2, op_eq),
                           "!="          : (2, op_ne),
                           "in"          : (2, op_in),
                           "nin"         : (2, op_nin),
                           "+"           : (2, op_add),
                           "-"           : (2, op_sub),
                           "*"           : (2, op_mul),
                           "/"           : (2, op_div),
                           "++"          : (2, op_union),
                           "--"          : (2, op_difference),
                           "&"           : (2, op_intersection),
                           "<:"          : (2, op_domain_restriction),
                           ":>"          : (2, op_range_restriction),
                           "."           : (2, op_join),
                           #Ternary Ops
                           "ifthenelse"  : (3, op_ifthenelse)       
                           }

def getOperationConversion(op):
    '''
    :param op: String representation of Clafer operation.
    :type op: str
    :returns: 2-tuple from ClaferToZ3OperationsMap with the fields:
    
    The 2-tuple has the fields:
        1. arity of the function
        2. function associated with the operator
    '''
    return ClaferToZ3OperationsMap[op]


class BracketedConstraint(Constraints.GenericConstraints):
    '''
    :var stack: ([]) Used to process a tree of expressions.
    Class for creating bracketed Clafer constraints in Z3.
    '''
    
    def __init__(self, z3, claferStack):
        ident = "BC:" + ".".join([str(i.element.uid) for i in claferStack])
        GenericConstraints.__init__(self, ident)
        self.z3 = z3
        self.claferStack = claferStack
        self.stack = []
        self.locals = {}
        self.value = None
        
    def addLocal(self, uid, expr):
        self.locals[uid] = expr
    
    def addArg(self, arg):
        self.stack.append(arg)
       
    #clean     
    def addQuantifier(self, quantifier, num_args, num_combinations, ifconstraints):
        localStack = []
        ifConstraints = []
        for _ in range(num_combinations):
            localStack.append(self.stack.pop())
            if ifconstraints:
                ifConstraints.append(ifconstraints.pop())
            else:
                ifConstraints = []
        localStack.reverse()
        ifConstraints.reverse()
        condList = []
        for _ in range(num_combinations):
            currExpr = localStack.pop(0)
            if ifConstraints:
                currIfConstraint = ifConstraints.pop(0)
            else:
                currIfConstraint = None
            if quantifier == "Some":
                cond = False
                for i in currExpr:
                    for j in i.getInstanceSorts():
                        (sort, mask) = j
                        for k in mask.keys():
                            cond = mOr(cond, mask.get(k) != sort.parentInstances)
                condList.append(cond)
            elif quantifier == "All":
                cond = []
                for i in currExpr:
                    for j in i.getInstanceSorts():
                        (sort, mask) = j
                        for k in mask.keys():
                            if isinstance(sort,basestring) and sort == "bool":
                                cond.append(mask.get(k))
                            else:
                                cond.append(mask.get(k) != sort.parentInstances)
                cond = And(*cond)
                if currIfConstraint:
                    cond = Implies(currIfConstraint, cond)
                condList.append(cond)
            elif quantifier == "No":
                cond = []
                for i in currExpr:
                    for j in i.getInstanceSorts():
                        (sort, mask) = j
                        for k in mask.keys():
                            if isinstance(sort,basestring) and sort == "bool":
                                cond.append(mask.get(k))
                            else:
                                cond.append(mask.get(k) != sort.parentInstances)
                cond = Not(Or(*cond))
                if currIfConstraint:
                    cond = Implies(currIfConstraint, cond)
                condList.append(cond)
            else:
                sys.exit("lone and one still unimplemented")
        self.stack.append([BoolArg([And(*condList)])])
           
    def extend(self, args):
        maxInstances = 0
        extendedArgs = []
        for i in args:
            maxInstances = max(maxInstances, len(i))
        for i in args:
            if len(i) != maxInstances:
                extendedArgs.append([i[0].clone() for _ in range(maxInstances)])
            else:
                extendedArgs.append(i)
        return (maxInstances, extendedArgs)
                
    def addOperator(self, operation):
        (arity, operator) = getOperationConversion(operation)
        args = []
        for _ in range(0,arity):
            args.insert(0, self.stack.pop())
        (maxInstances, extendedArgs) = self.extend(args)
        finalExprs = []
        for i in range(maxInstances):
            tempExprs = []
            for j in extendedArgs:
                tempExprs.append(j[i])
            finalExprs.append(tempExprs)
        finalExprs = [operator(*finalExprs[i]) for i in range(len(finalExprs))]
        self.stack.append(finalExprs)
    
    def endProcessing(self):
        self.value = self.stack.pop()
        expr = self.value
        if(self.claferStack):
            thisClafer = self.claferStack[-1]
            for i in range(thisClafer.numInstances):
                if thisClafer.numInstances == len(expr):
                    self.addConstraint(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr[i].finish()))
                #hack for now
                else:
                    self.addConstraint(Implies(thisClafer.instances[i] != thisClafer.parentInstances, expr[0].finish()))
        else:
            for i in expr:
                for j in i.getInstanceSorts():
                    (_, mask) = j
                    self.addConstraint(mask.pop_value())
        self.z3.z3_bracketed_constraints.append(self)
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self.value)