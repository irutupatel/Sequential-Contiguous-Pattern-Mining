# Hackerrank Sequential Contiguous Pattern Mining
# Using pandas dataframe

# Minimum length is 2, maximum length is 5, and minimum support is 2.
# That is, the patterns have to contain at least two words, but no more than 5.
# The frequency of the patterns is no less than 2.

import sys
import itertools
import re
from collections import OrderedDict
import pandas as pd


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

    # First create a minSup dictionary only for frequent items
    minSupDictionary = dict()
    for whichSID, line in enumerate(textCorpus):
        words = line.split(" ")
        for whichEID, word in enumerate(words):
            if word not in minSupDictionary:
                minSupDictionary[word] = 1
            else:
                minSupDictionary[word] += 1

    # Removing non frequent words; less than minsup from minSupDictionary
    frequentWordDictionary = {k: v for k, v in minSupDictionary.items() if v >= 2}

    # Create dataframe as SPADE algorithm, with frequent words; ie words of sup >= minsup
    dataframeDictionary = OrderedDict()
    dataframeDictionary["SID"] = list()
    dataframeDictionary["EID"] = list()
    dataframeDictionary["Items"] = list()
    for whichSID, line in enumerate(textCorpus):
        words = line.split(" ")
        for whichEID, word in enumerate(words):
            if word in frequentWordDictionary:
                dataframeDictionary["SID"].append(whichSID+1)
                dataframeDictionary["EID"].append(whichEID+1)
                dataframeDictionary["Items"].append(word)

    sequenceDatabase = pd.DataFrame(dataframeDictionary)

    return sequenceDatabase


def getSubsequence(wordsList, length):
    return True


def findsubsets(s, n):
    xs = [s[i:j] for i, j in itertools.combinations(range(len(s) + 1), n)]
    return xs


def pairPossibleWordsBasedOnConstraint(dataframe):
    """

    :param dataframe: Enter    EID Items
                            2    1   how
                            3    2  rutu
                            4    3   you
                            5    6   how
                            6    7  rutu
    :return: Ex #1:
             list of possible [['how', 'rutu', 'you'], ['how', 'rutu']]
             list of constraint [['how', 'rutu', 'you'], ['how', 'rutu']]

             Ex #2
             list of possible []
             list of constraint [['how'], ['you']]
    """

    listOfListOfConstraintPairs = list()
    previousEID = dataframe["EID"].iloc[0]
    pairToAdd = list()
    firstTime = True
    for rowIndex, columnValueOf in dataframe.iterrows():
        currentEID = columnValueOf.EID
        if abs(previousEID - currentEID) == 1 or firstTime:
            firstTime = False
            pairToAdd.append(columnValueOf.Items)
        else:
            listOfListOfConstraintPairs.append(pairToAdd)
            pairToAdd = list()
            pairToAdd.append(columnValueOf.Items)
        previousEID = currentEID
    listOfListOfConstraintPairs.append(pairToAdd)

    # Remove pairs of words that cannot be in contiguous patterns
    listOflistOfpossiblePairs = list()
    for listOfWords in listOfListOfConstraintPairs:
        if len(listOfWords) > 1:
            listOflistOfpossiblePairs.append(listOfWords)

    return listOflistOfpossiblePairs


def performSPADE(dataframe):

    # columnNames = ['SID', 'EID', 'Items']
    ex = dataframe.loc[dataframe['Items'] == "good"]

    k_itemsetDictionary = dict()
    for whichLine in range(1, howManyLines+1):
        whichLineSID = dataframe.loc[dataframe['SID'] == whichLine]
        wordsFrame = whichLineSID.drop(["SID"], axis=1)
        possiblePairsOfWords = pairPossibleWordsBasedOnConstraint(dataframe=wordsFrame)
        for pairOfWords in possiblePairsOfWords:
            subsetsOfWords = findsubsets(pairOfWords, 2)
            for aSubsetOfWords in subsetsOfWords:
                if len(aSubsetOfWords) > 1 and len(aSubsetOfWords) < 6:
                    stichedWords = " ".join(aSubsetOfWords)
                    if stichedWords not in k_itemsetDictionary:
                        k_itemsetDictionary[stichedWords] = 1
                    else:
                        k_itemsetDictionary[stichedWords] += 1

    k_itemsetDictionary = {k: v for k, v in k_itemsetDictionary.items() if v > 1}

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
        if value not in remodeled_k_itemsetDictionary:
            remodeled_k_itemsetDictionary[value] = list()
        remodeled_k_itemsetDictionary[value].append(key)

    sorted_remodeled_k_itemsetDictionary = dict()
    for key, value in remodeled_k_itemsetDictionary.items():
        sorted_remodeled_k_itemsetDictionary[key] = sort_nicely(value)

    return sorted_remodeled_k_itemsetDictionary


def sort_nicely(l):
    """ Sort the given list in the way that humans expect. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort(key=alphanum_key)
    return l


def printFrequentPatterns(minsupToPatternsDictionary):

    for k in sorted(minsupToPatternsDictionary, reverse=True):
        for patterns in minsupToPatternsDictionary[k]:
            printString = "[" + str(k) + ", '" + patterns + "']"
            print (printString)


if __name__ == '__main__':

    minSupport = 2
    # textCorpus = getHackerrankInput()
    textCorpus = getInput()
    howManyLines = len(textCorpus)
    sequenceDatabase = createSpadeDatabase(textCorpus=textCorpus)
    k_itemsetDictionary = performSPADE(dataframe=sequenceDatabase)
    sorted_remodeled_k_itemsetDictionary = remodel_k_itemsetDictionary(k_itemsetDictionary)
    printFrequentPatterns(sorted_remodeled_k_itemsetDictionary)
