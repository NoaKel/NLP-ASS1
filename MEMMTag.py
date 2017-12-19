import sys #for system arguments
import numpy as np
import GreedyMaxEntTag as gmet
import liblin as ll
import datetime
input_file_name = sys.argv[1]
modelname = sys.argv[2]
out_file_name = sys.argv[3]
feature_map_file = sys.argv[4]

def vitterbiAlgorithm(lines, llp, featureMap, tagMap,wordTagDict, allTags):
    """
    viterbi algorithm O(words*tags^3)
    returns: tags for data
    """
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{('start', 'start'): 0}]
        bp = []
        for i, word in enumerate(line):
            maxProb = {}
            max_prob_tag = {}
            for t_tag, t in v[i]:
                history = gmet.build_history(i,line,t,t_tag)
                features = gmet.createFeatureLine(history,[])
                feature_indexes = gmet.convertToIndexes(features,featureMap)
                tags_with_prob = llp.predict(feature_indexes)

                for r in gmet.pruning(word,wordTagDict, allTags):
                    temp = v[i][(t_tag, t)] + np.log(tags_with_prob[str(tagMap[r])])
                    if (t, r) not in maxProb or temp > maxProb[(t, r)]:
                        maxProb[(t, r)] = temp
                        max_prob_tag[(t, r)] = t_tag
            v.append(maxProb)
            bp.append(max_prob_tag)
        print line_number
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
    llp = ll.LiblinearLogregPredictor(modelname)
    inputData = gmet.extractWords(input_file_name)
    featureMap, tagMap, wordTagDict, allTags = gmet.getFeatureIdxMap(feature_map_file)
    inputTags = vitterbiAlgorithm(inputData, llp, featureMap, tagMap,wordTagDict, allTags)
    realTags = gmet.extractRes('../ass1-tagger-test')
    accuracy = gmet.calulateAccuracy(inputTags, realTags)
    print "result: " + str(accuracy)
    open(out_file_name, 'w').write(gmet.tagInputData(inputData, inputTags))

