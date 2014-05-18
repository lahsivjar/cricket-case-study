from pybrain.datasets import ClassificationDataSet
from pybrain.structure import FeedForwardNetwork

import pickle

def write_file(file_name, contents=None):
    w_file = open(file_name, 'wb')

    if contents is not None:
        w_file.write(contents)

def main():
    numberOfNet = 1
    file_prefix = 'neuralNet'
    #file_name = file_prefix + str(i)
    file_name = 'neuralNetBestBall'
    net = []

    for i in range(numberOfNet):
        fileObject = open(file_name, 'r')
        net.append(pickle.load(fileObject))

    csv = open('LASTBOWLER.csv', 'r')

    pid = []
    feature = 11
    output = 1

    dataset = ClassificationDataSet(feature, output)

    feature += 1

    header = csv.readline()

    for line in csv.readlines():
        data = [float(x) for x in line.strip().split(',') if x !='']
        pid.append(data[0])
        indata = tuple(data[1:feature])
        outdata = tuple(data[feature:])
        dataset.addSample(indata, outdata)

    dataset._convertToOneOfMany()

    temp  = 'PID\tTarget\tPlayerName\tRank\tProbablity\n'
    temp1 = "=VLOOKUP(A"
    temp2 = ",'[Dictionaries.xlsx]Player Codes'!$A$2:$B$3614,2,FALSE)"
    temp3 = "=VLOOKUP(A"
    #temp4 = ",'[Training Dataset.xlsx]2008 Rankings'!$A$2:$E$498,5,FALSE)"
    temp4 = ",'[Training Dataset.xlsx]2008 Rankings'!$A$2:$D$498,4,FALSE)"

    for i in range(len(dataset['input'])):
        value = ''
        for j in range(len(net)):
            value += str(net[j].activate(dataset['input'][i])[1]) + '\t'
        temp += str(pid[i]) + '\t' + str(dataset['class'][i]) + '\t' +\
                temp1 + str(i+2) + temp2 + '\t' + temp3 + str(i+2) + temp4 + \
                '\t' + value + '\n'

    write_file('Results.txt', temp)

if __name__=="__main__":
    main()
