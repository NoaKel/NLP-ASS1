import sys #for system arguments
import numpy as np
from hmm2.GreedyTag import readFile, extractWords, extractRes, calulateAccuracy, tagInputData
from memm1.ExtractFeatures import createFeatureLine
from collections import defaultdict
import liblin as ll
input_file_name = sys.argv[1]
modelname = sys.argv[2]
out_file_name = sys.argv[3]
feature_map_file = sys.argv[4]


def greedyMaxEntTag(lines, llp, featureMap, tagMap,wordTagDict,allTags):
    """
    greedy algorithm O(words*tags)
    returns: tags for data
    """
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{('start', 'start'): 0}]
        prev_tag = 'start'
        prev_prev_tag = 'start'
        tags = []
        for i, word in enumerate(line):
            maxProb = - float("inf")
            maxTag = {}
            history = build_history(i,line,prev_tag,prev_prev_tag)
            features = createFeatureLine(history,[])
            feature_indexes = convertToIndexes(features,featureMap)
            tags_with_prob = llp.predict(feature_indexes)
            for r in pruning(word,wordTagDict, allTags):
                if maxProb < tags_with_prob[str(tagMap[r])]:
                    maxProb = tags_with_prob[str(tagMap[r])]
                    maxTag = r
            prev_prev_tag = prev_tag
            prev_tag = maxTag
            tags.append(maxTag)
        print line_number
        final_line_tags.append(tags)
    return final_line_tags

def getFeatureIdxMap(feature_map_file):
    """
    build feature to index dictionary
    feature_map_file : feature_map_file file path
    returns: feature_map_file
    """
    featureMap = {}
    tagMap = {}
    allTags = set()
    d = defaultdict(set)
    is_tag = 0
    is_dictionary = 0
    for line in readFile(feature_map_file):
        if line.strip('\n') == 'tags':
            is_tag = 1
        elif line.strip('\n') == 'dictionary':
            is_tag = 0
            is_dictionary = 1
        else:
            if is_tag:
                tag, idx = line.rsplit(" ", 1)
                tagMap[tag] = int(idx)
                allTags.add(tag)
            if is_dictionary:
                word, tags = line.split(" ", 1)
                d[word].update(tuple(tags.split()))
            else:
                feature, idx = line.rsplit(" ", 1)
                featureMap[feature] = int(idx)
    return featureMap, tagMap, d, allTags

def convertToIndexes(features,featureMap):
    """
    converts features to indexes
    returns: features indexes
    """
    res = []
    for f in features:
        if f in featureMap:
            res.append(featureMap[f])
    return res

def build_history(i,line,pt,ppt):
    """
    builds history
    """
    return {'wi': line[i],
            'wi-1': line[i - 1] if i > 0 else 'start',
            'wi-2': line[i - 2] if i > 1 else 'start',
            'wi+1': line[i + 1] if i < len(line) - 1 else 'end',
            'wi+2': line[i + 2] if i < len(line) - 2 else 'end',
            'ti-1': pt,
            'ti-2': ppt}

def pruning(word,wordTagDict,allTags):
    """
    pruning
    returns: possible tags
    """
    t = set()
    if word in wordTagDict:
        t = wordTagDict[word]
    else:
        t = allTags
    return t

if __name__ == '__main__':
    llp = ll.LiblinearLogregPredictor(modelname)
    inputData = extractWords(input_file_name)
    featureMap,tagMap, wordTagDict, allTags = getFeatureIdxMap(feature_map_file)
    inputTags = greedyMaxEntTag(inputData, llp, featureMap, tagMap,wordTagDict,allTags)
    realTags = extractRes('../ass1-tagger-test')
    accuracy = calulateAccuracy(inputTags, realTags)
    print "result: " + str(accuracy)
    open(out_file_name, 'w').write(tagInputData(inputData, inputTags))