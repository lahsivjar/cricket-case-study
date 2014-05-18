from os.path import join

import Orange
import utilities as util

def accuracy(test_data, classifier):
    correct = 0.0
    for ex in test_data:
        if classifier(ex) == ex.getclass():
            correct += 1

    correct = correct / len(test_data)
    print "Classification accuracy: ", correct

def main():
    data = Orange.data.Table(join(util.module_path(), "NeuralSheet.tab"))
    learner = Orange.classification.neural.NeuralNetworkLearner(n_mid=20, reg_fact=0.6, max_iter=100, normalize=True, name="Neural Network")

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
    neural = learner(data)
    neural.name = "Neural Network"

    accuracy(data, neural)

    pred_data = Orange.data.Table(join(util.module_path(), "NeuralSheetTest.tab"))

    write_file = open(join(util.module_path(), "Pred.txt"), "wb")

    print "Working on your predictions <Fingers crossed> ..."
    for ele in pred_data:
        pred = neural(ele, Orange.classification.Classifier.GetBoth)[0]
        write_file.write(str(pred)+"\n")

    print "Done go and see the file ..."
    write_file.close()

if __name__=="__main__":
    main()
