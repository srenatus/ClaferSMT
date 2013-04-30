'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class ClaferId(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, moduleName, my_id, isTop):
        self.moduleName = moduleName
        self.id = my_id
        self.isTop = isTop
        
        
    def __str__(self):
        return self.id
    
    def toString(self, level):
        print('\t' * level + "A")