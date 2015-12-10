#!/bin/python


# The script generator will help you make FreeSurfer scripts to run on the BYU supercomputer.
#
# Note: You might still get errors while trying to run this script on some participants. 
# If that is the case, pay attention to the errors that FreeSurfer gives you.
# You will have to adjust the script accordingly.

from os import listdir

##################################
# CHANGE THE FOLLOWING VARIABLES #
##################################

emailAddress = 'youremail@gmail.com'
subjectDir = '/fslhome/yourusername/compute/phantom/' # Where are your original subjects found?
fs_subjectDir = '/fslhome/yourusername/compute/freesurfer/wilde/' # Where is your FreeSurfer subject Directory for this study?
fsLocation = '/fslhome/yourusername/bin/freesurfer' # File path to your freesurfer program directory
scriptDir = '/fslhome/yourusername/scripts/freesurfer/wilde/scripts/' # Where do you want to save your scripts?
scriptName = 'name_fs' # What do you want the name of the scripts to be?

########################################################################
# DO NOT CHANGE ANYTHING AFTER THIS UNLESS YOU KNOW WHAT YOU ARE DOING #
########################################################################

dirList=listdir(subjectDir) # Create a list of all of the files and folders in the designated directory.

i=0
for subject in dirList: # Search the designated folder
        dcm=(listdir(subjectDir+subject))[0]
        if '.DS_Store' in dcm:
                dcm=(listdir(subjectDir+subject))[1]
        myScript = (
        """#!/bin/tcsh

#SBATCH --time=50:00:00 # walltime
#SBATCH --ntasks=1 # number of processor cores (i.e. tasks)
#SBATCH --nodes=1 # number of nodes
#SBATCH --mem-per-cpu=8192M # memory per CPU core
#SBATCH -o /fslhome/huff6/logfiles/freesurfer/wilde/output_""" + scriptName + str(i) + """.txt
#SBATCH -e /fslhome/huff6/logfiles/freesurfer/wilde/error_""" + scriptName + str(i) + """.txt
#SBATCH -J \"""" + scriptName + str(i) + """\" # job name
#SBATCH --mail-user=""" + emailAddress + """ # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

setenv FREESURFER_HOME """ + fsLocation + """
source $FREESURFER_HOME/SetUpFreeSurfer.csh
setenv SUBJECTS_DIR """ + fs_subjectDir + """
cd $SUBJECTS_DIR

""" + fsLocation + """/bin/recon-all  -all -subjid """ + subject + """ -i """ + subjectDir + subject + """/""" + dcm + """
"""
        )
        print(myScript)
        fileName = scriptDir + scriptName + str(i) + ".sh"
        print("Saving file as: " + fileName)
        subjectFile = open(fileName,'w')
        subjectFile.write(myScript)
        subjectFile.close()
        i+=1

### To print out FreeSurfer table:
# asegstats2table --subjects sd* --meas volume --tablefile ~/Desktop/aseg_stats.txt --skip
