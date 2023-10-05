#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:24:57 2019

@author: drabek
"""
##################################################################################################################################
class CisBio_Well():#uses the data point in read input file and make seperate well objects containing its points and ratio
	def __init__(self, data_665nm, data_620nm):
		self.Data_665nm = data_665nm #data point of 665nm from the reading object
		self.Data_620nm = data_620nm #data point of 620nm from the reading object
		self.Ratio_Data = 0 #calculated ratio, default is zero 
	def calc_ratio(self): # function for calculation the ratio
		self.Ratio_Data = (self.Data_665nm/self.Data_620nm)*10000 # ratio function
		return()
##################################################################################################################################