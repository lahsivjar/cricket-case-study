#PID PlayerName DismissalRate Hscore Century HalfCentury RpW RpB<100> WinPercent
#Score = 50's + 100's + Ducks + HighScore + RpW^a * RpB<100>^b + RpW^y + RpB<100>^d
import scipy.stats as ss
import random
import math
import itertools

from pybrain.datasets import ClassificationDataSet

def write_file(file_name, contents=None, flag='wb'):
    w_file = open(file_name, flag)

    if contents is not None:
        w_file.write(contents)

def foo(var, w):
    a   = w[7]
    b   = w[8]
    y   = w[9]
    d   = w[10]

    score = 0.0
    l = 0
    eff_length = len(var) - 1
    for i in range(1, len(var)):
        for k in itertools.combinations(range(eff_length), i):
            temp = 1
            for j in k:
                temp = temp * var[j]
            score += w[l] * temp

            l += 1;
    return score

def fitness(var, w, getRank=False):
    score = []
    rank = []
    for i in var:
        score.append(foo(i, w))

    rank = ss.rankdata(score)

    count = 0
    assert(len(rank)==len(var))

    for i in range(len(rank)):
        tutu = rank[i] - var[i][-1]
        if(tutu != 0):
            count += 1

    fit = 1/(count+0.1)

    if getRank:
        return rank

    return fit

def mutation(fit, var, w):
    mutation_rate = 0.3
    for i in w:
        f_min = min(fit)
        i_swap = fit.index(f_min)
        p_ind = random.random()
        if p_ind < mutation_rate:
            w_temp = i
            index = random.randint(1,len(w_temp))
            index -= 1
            w_left = w_temp[:index]
            w_right = w_temp[index:]
            w_temp = w_right + w_left
            w_temp[index] = random.uniform(-1, 1)
            fit_score = fitness(var, w_temp)
            if fit_score-f_min > 0:
                w[i_swap] = w_temp
                fit[i_swap] = fit_score

    ret = [fit, w]
    return ret

def calc_fit_score(var, weight):
    fit_score = [0]*len(weight)

    for i in range(len(weight)):
        fit_score[i] = fitness(var, weight[i])

    print max(fit_score)
    return fit_score

def crossover(fit, var, w):
    crossover_rate = 0.6
    for k in range(len(w)/3):
        prob = random.random()
        if prob < crossover_rate:
            i = fit.index(max(fit)) + int(round(random.random()))
            j = random.randint(1, len(fit))
            j -= 1

            index = random.randint(1, len(w[i]))
            index -= 1

            wi_left = w[i][:index]
            wi_right = w[i][index:]

            wj_left = w[j][:index]
            wj_right = w[j][index:]

            w_i = wi_left + wj_right
            w_j = wj_left + wi_right

            fit_temp_i = fitness(var, w_i)
            fit_temp_j = fitness(var, w_j)

            fit_min = min(fit)
            index_min = fit.index(fit_min)

            if fit_temp_i-fit_min > 0:
                w[index_min] = w_i
                fit[index_min] = fit_temp_i

            fit_min = min(fit)
            index_min = fit.index(fit_min)

            if fit_temp_j-fit_min > 0:
                w[index_min] = w_j
                fit[index_min] = fit_temp_j

    ret = [fit, w]
    return ret


def main():
    csv = open('dataTour.csv', 'r')
    pid = []
    var = []
    population_size = 75
    maxRange = 100
    maxWeightRange = 63
    count = 0

    weight = [[0]*maxWeightRange]*population_size

    header = csv.readline()

    for line in csv.readlines():
        data = [float(x) for x in line.strip().split(',') if x!='']
        pid.append(data[0])
        v = tuple(data[6:])
        var.append(v)

    for i in range(population_size):
        for j in range(maxWeightRange):
            weight[i][j] = random.uniform(-1, 1)

    fit_score = calc_fit_score(var, weight)
    for i in range(1000000):
        [fit_score, weight] = crossover(fit_score, var, weight)
        [fit_score, weight] = mutation(fit_score, var, weight)
        #print weight[0]
        print max(fit_score)
        if (i%10000)==0:
            print 'Printing rank to file\n'
            rank = fitness(var, weight[fit_score.index(max(fit_score))], True)
            temp = ''
            for k in rank:
                temp += str(k) + '\n'
            file_name = 'rankat' + str(count) + '.txt'
            write_file(file_name, temp, 'wb')
            file_name = 'weightsGA' + '.txt'
            write_file(file_name, str(count) + '\t' + str(weight[fit_score.index(max(fit_score))]) + '\n', 'a')
            count += 1


if __name__ == "__main__":
    main()
