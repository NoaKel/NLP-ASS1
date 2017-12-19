import sys #for system arguments
from collections import Counter
input_file_name = sys.argv[1]
features_file = sys.argv[2]

def readInputFile():
    """
    reads the input file.
    returns: input file.
    """
    with open(input_file_name) as inputFile:
        return inputFile.read()

def parseFile(File):
    """
    makes a list of words, tags, and word and tags pairs
    File : input file
    returns: words, tags, and words and tags pairs
    """
    wordsAndTags = []
    words = []
    for sentence in File.split('\n')[:-1]: # add start tag for starting paragraph
        s = []
        m = []
        for pair in sentence.split(' '):
            word, tag = pair.rsplit("/", 1) #if word contains / will be part of the word
            s.append((word, tag))
            words.append(word)
        wordsAndTags.append(s)
    return words, wordsAndTags


def createFeatureLine(history,uniqueWords):
    """
    writes features for each word and tag pair
    history : [wi-2,wi-1,wi,wi+1,wi+2,ti,ti-2,ti-1]
    returns: feature line
    """
    features = []
    word = history['wi']
    #tag
    if uniqueWords:
        features.append(str(history['ti']))
    #features
    if word in uniqueWords or not uniqueWords:
        for i in xrange(1, min(5, len(word))):
            features.append('prefix'+str(i)+'='+word[:i])
        for i in xrange(1, min(5, len(word))):
            features.append('suffix'+str(i)+'='+word[-i:])
        if any(x.isdigit() for x in word):
            features.append('has_number')
        if any(x.isupper() for x in word):
            features.append('has_upper')
        if '-' in word:
            features.append('contains_hyphen')
    if word not in uniqueWords or not uniqueWords:
        features.append('form=' + str(word))
    #for every word:
    features.append('pt='+str(history['ti-1']))
    features.append('ppt='+str(history['ti-1']+'^'+str(history['ti-2'])))
    features.append('pw='+str(history['wi-1']))
    features.append('ppw='+str(history['wi-2']))
    features.append('nw='+str(history['wi+1']))
    features.append('nnw='+str(history['wi+2']))
    return features

def writeToOutput(words, wordsAndTags, features_file):
    """
    writes features to features_file
    wordsAndTags : word and tags list
    """
    counter = Counter(words)
    uniqueWords = set([word for word, appear in counter.iteritems() if appear <= 5])
    f = open(features_file, 'w')
    for list in wordsAndTags:
        for i, val in enumerate(list):
            f.write(" ".join(createFeatureLine(build_history(i,list),uniqueWords)))
            f.write("\n")
    f.close()

def build_history(i,list):
    """
    builds history
    i: word index
    list: line
    """
    return {'wi': list[i][0],
            'wi-1': list[i - 1][0] if i > 0 else 'start',
            'wi-2': list[i - 2][0] if i > 1 else 'start',
            'wi+1': list[i + 1][0] if i < len(list) - 1 else 'end',
            'wi+2': list[i + 2][0] if i < len(list) - 2 else 'end',
            'ti': list[i][1],
            'ti-1': list[i - 1][1] if i > 0 else 'start',
            'ti-2': list[i - 2][1] if i > 1 else 'start'}

if __name__ == '__main__':
    File = readInputFile()
    words, wordsAndTags = parseFile(File)
    writeToOutput(words, wordsAndTags, features_file)