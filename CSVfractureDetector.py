############################################################################
## $ python3                                                              ##
##                                                                        ##
############################################################################

import csv
import time


# Opens a text file that holds the appropriate CSV files to read for data
# processing. 
files_to_use = open("files-to-read.txt",'r')
files_list = files_to_use.readlines()
flist = []
for i in range(len(files_list)):
    flist.append(files_list[i].rstrip('\n'))
files_to_use.close()

# Generating time stamp for file name
timestr = time.strftime("%Y%m%d-%H%M%S")

# Create a new text file to hold fractures 
cheese = open("fractures-" + timestr + ".txt",'w+')

N = 20           # number of points to running average
change = round(1/100.0,3)  # amount of change in load for fracture detection
                 # generally leave at 0.010 


# This section reads through all the files in the read text file to search
# for fractures. 

header_skip = 42   # Number of rows to skip to enter header section of
                   # data file. Typically around 42 to get to labels.

          
for j in range(0, len(files_list)):

    with open(flist[j], newline='\r\n') as csvfile:
        # skipping preamble rows to header row
        for i in range(header_skip):
           next(csvfile)
        # reading csv data
        reader = csv.reader(csvfile)
        my_Data = list(reader)
	
    cheese.write(str(flist[j]) + '\n' +'\n') # writes the name of the file


    numrows = len(my_Data)
    numcols = len(my_Data[0])

    Axial = []         # axial counter holder array

    # iterating through the column of data
    for k in range(0, numcols):

        if "Axial" in my_Data[0][k]:
            for w in range(2, numrows):
                Axial.append(my_Data[w][k])

        run_avg = []    # holder for running average
        run_sum = 0     # re-zeroing the running sum for averaging.

        if "Load" in my_Data[0][k]:

            cheese.write("---------------------" + '\n')

            # checking to see if the column of data is on the valley side.
            # if on the peak side, then skipping.
            if float(my_Data[50][k]) > -0.5:
                continue
           
            for w in range(2, numrows):

                currentForce = round(float(my_Data[w][k]),3)

                if w < N+2:
                    run_sum += currentForce

                if w > N+5:
                    run_avg = round(run_sum / N,3)

##                    print("running avg = ")
##                    print(run_avg)
##
##                    time.sleep(.1)

                    # Fracture detection, if the current read values is
                    # greater than the running average, the write the 
                    # location into the text file.
                    if  currentForce > (1 - change) * run_avg:
                        cheese.write("Fracture found at " +
                                     Axial[w-2] +
                                     " cycles, for " +
                                     my_Data[0][k] + '\n')

                    # Updating the running sum.
                    run_sum += round(currentForce -
                                     float(my_Data[w-N][k]),3)

    # Writes a dividing line between files being read. 
    cheese.write("~~~~ ---- ~~~~ ---- ~~~~~ ---- ~~~~ ---- ~~~~" +
                 '\n')

# closing the fracture.txt file after writing all the lines to it.
cheese.close()
