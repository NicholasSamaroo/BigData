import sys
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["hetionet"]

nodeCollection = db["nodes_test"]
edgesCollection = db["edges_test"]

disease = str(sys.argv[1])
diseaseDocument = nodeCollection.find_one( {"name": disease})

if diseaseDocument == None:
    print("This is not a Disease name, please run the program again with a disease name")
    exit()
elif diseaseDocument['kind'] != "Disease":
    print("This is a " + diseaseDocument['kind'] + " name, please run the program again with a disease name")
    exit()

diseaseID = diseaseDocument["id"]

#Query 1
firstQuery = edgesCollection.find( { "$and": [ {"metaedge": {"$in": [ "CtD", "CpD", "DdG", "DaG", "DuG", "DlA"]}} , 
{ "$or": [ {"target": diseaseID} , {"source": diseaseID} ] } ] } )

#Prints the result of firstQuery
for edges in firstQuery:
    if edges['metaedge'] == "CtD" or edges['metaedge'] == "CpD":
        compoundID = edges['source']
        compoundDocument = nodeCollection.find_one( {"id": compoundID})
        compoundName= compoundDocument["name"]
        print(compoundName + " treats / palliates " + disease)
    elif edges['metaedge'] == "DdG" or edges['metaedge'] == "DaG" or edges['metaedge'] == "DuG":
        geneID = edges['target']
        geneDocument = nodeCollection.find_one( {"id": geneID})
        geneName = geneDocument["name"] 
        print(geneName + " causes " + disease)
    elif edges['metaedge'] == "DlA":
        localizes = edges['target']
        localizesDocument = nodeCollection.find_one( {"id": localizes})
        localizesName = localizesDocument["name"]
        print(disease + " localizes / occurs here: " + localizesName)