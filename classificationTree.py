from os.path import join

import Orange
import utilities as util

def main():
    data_path = join(util.module_path(), "..\\tabFile\newData2");
    data = Orange.data.Table(data_path)

    print "Learning please be patient ..."
    classification_tree = Orange.classification.tree.TreeLearner(data)

    print "Saving tree to file ..."
    classification_tree.dot(file_name=join(util.module_path(), "0.dot"), node_shape="ellipse", leaf_shape="box")

##    pred_data = Orange.data.Table("C:\Users\megamind\Documents\Python codes\\testCase2")
##
##    write_file = open("C:\Users\megamind\Documents\Python codes\prediction.txt", "wb")
##
##    print "Working on your predictions <Fingers crossed> ..."
##    for ele in pred_data:
##        pred = classification_tree(ele, Orange.classification.Classifier.GetBoth)[0]
##        write_file.write(str(pred)+"\n")
##
##    print "Done go and see the file ..."
##    write_file.close()

if __name__=="__main__":
    main()
