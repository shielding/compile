#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shielding
"""

from DFA import *

class MINI:
    def __init__(self,dfa):
        self.dfa = dfa.graph
        # self.graph = []
        self.accept = dfa.accept
        self.no = dfa.no
    def move(self,node,i):        
        aims = []
        for n in self.dfa:
            if n.ID == node and n.input == i:
                aims.append(n.next_ID)
        return list(set(aims))
    def substitute(self,n1,n2):
        for n in self.dfa:
            if n.ID == n1:
                n.ID = n2
            if n.next_ID == n1:
                n.next_ID = n2
    def minimize(self,nodes):
        nodes.sort()
        need = 0
        for n1 in nodes:
            for n2 in nodes:
                if n1 >= n2:
                    continue
                else:
                    flag = 1 
                    for c in char:
                        if not self.move(n1,c) == self.move(n2,c):
                            flag = 0
                            break
                    if flag == 1:
                        need = 1
                        print(n1,n2)
                        self.substitute(n2,n1)
                        nodes.remove(n2)
                        nodes.sort()
        return need
    def printMINI(self):
        for g in self.dfa:
            p = "%d--[%s]-- %d" % (g.ID,g.input,g.next_ID)
            print(p)
                        
if __name__ == "__main__":
    s = 'ab*(a*|(ab)*|b)*b'
    nfa = NFA(s+')')
    nfa.convert()
    print("NFA:")
    nfa.printNFA()
    dfa = DFA(nfa)
    print("DFA:")
    dfa.determinate()
    # dfa.printAccept()
    mini = MINI(dfa)
    if mini.minimize(mini.accept)==1 or mini.minimize(mini.no)==1:
        mini.printMINI()
    else:
        print("DFA无需最小化")
                        

