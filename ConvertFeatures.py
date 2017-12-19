import sys #for system arguments
from collections import defaultdict
from collections import Counter
from itertools import dropwhile

features_file  = sys.argv[1]
feature_vecs_file  = sys.argv[2]
feature_map_file = sys.argv[3]

def readInputFile():
    """
    reads the input file.
    returns: input file.
    """
    with open(features_file) as inputFile:
        return inputFile.read()

def parseFile(File):
    """
    makes a list of words, tags, and word and tags pairs
    returns: words, tags, and words and tags pairs
    """
    featureHist = Counter()
    tagsAndFeatures = []
    tags = set()
    features = set()
    d = defaultdict(set)
    for sentence in File.split('\n')[:-1]: # add start tag for starting paragraph
        s = sentence.split()
        tags.add(s[0])
        features.update(s[1:])
        featureHist.update(s[1:])
        tagsAndFeatures.append(([s[0]],s[1:]))
        if s[1][:5] == 'form=':
            d[s[1][5:]].add(s[0])


    return tags, features, tagsAndFeatures, d, featureHist

def tagsToIdx(tags):
    """
    reads tags.
    returns: tag index dictionary.
    """
    return dict((tag, str(index)) for index, tag in enumerate(tags))

def featureToIdx(features):
    """
    reads features.
    returns: feature index dictionary starting from 1 for liblinear
    """
    return dict((feature, str(index+1)) for index, feature in enumerate(features))

def writeFeatureMap(featureMap,tagMap,feature_map_file, d):
    """
    writes features to features_file
    """
    f = open(feature_map_file, 'w')
    for feature,idx in featureMap.iteritems():
        f.write("%s %s\n" %(feature,int(idx)))
    f.write('tags\n')
    for tag,idx in tagMap.iteritems():
        f.write("%s %s\n" %(tag,int(idx)))
    f.write('dictionary\n')
    for word in d:
        f.write("%s" %word)
        for e in d[word]:
            f.write(" %s" % e)
        f.write("\n")
    f.close()

def featuresToVec(tagsAndFeatures, featureMap, tagsMap, feature_vecs_file, commonFeatures):
    """
    converts features to vectors
    """
    f = open(feature_vecs_file, 'w')
    for tag, features in tagsAndFeatures:
        res = []
        for feature in features:
            if feature in commonFeatures:
                res.append(int(featureMap[feature]))
        res.sort()
        f.write("%s " % tagsMap[tag[0]])
        f.write(':1 '.join(str(i) for i in res))
        f.write(':1\n')
    f.close()

if __name__ == '__main__':
    File = readInputFile()
    tags, features, tagsAndFeatures, d, featureHist= parseFile(File)
    for key, count in dropwhile(lambda key_count: key_count[1] >= 10, featureHist.most_common()):
        del featureHist[key]
    featureMap = featureToIdx(features)
    tagMap = tagsToIdx(tags)
    writeFeatureMap(featureMap, tagMap, feature_map_file, d)
    featuresToVec(tagsAndFeatures, featureMap, tagMap, feature_vecs_file, featureHist)

