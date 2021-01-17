import sys
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["hetionet"]

nodeCollection = db["nodes"]
edgesCollection = db["edges"]

disease = str(sys.argv[1])

diseaseDocument = nodeCollection.find_one({"name": disease})

if diseaseDocument == None:
    print("This is not a Disease name, please run the program again with a disease name")
    exit()
elif diseaseDocument['kind'] != "Disease":
    print("This is a " + diseaseDocument['kind'] + " name, please run the program again with a disease name")
    exit()

diseaseID = diseaseDocument["id"]

'''
    We need to find out where the Disease occurs before we do anything.
    So, first we find where the Disease occurs, then we find the genes we need, by using the Anatomies we just found, 
    and save those genes in a list. We then find the compounds we need by using the gene list and then query for the similar compounds 
    in order to check if any similar compounds treat the disease. After that we look at CuG, AdG and CdG, AuG by using the 
    gene list and return the rest of compounds that can treat the disease.
'''

# Finds where the Disease localizes
findAnatomy = edgesCollection.find({"source": diseaseID , "metaedge": "DlA"})
anatomyList = []

for i in findAnatomy:
    anatomyList.append(i['target'])

# Returns all of the genes associated with the correct Anatomies
anatomyGene = edgesCollection.find( {"$and": [ {"source": {"$in": anatomyList } } , {"metaedge": {"$in": ["AuG", "AdG"] } } ] } )
geneList = []

anatomyGeneCopy = []

for i in anatomyGene:
    anatomyGeneCopy.append(i)

for j in anatomyGeneCopy:
    geneList.append(j['target'])

# Returns all of the compounds associated with the correct genes 
compoundGene = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CuG","CdG"] } } , {"target": {"$in": geneList } } ] } )
compoundList = []

for k in compoundGene:
    compoundList.append(k['source'])

# Returns compounds similar to the ones returned in the last query
compoundSimilarity = edgesCollection.find( {"$and": [ {"source": {"$in": compoundList} }, {"metaedge": "CrC"} ] } )
simList = []

for l in compoundSimilarity:
    simList.append(l['target'])

# Returns the CuG and CdG for the similar compounds
SIMcompoundAndGene = edgesCollection.find({"$and": [ {"source": {"$in": simList} } , {"metaedge": {"$in": ["CuG", "CdG"] } } , {"target": {"$in": geneList} } ] } )
SIMcompoundAndGeneCOPY = []

for i in SIMcompoundAndGene:
    SIMcompoundAndGeneCOPY.append(i)

finalSimList = []

for m in SIMcompoundAndGeneCOPY:
    for n in anatomyGeneCopy:
        if m['metaedge'] == "CuG" and n['metaedge'] == "AdG" and m['target'] == n['target']:
            if m['source'] in finalSimList:
                continue
            else:
                finalSimList.append(m['source'])
                compoundSIMTreatment = nodeCollection.find_one( {"id": m['source'] } )
                print(compoundSIMTreatment['name'] + " treats " + disease)

for m in SIMcompoundAndGeneCOPY:
    for n in anatomyGeneCopy:
        if m['metaedge'] == "CdG" and n['metaedge'] == "AuG" and m['target'] == n['target']:
            if m['source'] in finalSimList:
                continue
            else:
                finalSimList.append(m['source'])
                compoundSIMTreatment = nodeCollection.find_one( {"id": m['source'] } )
                print(compoundSIMTreatment['name'] + " treats " + disease)
    
if len(finalSimList) == 0:
    print("No similar drugs can treat this disease")

finalList = []

# Returns CuG and AdG for the necessary genes
compoundGeneCUG = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CuG", "AdG"] } } , {"target": {"$in": geneList } } ] } )
compoundGeneCUGCOPY = []

for i in compoundGeneCUG:
    compoundGeneCUGCOPY.append(i)

for i in compoundGeneCUGCOPY[0:]:
    for j in compoundGeneCUGCOPY[1:]:
        if i['metaedge'] == "CuG" and j['metaedge'] == "AdG" and i['target'] == j['target']:
            if i['source'] in finalList or i['source'] in finalSimList:
                continue
            else:
                finalList.append(i['source'])
                compoundTreatment = nodeCollection.find_one( {"id": i['source'] } )
                print(compoundTreatment['name'] + " treats " + disease)

# Returns CdG and AuG for the necessary genes
compoundGeneCDG = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CdG", "AuG"] } } , {"target": {"$in": geneList } } ] } )
compoundGeneCDGCOPY = []

for i in compoundGeneCDG:
    compoundGeneCDGCOPY.append(i)

for i in compoundGeneCDGCOPY[0:]:
    for j in compoundGeneCDGCOPY[1:]:
        if i['metaedge'] == "CdG" and j['metaedge'] == "AuG" and i['target'] == j['target']:
            if i['source'] in finalList or i['source'] in finalSimList:
                continue
            else:
                finalList.append(i['source'])
                compoundTreatment = nodeCollection.find_one( {"id": i['source'] } )
                print(compoundTreatment['name'] + " treats " + disease)

if len(finalList) == 0:
    print("No drugs can treat this disease")