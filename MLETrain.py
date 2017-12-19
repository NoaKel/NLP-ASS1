import sys #for system arguments
import itertools
from collections import Counter

input_file_name = sys.argv[1]
q_mle_filename = sys.argv[2]
e_mle_filename = sys.argv[3]

STUDENT={'name': 'Noa Yehezkel Lubin',
         'ID': '305097552'}

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
    words = []
    tags = []
    wordsAndTags = []
    for sentence in File.split('\n')[:-1]: # add start tag for starting paragraph
        tags.append('start')
        tags.append('start')
        for pair in sentence.split(' '):
            word, tag = pair.rsplit("/", 1) #if word contains / will be part of the word
            words.append(word)
            tags.append(tag)
            wordsAndTags.append((word, tag))
    return words, tags, wordsAndTags

def qMLECalc(tags):
    """
    Compute q (p(y)) MLE and write to q_mle_filename.
    tags: list of tags
    """
    # count triples, pairs and tags
    tripletHist = Counter(itertools.izip(tags,tags[1:],tags[2:]))
    pairsHist = Counter(itertools.izip(tags,tags[1:]))
    tagsHist = Counter(tags)

    #write MLE to file
    f = open(q_mle_filename, 'w')
    for tag1 in tagsHist:
        f.write("%s\t%d\n "% (tag1,tagsHist[tag1]))
        for tag2 in tagsHist:
            f.write("%s %s\t%d\n "% (tag1,tag2,pairsHist[(tag1, tag2)]))
            for tag3 in tagsHist:
                f.write("%s %s %s\t%d\n "% (tag1,tag2,tag3,tripletHist[(tag1, tag2, tag3)]))
    f.close()

def eMLECalc(words, tags, wordsAndTags):
    """
    Compute e (p(x/y)) MLE and write to e_mle_filename.
    words: list of words
    tags: list of tags
    wordsAndTags: pairs of words and their tag
    """
    
    # handle UNK words
    counter = Counter(words[:int(0.8*len(words))])
    #uniqueWords = set([word for word, appear in counter.iteritems() if appear == 1])
    for idx,(word,tag) in enumerate(wordsAndTags):
        if (idx > len(wordsAndTags)*0.8) and (word not in counter):
            wordsAndTags[idx] = (wordSign(word), tag)
    for idx,word in enumerate(words):
        if (idx > len(words)*0.8) and (word not in counter):
            words[idx] = (wordSign(word), tag)

    # count tags and wordsAndTags and write MLE to file
    wordAndTagsHist = Counter(wordsAndTags)
    
    f = open(e_mle_filename, 'w')
    for pair in wordAndTagsHist:
        f.write("%s %s\t%d\n" %(pair[0],pair[1],wordAndTagsHist[pair]))
    f.close()

def wordSign(word):
    try:
        word = float(word)
        return '*UNK-NUM*'
    except ValueError:
        pass  # it was a string, not an float.
    if len(word) >= 3 and word[-3:-2] == ':':
        return '*UNK-:*'
    if any(x == '-' for x in word):
        return '*UNK--*'
    if not word.isalpha():
        return '*UNK-char*'
    if word[-2:] == 'ed':
        return '*UNK-ED*'
    if word[-3:] == 'ing':
        return '*UNK-ING*'
    if word[-2:] == 'ly':
        return '*UNK-LY*'
    if word.isupper():
        return '*UNK-UPP*'
    if word.istitle():
        return '*UNK-TITLE*'
    if any(x.isupper() for x in word):
        return '*UNK-HAS-UPPER*'
    if word[-1:] == 's':
        return '*UNK-s*'
    if len(word) < 3:
        return '*UNK-SHORT*'
    else:
        return '*UNK-LONG*'
    #return '*UNK*'

if __name__ == '__main__':
    File = readInputFile()
    words, tags, wordsAndTags = parseFile(File)
    eMLECalc(words, tags, wordsAndTags)
    qMLECalc(tags)

