import os.path, requests, json, csv, re

with open('stopwords.csv', 'r+') as f:
	reader = csv.reader(f)
	stopwords = reader.next()

f.close()	

def remove_stop_words_and_nums(w):
	words = []
	for word in w:
		word = word.lower()
		if word not in stopwords and word.isalpha():
			if len(word) > 1:
				words.append(word)
	#print words
	return words	

desc_website = ''

for x in ['crises','people','organizations']:
	desc_all = ''

	for i in range(1,11):
		r = requests.get('http://tcp-connections.herokuapp.com/api' +'/'+ str(x) +'/'+ str(i))
		r_json = r.json()
		desc = r_json['description']
		desc = desc.encode('utf-8')

		desc_all += desc
		desc_website += desc

		words = re.split('\W+',desc)
		words = remove_stop_words_and_nums(words)

		tf_d = dict.fromkeys(words,0)

		for w in words:
			tf_d[w] += 1.0

		num_words = len(tf_d)
		print num_words
		data = []
		for k,v in tf_d.iteritems():
			v = v/num_words * 100 * 10
			data.append({'text':k , 'size':v})

		f = open('../static/assets/word-cloud/' + x + str(i) +'.json', 'w+')
		f.write(json.dumps(data))	


	words = re.split('\W+',desc_all)
	words = remove_stop_words_and_nums(words)

	tf_d = dict.fromkeys(words,0)

	for w in words:
		tf_d[w] += 1.0

	num_words = len(tf_d)
	print num_words
	print tf_d[max(tf_d, key=tf_d.get)]

	data = []
	for k,v in tf_d.iteritems():
		v = v * 10
		data.append({'text':k , 'size':v})

	#print data

	f = open('../static/assets/word-cloud/'+ x +'.json', 'w+')
	f.write(json.dumps(data))		

words = re.split('\W+',desc_website)
words = remove_stop_words_and_nums(words)

tf_d = dict.fromkeys(words,0)

for w in words:
	tf_d[w] += 1.0

num_words = len(tf_d)
print num_words
print tf_d[max(tf_d, key=tf_d.get)]

data = []
for k,v in tf_d.iteritems():
	v = v * 10
	data.append({'text':k , 'size':v})

#print data

f = open('../static/assets/word-cloud/all.json', 'w+')
f.write(json.dumps(data))		



