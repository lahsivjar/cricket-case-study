from os.path import join

import orange
import utilities as util

def main():
    data_path = join(util.module_path(), "data_path");
    data = orange.ExampleTable(data_path)

    print "Continuous attributes:"
    for a in range(len(data.domain.attributes)):
        if data.domain.attributes[a].varType == orange.VarTypes.Continuous:
            d = 0.; n = 0
            for e in data:
                if not e[a].isSpecial():
                    d += e[a]
                    n += 1
            print "  %s, mean=%3.2f" % (data.domain.attributes[a].name, d/n)

    print "\nNominal attributes (contingency matrix for classes:", data.domain.classVar.values, ")"
    cont = orange.DomainContingency(data)
    for a in data.domain.attributes:
        if a.varType == orange.VarTypes.Discrete:
            print "  %s:" % a.name
            for v in range(len(a.values)):
                sum = 0
                for cv in cont[a][v]:
                    sum += cv
                print "    %s, total %d" % (a.values[v], sum)#, %s" % (a.values[v], sum, cont[a][v])
            print

if __name__=="__main__":
    main()
