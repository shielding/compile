#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shielding
"""

# 简要分析：
# 正则式转NFA：
# 设置两个栈start和end，分别表示每对括号的开始和结束状态，默认整个正则表达式外也有一对括号
# 设置一个bool变量right标记前一个读入字符是否为右括号
# 1. 开始时，start和end各添加一个状态
# 2. 遇到“(”，end添加一个状态
# 3. 遇到“*”，如果之前为右括号，则弹出一对start和end，增加两个新节点，在两状态间添加空边；否则一对start和end用前两个状态替换
# 4. 遇到”|“，将当前状态与最后一个入栈end的状态相连，当前状态变为最后一个入栈start的状态
# 5. 遇到“）”，end弹出最后一个入栈的状态与当前状态相连，

# NFA转DFA：
# e-closure和move创建NFA状态合集的子集

# DFA化简：
# 是否都是终态或都不是终态、是否等价
# 分割法


class Node:
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
        right = 0 # 右括号
        status_pre = 0
        total = 1
        yes = 0 # 前一个是不是字母
        for c in self.string:
            if not c == '*' and yes:
                self.graph.append(Node(status_pre,c,status))
            if not c == '*' and right:
                self.graph.append(Node(status,'-',end[len(end)-1]))
                status = end[len(end)-1]
                # print(status)
            if c == '(':
                start.append(status)
                total += 1
                end.append(total) 
            elif c == '*':
                if right:
                    total += 1
                    status = total
                    s = start.pop()
                    e = end.pop()
                    # self.graph.remove(Node(s,rem[0],rem[1]))
                    self.graph.append(Node(s,'-',e))
                    self.graph.append(Node(s,'-',status))
                    total += 1
                    status = total
                    # self.graph.remove(Node(rem1[1],rem1[0],e))
                    self.graph.append(Node(status,'-',status-1))
                    self.graph.append(Node(status,'-',e))
                else:
                    # self.graph.remove(Node(status_pre,ch,status))
                    self.graph.append(Node(status_pre,'-',status))
                    tmp = status
                    total += 1
                    status = total
                    self.graph.append(Node(status_pre,'-',status))
                    total += 1
                    status = total
                    self.graph.append(Node(status,'-',status-1))
                    self.graph.append(Node(status,'-',tmp))
            elif c == '|':
                self.graph.append(Node(status,'-',end[len(end)-1]))
                status = start[len(start)-1]
                # print(status)
            elif c == ')':
                right = 1
            else:
                ch = c 
                yes = 1
                status_pre = status
                total += 1
                status = total
        self.total = total
            
    def printNFA(self):
        for g in self.graph:
            p = "%d--[%s]--%d" % (g.ID,g.input,g.next_ID)
            print(p)
        
            
if __name__ == "__main__":
    s = 'ab*(a*|(ab)*|b)*b'
    nfa = NFA(s+')')
    nfa.convert()
    nfa.printNFA()
    
    
        