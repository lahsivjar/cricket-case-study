#LOGISTIC REGRESSION
from os.path import join

import Orange
import utilities as util

data = Orange.data.Table(join(util.module_path(), "orangeDataMvrNorm"))
print "Learning please be patient ..."
lr = Orange.classification.logreg.LogRegLearner(data, remove_singular=1)

print "Loading test data ..."
test_data = Orange.data.Table(join(util.module_path(), "testCase2"))
write_file = open(join(util.module_path(), "prediction.txt"), "wb")

print "Working on your predictions <Fingers crossed> ..."

for ex in data:
    write_file.write(str(lr(ex))+"\n")

print "Done go and see the file :)"
Orange.classification.logreg.dump(lr)
