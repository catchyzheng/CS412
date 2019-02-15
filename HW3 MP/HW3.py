from collections import defaultdict
import copy

def obtain_super_item(lst1, lst2):
    res = copy.copy(lst1)
    for ele in lst2:
        if ele not in res:
            res.append(ele)
    return res
    
def notappear(candi_set, tmp):
    if sorted(tmp) not in candi_set:
        candi_set.append(sorted(tmp))
    return

def sort_format(freq_set):
    freq_set = sorted(freq_set, key = lambda item : item[1])
    freq_set = sorted(freq_set, reverse = True, key = lambda item : item[0])
    return freq_set

def print_set(_set):
    for ele in _set:
        print(ele[0], '[', end='')
        for i in range(len(ele[1])):
            if i!=0: print(' ', end='')
            print(ele[1][i], end='')
        print(']')

if __name__ == '__main__':
    min_sup = int(input())
    f = defaultdict(int)
    total = 0
    origin = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        itemlist = line.split(' ')
        #print('itemlist', itemlist)
        origin.append(itemlist)
        for ele in itemlist:
            f[ele] += 1
        total += 1
    
    itemset = [[]]
    for key, value in f.items():
        if value >= min_sup:
            itemset[0].append([value, [key]])
            
    pre_set = itemset[0]
    #print('pre set', pre_set)
    
    iter = 0
    while iter < 10:
        l = len(pre_set)
        if l<2: break
        candi_set = []
        
        for i in range(l-1):
            for j in range(i+1, l):
                #print('base set', pre_set[i][1], pre_set[j][1])
                tmp = obtain_super_item(pre_set[i][1], pre_set[j][1])
                if len(tmp) > len(pre_set[i][1])+1: continue
                #print('check when set', tmp)
                if notappear(candi_set, tmp): candi_set.append(tmp)
        #print('candi_set', candi_set)
        freq_set = []
        for candi in candi_set: # the element type in candi_set is list
            cnt = 0
            for trans in origin:
                if all(x in trans for x in candi):
                    cnt += 1
            if cnt >= min_sup:
                freq_set.append([cnt, candi])
        #print('freq set', freq_set)
        itemset.append(freq_set)
        pre_set = freq_set
        iter += 1
    
    #print('item set', itemset)
    final_freq_set = []
    for line in itemset:
        final_freq_set += line
    
    
    #print frequent set
    final_freq_set = sort_format(final_freq_set)
    print_set(final_freq_set)
    print()
    
    #find closed freq set
    closed_freq_set = []
    for i in range(len(itemset)-1):
        for base in itemset[i]:
            in_cnt = 0; bigger = 0
            for sup in itemset[i+1]:
                if all(char in sup[1] for char in base[1]):
                    in_cnt += 1
                    if base[0] > sup[0]: bigger += 1
            if in_cnt == bigger:
                closed_freq_set.append(base)
    
    closed_freq_set.extend(itemset[-1])
    #print closed freq set
    closed_freq_set = sort_format(closed_freq_set)
    print_set(closed_freq_set)
    print()
    
    #find max freq set
    max_freq_set = []
    for i in range(len(itemset)-1):
        for base in itemset[i]:
            in_cnt = 0; notfreq = 0
            for sup in itemset[i+1]:
                if all(char in sup[1] for char in base[1]):
                    in_cnt += 1
                    if min_sup > sup[0]: notfreq += 1
            if in_cnt == notfreq:
                max_freq_set.append(base)
    
    max_freq_set.extend(itemset[-1])
    #print closed freq set
    max_freq_set = sort_format(max_freq_set)
    print_set(max_freq_set)
    
    
    