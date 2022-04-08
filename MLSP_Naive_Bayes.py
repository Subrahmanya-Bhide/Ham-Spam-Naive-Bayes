# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:06:05 2021

@author: subbu
"""
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
#%%preprocessing
text = open(r'D:\SEM 6\AV489 MAchine Learning for Signal Processing\Assignment 3\spam.txt',encoding ='utf-8')
lines = text.read().split('\n')
n_spam = 0
n_ham = 0
hams = []
spams =[]
for line in lines:
    words = line.split(',')
    if words[0] == 'spam':
       n_spam = n_spam +1
       spams.append(words[1])
    else:
       n_ham = n_ham +1
       hams.append(words[1])
#%%for spams
spam_vocabulary =[]
spam_count_words ={}
for spam in spams:
    words = spam.split(' ')
    for word in words:
        if word.lower() not in spam_vocabulary:
            spam_vocabulary.append(word.lower())
        if word.lower() not in spam_count_words:
            spam_count_words[word.lower()] = 1
        else:
            spam_count_words[word.lower()] +=1
spam_words_count = len(spam_vocabulary)
spam_words_prob = copy.deepcopy(spam_count_words)
for word in spam_words_prob:
    spam_words_prob[word] = (spam_words_prob[word] + 1) /(spam_words_count + len(spam_vocabulary))
        
#%%for hams
ham_vocabulary =[]
ham_count_words ={}
for ham in hams:
    words = ham.split(' ')
    for word in words:
        if word.lower() not in ham_vocabulary:
            ham_vocabulary.append(word.lower())
        if word.lower() not in ham_count_words:
            ham_count_words[word.lower()] = 1
        else:
            ham_count_words[word.lower()] +=1
ham_words_count = len(ham_vocabulary)
ham_words_prob = copy.deepcopy(ham_count_words)
for word in ham_words_prob:
    ham_words_prob[word] = (ham_words_prob[word] + 1) / (ham_words_count + len(ham_vocabulary))        


ham_prob = n_ham/(n_ham + n_spam)
spam_prob = 1 - ham_prob      
#%%function for testing 
def is_spam(line):
    words = line.split(' ')
    spam_sum = 0
    for word in words:
        if word in spam_words_prob:
            spam_sum = spam_sum + math.log(spam_words_prob[word])
        else:
            spam_sum = spam_sum + 0
    ham_sum = 0
    for word in words:
        if word in ham_words_prob:
            ham_sum = ham_sum + math.log(ham_words_prob[word])
        else:
            ham_sum = ham_sum + 0
    spam_sum = spam_sum + math.log(spam_prob)
    ham_sum = ham_sum + math.log(ham_prob)
    ans = spam_sum - ham_sum 
    if ans < 0:
        return 1
    else:
        return 0

#%%testing 
test = open(r'D:\SEM 6\AV489 MAchine Learning for Signal Processing\Assignment 3\spam_test.txt',encoding ='utf-8')
test_lines = text.read().split('\n')
t_cls = []
for line in lines:
    words = line.split(",")
    if words[0] == 'spam':
        t_cls.append(1)
    else:
        t_cls.append(0)

e_cls = []
for line in lines:
    if is_spam(line) == 1:
        e_cls.append(1)
    else:
        e_cls.append(0)

t_cls = np.asarray(t_cls)
e_cls = np.asarray(e_cls)   
 
z = np.column_stack((e_cls,t_cls)) 
conf_mat_2 = np.zeros((2,2))

for i in range(4108):
    if z[i,0] == z[i,1] == 0:
        conf_mat_2[0,0] = conf_mat_2[0,0]+1
    elif z[i,0] == z[i,1] == 1:
        conf_mat_2[1,1] = conf_mat_2[1,1]+1
    elif z[i,0] == 0 and z[i,1] == 1:
        conf_mat_2[1,0] = conf_mat_2[1,0]+1
    else:
        conf_mat_2[0,1] = conf_mat_2[0,1]+1 

#%% Section for getting histogram
spam_freq = []
ham_freq = []
x_spam = np.linspace(0,len(spam_freq),len(spam_freq))
x_ham = np.linspace(0,len(ham_freq),len(ham_freq))
for i in range(len(spam_vocabulary)):
    spam_freq.append(int((spam_count_words[spam_vocabulary[i]])))
    ham_freq.append(int((ham_count_words[ham_vocabulary[i]])))
    
x_spam = np.linspace(0,len(spam_freq),len(spam_freq))
x_ham = np.linspace(0,len(ham_freq),len(ham_freq))


spam_sort = spam_freq
spam_sort.sort(reverse = True)
ham_sort = ham_freq
ham_sort.sort(reverse = True)

plt.xticks(x_spam,"")
plt.plot(spam_freq)


keys = np.linspace(0,20,20)

key_list_sp=list(spam_count_words.keys())
val_list_sp=list(spam_count_words.values())


key_list_hm=list(ham_count_words.keys())
val_list_hm=list(ham_count_words.values())


for i in range(len(keys)):
   ind=val_list_sp.index(spam_sort[int(keys[i])])
   indh=val_list_hm.index(ham_sort[int(keys[i])])
   print( key_list_sp[ind] ,spam_sort[int(keys[i])],  key_list_hm[indh], ham_sort[int(keys[i])] ) 

