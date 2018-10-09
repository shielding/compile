#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shielding
"""

class Connect:
    def __init__(self,ID,i,next_ID):
        self.ID = ID
        self.input = i
        self.next_ID = next_ID

class NFA:
   
    def __init__(self,string):
        self.string =  string
        self.graph = []
        self.total = 0
   
    def convert(self):
        ch = 'a' # 前一个处理的字母
        status = 0
        start =[0]
        end = [1]
        near_or = [] #记录“|”之前的状态
        or_num = 0 # #记录“|”的个数
        right = 0 # 右括号
        status_pre = 0
        total = 1
        l = len(self.string)
        yes = 0 # 前一个是不是字母
        l_now = 0
        lc = 1 # 记录左括号前的第一个状态
        for c in self.string:
            l_now += 1 
            if not c == '*' and right:
                self.graph.append(Connect(status,'-',end[len(end)-1]))
                status = end[len(end)-1]
                # print(status)
            if c == '(':
                if yes:
                    self.graph.append(Connect(status_pre,ch,status))
                yes = 0
                right = 0
                lc = status
                status_pre = status
                total += 1
                status = total
                start.append(status)
                self.graph.append(Connect(status_pre,'-',status))
                total += 1
                end.append(total) 
            elif c == '*':
                yes = 0
                if right:
                    self.graph.append(Connect(status_pre,ch,status))
                    s = start.pop()
                    e = end.pop()
                    self.graph.append(Connect(status,'-',s))    
                    self.graph.append(Connect(status,'-',e))
                    self.graph.append(Connect(lc,'-',e))
                    while not len(near_or) == 0:
                        i = near_or.pop()
                        self.graph.append(Connect(i,'-',s))
                    status = e
                else:
                    self.graph.append(Connect(status_pre,'-',status))
                    tmp = status
                    total += 1
                    status = total
                    self.graph.append(Connect(status_pre,'-',status))
                    total += 1
                    status = total
                    self.graph.append(Connect(status,'-',status-1))
                    self.graph.append(Connect(status-1,ch,status))
                    self.graph.append(Connect(status,'-',tmp))
                    status = tmp
                right = 0
            elif c == '|':
                near_or.append(status)
                or_num += 1
                if yes:
                    self.graph.append(Connect(status_pre,ch,status))
                yes = 0
                right = 0
                self.graph.append(Connect(status,'-',end[len(end)-1]))
                status = start[len(start)-1]
                # print(status)
            elif c == ')':
                yes = 0
                right = 1
                if l_now == l:
                    self.graph.append(Connect(status_pre,ch,status))
                    self.graph.append(Connect(status,'-',1))
            else:
                right = 0
                if yes:
                    self.graph.append(Connect(status_pre,ch,status))
                ch = c 
                yes = 1
                status_pre = status
                total += 1
                status = total
        self.total = total
            
    def printNFA(self):
        for g in self.graph:
            p = "%2d--[%s]--%2d" % (g.ID,g.input,g.next_ID)
            print(p)
        
            
if __name__ == "__main__":
    s = 'ab*(a*|(ab)*|b)*b'
    nfa = NFA(s+')')
    nfa.convert()
    nfa.printNFA()
    
    
        