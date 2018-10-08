#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shielding
"""

from NFA import *

char = ['a','b']

class Subset:
    sub_ID = 0
    def __init__(self,nodes):
        self.nodes = nodes
        self.already = 0
        self.id = Subset.sub_ID
        Subset.sub_ID += 1

class DFA:   
    def __init__(self, nfa):
        self.nfa = nfa.graph
        # self.total = 0
        self.subsets = []
        self.graph = []
        self.accept = []
        self.no = []
    
    def eclosure(self,nodes): # nodes为列表 函数返回对应闭包所在子集状态的id
        if nodes == []:
            return -1
        nodes.sort()
        for node in nodes:    
            for n in self.nfa:
                if n.ID == node and n.input == '-' and n.next_ID not in nodes:
                    nodes.append(n.next_ID)
                    # nodes.sort()
                    # print(n.next_ID)
        nodes.sort()
        f = 0 
        for n in self.subsets: # 已有该子集状态，直接返回子集状态的id
            if nodes == n.nodes:
                f = 1
                return n
        if f == 0:
            sub = Subset(nodes) # 创建新的子集状态
            self.subsets.append(sub)
            if 1 in nodes:
                self.accept.append(sub.id)
            else:
                self.no.append(sub.id)
            return sub              
   
    def move(self,nodes,i):
        aims = []
        for node in nodes: 
            for n in self.nfa:
                if n.ID == node and n.input == i:
                    aims.append(n.next_ID)
        return list(set(aims)) # 去重
        
    def determinate(self):
        self.subsets.append(self.eclosure([0]))
        for i in self.subsets:
            if i.already == 1:
                continue
            i.already = 1
            for c in char:
                if not self.eclosure(self.move(i.nodes,c)) == -1:
                    self.graph.append(Connect(i.id,c,self.eclosure(self.move(i.nodes,c)).id))
                    print(i.id,c,self.eclosure(self.move(i.nodes,c)).id,self.eclosure(self.move(i.nodes,c)).nodes)
                else:
                    continue
        
    def printDFA(self):
        for g in self.graph:
            p = "%d--[%s]-- %d" % (g.ID,g.input,g.next_ID)
            print(p)
            
    # def printAccept(self):
        # for a in self.accept:
           #  print(a)
        
    
if __name__ == "__main__":
    s = 'ab*(a*|(ab)*|b)*b'
    nfa = NFA(s+')')
    nfa.convert()
    nfa.printNFA()
    dfa = DFA(nfa)
    dfa.determinate()
    # dfa.printDFA()
    # dfa.printAccept()
        
