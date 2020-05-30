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

findAnatomy = edgesCollection.find({"source": diseaseID , "metaedge": "DlA"})
anatomyList = []

for i in findAnatomy:
    anatomyList.append(i['target'])

anatomyGene = edgesCollection.find( {"$and": [ {"source": {"$in": anatomyList } } , {"metaedge": {"$in": ["AuG", "AdG"] } } ] } )
geneList = []

anatomyGeneCopy = []

for i in anatomyGene:
    anatomyGeneCopy.append(i)

for j in anatomyGeneCopy:
    geneList.append(j['target'])

compoundGene = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CuG","CdG"] } } , {"target": {"$in": geneList } } ] } )
compoundList = []

for k in compoundGene:
    compoundList.append(k['source'])

compoundSimilarity = edgesCollection.find( {"$and": [ {"source": {"$in": compoundList} }, {"metaedge": "CrC"} ] } )
simList = []

for l in compoundSimilarity:
    simList.append(l['target'])

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

compoundGeneCUG = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CuG", "AdG"] } } , {"target": {"$in": geneList } } ] } )
compoundGeneCUGCOPY = []

for i in compoundGeneCUG:
    compoundGeneCUGCOPY.append(i)

for i in compoundGeneCUGCOPY[0:]:
    for j in compoundGeneCUGCOPY[1:]:
        if i['metaedge'] == "CuG" and j['metaedge'] == "AdG" and i['target'] == j['target']:
            if i['source'] in finalList:
                continue
            else:
                finalList.append(i['source'])
                compoundTreatment = nodeCollection.find_one( {"id": i['source'] } )
                print(compoundTreatment['name'] + " treats " + disease)

compoundGeneCDG = edgesCollection.find( {"$and": [ {"metaedge": {"$in": ["CdG", "AuG"] } } , {"target": {"$in": geneList } } ] } )
compoundGeneCDGCOPY = []

for i in compoundGeneCDG:
    compoundGeneCDGCOPY.append(i)

for i in compoundGeneCDGCOPY[0:]:
    for j in compoundGeneCDGCOPY[1:]:
        if i['metaedge'] == "CdG" and j['metaedge'] == "AuG" and i['target'] == j['target']:
            if i['source'] in finalList:
                continue
            else:
                finalList.append(i['source'])
                compoundTreatment = nodeCollection.find_one( {"id": i['source'] } )
                print(compoundTreatment['name'] + " treats " + disease)

if len(finalList) == 0:
    print("No drugs can treat this disease")