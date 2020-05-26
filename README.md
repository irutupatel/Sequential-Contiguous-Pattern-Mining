# Sequential Contiguous Pattern Mining
This question aims to provide you a better understanding of adapting a pattern mining algorithm on real-world applications based on what you learned in class.
1. Understand a new problem and design an algorithm to solve it.
2. Implement a frequent contiguous sequential pattern mining algorithm to mine the frequent phrases from a text corpus.

## Problem Definition
A contiguous sequential pattern is a sequence of items that frequently appears as a consecutive subsequence in a database of many sequences. For example, if the corpus is

    good fish sandwich and french fries
    disgusting fish sandwich but good french fries 
    their fish sandwich is the best fish sandwich
    
and the minimum support is 2, then patterns like “fish sandwich” and “french fries” are both frequent contiguous sequential patterns, while the pattern “sandwich fries” is not a frequent contiguous sequential pattern because these two words are not consecutive to each other. Notice that “sandwich fries” is still a frequent sequential pattern though.

In this problem, the frequency is also defined differently: multiple appearances of a subsequence in a single sequence record count multiple times. The reason is that we want to find phrases, and a phrase can be repeated in a single sentence. For example, the pattern “fish sandwich” appears once in the first sequence, once in the second sequence and twice in the last, so its support should be calculated as 4. Another example: “A B A B A”. Subsequence “A B A” actually occurs twice, so the support is 2.

## Input Format
The input dataset is a text corpus. Each line is basically a sequence of strings separated by spaces. Note, punctuations are also considered as words, and are also separated by spaces.

Space is not a word. The lower case letters and upper case letters are different (i.e., ‘A’ and ‘a’ are two different words).

Be aware of the size of the input.

## Constraints
Minimum length is 2, maximum length is 5, and minimum support is 2. That is, the patterns have to contain at least two words, but no more than 5. The frequency of the patterns is no less than 2.

## Output Format
The output are the **most frequent 20 patterns** you mined out from the input dataset. The frequent patterns should be ordered according to their support from largest to smallest. Ties should be resolved by ordering the frequent patterns according to the ASCII order (increasing order).

Each line of the output should be in the format:

    [Support frequent-pattern] 
    [Support frequent-pattern] 
    ......
Please refer to the sample input and output below.

## Solution Approach
SPADE Algorithm is used to mine sequential contiguous patterns.

## Run as either
    python SeqConPatMin.py (Using Dictionary)
    
    python SequentialContiguousPatternMining.py (Using Pandas Dataframe)

## Imported Modules
- import sys
- import itertools
- import re
- from collections import OrderedDict
- import pandas as pd

## Requirements
- Python 3

## Dependencies
- None

### Sample Input
    good grilled fish sandwich and french fries , but the service is bad 
    disgusting fish sandwich , but good french fries
    their grilled fish sandwich is the best fish sandwich , but pricy 
    A B A B A B A

### Sample Output
    [4, 'fish sandwich '] 
    [3, ', but']
    [3, 'A B']
    [3, 'A B A']
    [3, 'B A']
    [2, 'A B A B']
    [2, 'A B A B A']
    [2, 'B A B']
    [2, 'B A B A']
    [2, 'fish sandwich ,']
    [2, 'fish sandwich , but ']
    [2, 'french fries']
    [2, 'grilled fries']
    [2, 'grilled fish sandwich '] [2, 'sandwich ,']
    [2, 'sandwich , but']
