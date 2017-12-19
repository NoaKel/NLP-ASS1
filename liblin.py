import numpy as np
from codecs import open

class LiblinearLogregPredictor(object):
    def __init__(self, model_file_name):
        self.weights = {} # dict of feat-num -> numpy array, where array is the per-class values
        with open(model_file_name) as fh:
            solver_type = fh.next().strip()
            nr_classes  = fh.next().strip()
            label       = fh.next().strip()
            nr_feature  = fh.next().strip()
            bias        = fh.next().strip()
            w           = fh.next().strip()
            assert(w == "w")
            assert(nr_classes.startswith("nr_class"))
            assert(nr_feature.startswith("nr_feature"))
            assert(label.startswith("label"))
            nr_classes = int(nr_classes.split()[-1])
            for i,ws in enumerate(fh,1):
                ws = [float(x) for x in ws.strip().split()]
                if all([x==0 for x in ws]): continue # skip unused features
                assert len(ws) == nr_classes, "bad weights line %s" % i
                self.weights[i] = np.array(ws)
            self.bias = float(bias.split()[-1])
            self.labels = label.split()[1:]

    def predict(self, feature_ids):
        weights = self.weights
        scores = np.zeros(len(self.labels))
        for f in feature_ids:
            if f in weights: scores += weights[f]
        scores = 1/(1+np.exp(-scores))
        scores = scores/np.sum(scores)
        return dict(zip(self.labels, scores))
