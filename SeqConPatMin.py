# Hackerrank Sequential Contiguous Pattern Mining
# CS 412 HW 2 Spring 2020
# WORKING CODE using dictionary

# Minimum length is 2, maximum length is 5, and minimum support is 2.
# That is, the patterns have to contain at least two words, but no more than 5.
# The frequency of the patterns is no less than 2.

import sys
import itertools
import re


def getHackerrankInput():

    input = list()
    for line in sys.stdin.readlines():
        input.append(line.strip())
    return input


def getInput():

    input = ['good grilled fish sandwich and french fries , but the service is bad',
             'disgusting fish sandwich , but good french fries',
             'their grilled fish sandwich is the best fish sandwich , but pricy',
             'A B A B A B A']
    return input


def createSpadeDatabase(textCorpus):
    """
    :param textCorpus:
    :return: dataframeDictionary: {'1': {'10': 'the', '12': 'is', '1': 'good', '3': 'fish', '2': 'grilled', '4': 'sandwich', '7': 'fries', '6': 'french', '9': 'but', '8': ','}, '3': {'11': 'but', '10': ',', '3': 'fish', '2': 'grilled', '5': 'is', '4': 'sandwich', '6': 'the', '9': 'sandwich', '8': 'fish'}, '2': {'3': 'sandwich', '2': 'fish', '5': 'but', '4': ',', '7': 'french', '6': 'good', '8': 'fries'}, '4': {'1': 'A', '3': 'A', '2': 'B', '5': 'A', '4': 'B', '7': 'A', '6': 'B'}}

    """

    # First create a minSup dictionary only for frequent items
    minSupDictionary = dict()
    for whichSID, line in enumerate(textCorpus):
        words = line.split(" ")
        for whichEID, word in enumerate(words):
            if word not in minSupDictionary:
                minSupDictionary[word] = 1
            else:
                minSupDictionary[word] += 1

    # Create dataframe as SPADE algorithm, with frequent words; ie words of sup >= minsup
    dataframeDictionary = dict()
    for lineIndex, line in enumerate(textCorpus):
        whichSID = str(lineIndex + 1)
        words = line.split(" ")
        for wordIndex, word in enumerate(words):
            whichEID = str(wordIndex+1)
            # Only considering frequent words; >= minsup
            if minSupDictionary[word] >= 2:
                if whichSID not in dataframeDictionary:
                    dataframeDictionary[whichSID] = dict()
                dataframeDictionary[whichSID][whichEID] = word

    return dataframeDictionary


def createSpadeDatabaseRough():
    """
    :param textCorpus:
    :return: dataframeDictionary: {'1': {'10': 'the', '12': 'is', '1': 'good', '3': 'fish', '2': 'grilled', '4': 'sandwich', '7': 'fries', '6': 'french', '9': 'but', '8': ','},
                                    '3': {'11': 'but', '10': ',', '3': 'fish', '2': 'grilled', '5': 'is', '4': 'sandwich', '6': 'the', '9': 'sandwich', '8': 'fish'},
                                    '2': {'3': 'sandwich', '2': 'fish', '5': 'but', '4': ',', '7': 'french', '6': 'good', '8': 'fries'},
                                    '4': {'1': 'A', '3': 'A', '2': 'B', '5': 'A', '4': 'B', '7': 'A', '6': 'B'}}

    """

    # First create a minSup dictionary only for frequent items
    # minSupDictionary = dict()
    # textCorpus = list()
    # for whichSID, line in enumerate(sys.stdin.readlines()):
    #     words = line.strip().split(" ")
    #     textCorpus.append(line.strip())
    #     for whichEID, word in enumerate(words):
    #         if word not in minSupDictionary:
    #             minSupDictionary[word] = 1
    #         else:
    #             minSupDictionary[word] += 1

    # Create dataframe as SPADE algorithm, with frequent words; ie words of sup >= minsup
    dataframeDictionary = dict()
    for lineIndex, line in enumerate(sys.stdin.readlines()):
        whichSID = str(lineIndex + 1)
        words = line.strip().split(" ")
        for wordIndex, word in enumerate(words):
            whichEID = str(wordIndex+1)
            # Only considering frequent words; >= minsup
            # if minSupDictionary[word] >= 2:
            if whichSID not in dataframeDictionary:
                dataframeDictionary[whichSID] = dict()
            dataframeDictionary[whichSID][whichEID] = word

    # for SID in sorted(dataframeDictionary.keys()):
    #     for sortedEID in sort_nicely(dataframeDictionary[SID].keys()):
    #         print SID, sortedEID, dataframeDictionary[SID][sortedEID]

    return dataframeDictionary


def findsubsets(s, n):
    xs = [s[i:j] for i, j in itertools.combinations(range(len(s) + 1), n)]
    return xs


def pairPossibleWordsBasedOnConstraint(dataframe):
    """
    :param dataframe: {'10': 'the', '12': 'is', '1': 'good', '3': 'fish', '2': 'grilled', '4': 'sandwich',
                        '7': 'fries', '6': 'french', '9': 'but', '8': ','}

    :return: Ex #1:
            listOfListOfConstraintPairs [['good', 'grilled', 'fish', 'sandwich'],
                                        ['french', 'fries', ',', 'but', 'the'],
                                        ['is']]
            listOflistOfpossiblePairs [['good', 'grilled', 'fish', 'sandwich'],
                                        ['french', 'fries', ',', 'but', 'the']]
    """

    listOfListOfConstraintPairs = list()
    previousEID = 0
    pairToAdd = list()
    firstTime = True
    for EID in sort_nicely(dataframe.keys()):
        currentEID = int(EID)
        if abs(previousEID - currentEID) == 1 or firstTime:
            firstTime = False
            pairToAdd.append(dataframe[EID])
        else:
            if len(pairToAdd) > 1:
                listOfListOfConstraintPairs.append(pairToAdd)
            pairToAdd = list()
            pairToAdd.append(dataframe[EID])
        previousEID = currentEID
    if len(pairToAdd)>1:
        listOfListOfConstraintPairs.append(pairToAdd)


    return listOfListOfConstraintPairs


def performSPADE(dataframe):

    k_itemsetDictionary = dict()
    for whichLine in dataframe.keys():
        wordsFrame = dataframe[(whichLine)]
        for pairOfWords in pairPossibleWordsBasedOnConstraint(dataframe=wordsFrame):
            subsetsOfWords = findsubsets(pairOfWords, 2)
            for aSubsetOfWords in subsetsOfWords:
                if 1 < len(aSubsetOfWords) < 6:
                    stichedWords = " ".join(aSubsetOfWords)
                    if stichedWords not in k_itemsetDictionary:
                        k_itemsetDictionary[stichedWords] = 1
                    else:
                        k_itemsetDictionary[stichedWords] += 1


    return k_itemsetDictionary


def remodel_k_itemsetDictionary(k_itemsetDictionary):
    """

    :param k_itemsetDictionary: {'fish sandwich': 4, 'sandwich ,': 2, 'A B A': 3, 'A B': 3, 'B A B': 2,
                                'B A B A': 2, ', but': 3, 'french fries': 2, 'grilled fish sandwich': 2,
                                'B A': 3, 'fish sandwich , but': 2, 'sandwich , but': 2, 'fish sandwich ,': 2,
                                'A B A B': 2, 'A B A B A': 2, 'grilled fish': 2}

    intermediate: remodeled_k_itemsetDictionary: {2: ['sandwich ,', 'B A B', 'B A B A', 'french fries',
                                                'grilled fish sandwich', 'fish sandwich , but', 'sandwich , but',
                                                'fish sandwich ,', 'A B A B', 'A B A B A', 'grilled fish'],
                                            3: ['A B A', 'A B', ', but', 'B A'],
                                            4: ['fish sandwich']}

    :return: sorted_remodeled_k_itemsetDictionary: {2: ['A B A B', 'A B A B A', 'B A B', 'B A B A',
                                                        'fish sandwich ,', 'fish sandwich , but', 'french fries',
                                                        'grilled fish', 'grilled fish sandwich', 'sandwich ,',
                                                        'sandwich , but'],
                                                    3: [', but', 'A B', 'A B A', 'B A'],
                                                    4: ['fish sandwich']}

    """

    remodeled_k_itemsetDictionary = dict()
    for key, value in k_itemsetDictionary.items():
        if value > 1:
            if value not in remodeled_k_itemsetDictionary:
                remodeled_k_itemsetDictionary[value] = list()
            remodeled_k_itemsetDictionary[value].append(key)

    return remodeled_k_itemsetDictionary


def sort_nicely(l):
    """ Sort the given list in the way that humans expect. """
    nicelySorted = sorted(l, key=alphanum_key)
    return nicelySorted

def printFrequentPatterns(minsupToPatternsDictionary):

    mineFirst20 = 1
    for k in sorted(minsupToPatternsDictionary, reverse=True):
        if mineFirst20 < 21:
            for patterns in sort_nicely(minsupToPatternsDictionary[k]):
                if mineFirst20 < 21:
                    printString = "[" + str(k) + ", '" + patterns + "']"
                    print (printString)
                    mineFirst20 += 1
                else:
                    break
        else:
            break


def read_dataset():

    dataset = list()
    filepath = 'trump_speech_new.txt'
    with open(filepath) as datafile:
        for line in datafile.readlines():
            dataset.append(line.strip())

    return dataset


if __name__ == '__main__':

    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

    minSupport = 2
    # textCorpus = getHackerrankInput()
    textCorpus = getInput()
    dataframeDict = createSpadeDatabase(textCorpus=textCorpus)
    k_itemsetDictionary = performSPADE(dataframe=dataframeDict)
    sorted_remodeled_k_itemsetDictionary = remodel_k_itemsetDictionary(k_itemsetDictionary)
    printFrequentPatterns(sorted_remodeled_k_itemsetDictionary)