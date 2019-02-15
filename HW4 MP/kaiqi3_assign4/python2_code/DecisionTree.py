import sys
from math import log
import operator
import copy
from collections import defaultdict

def calc_gini_index(dataset):
    num_entries = len(dataset)
    label_counts = defaultdict(int)
    for feat_vec in dataset: #the the number of unique elements and their occurance
        current_label = feat_vec[-1]
        label_counts[current_label] += 1

    giniIndex = 1.0
    for key in label_counts:
        giniIndex -= (1.0*label_counts[key]/num_entries) * (1.0*label_counts[key]/num_entries)

    return giniIndex
    
def split_dataset(data_set, axis, value):
    splitted_dataset = []
    for feat_vec in data_set:
        # if len(feat_vec) <= axis: break
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]     #chop out axis used for splitting
            reduced_feat_vec.extend(feat_vec[axis+1:])
            splitted_dataset.append(reduced_feat_vec)
    return splitted_dataset
    
def choose_best_feature(dataset, attri_list):

    base_entropy = calc_gini_index(dataset)
    best_info_gain = 0.0
    best_feature = -1

    for i in range(len(attri_list)):
        feat_list = [example[i] for example in dataset] # obtain all example values of this feature
        unique_vals = set(feat_list)       #get a set of unique values
        new_entropy = 0.0

        for value in unique_vals:
            # sub_dataset = splitDataSet(dataSet, all_attriList.index(attriList[i]), value)
            sub_dataset = split_dataset(dataset, i, value)
            pr = len(sub_dataset)/float(len(dataset))
            new_entropy += pr * calc_gini_index(sub_dataset)

        info_gain = base_entropy - new_entropy     #calculate the info gain
        if info_gain > best_info_gain:       #compare this to the best gain
            best_info_gain = info_gain         #if better than current best, set to best
            best_feature = i
    return best_feature                      #returns an integer

def majority_cnt(class_list):
    class_count = defaultdict(int)
    for vote in class_list:
        class_count[vote] += 1

    sorted_class_count = sorted(class_count.iteritems(), key= lambda x: x[1], reverse=True)
    return sorted_class_count[0][0]

def create_tree(dataset, labels, all_labels):
    class_list = [example[-1] for example in dataset]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]  # stop splitting when all of the classes are equal
    if len(labels) == 1:  # stop splitting when there are no more features in dataset
        return majority_cnt(class_list)

    best_feat = choose_best_feature(dataset, labels)
    # print bestFeat, len(labels)
    best_feat_label = labels[best_feat]
    myTree = {best_feat_label: defaultdict()}

    # labels.remove(bestFeat)
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in dataset]
    unique_vals = set(feat_values)
    for value in unique_vals:
        sub_labels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[best_feat_label][value] = create_tree(split_dataset(dataset, best_feat, value), sub_labels, all_labels)
    return myTree
    
def classify(tree_input, feat_labels, all_feat_labels, test_vec):
    first_str = tree_input.keys()[0]
    second_dict = tree_input[first_str]
    # print feat_labels, first_str

    feat_index = feat_labels.index(first_str)

    key = test_vec[feat_index]
    
    if key in second_dict:
        value_of_feat = second_dict[key]
    else:
        value_of_feat = second_dict[second_dict.keys()[0]]
    
    if isinstance(value_of_feat, dict):
        class_label = classify(value_of_feat, feat_labels, all_feat_labels, test_vec)
    else: class_label = value_of_feat
    return class_label

def get_tree_depth(tree):
    max_depth = 0
    first = tree.keys()[0]
    second_dict = tree[first]
    for key in second_dict.keys():
        # if type(second_dict[key]).__name__ == 'dict'
        if type(second_dict[key]) == 'dict':
            cur_depth = 1 + get_tree_depth(second_dict[key])
        else:
            cur_depth = 1
        if cur_depth > max_depth: max_depth = cur_depth
    return max_depth

if __name__ == '__main__':
    arg = sys.argv
    train_file = open(arg[1], 'r')
    test_file = open(arg[2], 'r')

    label_dict = defaultdict(int)

    # build training set
    line_cnt = 0
    training = []
    for line in train_file:
        lst = line.split(' ')
        label = int(lst[0])
        if label not in label_dict: label_dict[label] = 1
        
        sample = [int(ele.split(':')[1]) for ele in lst[1:]]
        sample.append(int(lst[0]))
        training.append(sample)
        line_cnt += 1
    
    #print labelDict
    
    #build testing set
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
    else: attri_labels = [i for i in range(1, length + 1)]
    #print 'build', attriLabels

    #treeModel = createTree(training, [i for i in range(1, length+1)])
    decision_tree = create_tree(training, copy.copy(attri_labels), copy.copy(attri_labels))

    depth = get_tree_depth(decision_tree)
    #print 'depth', depth, 'attri num', length
    
    attri_num = len(label_dict)
    confusion_mat = [[0 for _ in range(attri_num)] for __ in range(attri_num)]
    total = len(testing) # length of testing
    accruate_cnt = 0

    
    for testSam in testing:
        #print treeModel
        #predict = classify(treeModel, origin, testSam[:-1])
        predict = classify(decision_tree, copy.copy(attri_labels), copy.copy(attri_labels), testSam[:-1])
        confusion_mat[testSam[-1]-1][predict-1] += 1
        if predict == testSam[-1]:
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
        F1[i] = 2.0 * confusion_mat[i][i] / (vertical + horizontal)

    '''
    for ele in F1:
        print ele, 
    print ''
    '''

    train_file.close()
    test_file.close()


    

