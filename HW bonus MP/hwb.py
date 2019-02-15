from collections import defaultdict
import copy


def filter_(dic, sup):
    garbage = []
    for key in dic.keys():
        if dic[key] < sup:
            garbage.append(key)
    
    for ele in garbage:
        del dic[ele]
    
def sort_format(freq_list):
    freq_list = sorted(freq_list, key = lambda item : item[1])
    freq_list = sorted(freq_list, reverse = True, key = lambda item : item[0])
    return freq_list

def print_set(_set):
    for ele in _set:
        print('[%d, \'%s\']' % (ele[0], ele[1]))

level = 1
min_sup = 2
min_level = 2
max_level = 5
N = 20
final_res = []
f = defaultdict(lambda : defaultdict(int))
origin = []
if __name__ == '__main__':
    while True:
        try:
            line = input()
        except EOFError:
            break
        itemlist = line.split(' ')
        origin.append(itemlist)
        for i in range(len(itemlist)):
            f[level][itemlist[i]] += 1

    filter_(f[level], min_sup)        
    

    while len(f[level]) > 0 and level < max_level:
        level += 1
        # find frequent itemset in current level 
        for word_list in origin:
            for i in range(len(word_list) - level + 1):
                prev = word_list[i: i + level - 1] 
                if f[level - 1][' '.join(prev)] >= min_sup:
                    curr = word_list[i: i + level]
                    f[level][' '.join(curr)] += 1

        f.pop(level - 1)
        filter_(f[level], min_sup)

        # update list
        for key in f[level]:
            candi = [f[level][key], key]
            final_res.append(candi)
            if len(final_res) > 2 * N:
                final_res = sort_format(final_res)[:N]         



    final_res = sort_format(final_res)[:N]
    print_set(final_res)

    
            
        
    