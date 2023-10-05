#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:55:37 2019

@author: drabek
"""
import numpy as np
from scipy.optimize import curve_fit												# module for nonlinear regression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt_3D
import math
import pandas as pd
import re
import statistics as stat
from matplotlib.lines import Line2D
##################################################################################################################################
class Assay_Plots():
##################################################################################################################################
	def __init__(self, concentrations, molecule_object, plot_true, mode_choice, date):
		self.Concentrations = concentrations
		self.Molecule_Object = molecule_object
		self.Plot_True = plot_true
		self.Mode_Choice = mode_choice
		self.Date = date
	####################################################
	####################################################
	def Hill_function(self, x, minimum, maximum, IC50, d):
		return(minimum + ((maximum - minimum)/(1 + 10**((x-IC50)*d))))
	####################################################
	def Hill_fit(self, x_data_points):
		print('x_data   ' + str(x_data_points))
		for x in range(len(self.Molecule_Object)):
			print('{}'.format(self.Molecule_Object[x].Name_Of_Molecule))
####################################################################################################
			if self.Molecule_Object[x].Name_Of_Molecule == 'Carbachol':#making sure that in ago_high condition Carbachol fitting is done normal condition
				print(x_data_points)
				if not x_data_points[0] == -10 and len(self.Concentrations) == 10: # checking if Carbachol is in high condition
					x_data_points[:] = [i -1 for i in x_data_points]#substracting every float with -1
			y = []#y data
			y_errorbar = []#stdev of y
			for i in range(len(x_data_points)):#building the y data by the length of x data points
				y.append(self.Molecule_Object[x].Average_Data_Points[i])#for each molecule x,y appends all average data points i
				y_errorbar.append(self.Molecule_Object[x].Stdev_Data_Points[i])#for each molecule x, y_errorbar appends all stdev_data_points i
			y = np.array(y)#converting the data list into a numpy array
			if y_errorbar:#checks if stdev exists
				y_errorbar = np.array(y_errorbar)#converting y_errorbar into a numpy array
			print('y_data   ' + str(y))#prints
			print('y_errorbar   ' + str(y_errorbar))#prints
#################Making Figure Object####################################
			figure = plt.figure()#generate a figure object
			ax = figure.add_subplot(111)#add a subplot to that figure which takes the size of the figure object
			ax.set_xlabel('Concentration log(c)', fontsize=16)#setting x axis label
			ax.set_ylabel('HTRF', fontsize=16)#setting y axis label
################Title of the Figure#####################################
			if self.Mode_Choice == 'ago':#checks mode for printing correct subtitle
				figure.suptitle('{} Gq Activation {}'.format(self.Molecule_Object[x].Name_Of_Molecule, self.Date), fontsize = 14, fontweight = 'bold', y = 0.92)
			elif self.Mode_Choice == 'agoH':
				figure.suptitle('{} Gq Activation {}'.format(self.Molecule_Object[x].Name_Of_Molecule, self.Date), fontsize = 14, fontweight = 'bold')
			elif self.Mode_Choice == 'anta' or self.Mode_Choice == 'anta_10':
				figure.suptitle('{} + 10 \u03BC M Carbachol Gq Inhibition {}'.format(self.Molecule_Object[x].Name_Of_Molecule, self.Date), fontsize = 14, fontweight = 'bold')
#####################################################
			if len(y_errorbar) == len(y):#checks if y_errorbar number is equal to y number
				ax.errorbar(x_data_points, y, yerr=y_errorbar, fmt='ok',color='black',capsize=2, label = 'raw data  of {}'.format(self.Molecule_Object[x].Name_Of_Molecule))#plots  y data with its errorbars
				ax.set_yticks(np.arange(0,16000, step=1000))#normalize yticks size
			else:
				ax.scatter(x_data_points, y, label = 'raw data  of {}'.format(self.Molecule_Object[x].Name_Of_Molecule))#if no errorbar had been made then it plots only the y data points
				ax.set_yticks(np.arange(0,16000, step=1000))#normalize the yticks size
			if not self.Plot_True:#pass if its not true
				ax.set_yticks(np.arange(0,16000,step=1000))
################Fit of the Data##################################################################################
			try:
				if self.Plot_True:#if true then it tries to fit y data with the x-data and the hill equation
					popt, pcov = curve_fit(self.Hill_function,x_data_points, y, p0=[min(y),max(y),-7.5,1])
					x_plot_data = np.linspace(-11,-2, num=100000,dtype =np.complex)
					ax.plot(x_plot_data, self.Hill_function(x_plot_data,*popt),'r', label = 'fitting curve for {}'.format(self.Molecule_Object[x].Name_Of_Molecule))
					ax.set_yticks(np.arange(0,16000,step=1000))
			except:
				pass
##################################################################################################
			try:
				if self.Plot_True:#writes every fitted parameter into the console 
					print('{}: {}'.format('Covariance Matrix', pcov)) 
					print('Minimum Parameter:   '+ str(popt[0]) + '+/-' + str(pcov[0,0]**0.5))
					print('Maximum Parameter:   '+ str(popt[1]) + '+/-' + str(pcov[1,1]**0.5))
					print('IC50/EC50 Parameter:   '+ str(popt[2]) + '+/-' + str(pcov[2,2]**0.5))
					print('Hill-Slope Parameter:   '+ str(popt[3]) + '+/-' + str(pcov[3,3]**0.5))
			except:
				pass
#################################################################################################
			ax.legend()
			plt.savefig('{}_{}.png'.format(self.Molecule_Object[x].Name_Of_Molecule,re.sub('[.]', '',self.Date)),dpi=300,format = 'png',transparent = True)
			plt.savefig('{}_{}.svg'.format(self.Molecule_Object[x].Name_Of_Molecule,re.sub('[.]', '',self.Date)),dpi=300,format = 'svg',transparent = True)
			plt.show()#plots the figures for visual inspection
		return()
	################################################################################################
	def Hill_Fit_Pandas(self, reference, compound, mode, tp_pred, error):
		x_data_reference = np.array([])
		x_data = np.array([])
		y_data_reference = np.array([])
		y_error_reference = np.array([])
		y_data = np.array([])
		y_error = np.array([])
		y_histogramm = np.array([])
		y_histogramm_error = np.array([])
		figure = plt.figure(figsize = (13,6),tight_layout = True)#generate a figure object
		ax = figure.add_subplot(111)#add a subplot to that figure which takes the size of the figure object
		ax.set_xlabel('log(c)', fontsize=25)#setting x axis label
		ax.set_ylabel('HTRF normalized/%', fontsize = 25)#setting y axis label
		ax.set_xticks(np.arange(-10,-1, step =1))
		ax.set_clip_on(False)
		for rows in self.Molecule_Object.index:
			if type(rows) == int or type(rows) == float:
				if not pd.isnull(self.Molecule_Object.at[rows,'{} Average Norm'.format(reference)]):
					x_data_reference = np.append(x_data_reference, rows)
					y_data_reference = np.append(y_data_reference, self.Molecule_Object.at[rows,'{} Average Norm'.format(reference)])
					x_histogramm = np.append(min(x_data_reference)-2,min(x_data_reference)-3)
					x_breakline_1 = np.append(min(x_data_reference)-1, min(x_data_reference)-1)
					x_breakline_2 = np.append(min(x_data_reference)-1.2, min(x_data_reference)-1.2)
					y_breakline_1 = np.append(-10, 10)
				if not pd.isnull(self.Molecule_Object.at[rows,'{} StDev Norm'.format(reference)]):
					if error == 'StError':
						y_error_reference = np.append(y_error_reference, self.Molecule_Object.at[rows,'{} StError Norm'.format(reference)])
					else:
						y_error_reference = np.append(y_error_reference, self.Molecule_Object.at[rows,'{} StDev Norm'.format(reference)])
				if not pd.isnull(self.Molecule_Object.at[rows,'{} Average Norm'.format(compound)]):
					x_data = np.append(x_data, rows)
					y_data = np.append(y_data, self.Molecule_Object.at[rows,'{} Average Norm'.format(compound)])
				if not pd.isnull(self.Molecule_Object.at[rows,'{} StDev Norm'.format(compound)]):
					if error == 'StError':
						y_error = np.append(y_error, self.Molecule_Object.at[rows,'{} StError Norm'.format(compound)])
					else:
						y_error = np.append(y_error, self.Molecule_Object.at[rows,'{} StDev Norm'.format(compound)])
			else:
				y_histogramm = np.append(110.72, 7.12)
				y_histogramm_error = np.append(0.83, 0.14)
				y_breakline = np.append(-1,5)
		ax.errorbar(x_data_reference, y_data_reference, yerr=y_error_reference, fmt='ok',mfc='r',capsize=2, label = 'raw data of {}'.format(reference))#plots  y data with its errorbars
		ax.errorbar(x_data, y_data, yerr=y_error, fmt='ok', mfc='b', capsize=2, label = 'raw data of {}'.format(compound))
		ax.bar(x_histogramm[0], y_histogramm[0], yerr=y_histogramm_error[0], capsize=2, color = 'w', hatch ='--',
				edgecolor ='k' , label = 'Positive Control', align = 'center', width = 0.5)
		ax.bar(x_histogramm[1], y_histogramm[1], yerr=y_histogramm_error[1], capsize=2, color = 'w', hatch = '+',
				edgecolor ='k' , label = 'Negative Control', align = 'center', width = 0.5)
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		line = Line2D(x_breakline_1, y_breakline_1, clip_on = False, color = 'k')
		line_2 = Line2D(x_breakline_1-0.2, y_breakline_1, clip_on = False, color = 'k')
		ax.add_artist(line)
		ax.add_artist(line_2)
		try:
			if self.Plot_True:#if true then it tries to fit y data with the x-data and the hill equation
				print('{}: {} \n {}'.format(reference, x_data_reference, y_data_reference))
				print('{}: {} \n {}'.format(compound, x_data, y_data))
				popt, pcov = curve_fit(self.Hill_function,x_data_reference, y_data_reference, p0=[min(y_data_reference),max(y_data_reference),-7.5,1], bounds =((-np.inf,-np.inf,-np.inf,1.),(np.inf,np.inf,np.inf,1.00000000000001)))
				x_plot_data = np.linspace(-10.5,-2.5, num=100000,dtype =np.float64)
				print('Parameters for {}:'.format(reference))
				print('{}: {}'.format('Covariance Matrix', pcov)) 
				print('Minimum Parameter:   '+ str(popt[0]) + '+/-' + str(pcov[0,0]**0.5))
				print('Maximum Parameter:   '+ str(popt[1]) + '+/-' + str(pcov[1,1]**0.5))
				print('IC50/EC50 Parameter:   '+ str(popt[2]) + '+/-' + str(pcov[2,2]**0.5))
				print('Hill-Slope Parameter:   '+ str(popt[3]) + '+/-' + str(pcov[3,3]**0.5))
				ax.plot(x_plot_data, self.Hill_function(x_plot_data,*popt),'r', label = 'fitting curve for {}'.format(reference))
				popt, pcov = curve_fit(self.Hill_function,x_data, y_data, p0=[min(y_data),max(y_data),tp_pred,1], bounds =((-np.inf,-np.inf,-np.inf,1.),(np.inf,np.inf,np.inf,1.00000000000001)))
				print('Parameters for {}:'.format(compound))
				print('{}: {}'.format('Covariance Matrix', pcov)) 
				print('Minimum Parameter:   '+ str(popt[0]) + '+/-' + str(pcov[0,0]**0.5))
				print('Maximum Parameter:   '+ str(popt[1]) + '+/-' + str(pcov[1,1]**0.5))
				print('IC50/EC50 Parameter:   '+ str(popt[2]) + '+/-' + str(pcov[2,2]**0.5))
				print('Hill-Slope Parameter:   '+ str(popt[3]) + '+/-' + str(pcov[3,3]**0.5))
				x_plot_data = np.linspace(-10.5,-2.5, num=100000,dtype =np.float64)
				ax.plot(x_plot_data, self.Hill_function(x_plot_data,*popt),'b', label = 'fitting curve for {}'.format(compound), clip_on=False)
		except:
			print('Fitting did not work')
			pass
		ax.legend(loc = 'upper left',bbox_to_anchor=(1, 1), fancybox =True, fontsize = 15)
		if self.Mode_Choice == 'ago':#checks mode for printing correct subtitle
			label = 'Agonist'
			plt.title('{} Gq Activation'.format(compound), fontsize = 25, fontweight = 'bold')
		elif self.Mode_Choice == 'agoH':
			label = 'Agonist'
			plt.title('{} Gq Activation'.format(compound), fontsize = 25, fontweight = 'bold')
		elif self.Mode_Choice == 'anta' or self.Mode_Choice == 'anta_10':
			label = 'Antagonist'
			plt.title('{} + 10 \u03BC M Carbachol Gq Inhibition'.format(compound), fontsize = 25, fontweight = 'bold')
		elif self.Mode_Choice == 'empty' or self.Mode_Choice == 'emptyH':
			label = 'Empty'
			plt.title('{} Gq Activation \n without the overexpression of M3AR'.format(compound), fontsize = 25, fontweight = 'bold')
		elif self.Mode_Choice == 'antaH':
			label = 'Antagonist'
			figure.title('{} + 10 \u03BC M \n Carbachol Gq Inhibition'.format(compound), fontsize = 25, fontweight = 'bold')
		ax.set_yticks(np.arange(0,130, step=10))#normalize yticks size
		plt.yticks(fontsize = 15)
		plt.xticks(fontsize = 15)
		plt.savefig('Summary_{}_{}_{}.png'.format(compound, label, re.sub('[.]', '',self.Date)), dpi=300,format = 'png',transparent = True)
		plt.savefig('Summary_{}_{}_{}.svg'.format(compound, label, re.sub('[.]', '',self.Date)), dpi=300,format = 'svg',transparent = True)
		plt.show()#plots the figures for visual inspection
		return()
############################################################