import sys
import numpy as np
from hmm1.MLETrain import wordSign
from collections import defaultdict
input_file_name = sys.argv[1]
q_mle_filename = sys.argv[2]
e_mle_filename = sys.argv[3]
output_file_name = sys.argv[4]

STUDENT={'name': 'Noa Yehezkel Lubin',
         'ID': '305097552'}

def greedyAlgorithm(lines, e_mle, q_mle, wordTagDict, num_of_words):
    """
    greedy algorithm O(words*tags)
    returns: tags for data
    """
    final_line_tags = []
    for line_number, line in enumerate(lines):
        prev_tag = 'start'
        prev_prev_tag = 'start'
        tags = []
        for i, word in enumerate(line):
            if (word not in wordTagDict) and (word.lower() in wordTagDict):
                word = word.lower()
            if word not in wordTagDict:
                word = wordSign(word)
            maxProb = - float("inf")
            maxProbTag = 'start'
            for r in wordTagDict[word]:
                e = smooth(e_mle, (word, r), q_mle)
                if e != 0.0:
                    q = backoff(q_mle,num_of_words,r, prev_tag, prev_prev_tag)
                    temp = np.log(q) + np.log(e)
                    if temp > maxProb:
                        maxProb = temp
                        maxProbTag = r
            prev_prev_tag = prev_tag
            prev_tag = maxProbTag
            tags.append(maxProbTag)
        print line_number
        final_line_tags.append(tags)
    return final_line_tags

def readFile(filePath):
    """
    reads input file
    returns: file
    """
    with open(filePath) as inputFile:
        return inputFile.readlines()

def backoff(q_mle,num_of_words,a,b,c):
    """
    backoff interpulation
    returns: p(c/a,b)
    """
    lambda1 = 0.8
    lambda2 = 0.099
    return lambda1 * float(q_mle[(a,b,c)])/max(float(q_mle[(a,b)]),1) \
           + lambda2 * float(q_mle[(b,c)])/float(q_mle[b,]) \
           + (1.0 - lambda2 - lambda1) * float(q_mle[c,])/num_of_words

def smooth(e_mle, param, tags):
    """
    e_mle smoothing for words and tags that haven't been seen
    e_mle : e_mle
    param : word, tag
    tags: tags count
    returns: smooth emle
    """
    if param not in e_mle:
        return 1/sum(e_mle.values())
    else:
        return float(e_mle[param])/float(tags[(param[1],)])


def allTags(q_mle):
    """
    makes a set of all seen tags
    q_mle_lines : q_mle
    returns: tags
    """
    tags = set()
    for line in q_mle:
        tags.update(line[:3])
    return tags

def wordTagDict(e_mle):
    """
    makes a dictionary for each word the tags it can have
    q_mle_lines : q_mle
    returns: dictionary
    """
    d = defaultdict(set)
    for word,tag in e_mle:
        d[word].add(tag)
    return d

def parseMLEFile(filePath):
    """
    parses e-mle and q-mle file under the assupmtion key<tab>value
    file_path : mle file path
    returns: mle
    """
    mle = {}
    for line in readFile(filePath)[:-1]:
        key, val = line.rsplit("\t", 1)
        tags = key.split()
        mle[tuple(tags)] = int(val)
    return mle

def extractWords(filePath):
    """
    extract words from file
    file_path :  file path
    returns: words
    """
    return [line[:-1].split(' ') for line in readFile(filePath)]


def real_tag_lines(args):
    pass


def calulateAccuracy(inputTags, realTags):
    total = good = 0
    for i, line in enumerate(inputTags):
        for j, tag in enumerate(line):
            total += 1
            if tag == realTags[i][j]:
                good += 1
    return float(good) / total


def extractRes(test_file):
    return [sp(line) for line in extractWords(test_file)]


def sp(line):
    return [word_tag.rsplit('/', 1)[-1] for word_tag in line]


def tagInputData(InputData, inputTags):
    """
    parses e-mle and q-mle file under the assumption key<tab>value
    InputData : untagged sentences
    tag_lines: tags for sentences
    returns: word and its tag
    """
    output = ''
    for i, line in enumerate(InputData):
        for j, word in enumerate(line):
            output += word + '/' + inputTags[i][j] + ' '
        output += '\n'
    return output


if __name__ == '__main__':
    inputData = extractWords(input_file_name)
    q_mle = parseMLEFile(q_mle_filename)
    e_mle = parseMLEFile(e_mle_filename)
    inputTags = greedyAlgorithm(inputData, e_mle, q_mle, wordTagDict(e_mle),sum(e_mle.values()))
    #realTags = extractRes('../ass1-tagger-test')
    #accuracy = calulateAccuracy(inputTags, realTags)
    #print "result: " + str(accuracy)
    open(output_file_name, 'w').write(tagInputData(inputData, inputTags))
