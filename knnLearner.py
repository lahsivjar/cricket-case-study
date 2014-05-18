from os.path import join

import Orange
import utilities as util

def main():
    data_path = join(util.module_path(), "orangeDat")
    data = Orange.data.Table(data_path)
    learner = Orange.classification.knn.kNNLearner()
    learner.k = 10
    print "Learning please be patient ..."
    classifier = learner(data)

    pred_data = Orange.data.Table(join(util.module_path(), "testCase2"))

    write_file = open(join(util.module_path(), "prediction.txt"), "wb")

    print "Working on your predictions <Fingers crossed> ..."
    for ele in pred_data:
        pred = classifier(ele, Orange.classification.Classifier.GetBoth)[0]
        write_file.write(str(pred)+"\n")

    print "Done go and see the file ..."
    write_file.close()

if __name__=="__main__":
    main()
