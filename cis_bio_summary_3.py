#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:26:38 2019

@author: drabek
"""

import pandas as pd
import argparse
import re
import Plot
import os
from Molecule import CisBio_Molecule_Summary
class CisBio_Summary_Call():
	def __init__(self):
		self.Data_Output = args.output_name
		self.Date = args.date
		self.Mode = args.mode_choice
		self.Concentrations = []
		self.Compound = args.compound
		self.Reference = args.reference
		self.Molecules = []
		self.Reference_Norm_Average = {}
		self.Reference_Norm_Stdev = {}
		self.Norm_Average = {}
		self.Norm_Stdev = {}
####################################################################################################
	def Pattern_Set(self):
		if args.mode_choice in ['ago']:
			r = re.compile('[s\S]ummary_(ago)+_([\w])+.xlsx')
		elif args.mode_choice in ['empty']:
			r = re.compile('[s/S]ummary_(empty)+_(ago)+_([\w])+.xlsx')
		else:
			parser.error('Mode can be these two modes: ago; empty')
		return(r)
##########################################################################
	def Make_Dataframes(self, data_folder, write_output, summary_file, r):
		summary_file_match = re.match(r, summary_file)
		read_input = pd.ExcelFile('{}/summary/{}'.format(data_folder,\
						 summary_file_match.group()))
		if '{}'.format(self.Compound) in read_input.sheet_names:
			try:
				print('read_input: {}'.format(read_input.sheet_names))
				for concentration_keys in read_input.parse(self.Reference)['Concentrations']:
					if not concentration_keys in self.Concentrations:
						self.Concentrations.append(concentration_keys)
						self.Reference_Norm_Average[concentration_keys]= []
						self.Reference_Norm_Stdev[concentration_keys] = []
						self.Norm_Average[concentration_keys]= []
						self.Norm_Stdev[concentration_keys] = []
				for concentration_keys in read_input.parse(self.Compound)['Concentrations']:
					if not concentration_keys in self.Concentrations:
						self.Concentrations.append(concentration_keys)
						self.Norm_Average[concentration_keys]= []
						self.Norm_Stdev[concentration_keys] = []
			except:
				print('Error')
				pass
			data_frame = pd.DataFrame(read_input.parse(self.Reference, index_col = 0))
			for value in data_frame['Concentrations']:
				row_number = data_frame.index[data_frame.Concentrations == value]
				self.Reference_Norm_Average[value].append(data_frame.at[row_number[0],'Normalized_Average'])
				self.Reference_Norm_Stdev[value].append(data_frame.at[row_number[0],'Normalized_StDev'])
			data_frame.to_excel(write_output, sheet_name = '{} {}'.format(self.Reference, data_folder))
			data_frame = pd.DataFrame(read_input.parse(self.Compound,index_col = 0))
			for value in data_frame['Concentrations']:
				row_number = data_frame.index[data_frame.Concentrations == value]
				self.Norm_Average[value].append(data_frame.at[row_number[0],'Normalized_Average'])
				self.Norm_Stdev[value].append(data_frame.at[row_number[0],'Normalized_StDev'])
			data_frame.to_excel(write_output, sheet_name = '{} {}'.format(self.Compound, data_folder))

		else:
			print('In {}/summary/{}: {} has not been found'.format(data_folder,\
		   summary_file_match.group(), self.Compound))
		read_input.close()
		return(None)
########################################################
	def Call_Summary_Molecule(self,r):
		write_output = pd.ExcelWriter(self.Data_Output)
		print('Exclude following Data Directories: {}'.format(args.exclude))
		for data_folder in os.listdir(os.getcwd()):# search for all dated measurements
			print('Searching in {}'.format(data_folder))
			if not data_folder in args.exclude:
				try:
					for summary_file in os.listdir('{}/summary/'.format(data_folder)):
						try:
							print(summary_file)
							if re.match(r, summary_file):
								self.Make_Dataframes(data_folder, write_output, summary_file, r)
							if re.match('[s\S]ummary_(agoH)+_([\w])+.xlsx', summary_file) and self.Mode == 'agoH':
								self.Make_Dataframes(data_folder, write_output, summary_file, '[s\S]ummary_(agoH)+_([\w])+.xlsx')
							if re.match('[s/S]ummary_(empty)+_(agoH)+_([\w])+.xlsx', summary_file) and self.Mode == 'emptyH':
								print('hello')
								self.Make_Dataframes(data_folder, write_output, summary_file, '[s/S]ummary_(empty)+_(agoH)+_([\w])+.xlsx')
						except:
							pass
				except NotADirectoryError:
					pass
					print('{} is not a directory'.format(data_folder))
				except FileNotFoundError:
					pass
					print('no summary file found in {}'.format(data_folder))
		reference = CisBio_Molecule_Summary(self.Reference,self.Reference_Norm_Average,self.Reference_Norm_Stdev)
		reference.normalize_data_all(args.verbose)
		compound = CisBio_Molecule_Summary(self.Compound,self.Norm_Average,self.Norm_Stdev)
		compound.normalize_data_all(args.verbose)
		data_frame = pd.DataFrame({'{} Average Norm'.format(self.Reference): reference.Average_Data_Points_Norm_All,'{} StDev Norm'.format(self.Reference):\
							  reference.Stdev_Data_Points_Norm_All,'{} StError Norm'.format(self.Reference):reference.StError_Data_Points_Norm_All,\
							  '{} Average Norm'.format(self.Compound): compound.Average_Data_Points_Norm_All,'{} StDev Norm'\
							  .format(self.Compound): compound.Stdev_Data_Points_Norm_All, '{} StError Norm'.format(self.Compound):compound.StError_Data_Points_Norm_All})
		
		self.Concentrations = pd.DataFrame({'Concentrations':self.Concentrations})
		data_frame.to_excel(write_output, sheet_name = 'Summary of {}'.format(self.Compound))
		self.Molecules = data_frame
		print(self.Molecules)
		write_output.save()
		return()
####################################################################################################
	def Call_Plot(self):
		Plot.Assay_Plots(self.Concentrations, self.Molecules, args.plot, args.mode_choice, args.date).Hill_Fit_Pandas(self.Reference, self.Compound, \
				  args.mode_choice, args.tp_pred, args.error)
		return()
####################################################################################################
class LoadFromFile(argparse.Action):
	def __call__ (self, parser, namespace, values, option_string = None):
		with values as f:
			parser.parse_args(f.read().split(), namespace)
		return()
	################################################################################################
 ### define Argeparse ##############################################################################
parser = argparse.ArgumentParser(description='Summaries Data Points of the wanted Compound')
####################################################################################################
parser.add_argument('--output', '-o', type = str, dest = 'output_name', help = 'name of the output')
parser.add_argument('--conc', '-c', dest = 'mode_choice', type = str, choices = ['ago', 'empty'], help = 'choose between agonist or \
					antagonist assay')
parser.add_argument('--turningpoint', '-tp', type = float, dest = 'tp_pred', default = -7.5, help = 'Starting Point of the IC/EC50 default= 7.5')
parser.add_argument('--compound', '-com', dest = 'compound', type = str, help = 'Compound name; should be the same name in the sheets')
parser.add_argument('--reference', '-ref', dest = 'reference', type = str, help = 'Reference name, should be the same name in the sheets')
parser.add_argument('--plot', '-p', dest = 'plot', default = False, action = 'store_true', help = 'Set True for Plotting')
parser.add_argument('--parameter', '-param', dest ='parameter_list', action = LoadFromFile, type = open, help = 'Parameter File')
parser.add_argument('--date', '-d', dest = 'date', type = str, help = 'Date of of the Summary')
parser.add_argument('--verbose', '-v', dest = 'verbose', action = 'store_true', default = False, help = 'Write a lot of Data')
parser.add_argument('--exclude', '-e', dest = 'exclude', nargs='+',default = [], help = 'List of data folders to exclude from the summary')
parser.add_argument('--error', '-er', dest = 'error', choices = ['StError', 'StDev'], default = 'StError', help = 'Error')
############################################################################################################################################
args = parser.parse_args()
test = CisBio_Summary_Call()
test.Call_Summary_Molecule(test.Pattern_Set())
test.Call_Plot()