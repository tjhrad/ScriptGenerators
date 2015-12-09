#!/bin/python

# This script generator will help you make ANTs scripts to run on the supercomputer. It produces a script that will acpc align, resample, N4 bias correct, and skull strip t1 images for each subject in a dataset. It assumes that you have saved the original files as "t1.nii" NOT "t1.nii.gz" in individual directories.

# Note: You might still get errors while trying to run this script on some participants. If that is the case, pay attention to the errors. Many things can go wrong so it is always a good idea to become familiar with the individual steps. Also, pay close attention to your template names. I have the templates named according to the OASIS-30 template, but that will change according to whichever template you choose.

# NOTE: You will have to adjust the script to match your dataset!

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
#SBATCH --ntasks=1 # number of processor cores (i.e. tasks)
#SBATCH --nodes=1 # number of nodes
#SBATCH --mem-per-cpu=8192M # memory per CPU core
#SBATCH -o """ +logfilesDir+ """output_""" + scriptName + str(i) + """.txt
#SBATCH -e """ +logfilesDir+ """error_""" + scriptName + str(i) + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name
#SBATCH --mail-user=""" + emailAddress + """ # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

name=""" +subject+ """
files=""" +subjectDir+ subject+"""

ARTHOME=""" +acpcLocation+ """
export ARTHOME

export ANTSPATH=""" + antsLocation + """
PATH=${ANTSPATH}:${PATH}

#ACPC align the T1 image.

echo $files
""" + acpcLocation + """acpcdetect -M -o $files/acpc.nii -i $files/t1.nii

echo N4 bias for: $files

N4BiasFieldCorrection -d 3 -i $files/acpc.nii -o [$files/corrected.nii.gz,$files/biasfield.nii.gz] -s 4 -b [200] -c [50x50x50x50,0.000001]

echo Resampling image from $files to 1x1x1mm..

""" + c3dLocation + """c3d -verbose $files/corrected.nii.gz -resample-mm 1x1x1mm -o $files/n4_resampled.nii.gz

echo Skull Strip

sh """ +antsLocation+ """antsBrainExtraction.sh -d 3 -a $files/n4_resampled.nii.gz -e """+templateLocation+"""T_template0.nii.gz -m """+templateLocation+"""T_template0_BrainCerebellumProbabilityMask.nii.gz -o $files/

"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1
