#!/bin/python


# The script generator will help you make ANTs scripts to run on the supercomputer.
# Note: You might still get errors while trying to run this script on some participants. 
# If that is the case, pay attention to the errors that you are given and you will have to adjust the script accordingly.

# Specifically, this script will generate sbatch scripts to run antsJointLabelFusion.sh on all of the participants in a
# dataset. 

from os import listdir

##########################
# CHANGE THESE VARIABLES #
##########################

emailAddress = 'emailaddress@gmail.com'
subjectDir = '/fslhome/huff6/compute/huff_nifty/' # Where are your original subjects found?
antsLocation = '/fslhome/huff6/bin/antsbin/bin/' # File path to your ants bin
acpcLocation = '/fslhome/huff6/bin/art/'
logfilesDir = '/fslhome/huff6/logfiles/'
templateLocation = '/fslhome/huff6/Templates/OASIS-30_Atropos_template/'
c3dLocation = '/fslhome/huff6/bin/'
scriptDir = '/fslhome/huff6/scripts/ants/huff/scripts/' # Where do you want to save your scripts?
scriptName = 'huff_ants' # What do you want the name of the scripts to be?

###################################################################
# ONLY CHANGE THE FOLLOWING SCRIPT IF YOU KNOW WHAT YOU ARE DOING #
###################################################################


dirList=listdir(subjectDir) # Create a list of all of the files and folders in the designated directory.

i=0
for subject in dirList: # Search the designated folder
        t1=(listdir(subjectDir+subject))[0]
        if '.DS_Store' in t1:
                t1=(listdir(subjectDir+subject))[1]
        myScript = (
        """#!/bin/bash

#SBATCH --time=50:00:00 # walltime
#SBATCH --ntasks=2 # number of processor cores (i.e. tasks)
#SBATCH --nodes=1 # number of nodes
#SBATCH --mem-per-cpu=32768M # memory per CPU core
#SBATCH -o """ +logfilesDir+ """output_""" + scriptName + str(i) + """.txt
#SBATCH -e """ +logfilesDir+ """error_""" + scriptName + str(i) + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name
#SBATCH --mail-user=""" + emailAddress + """ # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

name=""" +subject+ """
files=""" +subjectDir+ subject+"""

ARTHOME=/fslhome/huff6/bin/art/
export ARTHOME

export ANTSPATH=""" + antsLocation + """
PATH=${ANTSPATH}:${PATH}

mkdir $files/labels/

${ANTSPATH}/antsJointLabelFusion.sh \
-d 3 \
-c 5 -j 2 \
-o $files/labels/ \
-p $files/labels/Posteriors%02d.nii.gz \
-t $files/BrainExtractionBrain.nii.gz \
-x $files/BrainExtractionMask.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-1/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-1/OASIS-TRT-20-1_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-2/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-2/OASIS-TRT-20-2_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-3/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-3/OASIS-TRT-20-3_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-4/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-4/OASIS-TRT-20-4_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-5/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-5/OASIS-TRT-20-5_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-6/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-6/OASIS-TRT-20-6_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-7/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-7/OASIS-TRT-20-7_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-8/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-8/OASIS-TRT-20-8_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-9/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-9/OASIS-TRT-20-9_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-10/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-10/OASIS-TRT-20-10_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-11/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-11/OASIS-TRT-20-11_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-12/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-12/OASIS-TRT-20-12_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-13/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-13/OASIS-TRT-20-13_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-14/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-14/OASIS-TRT-20-14_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-15/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-15/OASIS-TRT-20-15_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-16/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-16/OASIS-TRT-20-16_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-17/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-17/OASIS-TRT-20-17_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-18/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-18/OASIS-TRT-20-18_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-19/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-19/OASIS-TRT-20-19_DKT31_CMA_labels.nii.gz \
-g """+ templateLocation + """OASIS-TRT-20-20/t1weighted_brain.nii.gz -l """+ templateLocation + """OASIS-TRT-20-20/OASIS-TRT-20-20_DKT31_CMA_labels.nii.gz \
-k 1

"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1

