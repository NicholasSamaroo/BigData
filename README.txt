INSTRUCTIONS FOR RUNNING QUERY 1

- Go to https://www.mongodb.com/download-center/community and download MongoDB for your system
- Make sure you also have PyMongo installed on your system. Instructions can be found here: https://api.mongodb.com/python/current/installation.html

- Find your MongoDB folder and open mongo.exe. In my case, the path would be C:\Program Files\MongoDB\Server\4.2\bin\mongo.exe
- In the mongo.exe terminal run each command separately:
	use hetionet 
	db.createCollection("nodes")
	db.createCollection("edges")

- In order to import the data, run these two import statements separately in your system terminal (Command Prompt- Windows, Terminal- Mac) where nodes.tsv and edges.tsv are located
	mongoimport -d hetionet -c nodes --type tsv --file FILE_PATH_OF_nodes.tsv --headerline
	mongoimport -d hetionet -c edges --type tsv --file FILE_PATH_OF_edges.tsv --headerline 

- After the data has been loaded in, follow these instructions to run the program:
	In your system terminal, cd into into the folder with our files, then run:
	python HetioNet.py "DISEASE_NAME" 
		IMPORTANT - DISEASE_NAME must be enclosed in " " and must also be a valid disease name found in the nodes.tsv file


	

