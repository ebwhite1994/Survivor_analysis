# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 16:33:26 2022

@author: Ethan
"""


import numpy as np
from matplotlib import pyplot as plt
import re
import matplotlib

font = {
        'size'   : 16}
plt.rc('axes', titlesize = 24)
plt.rc('axes', labelsize = 20)

matplotlib.rc('font', **font)

#listed in the order I watched them
season_list = ['Philippines', 'Pearl_Islands', 'Panama', 'Cook_Islands', 'Fiji', 'China', 'Micronesia', 'Gabon', 'Tocantins']


#Reads in text from the files
#output list of strings
def read_text(season):
    path = 'D:/projects/Survivor/' + season +'.txt'
    
    with open(path) as f:
        lines = f.readlines()
    return(lines)

#count the number of words, punctuation, and pictures
#input list of lines of text
def word_count(string):

    uppercase = 0
    lowercase = 0
    exclame = 0
    question = 0
    exclame_question = 0
    pictures = 0

    for k in string:
        words = k.split()
        # words = re.split('[\s.,?!-]', k)
        
        for i in words:
            # print(i)
            if i.isupper() == True and i != "I" and i != "A" and i != "J" and i != "T" and i != 'J.T.':
                # print(i)
                uppercase = uppercase + 1
            if i.isupper() == False or i == "I" or i == "A":
                # print(i)
                lowercase = lowercase + 1
            if ('!?' in i) == True:
                # print(i)
                exclame_question = exclame_question + 1
            if ('!?' in i) == False and ('!' in i) == True:
                # print(i)
                exclame = exclame + 1
            if ('!?' in i) == False and ('?' in i) == True:
                # print(i)
                question = question + 1
            if ('PicturE' in i) == True:
                pictures = pictures + 1
        
            
    return(uppercase, lowercase, exclame, question, exclame_question, pictures)

#counts the number of completely uppercase and sentences which are not all uppercase (lowercase sentences)
#input a list of strings
def sentence_count(string):
    #read in the whole text file
    #then run this to determine which sentences are fully capitalized 
    
    if type(string) == list:
        sentences = []
        for i in string:
            sent_temp = re.split('[\n?.!-]', i)
            # print(sent_temp)
            sentences.append(sent_temp)
        # print(sentences)
        uppercase = 0
        lowercase = 0

        for k in sentences:
            # print(k)
            for i in k:
                if i.isupper() == True and i != 'J' and i != "T":
                    uppercase = uppercase + 1
                else:
                    lowercase = lowercase + 1

    else:
        sentences = re.split('[.?!-]', string)
        uppercase = 0
        lowercase = 0

        for i in sentences:
            if i.isupper() == True:
                uppercase = uppercase + 1
            else:
                lowercase = lowercase + 1

    # print(sentences)
    
            
    return(uppercase, lowercase)

#does the analysis of word count and sentence count for each individual episode/section
def episode_split(string):
    #I need to determine all text between thoughts, ep. #, and reunion
    #Check if distinguishing marker is the line
    checks = ['Thoughts:', 'Ep.', 'Reunion:']  
    # print(checks)
    #see if the line includes the check
    #run sentence count and word count for the lines in between the checks
    # for k in string:
    
    check_inds = []
    for i in range(len(string)):
        for k in checks:
            # if i == 0:
            #     print(k)
            if (k in string[i]) == True:
                check_inds.append(i)
    
                
    labels = np.asarray(string)[check_inds]
    for i in range(len(labels)):
        # print(labels[i])
        labels[i] = labels[i][:-1]
        # print(labels[i])
    
    ups = []
    lows = []
    exls = []
    quests = []
    exl_quests = []
    pictures = []
    
    upp_sents = []
    low_sents = []
    
    for i in range(len(check_inds)):
        if i != range(len(check_inds))[-1]:
            strings = string[check_inds[i]:check_inds[i+1]]
        if i == range(len(check_inds))[-1]:
            strings = string[check_inds[i]:]
        up, low, exl, quest, exl_ques, pict = word_count(strings)
        ups.append(up)
        lows.append(low)
        exls.append(exl)
        quests.append(quest)
        exl_quests.append(exl_ques)
        pictures.append(pict)
        
        up_sent, low_sent = sentence_count(strings)
        upp_sents.append(up_sent)
        low_sents.append(low_sent)
    
    for i in range(len(labels)):
        if ('\xa0' in labels[i]) == True:
            labels[i] = labels[i][:-1]
    
    #Once I have the info, I need to sort these lists/arrays by the epiode titles sorting
    return(ups, lows, exls, quests, exl_quests, pictures, upp_sents, low_sents, check_inds, labels)
#
#I need a way to combine the episode titles/thoughts/reunion into one list/array
#I then need to fill in 0s or null values for the episodes that have no data
#   ex. skipped episodes or seasons that have more episodes than others
#

#This helps sort the episode titles
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#this returns the list of episodes in order (8, 9, 10, 11, etc)
def sort_list(string):
    list_labels = list(string)
    list_labels.sort(key= natural_keys)
    return(list_labels)    

#input a list or array of labels
#output the list of labels with duplicates removed
#I need a way to check which labels were copies maybe though?
def combine_lists(lists):
    l1 = list(lists[0])
    for i in range(len(lists) -1):
        l1 = list(l1) + list(lists[i + 1])
    res = []
    [res.append(x) for x in l1 if x not in res]
    return(res)
    
#input list of seasons
#create plots of seasons
def plotting(inputs):
    tots = []
    exls = []
    quests = []
    ups = []
    lows = []
    exl_quests = []
    pictures = []
    upp_sent = []
    low_sent = []
    
    ep_per_season = []
    for i in range(len(inputs)):
        up, low, exl, quest, exl_ques, pict =  word_count(read_text(inputs[i]))
        tot = up + low
        tots.append(tot)
        ups.append(up)
        lows.append(low)
        exls.append(exl)
        quests.append(quest)
        exl_quests.append(exl_ques)
        pictures.append(pict)
        
        up_se, lo_se = sentence_count(read_text(inputs[i]))
        upp_sent.append(up_se)
        low_sent.append(lo_se)
        
        labl_temp = episode_split(read_text(inputs[i]))[-1]
        ep_per_season.append(len(labl_temp))
        
    tots = np.asarray(tots)
    exls = np.asarray(exls)
    quests = np.asarray(quests)
    ups = np.asarray(ups)
    lows = np.asarray(lows)
    exl_quests = np.asarray(exl_quests)
    upp_sent = np.asarray(upp_sent)
    low_sent = np.asarray(low_sent)
    ep_per_season = np.asarray(ep_per_season)
    pictures = np.asarray(pictures)
    
    nums = np.arange(len(inputs))
    plt.figure(figsize = (10,7))
    plt.title("Words per Season")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Number of Words")
    plt.plot(nums, tots, color = 'blue')
    plt.plot(nums, tots, 'o', color = 'blue')
    plt.show()
    
    tot_and_pic = tots + (pictures * 1000)

    plt.figure(figsize = (10,7))
    plt.title("Words per Season (Including Pictures)")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Number of Words")
    plt.plot(nums, tot_and_pic, color = 'blue')
    plt.plot(nums, tot_and_pic, 'o', color = 'blue')
    plt.show()

    plt.figure(figsize = (10,7))
    plt.title("Average Words per Section per Season")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Number of Words")
    plt.plot(nums, tots/ep_per_season, color = 'blue')
    plt.plot(nums, tots/ep_per_season, 'o', color = 'blue')
    
    plt.show()

    plt.figure(figsize = (10,7))
    plt.title("Pictures per Season")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Number of Pictures")
    plt.plot(nums, pictures, color = 'blue')
    plt.plot(nums, pictures, 'o', color = 'blue')
    plt.show()

    
    plt.figure(figsize = (10,7))
    plt.title("Punctuation Type")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Number of Punctuation")
    plt.plot(nums, exls, label = "!", color = 'blue')
    plt.plot(nums, quests, label = "?", color = 'orange')
    plt.plot(nums, exl_quests, label = "!?", color = 'green')
    plt.plot(nums, exls, 'o', color = 'blue')
    plt.plot(nums, quests, 'o', color = 'orange')
    plt.plot(nums, exl_quests,'o', color = 'green')
    
    plt.legend()
    plt.show()


    tot_punct = exls + quests + exl_quests
    # print(tot_punct)
    # print(quests)

    #Shows how my questions about the game turned into questions about what people are thinking?
    plt.figure(figsize = (10,7))
    plt.title("Fraction of Punctuation Type")
    plt.xticks(nums, inputs, rotation = 45)
    plt.ylabel("Fraction of Punctuation")
    plt.plot(nums, exls/tot_punct, label = "!", color = 'blue')
    plt.plot(nums, quests/tot_punct, label = "?", color = 'orange')
    plt.plot(nums, exl_quests/tot_punct, label = "!?", color = 'green')
    plt.plot(nums, exls/tot_punct, 'o', color = 'blue')
    plt.plot(nums, quests/tot_punct, 'o', color = 'orange')
    plt.plot(nums, exl_quests/tot_punct,'o', color = 'green')
    
    plt.legend()
    plt.show()


    
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize = (10,7))
    # make a plot
    ax.set_title("Words per Season")
    ax.plot(nums, ups, color="red", marker="o")
    ax.set_ylabel("Uppercase Words", color = 'red')
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(nums, lows,color="blue",marker="o")
    ax2.set_ylabel("Lowercase Words", color =  'blue')
    
    # ax.set_xticklabels(inputs)
    plt.xticks(nums, inputs)
    # plt.xticks(rotation = 45)
    ax.tick_params(axis = 'x', labelrotation = 45)
    plt.show()
    
    fig,ax = plt.subplots(figsize = (10,7))
    # make a plot
    ax.set_title("Sentences per Season")
    ax.plot(nums, upp_sent, color="red", marker="o")
    ax.set_ylabel("Uppercase Sentences", color = 'red')
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(nums, low_sent,color="blue",marker="o")
    ax2.set_ylabel("Lowercase Sentences", color =  'blue')
    
    # ax.set_xticklabels(inputs)
    plt.xticks(nums, inputs)
    # plt.xticks(rotation = 45)
    ax.tick_params(axis = 'x', labelrotation = 45)
    plt.show()
                
#create arrays of values from each episode of each season
def big_combine(seasons):    
    vals = []
    for i in seasons:
        val_temp = episode_split(read_text(i))
        vals.append(val_temp)
    vals = np.asarray(vals)
    labels = combine_lists(vals[:,-1])
    labels = sort_list(labels)
    
    ups = np.zeros((len(seasons), len(labels)))
    # ups[:] = np.nan
    lows = np.zeros((len(seasons), len(labels)))
    # lows[:] = np.nan
    exls = np.zeros((len(seasons), len(labels)))
    # exls[:] = np.nan
    quests = np.zeros((len(seasons), len(labels)))
    # quests[:] = np.nan
    exl_quests = np.zeros((len(seasons), len(labels)))
    # exl_quests[:] = np.nan 
    pictures = np.zeros((len(seasons), len(labels))) 
    
    upp_sents = np.zeros((len(seasons), len(labels)))
    # upp_sents[:] = np.nan
    low_sents = np.zeros((len(seasons), len(labels)))
    # low_sents[:] = np.nan
    
    #Now:
        #go through each episode split for each season
        #if labels[i] = label_for_season[k]
        #append value for that episode to value_list (ex. ups.append(up_for_ep1))

    #for each season
    for i in range(len(vals)):
        #for each episode
        for k in range(len(vals[i][0])):
            # print(vals[i][-1][k])
            for j in range(len(labels)):
                if labels[j] == vals[i][-1][k]:
                    # print(labels[j])
                    # print(vals[i][-1][k])
                    ups[i][j] = vals[i][0][k]
                    lows[i][j] = vals[i][1][k]
                    exls[i][j] = vals[i][2][k]
                    quests[i][j] = vals[i][3][k]
                    exl_quests[i][j] = vals[i][4][k]
                    pictures[i][j] = vals[i][5][k]
                    upp_sents[i][j] = vals[i][6][k]
                    low_sents[i][j] = vals[i][7][k]
    tots = ups + lows
    return(labels, vals, ups, lows, exls, quests, exl_quests, pictures, tots, upp_sents, low_sents)

#create plots of all or a specific episode/section
#input season list
#if desired, input a specific episode
def episode_plot(seasons, episode = 'all'):
    labels, val, ups, lows, exls, quests, exl_quests, pictures, tots, upp_sents, low_sents = big_combine(seasons)
    
    # ups[ups == 0] = np.nan
    # lows[lows==0]
    
    
    if episode == 'all':
        nums = np.arange(len(labels))
        # plt.figure(figsize = (10,8))
        # for i in range(len(seasons)):
        #     plt.plot(nums, ups[i], label = seasons[i])
        # plt.legend()
        # plt.xticks(nums, labels, rotation = 45)
        # plt.show()
        plt.figure(figsize = (10,8))
        lows = np.asarray(lows)
        ups = np.asarray(ups)
        tots = lows + ups
        for i in range(len(seasons)):
            plt.plot(nums, tots[i], marker = 'o', label = seasons[i])
        plt.legend()
        plt.title("Words per Episode")
        plt.ylabel("Number of Words")
        plt.xticks(nums, labels, rotation = 45)
        plt.show()
    
    else:
        nums = np.arange(len(seasons))
        plt.figure(figsize = (10,7))
        plt.plot(nums, tots[:,episode], color = 'blue')
        plt.plot(nums, tots[:,episode], 'o', color = 'blue')
        plt.title(labels[episode] + ', Total Words')
        # plt.legend()
        plt.ylabel("Words")
        plt.xticks(nums, seasons, rotation = 45)
        plt.show()

        tot_and_pic = tots + (1000 * pictures)

        plt.figure(figsize = (10,7))
        plt.plot(nums, tot_and_pic[:,episode], color = 'blue')
        plt.plot(nums, tot_and_pic[:,episode], 'o', color = 'blue')
        plt.title(labels[episode] + ', Total Words (Including Pictures)')
        # plt.legend()
        plt.ylabel("Words")
        plt.xticks(nums, seasons, rotation = 45)
        plt.show()

        plt.figure(figsize = (10,7))
        plt.plot(nums, exls[:,episode], label = "!",color = 'blue')
        plt.plot(nums, exls[:,episode], 'o', color = 'blue')
        plt.plot(nums, quests[:,episode], label = "?", color = 'orange')
        plt.plot(nums, exl_quests[:,episode], label = "!?", color = 'green')
        plt.plot(nums, quests[:,episode], 'o', color = 'orange')
        plt.plot(nums, exl_quests[:,episode],'o', color = 'green')

        plt.title(labels[episode] + ', Punctuation Type')
        # plt.legend()
        plt.ylabel("Number of Punctuation")
        plt.legend()
        plt.xticks(nums, seasons, rotation = 45)
        plt.show()
        
        tot_punct = quests + exls + exl_quests
        
        plt.figure(figsize = (10,7))
        plt.plot(nums, exls[:,episode]/tot_punct[:,episode], label = "!",color = 'blue')
        plt.plot(nums, exls[:,episode]/tot_punct[:,episode], 'o', color = 'blue')
        plt.plot(nums, quests[:,episode]/tot_punct[:,episode], label = "?", color = 'orange')
        plt.plot(nums, exl_quests[:,episode]/tot_punct[:,episode], label = "!?", color = 'green')
        plt.plot(nums, quests[:,episode]/tot_punct[:,episode], 'o', color = 'orange')
        plt.plot(nums, exl_quests[:,episode]/tot_punct[:,episode],'o', color = 'green')

        plt.title(labels[episode] + ', Fraction of Punctuation Type')
        # plt.legend()
        plt.ylabel("Fraction of Punctuation")
        plt.legend()
        plt.xticks(nums, seasons, rotation = 45)
        plt.show()

        
        # plot_indiv(seasons, ups[:,episode], labels[episode], 'Uppercase Words', 'Words')
        # plot_indiv(seasons, lows[:,episode], labels[episode], 'Lowercase Words', 'Words')
        # # print(upp_sents)
        # plot_indiv(seasons, upp_sents[:,episode], labels[episode], 'Uppercase Sentences', 'Sentences')
    
        fig,ax = plt.subplots(figsize = (10,7))
        # make a plot
        ax.set_title(labels[episode] + ", Sentences")
        ax.plot(nums, upp_sents[:,episode], color="red", marker="o")
        ax.set_ylabel("Uppercase Sentences", color = 'red')
        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        ax2.plot(nums, low_sents[:,episode],color="blue",marker="o")
        ax2.set_ylabel("Lowercase Sentences", color =  'blue')
        
        # ax.set_xticklabels(inputs)
        plt.xticks(nums, seasons)
        # plt.xticks(rotation = 45)
        ax.tick_params(axis = 'x', labelrotation = 45)
        plt.show()

        fig,ax = plt.subplots(figsize = (10,7))
        # make a plot
        ax.set_title(labels[episode] + ", Words")
        ax.plot(nums, ups[:,episode], color="red", marker="o")
        ax.set_ylabel("Uppercase Words", color = 'red')
        # twin object for two different y-axis on the sample plot
        ax2=ax.twinx()
        # make a plot with different y-axis using second axis object
        ax2.plot(nums, lows[:,episode],color="blue",marker="o")
        ax2.set_ylabel("Lowercase Words", color =  'blue')
        
        # ax.set_xticklabels(inputs)
        plt.xticks(nums, seasons)
        # plt.xticks(rotation = 45)
        ax.tick_params(axis = 'x', labelrotation = 45)
        plt.show()
        
        



#create a plot of a specific variable
def plot_indiv(seasons, var, ep_title, second_title, ylabel):
    nums = np.arange(len(seasons))
    plt.figure(figsize = (10,7))
    plt.plot(nums, var, color = 'blue')
    plt.plot(nums, var, 'o', color = 'blue')
    plt.title(ep_title + ', ' + second_title)
    # plt.legend()
    plt.ylabel(ylabel)
    plt.xticks(nums, seasons, rotation = 45)
    plt.show()
    
        
        
    
    