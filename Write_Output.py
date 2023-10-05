#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 15:57:18 2019

@author: drabek
"""
import xlsxwriter																	# module for writing excel sheet?
import pandas as pd
##################################################################################################################################
class CisBio_Output():
##################################################################################################################################
	def __init__(self, molecule_object, number_of_molecules, concentration_list, data_frame_keys):
		#########################################################################
		self.Number_Of_Molecules = number_of_molecules#number of molecules for the output
		self.Concentrations = concentration_list
		self.Molecule = molecule_object# the molecule object is saved here to get all the information for the output
		self.Data_Frame_Keys = data_frame_keys
		#########################################################################
	def Generate_Output(self, worksheet_list, cell_format_1, cell_format_2):
		#########################################################################
		for i in range(self.Number_Of_Molecules):#iterates through the number of molecules, to get a sheet with only one molecule data
			worksheet_list[i].write('A2','Concentration', cell_format_2)#default concetration cell
			worksheet_list[i].merge_range('B1:E1',self.Molecule[i].Name_Of_Molecule, cell_format_1)#default molecule name cell
			worksheet_list[i].write('B2','1. Experiment 665 nm', cell_format_2)#default 
			worksheet_list[i].write('C2','2. Experiment 665 nm', cell_format_2)#default
			worksheet_list[i].write('D2','1. Experiment 620 nm', cell_format_2)#default
			worksheet_list[i].write('E2','2. Experiment 620 nm', cell_format_2)#default
			worksheet_list[i].merge_range(2+len(self.Concentrations), 1, 2+len(self.Concentrations), 2, 'Ratio 1. Experiment', cell_format_2)#default
			worksheet_list[i].merge_range(2+len(self.Concentrations), 3, 2+len(self.Concentrations), 4, 'Ratio 2. Experiment', cell_format_2)#default
			worksheet_list[i].merge_range(2+1+2*(len(self.Concentrations)), 1, 2+1+2*(len(self.Concentrations)),4, 'Average', cell_format_2)#default for the average name
			worksheet_list[i].merge_range(2+1+2*(len(self.Concentrations)), 5, 2+1+2*(len(self.Concentrations)),8, 'Stdev', cell_format_2)
			worksheet_list[i].merge_range(2+2+3*(len(self.Concentrations)), 1, 2+2+3*(len(self.Concentrations)),4, 'Normalized Average', cell_format_2)
			worksheet_list[i].merge_range(2+2+3*(len(self.Concentrations)), 5, 2+2+3*(len(self.Concentrations)),8, 'Normalized Stdev', cell_format_2)
		#########################################################################
			for row in range(2,2+len(self.Concentrations)):#iterate through the number of concentrations
				worksheet_list[i].write(row,0, self.Concentrations[row-2])#write down in the first column the concentrations
				worksheet_list[i].write(row,1, self.Molecule[i].Molecule_Data_List[row-2].Data_665nm) #write down in the second column the datapoints of 665nm
				worksheet_list[i].write(row,2, self.Molecule[i].Molecule_Data_List[(row-2)+len(self.Concentrations)].Data_665nm)#write down in the third column the second datapoints of 665nm
				worksheet_list[i].write(row,3, self.Molecule[i].Molecule_Data_List[row-2].Data_620nm)#write down the in the fourth column the first 620nm datapoints
				worksheet_list[i].write(row,4, self.Molecule[i].Molecule_Data_List[(row-2)+len(self.Concentrations)].Data_620nm)#write down in the fifth column the second 620nm datapoints
				################################################################################################################
				worksheet_list[i].write(row+len(self.Concentrations)+1,0, self.Concentrations[row-2])#write down the concentrations in the first column for the ratio points
				worksheet_list[i].merge_range(row+len(self.Concentrations)+1,1, row+len(self.Concentrations)+1, 2, self.Molecule[i].Molecule_Data_List[row-2].Ratio_Data)#
				worksheet_list[i].merge_range(row+len(self.Concentrations)+1,3, row+len(self.Concentrations)+1, 4, self.Molecule[i].Molecule_Data_List[len(self.Concentrations)+row-2].Ratio_Data)
				################################################################################################################
				worksheet_list[i].write(row+2+2*(len(self.Concentrations)),0, self.Concentrations[row-2])
				worksheet_list[i].merge_range(row+2+2*(len(self.Concentrations)),1, row+2+2*(len(self.Concentrations)),4, self.Molecule[i].Average_Data_Points[row-2])
				worksheet_list[i].merge_range(row+2+2*(len(self.Concentrations)),5, row+2+2*(len(self.Concentrations)),8, self.Molecule[i].Stdev_Data_Points[row-2])
		#########################################################################
				worksheet_list[i].write(row+3+3*(len(self.Concentrations)), 0, self.Concentrations[row-2])
				worksheet_list[i].merge_range(row+3+3*(len(self.Concentrations)), 1, row+3+3*(len(self.Concentrations)), 4, self.Molecule[i].Normalized_Y_Data[row-2])
				worksheet_list[i].merge_range(row+3+3*(len(self.Concentrations)), 5, row+3+3*(len(self.Concentrations)), 8, self.Molecule[i].Normalized_Stdev_Data[row-2])
		return()
		#########################################################################
	#############################################################################
	def Generate_Output_Pandas(self, dkeys, i):
		key_number = 1
		counter = 0
		data_frame_list = []
		data_frame = pd.DataFrame(columns=([x for x in dkeys]))
		data_frame['Concentrations']=self.Concentrations
		for data_frame_value in self.Molecule[i].Molecule_Data_List:
			if not counter == len(self.Concentrations)-1:
				data_frame_list.append(data_frame_value.Data_665nm)
				counter += 1
			else:
				data_frame_list.append(data_frame_value.Data_665nm)
				data_frame.iloc[:,key_number] = data_frame_list
				data_frame_list = []
				key_number +=1
				counter = 0
		for data_frame_value in self.Molecule[i].Molecule_Data_List:
			if not counter == len(self.Concentrations)-1:
				data_frame_list.append(data_frame_value.Data_620nm)
				counter += 1
			else:
				data_frame_list.append(data_frame_value.Data_620nm)
				data_frame.iloc[:,key_number] = data_frame_list
				data_frame_list = []
				key_number +=1
				counter = 0
		for data_frame_value in self.Molecule[i].Molecule_Data_List:
			if not counter == len(self.Concentrations)-1:
				data_frame_list.append(data_frame_value.Ratio_Data)
				counter += 1
			else:
				data_frame_list.append(data_frame_value.Ratio_Data)
				data_frame.iloc[:,key_number] = data_frame_list
				data_frame_list = []
				key_number +=1
				counter = 0
		data_frame.iloc[:,key_number] = self.Molecule[i].Average_Data_Points
		key_number += 1
		data_frame.iloc[:,key_number] = self.Molecule[i].Stdev_Data_Points
		key_number += 1
		data_frame.iloc[:,key_number] = self.Molecule[i].Normalized_Y_Data
		key_number += 1
		data_frame.iloc[:,key_number] = self.Molecule[i].Normalized_Stdev_Data
		key_number += 1
		return(data_frame)
	#############################################################################
	def Generate_Ouput_Summary(self, worksheet_list, cell_format_1, cell_format_2):
		#########################################################################
		return()
	#############################################################################