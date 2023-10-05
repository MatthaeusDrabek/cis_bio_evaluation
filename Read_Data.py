#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:09:05 2019

@author: drabek
"""
##################################################################################################################################
import xlrd
import pandas as pd
import re
############################################################
class CisBio_Read_Data_File():#Read Input File for getting the data in list, 665nm and 620 nm 
	'''
	- Module for Reading Raw Data of Tecan Spark 20M for Cis Bio Funtionality Assay
	- Part of a Package
	- Two Functions implemented: 
	- Read_Data_665nm_620nm reads the raw file and implemente the information in its parameters.
	- The second Read_Data_665nm_620nm_Pandas is not implemented yet, the idea is to read the
		raw file into a pandas framework
	'''
	###########################################################
	def __init__(self, input_data, number_of_compounds, number_of_replica):
		self.Input_Data = input_data#Name of the Input File, Gets open as Excel
		self.Number_of_Compounds = number_of_compounds#Needed for the sum of data points
		self.Number_of_Replica = number_of_replica#Needed for the sum of data points
		self.Output_Data_665nm = []#the output of the 665nm data is saved 
		self.Output_Data_620nm = []#the output of the 620nm data is saved
	################################################################################################
	def Read_Data_665nm_620nm(self):#Read the input file and get the Data_665/620nm in a list
		book = xlrd.open_workbook(self.Input_Data)#creating a book environment
		first_sheet = book.sheet_by_index(0)#create a sheet environment
		row_num = 0#number of the row
		stop_timer = 0#counter for counting <>
		data_find = first_sheet.col_slice(colx=0, start_rowx=0)#slice data to the first column
		for identifier in data_find:#iterate through the items in the first column
			if identifier.value == '<>':# search for <>
				row_data = row_num + 1#because the data is saved one row later, I add one value to 
				#the counted
				if stop_timer == 1:#A counter for getting the second Table with Data, because the first 
					#one is not the data
					for counter in range(self.Number_of_Compounds*self.Number_of_Replica):#all data 
						#from the second table 665nm
						for item in first_sheet.row_values(row_data+counter):#get the floats from each row
							if type(item) is float:#check if the value is a float 
								self.Output_Data_665nm.append(item)#write it into this list parameter
				if stop_timer == 2:#A counter for getting the third table with 620nm Data
					for counter in range(self.Number_of_Compounds*self.Number_of_Replica):#see above
						for item in first_sheet.row_values(row_data+counter):#see for 665nm
							if type(item) is float:#see above
								self.Output_Data_620nm.append(item)#write data in 620nm
				stop_timer +=1#count up if <> is found
			row_num+=1#count the row number up
		return()
	################################################################################################
	def Read_Data_665nm_620nm_Pandas(self):
		book = pd.ExcelFile(self.Input_Data)
		for rows in book.parse(0).rows:
			print(rows)
		return()
############################################################
class Column_Data_Read(): 
	'''
	Class for Reading Data for a column plot
	'''
	##########################################################
	def __init__(self):
		self.X_Data = []#Read 4. Column for XData
		self.Y_Data = []#Read 1. Column for YData
		self.Y_StDev = []#Read 2.Column for StDev
		self.Y_StMean = []#Read 3. Column for StMean
		self.Name = []#Name for the Data
		self.X_Label = 'xlabel'#XLabel Name
		self.Y_Label = 'ylabel'#YLabel Name
	##########################################################
	def Read_Data_Excel(self, input_1):#Use this if Data is .xslx; not yet finished
		book = xlrd.open_workbook(self.Input_Data)#open the File
		for page in range(book.nsheets()):#
			first_sheet = book.sheet_by_index(page)
			print(first_sheet.get_rows())
		return()
	##########################################################
	def Read_Data_Data(self, input_1):#Read for .dat, .txt 
		r = re.compile(r"[#a-zA-Z]+")
		readinput = open(input_1,'r')#open file
		for line in readinput:#go trough lines
			line = line.rstrip('\n')#strip the \n
			line = line.split('\t')#split the line into a list
			if line:#Check if Line exists
				if not re.match(r, line[0]):#Check Header
					self.X_Data.append(line[-1])
					self.Y_Data.append(float(line[0]))
					self.Y_StDev.append(float(line[1]))
					self.Y_StMean.append(float(line[2]))
				else:
					self.X_Label = line[-1]
					self.Y_Label = line[0]
		self.Name = re.sub('_all', '', input_1.split('.')[0])
		self.Name = re.sub('_',' ',self.Name)
		readinput.close()
		return()
###########################################################
def Read_Data_Data_Infile(self, input_1):#Read for .dat, .txt 
		r = re.compile(r"[#a-zA-Z]+")
		for line in input_1:#go trough lines
			line = line.rstrip('\n')#strip the \n
			line = line.split('\t')#split the line into a list
			if line:#Check if Line exists
				if not re.match(r, line[0]):#Check Header
					self.X_Data.append(line[-1])
					self.Y_Data.append(float(line[0]))
					self.Y_StDev.append(float(line[1]))
					self.Y_StMean.append(float(line[2]))
				else:
					self.X_Label = line[-1]
					self.Y_Label = line[0]
		self.Name = re.sub('_all', '', input_1.split('.')[0])
		self.Name = re.sub('_',' ',self.Name)
		readinput.close()
		return()
###########################################################
class Normal_Read():
	'''
	Plot Class for normal Data Frames, such as *.dat, *.txt, *.xlsx
	'''
	##########################################################
	def __init__(self, x_label, y_label, name = False):
		self.X_Data = [] #List of all the X Data, 1. column
		self.Y_Data = [] #List of all the Y Data, 2.column
		self.Y_StDev = [] #List of StDev
		self.Y_StMean = []#List of StMean
		self.Name = name#Name of the Data
		self.X_Label = x_label#Name of the XLabel
		self.Y_Label = y_label#Name of the YLabel
	##########################################################
	def Read_Data_Panda(self, read_input):
		panda_read = pd.ExcelFile(read_input)
		for sheet_name in panda_read.sheet_names:
			self.X_Label = panda_read.parse(sheet_name).columns[0]
			self.Y_Label = panda_read.parse(sheet_name).columns[1]
			self.Data[sheet_name] = panda_read.parse(sheet_name).values
		return()
	##########################################################
	def Read_Data_Dat(self, input_1, rebose = False):#For Reading Normal .txt, .dat Files
		r = re.compile(r"[#a-zA-Z]+")#Used to check Header
		readinput = open(input_1,'r')#Read File
		for line in readinput:#Iterate Through File
			line = line.rstrip('\n')#Strip \n
			line = line.split()#Split line into List
			if line:#Check if Line exists
				if not re.match(r, line[0]):#Check Header
					self.X_Data.append(float(line[0]))#Write 1. column to XData
					self.Y_Data.append(float(line[1]))#Write 2. column to YData
					if len(line) == 3:#Checks if 3 Items exist per row
						self.Y_StDev.append(float(line[2]))#Write 3. column to YStDev
					if len(line) == 4:#Checks if 4 items exist per row
						self.Y_StDev.append(float(line[2]))#Write 3. column to YStDev
						self.Y_StMean.append(float(line[3]))#Write 4. column to YStMean
		readinput.close()#Close Read Input
		if rebose:
			print('Read_Data')
			print('X_Data: {}'.format(self.X_Data))
			print('Y_Data: {}'.format(self.Y_Data))
			print('Y_StDev: {}'.format(self.Y_StDev))
			print('Y_StMean: {}'.format(self.Y_StMean))
		return()
	##########################################################
