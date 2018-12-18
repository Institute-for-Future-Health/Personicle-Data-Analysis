import csv

from sklearn import svm
from sklearn.model_selection import cross_validate
from sklearn.svm import SVC

from SupervisedLearning import Experiment
from makeData import makeData
from paper_exp import paper_exp
import math
import numpy as np
import seaborn as sns

# name = 'Jordan'
name = 'Ramesh'
# name = 'Pooya'

date = '0601'
symbolicDataPath = name + '/symbolicResultHomeEvent'

lifelogPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-lifeLog-export-' + name + '-' + date + '-2018.json'
segmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-' + name + '-' + date + '-2018.json'
testSetPath = '/Users/hyungiko/Desktop/Personicle Data/' + name + '/normalizedeveningResult_' + name + '_test.csv'

timeType = 'evening'


# timeType = 'afternoon'

# timeType = 'morning'

def trainAll(interval: int):
    totalList = []
    trainAllLabel = []

    # name = 'Ramesh'
    # segmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-' + name + '-' + date + '-2018.json'
    #
    # mMakeData = makeData(segmentPath, symbolicDataPath, timeType, name)
    # experiment = Experiment(mMakeData, timeType)
    # totalList = experiment.svm_train_per_person(name, totalList)
    # trainAllLabel = experiment.get_all_label()

    name = 'Jordan'
    segmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-' + name + '-' + date + '-2018.json'

    mMakeData = makeData(segmentPath, symbolicDataPath, timeType, name)
    experiment = Experiment(mMakeData, timeType)
    totalList = experiment.svm_train_per_person(name, totalList, interval)

    for value in experiment.get_all_label():
        trainAllLabel.append(value)

    print(len(totalList))
    print(len(trainAllLabel))

    experiment.svm_train_all(timeType, totalList, trainAllLabel)


def testAll(interval: int):
    # model = 'svm'
    #
    # experiment = Experiment(mMakeData, timeType)
    # experiment.testAddPrevEating(model)

    totalList = []
    trainAllLabel = []

    # name = 'Jordan'
    name = 'Ramesh'
    # name = 'Pooya'

    segmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-' + name + '-' + date + '-2018.json'

    mMakeData = makeData(segmentPath, symbolicDataPath, timeType, name)
    experiment = Experiment(mMakeData, timeType)
    totalList = experiment.svm_train_per_person(name, totalList, interval)

    for value in experiment.get_all_label():
        trainAllLabel.append(value)

    print(len(totalList))
    print(len(trainAllLabel))

    experiment.test_for_each(totalList, trainAllLabel)


def svm_train_all():
    duration = 5
    path = '/Users/hyungiko/Desktop/Personicle Data/Train/eveningTrain_' + str(duration) + 'm_' + name + '.csv'

    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        trainTotal = []
        trainAllLabel = []
        for row in readCSV:
            trainTotal_temp = []
            trainTotal_temp.append(row[0])
            trainTotal_temp.append(float(row[1]))
            trainTotal_temp.append(float(row[2]))
            trainTotal_temp.append(float(row[3]))
            trainTotal_temp.append(float(row[4]))
            trainTotal_temp.append(float(row[5]))
            trainTotal_temp.append(float(row[6]))
            trainTotal_temp.append(float(row[7]))
            trainTotal_temp.append(float(row[8]))
            trainTotal_temp.append(float(row[9]))
            trainTotal.append(trainTotal_temp)
            trainAllLabel.append(int(row[9]))

    trainTotal = makeTrainSet(trainTotal)
    scoring = ['accuracy', 'precision', 'recall', 'f1']

    clf = svm.SVC(kernel='linear', C=1)

    X = np.array(np.array(trainTotal))
    y = np.array(np.array(trainAllLabel))

    scores = cross_validate(clf, X, y, scoring=scoring, cv=10)
    print('test_accuracy:', scores['test_accuracy'])
    print('test_precision:', scores['test_precision'])
    print('test_recall:', scores['test_recall'])
    print('test_f1:', scores['test_f1'])


def testAll(interval: int):
    # model = 'svm'
    #
    # experiment = Experiment(mMakeData, timeType)
    # experiment.testAddPrevEating(model)

    totalList = []
    trainAllLabel = []

    name = 'Jordan'
    # name = 'Ramesh'
    # name = 'Pooya'

    segmentPath = '/Users/hyungiko/Desktop/Personicle Data/json/personicle-1498515264813-segment-export-' + name + '-' + date + '-2018.json'

    mMakeData = makeData(segmentPath, symbolicDataPath, timeType, name)
    experiment = Experiment(mMakeData, timeType)
    totalList = experiment.svm_train_per_person(name, totalList, interval)

    for value in experiment.get_all_label():
        trainAllLabel.append(value)

    print(len(totalList))
    print(len(trainAllLabel))

    experiment.test_for_each(totalList, trainAllLabel)


def makeTrainSet(_tempTotalData: list) -> list:
    isEaten = False
    trainTotal = []

    length = len(_tempTotalData[0])
    for i in range(0, len(_tempTotalData)):
        newData = list(_tempTotalData[i])[1:length - 1]
        key = list(_tempTotalData[i])[0]
        label = int(list(_tempTotalData[i])[length - 1])

        # _trainAllLabel.append(label)
        if int(label) == 1:
            newData.append(0)
            trainTotal.append(newData)
            isEaten = True
        else:

            if i > 0 and _tempTotalData[i][0][0:4] != _tempTotalData[i - 1][0][0:4]:
                # date changed
                isEaten = False

            if isEaten:
                newData.append(10)
                trainTotal.append(newData)
            else:
                newData.append(0)
                trainTotal.append(newData)

    return trainTotal


if __name__ == "__main__":
    # svm_train_all()

    # valueType = 'symbol'
    mMakeData = makeData(segmentPath, symbolicDataPath, timeType, name)

    mMakeData.convertContinuousToDiscrete()
    # mMakeData.buildSampleSetWithHRandPrevSeg()
    # mMakeData.buildSymbolicResultCsv()
    # test = mMakeData.get_segment_size()

    # print(test)
    # dis_below_5 = 0
    # dis_below_20 = 0
    # dis_below_else = 0
    #
    # for count in range(0, len(test)):
    #     if int(test[count]) < 5:
    #         dis_below_5 = dis_below_5 + 1
    #     elif 5 <= int(test[count]) <= 30:
    #         dis_below_20 = dis_below_20 + 1
    #     else:
    #         dis_below_else = dis_below_else + 1
    #
    # total = dis_below_5 + dis_below_20 + dis_below_else
    # print(total)
    # print(dis_below_5, ',', dis_below_20, ',', dis_below_else)

    # sns.distplot(test, kde=False, rug=True);
    # sns.distplot(test)
    model = 'svm'

    # trainAll(10)
    # testAll(10)

    # experiment = Experiment(mMakeData, timeType)
    # experiment.svm_train()
    # experiment.svm_train_all(timeType)
    # experiment.decision_tree_train()
    # experiment.gaussian_nb()
    # experiment.test(model)
    # experiment.testAll(model)
    # experiment.testAddPrevEating(model)

    path = '/Users/hyungiko/Desktop/Personicle Data/Jordan/mm_paper.csv'
    mPaper_exp = paper_exp(path)
    # mPaper_exp.extractData()
    # mPaper_exp.drawFigure()
    # mPaper_exp.bar_plt()
    mPaper_exp.bar_first_fig()
    # mPaper_exp.figure_time_by()
    print('makeData Done')
