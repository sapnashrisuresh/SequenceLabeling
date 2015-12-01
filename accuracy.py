import sys

#Uses the ouput of  below command and comapres the first column (actual tags) with the second (predicted tags):
#./crfsuite tag -r -m modelfile testfile > output.txt
readfile=sys.argv[1]

with open(readfile,'r') as f:
	count=0
	totalcount=0
	for line in f.readlines():
		totalcount+=1
		if(line.strip()):
			words=line.split()
			if(words[0]==words[1]):
				count+=1
	print('Total occurances count=',totalcount,'\nTagged correctly occurances count=',count,'\nAccuracy=',count/totalcount)