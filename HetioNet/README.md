**INSTRUCTIONS FOR RUNNING QUERY 1**
----------------------------------

Given a DISEASE, this file returns to you: it's name, COMPOUND names that can treat or palliate this DISEASE, GENE names that cause the DISEASE, and where the DISEASE occurs.

- Go to https://www.mongodb.com/download-center/community and download MongoDB for your system
- Make sure you also have PyMongo installed on your system. Instructions can be found here: https://api.mongodb.com/python/current/installation.html

- Find your MongoDB folder and open mongo.exe. In my case, the path would be C:\Program Files\MongoDB\Server\4.2\bin\mongo.exe
- In the mongo.exe terminal run each command separately:
	- use hetionet 
	- db.createCollection("nodes")
	- db.createCollection("edges")

- In order to import the data, run these two import statements separately in your system terminal (Command Prompt- Windows, Terminal- Mac) where nodes.tsv and edges.tsv are located. NOTE: edges_test.tsv and nodes_test.tsv were used as new test data files to make sure the program ran on new data; change the file path to the respective test files if you wish to run the query on those.
	- mongoimport -d hetionet -c nodes --type tsv --file 'FILE_PATH_OF_nodes.tsv' --headerline
	- mongoimport -d hetionet -c edges --type tsv --file 'FILE_PATH_OF_edges.tsv' --headerline 

- After the data has been loaded in, follow these instructions to run the program:
	- In your system terminal, cd into into the folder with our files, then run:
		- python Query_1.py "DISEASE_NAME" 
			- IMPORTANT - DISEASE_NAME must be enclosed in " " and must also be a valid disease name found in the nodes.tsv file or nodes_test.tsv

**INTRUCTIONS FOR RUNNING QUERY 2**
---------------------------------

This file returns to you all the COMPOUNDS that can treat a DISEASE. A COMPOUND can treat a DISEASE if the ANATOMY where the DISEASE occurs up-regulates / down-regulates a GENE and COMPOUNDS or SIMILAR COMPOUNDS up-regulate / down-regulate the same GENE in an opposite direction (e.g. Disease_x occurs at Anatomy_0 , Anatomy_0 up-regulates Gene_2 and Compound_4 down-regulates Gene_2, therefore, Compound_4 is one compound that can treat Disease_x)

- You still need PyMongo and MongoDB installed on your system, see the beginning of Query 1 to find out how to download them
- The data from either nodes.tsv and edges.tsv or nodes_test.tsv and edges_test.tsv should be loaded into your local MongoDB if you are following from Query 1. If not, see Query 1 for how to import the data into MongoDB

- After you resolve the dependencies and your data is loaded in, follow these instructions to run the query:
	- CD into the folder that contains Query_2 and in the terminal type python Query_2 "DISEASE_NAME" where DISEASE_NAME must be enclosed in " " and must also be a valid disease name found in the nodes.tsv file or nodes_test.tsv file 
