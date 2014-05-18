from pybrain.datasets import ClassificationDataSet
from pybrain.utilities import percentError
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.structure import FullConnection
from pybrain.supervised.trainers import BackpropTrainer

import pickle

def printError(epochs, trainresult, testresult=None):
    #Print train error and testerror(if given)
    print "Epoch: %4d" % epochs, \
          "    train error: %5.2f%%" % trainresult
    if(testresult is not None):
        print "    test error: %5.2f%%" % testresult

def write_file(file_name, contents=None):
    w_file = open(file_name, 'wb')

    if contents is not None:
        w_file.write(contents)

def main():
    #Load the dataset
    #Batsman done through DA Which is DA<Bat> sheet in NNT.xlsx
    #Bowler done through DABa Which is DA<Ball> sheet in NTT.xlsx
    csv = open('DABa.csv', 'r')
    test_data = False
    print_dataset_info = True
    hidden_neurons = 9
    feature = 11
    output = 1

    complete_dataset = ClassificationDataSet(feature, output)
    test_dataset = ClassificationDataSet(feature, output)
    train_pid = []

    feature += 1

    header = csv.readline()

    for line in csv.readlines():
        data = [float(x) for x in line.strip().split(',') if x!='']
        train_pid.append(data[0])
        indata = tuple(data[1:feature])
        outdata = tuple(data[feature:])
        complete_dataset.addSample(indata, outdata)

    if test_data:
        csv_test = open('DT.csv', 'r')
        test_dataset = ClassificationDataSet(feature-1, output)
        test_pid = []
        header = csv_test.readline()

        for line in csv_test:
           data = [float(x) for x in line.strip().split(',') if x!='']
           test_pid.append(data[0])
           indata = tuple(data[1:feature])
           outdata = tuple(data[feature:])
           test_dataset.addSample(indata, outdata)

        test_dataset._convertToOneOfMany()

##    testdata, traindata = complete_dataset.splitWithProportion(0.2)
##
##    testdata._convertToOneOfMany()
##    traindata._convertToOneOfMany()

    complete_dataset._convertToOneOfMany()

    if print_dataset_info:
        print "Number of training patterns: ", len(complete_dataset)
        print "Input and output dimension: ", complete_dataset.indim, complete_dataset.outdim
        print "First Sample (input, target): "
        print complete_dataset['input'][0], complete_dataset['target'][0], complete_dataset['class'][0]
        print complete_dataset['input'][1], complete_dataset['target'][1], complete_dataset['class'][1]

    #Build a network
    feedForwardNetwork = FeedForwardNetwork()
    inLayer = LinearLayer(complete_dataset.indim, name="InputLayer")
    hiddenLayer = LinearLayer(hidden_neurons, name="HiddenLayer")
    outLayer = LinearLayer(complete_dataset.outdim, name="OutputLayer")

    feedForwardNetwork.addInputModule(inLayer)
    feedForwardNetwork.addModule(hiddenLayer)
    feedForwardNetwork.addOutputModule(outLayer)

    #in_to_out = FullConnection(inLayer, outLayer, name="InputToOutput")
    in_to_hidden = FullConnection(inLayer, hiddenLayer, name="InputToHidden")
    hidden_to_out = FullConnection(hiddenLayer, outLayer, name="HiddenToOutput")

    #feedForwardNetwork.addConnection(in_to_out)
    feedForwardNetwork.addConnection(in_to_hidden)
    feedForwardNetwork.addConnection(hidden_to_out)

    feedForwardNetwork.sortModules()

    #Set up a trainer
    trainer = BackpropTrainer(feedForwardNetwork, dataset = complete_dataset, momentum = 0.1, verbose = False)

    #Start training
    maxRange = 20
    for i in range(maxRange):
        print "Completed %d\n" % ((i*100)/maxRange)
        trainer.trainEpochs(5)

##    trainer.trainUntilConvergence()

    #Validation
    train = trainer.testOnClassData()
    trainresult = percentError(train, complete_dataset['class'])
##    testresult = percentError(trainer.testOnClassData(dataset = testdata), testdata['class'])

    if test_data:
        test = trainer.testOnClassData(dataset = test_dataset)
        testresult = percentError(test, test_dataset['class'])

        printError(trainer.totalepochs, trainresult, testresult)
    else:
        printError(trainer.totalepochs, trainresult)

    #Print and save the weights and also the result Also Save The Probability
    temp = 'PID\tTarget\tPred\tPlayerName\tRank\tProbablity\tRankFromPred\n'
    temp1 = "=VLOOKUP(A"
    temp2 = ",'[Training Dataset.xlsx]2008 Rankings'!$A$2:$D$498,2,FALSE)"
    temp3 = "=VLOOKUP(A"
    temp4 = ",'[Training Dataset.xlsx]2008 Rankings'!$A$2:$E$498,5,FALSE)"
    #temp4 = ",'[Training Dataset.xlsx]2008 Rankings'!$A$2:$D$498,4,FALSE)"
    temp5 = "=RANK(F"
    temp6 = ",$F$2:$F$67)"
    for i in range(len(train)):
        temp += str(train_pid[i]) + '\t' + str(complete_dataset['class'][i]) + '\t' +\
                str(train[i]) + '\t' + temp1 + str(i+2) + temp2 + '\t' + temp3 + str(i+2) + temp4 + \
                '\t' + str(feedForwardNetwork.activate(complete_dataset['input'][i])[1]) + '\t' + \
                temp5 + str(i+2) + temp6 + '\n'

    write_file('Weights.txt', str(feedForwardNetwork.params))
    write_file('Result.txt', temp)

    #Dump the network to a file
    fileObject = open('neuralNet', 'wb')
    pickle.dump(feedForwardNetwork , fileObject)



if __name__=="__main__":
    main()
