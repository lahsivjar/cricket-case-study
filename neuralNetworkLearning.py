from os.path import join

import Orange
import utilities as util

def main():
    data = Orange.data.Table(join(util.module_path(), "neural2010"))
    learner = Orange.classification.neural.NeuralNetworkLearner(n_mid=10, reg_fact=1.6, max_iter=300, normalize=True, name="Neural Network")

#####################################################################################
######################### FOR CROSSVALIDATION #######################################
##    print "Crossvalidation running ..."
##    result = Orange.evaluation.testing.cross_validation([learner], data, 5)
##    print "Accuracy: %.2f" % Orange.evaluation.scoring.CA(result)[0]
##    print "AUC:      %.2f" % Orange.evaluation.scoring.AUC(result)[0]
##    cm = Orange.evaluation.scoring.confusion_matrices(result)[0]
##    print "Confusion Matrix:: TP: %i, FP: %i, FN: %i, TN: %i" % (cm.TP, cm.FP, cm.FN, cm.TN)
#####################################################################################

    print "Learning please be patient ..."
    classifier = learner(data)

    pred_data = Orange.data.Table(join(util.module_path(), "neural2011"))

    write_file = open(join(util.module_path(), "neural2011Pred.txt"), "wb")

    print "Working on your predictions <Fingers crossed> ..."
    for ele in pred_data:
        pred = classifier(ele, Orange.classification.Classifier.GetProbabilities)[0]
        write_file.write(str(pred)+"\n")

    print "Done go and see the file ..."
    write_file.close()

if __name__=="__main__":
    main()
