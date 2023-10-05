# cis_bio_evaluation
This is part of the publication "A chemist’s viewpoint: Investigation of the interactions
required for receptor activation in atomistic detail
through the systematic variation of M3 R ligands"
###############################################
cis_bio_v3.py is used for the evaluation of one experiment
the parser arguments are :   
  --output -o ; name of the output file
  --input - i ; name of the input file, needs to be in the same directory
  --name_mol, -nam; a list of names of the molecules, sequence of the names need to be the same as the order of the pipetting sequence
  --conc, -c; [ago, agoc]; choose between agonist or agonist competition
  --num_repli, -nr; number of replica
  --num_conc, -nc; number of concentrations plus pos and neg used in the assay
  --upd, -u; updating or not generating a summary excel file
  --plot, -p set True for plotting
  --parameter, -param; Parameter file 
  --date, -d; Date of experiment
  --data_keys, -k; Headers of the output Excel file
  -verbose, -v; Write a lot of data
# cis_bio_summary_3.py
This script summarises all individual experiment into one excel sheet with the average and error propagation
##################################################
the parser arguments are:
  --output, -o; name of the output
  --conc, -c; assay type : agonist or empty
  --turningpoint, -tp; Starting point of the IC/EC50 for the fitting, default -7.5 logunits
  --compound, -com; Compound name, should be the same as in the excel sheets
  --reference, -ref; Reference name, should be the same as in the excel sheets
  --plot, -p; set True for plotting
  --parameter, -param; parameter file
  --date, -d; Date of the summary generation
  --verbose, -v; Write a lot of data
  --exclude, -e; list of data folders to exclude from the summary
  --error, -er; Choose between Stdev or Sterror for plotting
  
