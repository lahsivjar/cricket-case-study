from os.path import join

import Orange
import utilities as util

def main():
    data = Orange.data.Table(join(util.module_path(), "keeper"))
    learner = Orange.classification.neural.NeuralNetworkLearner
    print "Learning please be patient ..."
    classifier = learner(data)

    #pred_data = Orange.data.Table("C:\Users\megamind\Documents\Python codes\\testCase2")

    write_file = open(join(util.module_path(), "keeper_prediction.txt"), "wb")

    print "Working on your predictions <Fingers crossed> ..."
    for ele in data:
        pred = classifier(ele, Orange.classification.Classifier.GetBoth)[0]
        write_file.write(str(pred)+"\n")

    print "Done go and see the file ..."
    write_file.close()

if __name__=="__main__":
    main()
