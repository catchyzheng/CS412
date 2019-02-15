import copy
import random
import sys
import time

import DecisionTree as DT
from collections import defaultdict


if __name__ == '__main__':
    start_time = time.time()

    arg = sys.argv
    train_file = open(arg[1], 'r')
    test_file = open(arg[2], 'r')

    label_dict = defaultdict(int)

    # build training set
    line_cnt = 0 # training line count
    training = []
    for line in train_file:
        lst = line.split(' ')
        label = int(lst[0])
        if label not in label_dict: label_dict[label] = 1

        sample = [int(ele.split(':')[1]) for ele in lst[1:]]
        sample.append(int(lst[0]))
        training.append(sample)
        line_cnt += 1

    # build testing set
    testing = []
    length = -1
    for line in test_file:
        lst = line.split(' ')
        if length < 0: length = len(lst) - 1
        sample = [int(ele.split(':')[1]) for ele in lst[1:]]
        sample.append(int(lst[0]))
        testing.append(sample)


    attri_labels = []

    if arg[1] == 'synthetic.social.train':
        attri_labels = [i for i in range(length)]
    else:
        attri_labels = [i for i in range(1, length + 1)]

    tree_num = 1
    if arg[1] == 'nursery.train':
        tree_num = 10
    elif arg[1] == 'led.train':
        tree_num = 10
    elif arg[1] == 'balance.scale.train':
        tree_num = 10
    else:
        tree_num = 20

    random_forest = []
    random_attribute_list = []

    for _ in range(tree_num):
        random_training = random.sample(training, int(line_cnt * 0.9))

        '''
        random_training = []
        for i in range(line_cnt):
            num = random.randint(0, line_cnt-1)
            random_training.append(training[num])
        '''

        random_attribute = []
        if arg[1] != 'synthetic.social.train':
            random_attribute = random.sample(attri_labels, length)
        else: random_attribute = random.sample(attri_labels, min(90, length))
        '''
        random_attribute = []
        cnt = 0
        for i in range(2*length):
            num = random.randint(0, length-1)
            if attriLabels[num] not in random_attribute:
                random_attribute.append(attriLabels[num])
                if len(random_attribute) >= length:
                    break
        '''


        # print random_attribute
        random_attribute_list.append(sorted(random_attribute))
        random_forest.append(DT.create_tree(random_training, sorted(random_attribute), copy.copy(attri_labels)))


    # print 'depth', depth, 'attri num', length

    attri_num = len(label_dict)
    confusion_mat = [[0 for _ in range(attri_num)] for __ in range(attri_num)]
    total = len(testing)  # length of testing
    accruate_cnt = 0


    for testSam in testing:
        dic = defaultdict(int)
        decision = -1
        majority = -1
        for i in range(tree_num):
            # print random_attribute_list[i]
            pred_val = DT.classify(random_forest[i], random_attribute_list[i], copy.copy(attri_labels), testSam[:-1])
            dic[pred_val] += 1
            if dic[pred_val] > majority:
                majority = dic[pred_val]
                decision = pred_val

        confusion_mat[testSam[-1] - 1][decision - 1] += 1
        if decision == testSam[-1]:
            accruate_cnt += 1

    for i in range(attri_num):
        for j in range(attri_num):
            print '%4d' % confusion_mat[i][j],
        print ''

    # print 'accuracy:', 1.0 * accruate_cnt / total

    # F1 = (2TP)/(2TP + FP + FN)
    F1 = [0 for i in range(attri_num)]
    for i in range(attri_num):
        vertical, horizontal = 0, 0
        for j in range(attri_num):
            vertical += confusion_mat[j][i]
            horizontal += confusion_mat[i][j]
        if vertical + horizontal == 0:
            F1[i] = 0
        else: F1[i] = 2.0 * confusion_mat[i][i] / (vertical + horizontal)

    '''
    for ele in F1:
        print ele,
    print ''
    '''

    # print random_forest[0]
    # print accruateCnt, 'len of test', total, 'len of train', len(training)

    train_file.close()
    test_file.close()
    # print 'time cost:', time.time() - start_time
