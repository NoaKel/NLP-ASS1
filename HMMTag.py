import sys
import numpy as np
import GreedyTag as gt
import operator

from collections import defaultdict
input_file_name = sys.argv[1]
q_mle_filename = sys.argv[2]
e_mle_filename = sys.argv[3]
output_file_name = sys.argv[4]

STUDENT={'name': 'Noa Yehezkel Lubin',
         'ID': '305097552'}

def vitterbiAlgorithm(lines, e_mle, q_mle, wordTagDict, num_of_words):
    """
    vitterbi algorithm O(words*tags^3)
    returns: tags for data
    """
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{('start', 'start'): 0}]
        bp = []
        for i, word in enumerate(line):
            if (word not in wordTagDict) and (word.lower() in wordTagDict):
                word = word.lower()
            if word not in wordTagDict:
                word = gt.wordSign(word)
            maxProb = {}
            maxTag = {}
            for t_tag, t in v[i]:
                for r in wordTagDict[word]:
                    e = gt.smooth(e_mle, (word, r), q_mle)
                    if e != 0.0:
                        q = gt.backoff(q_mle,num_of_words,t_tag, t, r)
                        temp = v[i][(t_tag, t)]*q*e
                        if (t, r) not in maxProb or temp > maxProb[(t, r)]:
                            maxProb[(t, r)] = temp
                            maxTag[(t, r)] = t_tag
            v.append(maxProb)
            bp.append(maxTag)
        print line_number
        # the final step
        before_last_tag, last_tag = max(v[-1], key=lambda tuple: tuple[-1])
        line_tags = [last_tag]
        if before_last_tag != 'start':
            line_tags.append(before_last_tag)
        for j in xrange(len(v) - 2, 1, -1):
            prev_t = bp[j][(before_last_tag, last_tag)]
            line_tags.append(prev_t)
            last_tag = before_last_tag
            before_last_tag = prev_t
        final_line_tags.append(list(reversed(line_tags)))

    return final_line_tags

if __name__ == '__main__':
    inputData = gt.extractWords(input_file_name)
    q_mle = gt.parseMLEFile(q_mle_filename)
    e_mle = gt.parseMLEFile(e_mle_filename)
    inputTags = vitterbiAlgorithm(inputData, e_mle, q_mle, gt.wordTagDict(e_mle),sum(e_mle.values()))
    realTags = gt.extractRes('../ass1-tagger-test')
    accuracy = gt.calulateAccuracy(inputTags, realTags)
    print "result: " + str(accuracy)
    open(output_file_name, 'w').write(gt.tagInputData(inputData, inputTags))
