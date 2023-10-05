#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:54:11 2019

@author: drabek
"""
##################################################################################################################################
class CisBio_Molecule():#Summary of Wells, take the well objects into a list, and oragnize these objects to their respective molecule name
##################################################################################################################################
	def __init__(self, well_object, number_of_concentrations, number_of_replica, name_of_molecule, molecule_number):
	#########################################################################
		self.Well = well_object #here the list of well object is piped into this class, later it gets deleted because it is not needed anymore
		self.Number_Of_Concentrations = number_of_concentrations #number of concentrations measured, even positiv/negativ control
		self.Number_Of_Replica = number_of_replica#number of replica measured for each molecule 
		self.Name_Of_Molecule = name_of_molecule#name of the molecule
		self.Molecule_Number = molecule_number#iterated number; each molecule gets a index number for finding the correct wells 
		self.Molecule_Data_List = [] #a list of the well objects containing only the well object of the specific molecule
		self.Average_Data_Points = [] #average points calculated of all ratio points of each well object
		self.Stdev_Data_Points = [] #calculated standard dev for each average point
		self.Normalized_Y_Data = 0
		self.Normalized_Stdev_Data = 0
	#########################################################################
	def make_molecule_list(self): # function for finding all correct well object for the molecule
	#########################################################################
		for i in range(self.Molecule_Number*self.Number_Of_Replica*self.Number_Of_Concentrations,(self.Molecule_Number+1)*self.Number_Of_Replica*self.Number_Of_Concentrations):
			self.Molecule_Data_List.append(self.Well[i]) #iterate through a range of numbers defined by the index_molecule_number. replica, and concentrations.
		return()
	#########################################################################
	def make_average_and_stdev(self): #calculating the average and the standard dev
	#########################################################################
		for i in range(self.Number_Of_Concentrations): #iterate through all concentrations
			average = (self.Molecule_Data_List[i].Ratio_Data + self.Molecule_Data_List[i+self.Number_Of_Concentrations].Ratio_Data) / self.Number_Of_Replica #function for calculating the average
			self.Average_Data_Points.append(average)
			self.Stdev_Data_Points.append((((((self.Molecule_Data_List[i].Ratio_Data - average)**2)+(self.Molecule_Data_List[i+self.Number_Of_Concentrations].Ratio_Data - average)**2))**0.5))#function for calculating the standard dev#save the standard dev points 
		return()
	#########################################################################
	#########################################################################
	def normalize_data_one(self, Reference, verbose):
	#########################################################################
		try:
			self.Normalized_Y_Data = [(x/max(Reference.Average_Data_Points[0:-3]))*100 for x in self.Average_Data_Points]
			self.Normalized_Stdev_Data = [self.Normalized_Y_Data[i]*(((self.Stdev_Data_Points[i]/self.Average_Data_Points[i])**2 +\
			(Reference.Stdev_Data_Points[Reference.Average_Data_Points.index(max(Reference.Average_Data_Points[0:-3]))]/Reference.Average_Data_Points[Reference.Average_Data_Points.index(max(Reference.Average_Data_Points[0:-3]))])**2)**0.5) for i in range(len(self.Average_Data_Points))]
			if verbose:
				print('Normalized Y_Data of {}: {}'.format(self. Name_Of_Molecule, self.Normalized_Y_Data))
				print('Normalized Stdev Data of {}: {}'.format(self.Name_Of_Molecule, self.Normalized_Stdev_Data))
		except:
			pass
		return()
####################################################################################################
class CisBio_Molecule_Summary():
####################################################################################################
	def __init__(self, name, average_data_points_norm, stdev_data_points_norm ):
		self.Name_Of_Molecule = name#name of the molecule; string
		self.Average_Data_Points_Norm = average_data_points_norm#Average Data Lists of the included Measurements Normalized
		self.Stdev_Data_Points_Norm = stdev_data_points_norm#Standard Deviation Lists of the included Measurements Normalized
		self.Average_Data_Points_Norm_All = {}#Normalized Average Data of the Compound of all measurements
		self.Stdev_Data_Points_Norm_All = {}#Normalized Standard Deviations of the Compound of all measurements
		self.StError_Data_Points_Norm_All = {}
	################################################################################################
	def normalize_data_all(self, verbose):
	################################################################################################
		for key in self.Average_Data_Points_Norm.keys():
			if not len(self.Average_Data_Points_Norm[key]) == 0:
				self.Average_Data_Points_Norm_All[key] =sum(self.Average_Data_Points_Norm[key])/len(self.Average_Data_Points_Norm[key])
				self.Stdev_Data_Points_Norm_All[key] = sum(self.Stdev_Data_Points_Norm[key])/len(self.Stdev_Data_Points_Norm[key])
				self.StError_Data_Points_Norm_All[key] = (self.Stdev_Data_Points_Norm_All[key]/(len(self.Stdev_Data_Points_Norm[key])*2)**0.5)
		return()
	#########################################################################