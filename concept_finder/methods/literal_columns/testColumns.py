import glob
import csv 
import pickle
import json

filePathsToLabeledTables = glob.glob("./extended_instance_goldstandard/property/*.csv")  

conceptsRelatedToLiteralValues = pickle.load(open('./floatOrIntPropertyConcepts.pkl', 'rb'))

# for con in conceptsRelatedToLiteralValues:
#     print (con)

tblIDtoColumnsMap = {}

for pathtoProperty in filePathsToLabeledTables:
    # open property dir
    with open(pathtoProperty) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if row[0] in conceptsRelatedToLiteralValues:
                    pathToTable = pathtoProperty.replace("property", "tables").replace("csv", "json")
                    # open tables dir
                    with open(pathToTable) as json_file:  
                        data = json.load(json_file)
                        print(row[0])
                        print(data['relation'][int(row[3])])
                           



for key in tblIDtoColumnsMap.keys():
    print (f'{key:{100}} {tblIDtoColumnsMap[key]}')



# http://dbpedia.org/ontology/speaker
# http://dbpedia.org/ontology/ranking
# http://dbpedia.org/ontology/humanDevelopmentIndex
# http://dbpedia.org/ontology/numberOfPlatformLevels
# http://dbpedia.org/ontology/enginePower
# http://dbpedia.org/ontology/graySubject
# http://dbpedia.org/ontology/shareOfAudience
# http://dbpedia.org/ontology/percentageLiteracyWomen
# http://dbpedia.org/ontology/minorityFloorLeader
# http://dbpedia.org/ontology/size_v
# http://dbpedia.org/ontology/infantMortality
# http://dbpedia.org/ontology/centuryBreaks
# http://dbpedia.org/ontology/waterPercentage
# http://dbpedia.org/ontology/carNumber
# http://dbpedia.org/ontology/nationalRanking
# http://dbpedia.org/ontology/landPercentage
# http://dbpedia.org/ontology/grossDomesticProduct
# http://dbpedia.org/ontology/coastLength
# http://dbpedia.org/ontology/totalTracks
# http://dbpedia.org/ontology/totalDiscs
# http://dbpedia.org/ontology/imageSize
# http://dbpedia.org/ontology/trackNumber
# http://dbpedia.org/ontology/glycemicIndex
# http://dbpedia.org/ontology/capacityFactor
# http://dbpedia.org/ontology/frontierLength
# http://dbpedia.org/ontology/radius_ly
# http://dbpedia.org/ontology/usk
# http://dbpedia.org/ontology/solubility
# http://dbpedia.org/ontology/ceiling
# http://dbpedia.org/ontology/maximumInclination
# http://dbpedia.org/ontology/numberOfCollectionItems
# http://dbpedia.org/ontology/geneLocationStart
# http://dbpedia.org/ontology/espnId
# http://dbpedia.org/ontology/tvComId
# http://dbpedia.org/ontology/statisticValue
# http://dbpedia.org/ontology/numberOfPages
# http://dbpedia.org/ontology/barPassRate
# http://dbpedia.org/ontology/testaverage
# http://dbpedia.org/ontology/giniCoefficient
# http://dbpedia.org/ontology/percentageLiteracyMen
# http://dbpedia.org/ontology/percentageOfAreaWater
# http://dbpedia.org/ontology/cmykCoordinateMagenta
# http://dbpedia.org/ontology/age
# http://dbpedia.org/ontology/averageClassSize
# http://dbpedia.org/ontology/cmykCoordinateYellow
# http://dbpedia.org/ontology/flagSize
# http://dbpedia.org/ontology/currentRank
# http://dbpedia.org/ontology/towerHeight
# http://dbpedia.org/ontology/partitionCoefficient
# http://dbpedia.org/ontology/shoeNumber
# http://dbpedia.org/ontology/bioavailability
# http://dbpedia.org/ontology/redListIdNL
# http://dbpedia.org/ontology/numberOfMatches
# http://dbpedia.org/ontology/casualties
# http://dbpedia.org/ontology/numberOfGoals
# http://dbpedia.org/ontology/minorityLeader
# http://dbpedia.org/ontology/inclination
# http://dbpedia.org/ontology/gdpPerCapita
# http://dbpedia.org/ontology/partyNumber
# http://dbpedia.org/ontology/numberOfDoors
# http://dbpedia.org/ontology/rating
# http://dbpedia.org/ontology/starRating
# http://dbpedia.org/ontology/establishment
# http://dbpedia.org/ontology/majorityLeader
# http://dbpedia.org/ontology/minimumInclination
# http://dbpedia.org/ontology/hsvCoordinateSaturation
# http://dbpedia.org/ontology/giniCoefficientRanking
# http://dbpedia.org/ontology/range
# http://dbpedia.org/ontology/illiteracy
# http://dbpedia.org/ontology/dist_pc
# http://dbpedia.org/ontology/lastPosition
# http://dbpedia.org/ontology/careerPoints
# http://dbpedia.org/ontology/omim
# http://dbpedia.org/ontology/numberOfCountries
# http://dbpedia.org/ontology/percentageLiterate
# http://dbpedia.org/ontology/hsvCoordinateHue
# http://dbpedia.org/ontology/populationTotalRanking
# http://dbpedia.org/ontology/artificialSnowArea
# http://dbpedia.org/ontology/highestRank
# http://dbpedia.org/ontology/wikiPageRevisionID
# http://dbpedia.org/ontology/highestBreak
# http://dbpedia.org/ontology/onChromosome
# http://dbpedia.org/ontology/orbitalEccentricity
# http://dbpedia.org/ontology/orbits
# http://dbpedia.org/ontology/flashPoint
# http://dbpedia.org/ontology/output
# http://dbpedia.org/ontology/floorCount
# http://dbpedia.org/ontology/sessionNumber
# http://dbpedia.org/ontology/grayPage
# http://dbpedia.org/ontology/orbitalInclination
# http://dbpedia.org/ontology/rankInFinalMedalCount
# http://dbpedia.org/ontology/facilityId
# http://dbpedia.org/ontology/majorityFloorLeader
# http://dbpedia.org/ontology/wikiPageID
# http://dbpedia.org/ontology/hsvCoordinateValue
# http://dbpedia.org/ontology/areaTotalRanking
# http://dbpedia.org/ontology/v_hb
# http://dbpedia.org/ontology/geneLocationEnd
# http://dbpedia.org/ontology/other
# http://dbpedia.org/ontology/cmykCoordinateBlack
# http://dbpedia.org/ontology/cmykCoordinateCyanic
# http://dbpedia.org/ontology/penaltyScore
# http://dbpedia.org/ontology/numberOfHoles