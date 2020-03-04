#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 02:58:44 2020

@author: mohamed
"""

class Player:
    def __init__(self, name):
        
        self.name = name
        self.balance = 0
        
    def decision(self):
        print(self.name + "'s turn ! Put 1 if you want to share. Otherwise put 0.")
        choice = int(input())
        
        return choice == 1
        

class state :
    def __init__(self, cr, mar, mir,ng):
        self.collective_reward = cr
        self.maximum_reward = mar
        self.minumum_reward = mir
        #self.num_of_players = np
        self.isEnd = False
        self.player1 = Player("p1")
        self.player2 = Player("p2")
        self.numofgames = ng
        
        
        
    def play(self):
        
        
        for i in range(self.numofgames):
            decision1 = self.player1.decision()
            decision2 = self.player2.decision()
            
            if decision1 and decision2:
                self.player1.balance += self.collective_reward
                self.player2.balance += self.collective_reward
                
            elif decision1:
                self.player2.balance += self.maximum_reward
                
            elif decision2:
                self.player1.balance += self.maximum_reward
            
            else :
                self.player1.balance += self.minumum_reward
                self.player2.balance += self.minumum_reward
                
