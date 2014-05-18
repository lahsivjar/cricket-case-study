from os.path import join

import orange, orngAssoc
import utilities as util

def main():
    data = orange.ExampleTable(join(util.module_path(), "f_assoc"))
    data = orange.Preprocessor_discretize(data, method=orange.EquiNDiscretization(numberOfIntervals=4))

    rules = orange.AssociationRulesInducer(data, support=0.2)

    orngAssoc.sort(rules, ["confidence", "support"])
    orngAssoc.printRules(rules, ["support", "confidence"])


if __name__=="__main__":
    main()
