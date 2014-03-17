# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# STRIP SPEAKERS

# <codecell>

#STRIP SPEAKERS

import os #allows for path crawling
import re

#variables
path="C:/Users/Christopher/Desktop/data-for-presentation/ORIGINAL/" #set the path that we are going to read through

for root,dirs,files in os.walk(path):
    for file in files:
        if file.endswith('.txt'):
            with open(path+file, 'rt') as f:
                text = f.read()
                text = re.sub('\(.+\)','',text)
                text = re.sub('[A-Z][A-Z][A-Za-z,\s\-\.\&]+?:','',text)
                with open("C:/Users/Christopher/Desktop/data-for-presentation/no-speakers/"+file,"w") as output:
                    output.write(text)
                    #for match in matches:
                        #output.write(match[1]+"\n")
                    output.close()

# <codecell>

path="C:/Users/Christopher/Desktop/data-for-presentation/no-speakers/" #set the path that we are going to read through
FNS=''
SOTU=''
MTP=''

for root,dirs,files in os.walk(path):
    for file in files:
        if file.endswith('.txt'):
            with open(path+file, 'rt') as f:
                text = f.read()   
                text = re.sub('\(.+\)','',text)
                text = re.sub('[A-Z][A-Z][A-Za-z,\s\-\.\&]+?:','',text)
                if 'FNS' in file:
                    FNS = FNS +' ' + text
                elif 'SOTU' in file:
                    SOTU = SOTU + ' ' + text
                elif 'MTP' in file:
                    MTP = MTP + ' ' + text
                    
f = open(path+'_FNS.txt',"w")
f.write(FNS)
f.close()

f = open(path+'_SOTU.txt',"w")
f.write(SOTU)
f.close()

f = open(path+'_MTP.txt',"w")
f.write(MTP)
f.close()

# <headingcell level=1>

# DIFFERENCE OF PROPORTIONS

# <codecell>

#DIFFERENCE OF PROPORTIONS

import os #allows for path crawling
import re
import nltk
from nltk.corpus import stopwords


#variables
path="C:/Users/Christopher/Desktop/data-for-presentation/no-speakers/" #set the path that we are going to read through
FNS_TEXT = ""
SOTU_TEXT = ""


for root,dirs,files in os.walk(path):
    for file in files:
        if file.endswith('.txt'):
            with open(path+file, 'rt') as f:
                if "FNS" in file:
                    FNS_TEXT = FNS_TEXT + " " + f.read().lower()
                elif "SOTU" in file:
                    SOTU_TEXT = SOTU_TEXT + " "+ f.read().lower()

def diff_prop(text1, text2):
    """
    returns a FreqDist that includes the difference in proportions between text 1 and text 2
    """
    vocab1 = text1.vocab()
    vocab2 = text2.vocab()

    diff_prop = nltk.FreqDist()

    for word in vocab1.keys():
        if word not in stopwords.words('english') and len(word) > 1 and word.isalpha():
            freq1 = vocab1.freq(word)
            freq2 = vocab2.freq(word)
            diff_prop.inc(word, freq1 - freq2)

    for word in vocab2.keys():
        if word not in diff_prop and word not in stopwords.words('english') and len(word)and word.isalpha() > 1:
            freq1 = vocab1.freq(word)
            freq2 = vocab2.freq(word)
            diff_prop.inc(word, freq1 - freq2)
    return diff_prop


#create texts from the two sets of newspapers (Les Antilles and Les Colonies)
FNS = nltk.text.Text(nltk.word_tokenize(FNS_TEXT))
SOTU = nltk.text.Text(nltk.word_tokenize(SOTU_TEXT))

#create a differences of proportion frequency distribution
differences = diff_prop(FNS,SOTU)


#-----------------------------------------------
#-PRINT THE DIFFERENCE OF PROPORTIONS FREQ DIST-
#-----------------------------------------------
x=[]
y=[]
label=[]
keys = differences.keys()
v1 = FNS.vocab()
v2 = SOTU.vocab()
print 'WORD\t','DIFF\t','FREQ'
for key in keys:
    print key,'\t',differences[key],'\t',int(v1[key]+v2[key])
    label.append(key)
    y.append(differences[key])
    x.append(int(v1[key]+v2[key]))


#------------
#-MATPLOTLIB-
#------------
#create a scatterplot with a colorscape 
import matplotlib.pyplot as plt #import plotter from matplotlib in the namespace plt
import matplotlib.cm as cm #import colormpas from matplotlib in the namespace cm (for more colormaps, see http://matplotlib.org/examples/pylab_examples/show_colormaps.html)

for a,b,c in zip(label,x,y):
    Val=1-(0.5+(c*1000))
    color=cm.Spectral(Val)
    plt.scatter(b, c,s=b**1.05,c=color,alpha=0.5)
    s=b/5
    if s > 14: s=14
    point_label = plt.annotate(a,xy=(b,c),size=s,horizontalalignment='center',verticalalignment='center') 
    point_label.draggable()
plt.xscale('log')
plt.xlim([0,200])
plt.ylim([-0.0025,0.0025])
plt.xlabel('Frequency of word in both shows (Logarithmic Scale)')
plt.ylabel('Difference of Proportions (Freq Difference)')
plt.title('Difference of Proportions in Word Distribution between FNS (top) and SOTU (bottom)')
plt.show()

# <codecell>


