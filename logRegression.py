from os.path import join

import Orange
import utilities as util

data = Orange.data.Table(join(util.module_path(), "orangeDataMvrNorm"))
lr = Orange.classification.logreg.LogRegLearner(data, remove_singular=1)
ones = 0
for ex in data:
 	if lr(ex)=='1':
 		ones += 1

print str(ones)
