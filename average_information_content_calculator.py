#load file
import sys
try:
	file_name=sys.argv[1]
except:
	print '	A input file is needed!\n 	The command should be like:\n python average_information_content_calculator.py INPUT_FILE.txt\n'
#sys.argv[1] is the input file (a text file) that you want to know about the average info content of each word in it  
txt=open(file_name,'r').readlines()

from collections import Counter 

def flatten(forest):
	''' in:		flatten([[1],[2],[3]])
		out:	 [1, 2, 3]
	'''
	return [leaf for tree in forest for leaf in tree]

#tokenize sentences into words: lists of words and add '#' to mark the initial position of sentences
#[
#['#', w1, w2, w3, ...], 
#['#', w1, w2, w3, ...], ...
# ] 
txt=[['#']+i.split() for i in txt]

# unigram frequency ditionary {word:545, ...}
uni_gram_freq=Counter(flatten(txt))
#total unigram token frequency 
total_unigram_frequency=sum([uni_gram_freq[i] for i in uni_gram_freq])

#convert unigram token frequency to probabality. p(w)=feq(w)/total unigram token frequency 
#{word:0.0004, ...}
uni_gram_model={}
for i in uni_gram_freq:
	uni_gram_model[i]=uni_gram_freq[i]*1.0/total_unigram_frequency

###build bigram probabality
bi=[zip(kk[:-1],kk[1:]) for kk in txt]
bi_bag=flatten(bi)
#bigram frequency ditionary
bi_freq=Counter(bi_bag)
total_bi_tokens=len(bi_bag)

#bi gram probabality
bi_prob={}
for i in bi_freq:
	bi_prob[i]=bi_freq[i]*1.0/total_bi_tokens

#Find all the context where the target word occurs
#h_pre[word]=[((context1, word), 1), ((context2, word), 1), ((context3, word), 2), ...]
#h_pre[word] gives all the context where word occurs as a set.  
h_pre={}
for i in bi_freq:
	if i[1] in h_pre:
		h_pre[i[1]].append(((i[0],i[1]),bi_freq[i]))
	else:
		h_pre[i[1]]=[((i[0],i[1]),bi_freq[i])]

freq_sur={}
import math
for i in uni_gram_model:
	if i != '#':
		occurance_of_i=sum([j[1] for j in h_pre[i]])
		#sur(w)=p(c,w)/p(c)
		#p(c,w)=(bi_gram_prob[j[0]]*1.0
		#p(c)=uni_gram_model[j[0][0]])
		#j[1] is the frequency of p(c,w)/p(c)
		sur_i=[ math.log(bi_prob[j[0]]*1.0/uni_gram_model[j[0][0]],2)*j[1] for j in h_pre[i]]
		#average_surpisal
		sur_i=sum(sur_i)*-1.0/occurance_of_i
		freq_sur[i]=(occurance_of_i,sur_i)

#save_to file 
with open(sys.argv[1][:-4]+'_average_info_content.tsv','w') as hhh:
	hhh.write("word\tfreq\taverage_surpisal\n")
	for i in freq_sur:
		hhh.write('{}\t{}\t{}\n'.format(i, freq_sur[i][0], freq_sur[i][1]))

print "\n\'{}\' is ready.\n".format(sys.argv[1][:-4]+'_average_info_content.tsv')
