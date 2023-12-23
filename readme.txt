Model files in the NetPyNE simulation environment for the paper:

Theta-gamma phase amplitude coupling in a hippocampal CA1 microcircuit

by Adam Ponzi, Salvador Dura-Bernal, and Michele Migliore


Usage:

Download the files. 

Compile the mod files on the command line with 'nrnivmodl mechanisms'.

Install the NetPyNE simulation environment (http://netpyne.org/install.html)

To run the code using mpi-exec: (1) Remove or rename the directory t42_data (which is subsequently recreated when the code is run). (2) Set the numcores parameter in t42_batch.py to the required number of cores. (3) On the command line : 'nrniv -python t42_batch.py' (4) On completion, in the file maketrace.py set asBatch = True. Run maketrace.py.

To run the code directly: (1) On the command line: 'nrniv -python t42_init.py'. In this case no new directories are created. (2) On completion, in the file maketrace.py set asBatch = False. Run maketrace.py.


Questions on how to use this model should be directed to adam.ponzi@ibf.cnr.it



 
