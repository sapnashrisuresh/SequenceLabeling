#!/usr/bin/env python3

"""
create_advanced_features.py: This scipt is used on the data to generate the advanced features

To run:
python3 create_advanced_features.py ./data/test/0001.csv > advanced_features.txt

The "hw3_corpus_tool.py" file provided with the assignment has been used in this script to read csv data. 
The baseline features have been retained here.
Multiple advanced features were generated that can be used to train the CRFSuite. The script can handle training 
and testing data.

On evaluation the final advanced features: bigram for POS and TOKEN tag was used along with stop word removal.
The lines used to generate other advance dfeatures like trigram that was tested initially, has been commented out in the program.

"""

__author__ = "Sapnashri Suresh"
__email__ = "sapnashs@usc.edu"

from collections import namedtuple
import csv
import glob
import os
import sys

filename=sys.argv[1]

def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

DialogUtterance = namedtuple(
    "DialogUtterance", ("act_tag", "speaker", "pos", "text"))

DialogUtterance.__doc__ = """\
An utterance in a dialog. Empty utterances are None.

act_tag - the dialog act associated with this utterance
speaker - which speaker made this utterance
pos - a list of PosTag objects (token and POS)
text - the text of the utterance with only a little bit of cleaning"""

PosTag = namedtuple("PosTag", ("token", "pos"))

PosTag.__doc__ = """\
A token and its part-of-speech tag.

token - the token
pos - the part-of-speech tag"""

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with 
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)


def main():
        DialogUtterance=get_utterances_from_filename(filename)
        firstline=True;
        #The following stopwords have not been considered while generating the TOKEN_ features.
        stopwords={'a-','the-','an-','in-','to-','a','the','an','in','to'}
        print()
        for x in DialogUtterance:
            feature=''
            if(x[0] is not None):
                feature+=x[0]+'\t'
            else:
                feature+='UNK'+'\t'
            if(firstline):
                feature+='FIRST_LINE'+'\t'
                speaker=x[1]
                firstline=False
            else:
                if(x[1]!=speaker):
                    feature+='CHANGE_SPEAKER'+'\t'
                speaker=x[1]
            pos=''
            token=''
            bigram=''
            posbigram=''
            #bigram (pairs of neighboring tokens and their respective POS tags) have been used as advanced features
            if(x[2] is not None):
                for y in range(len(x[2])):
                    #all tokens have been converted to lower case to add weight to the repetitive words irrespective of the case.
                    if(x[2][y][0] not in stopwords):
                        token+='TOKEN_'+x[2][y][0]+'\t'
                        pos+='POS_'+x[2][y][1]+'\t'
                    #####
                    if(y<len(x[2])-1):
                        bigram+='BIGRAM_'+x[2][y][0]+'_'+x[2][y+1][0].lower()+'\t'
                        posbigram+='POSBIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'\t'
                    #####
                    #trigram (three consectuive neighboring tokens and their respective POS tags) have been used as advanced features
                    #if(y<len(x[2])-2):
                    #    bigram+='TRIGRAM_'+x[2][y][0]+'_'+x[2][y+1][0]+'_'+x[2][y+2][0]+'\t'
                    #    posbigram+='POSTRIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'_'+x[2][y+2][1]+'\t'
                    #####
                    #if(y<len(x[2])-1):
                    #    posbigram+='POSBIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'\t'
                    #if(y<len(x[2])-2):
                    #    posbigram+='POSTRIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'_'+x[2][y+2][1]+'\t'
                    #####
                    #if(y<len(x[2])-1):
                    #    bigram+='BIGRAM_'+x[2][y][0]+'_'+x[2][y+1][0]+'\t'
                    #    posbigram+='POSBIIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'\t'
                    #if(y<len(x[2])-2):
                    #    bigram+='TRIGRAM_'+x[2][y][0]+'_'+x[2][y+1][0]+'_'+x[2][y+2][0]+'\t'
                    #    posbigram+='POSTRIGRAM_'+x[2][y][1]+'_'+x[2][y+1][1]+'_'+x[2][y+2][1]+'\t'
                    bigram=bigram.replace(':','COLON')
                    bigram=bigram.replace('\\','BACKSLASH')
                    posbigram=posbigram.replace(':','COLON')
                    posbigram=posbigram.replace('\\','BACKSLASH')
                    token=token.replace(':','COLON')
                    token=token.replace('\\','BACKSLASH')
                    pos=pos.replace(':','COLON')
                    pos=pos.replace('\\','BACKSLASH')
                feature+=pos
                feature+=token
                feature+=posbigram
                feature+=bigram
            print(feature)


#   myclass.myfunc(6)

if __name__ == "__main__": main()
