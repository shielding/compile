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
                    star = 0
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
    
    
        