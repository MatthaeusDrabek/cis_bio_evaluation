#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:00:20 2019

@author: drabek
"""

import xlsxwriter																	# module for writing excel sheet
import numpy as np
import argparse
import Plot
import Well
import Molecule
import Write_Output
import Read_Data
import pandas as pd
####################################################################################################
class CisBio_Gq():
	################################################################################################
	def __init__(self, output_name, read_input, names_of_molecules, mode_choice, number_of_replica, number_of_concentrations, data_frame_keys):
	################################################################################################
		self.Output_Name = output_name
		self.Read_Input = read_input
		self.Well_Object_List = []
		self.Name_Of_Molecule_List = names_of_molecules
		self.Experiment_Molecule_List = []
		self.Number_Of_Molecules = len(names_of_molecules)
		self.Workbook = 'default'
		self.Worksheet = []
		self.Choice = mode_choice
		self.Number_Of_Concentrations = number_of_concentrations
		self.Concentrations_Agonist_10 = [-10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, 'pos', 'neg']
		self.Concentrations_Agonist_10_comp = [-10.15, -9.15, -8.15, -7.15, -6.15, -5.15, -4.15, -3.15, 'pos', 'neg']
		self.Data_Frame_Keys = data_frame_keys
		self.Concentration = []
		self.Number_Of_Replica = number_of_replica
	################################################################################################
	def Call_Read_Data_File(self):
	################################################################################################
		self.Read_Input = Read_Data.CisBio_Read_Data_File(self.Read_Input,self.Number_Of_Molecules,self.Number_Of_Replica)
		self.Read_Input.Read_Data_665nm_620nm()
		if args.verbose:
			print('665nm Data: {}'.format(self.Read_Input.Output_Data_665nm))
			print('620nm Data: {}'.format(self.Read_Input.Output_Data_620nm))
		print('Finished Reading the Input File')
		return()
	################################################################################################
	def Call_Concentrations(self):
		if self.Choice == 'ago':
			if self.Number_Of_Concentrations == 10:
				self.Concentration = self.Concentrations_Agonist_10
		elif self.Choice == 'agoc':
			if self.Number_Of_Concentrations == 10:
				self.Concentration = self.Concentrations_Agonist_10_comp
		return()
	################################################################################################
	def Call_Well(self):
	################################################################################################
		for i in range(len(self.Concentration)*self.Number_Of_Replica*self.Number_Of_Molecules):
			well_object = Well.CisBio_Well(self.Read_Input.Output_Data_665nm[i],self.Read_Input.Output_Data_620nm[i])
			well_object.calc_ratio()
			self.Well_Object_List.append(well_object)
		print('Finished building Well Objects')
		return()
	################################################################################################
	def Call_Molecule(self):
	################################################################################################
		for i in range(self.Number_Of_Molecules):
			molecule_object = Molecule.CisBio_Molecule(self.Well_Object_List,len(self.Concentration), self.Number_Of_Replica,self.Name_Of_Molecule_List[i],i)
			molecule_object.make_molecule_list()
			molecule_object.make_average_and_stdev()
			delattr(molecule_object, 'Well')
			self.Experiment_Molecule_List.append(molecule_object)
			if args.verbose:
				print('{} {}'.format(self.Experiment_Molecule_List[i].Name_Of_Molecule,self.Experiment_Molecule_List[i].Average_Data_Points))
		print('Finished building Molecule Objects')
		return()
	################################################################################################
	def Call_Normal_Molecule(self):
	################################################################################################
		for i in range(len(self.Experiment_Molecule_List)):
			self.Experiment_Molecule_List[i].normalize_data_one(self.Experiment_Molecule_List[0],args.verbose)
		return()	
	################################################################################################
	def Call_Output(self):
	################################################################################################
		self.Workbook = xlsxwriter.Workbook('{}.xlsx'.format(self.Output_Name))
		for i in range(self.Number_Of_Molecules):
			self.Worksheet.append(self.Workbook.add_worksheet(self.Name_Of_Molecule_List[i]))
			cell_format_1 = self.Workbook.add_format({'bold': True, 'font_size': 20, 'align' : 'center', 'valign' : 'vcenter'})
			cell_format_2 = self.Workbook.add_format({'bold': True, 'font_size': 14, 'align' : 'center', 'valign' : 'vcenter'})
		Output_output = Write_Output.CisBio_Output(self.Experiment_Molecule_List, self.Number_Of_Molecules, self.Concentration).Generate_Output\
		(self.Worksheet, cell_format_1, cell_format_2)
		self.Workbook.close()
		return()
	################################################################################################
	def Call_Output_Pandas(self):
		self.Workbook = pd.ExcelWriter('{}'.format(self.Output_Name))
		for i in range(self.Number_Of_Molecules):
			print(i)
			data_frame = Write_Output.CisBio_Output(self.Experiment_Molecule_List, self.Number_Of_Molecules, self.Concentration,self.Data_Frame_Keys).Generate_Output_Pandas(self.Data_Frame_Keys, i)
			data_frame.to_excel(self.Workbook,self.Name_Of_Molecule_List[i])
		self.Workbook.save()
		return()
	################################################################################################
	def Call_Plot(self):
	################################################################################################
		print(args.date)
		test = Plot.Assay_Plots(self.Concentration, self.Experiment_Molecule_List, args.plot, args.mode_choice, args.date)
		x_data_points = []
		for i in range(len(self.Concentration)):
			if type(self.Concentration[i]) == float:
				x_data_points.append(self.Concentration[i])
		x_data_points = np.array(x_data_points)
		test.Hill_fit(x_data_points)
		return()
	################################################################################################
class LoadFromFile(argparse.Action):
	def __call__ (self, parser, namespace, values, option_string = None):
		with values as f:
			parser.parse_args(f.read().split(), namespace)
		return()
	################################################################################################
 ### define Argeparse ##############################################################################
parser = argparse.ArgumentParser(description='Evaluating Cis Bio Gq Raw Data')
####################################################################################################
parser.add_argument('--output', '-o', type = str, dest = 'output_name', help = 'name of the output')
parser.add_argument('--input', '-i', type = str, dest = 'read_input', help = 'name of the input file, needs to be in the same folder')
parser.add_argument('--name_mol', '-nam', nargs='+', dest = 'names_of_molecules', help = 'a list of names of the molecules, sequence needs to be correct')
parser.add_argument('--conc', '-c', dest = 'mode_choice', type = str, choices = ['ago', 'agoc'], help = 'choose between agonist or agonist competition assay')
parser.add_argument('--numb_repli', '-nr', type = int, dest = 'number_of_replica', help = 'number of replica')
parser.add_argument('--num_conc','-nc', dest ='number_of_concentrations', type=int, choices=[10,11], help='number of concentrations used in the assay')
parser.add_argument('--upd', '-u', dest = 'update', action = 'store_false', default = True, help =' Updating or not making a summary excel file')
parser.add_argument('--plot', '-p', dest = 'plot', default = False, action = 'store_true', help = 'Set True for Plotting')
parser.add_argument('--parameter', '-param', dest ='parameter_list', action = LoadFromFile, type = open, help = 'Parameter File')
parser.add_argument('--date', '-d', dest = 'date', type = str, help = 'Date of Experiment')
parser.add_argument('--data_keys', '-k', dest = 'data_frame_keys', nargs='+', help = 'The Headers of the Output Excel File')
parser.add_argument('--verbose', '-v', dest = 'verbose', action = 'store_true', default = False, help = 'Write a lot of Data')
####################################################################################################
args = parser.parse_args()
####################################################################################################
if __name__ == '__main__':
	test = CisBio_Gq(args.output_name, args.read_input, args.names_of_molecules, args.mode_choice, args.number_of_replica, args.number_of_concentrations, args.data_frame_keys)
	test.Call_Concentrations()
	test.Call_Read_Data_File()
	test.Call_Well()
	test.Call_Molecule()
	test.Call_Normal_Molecule()
	if args.update:
		test.Call_Output_Pandas()
	test.Call_Plot()
 ####################################################################################################
