#!/usr/bin/env python3

"""
create_baseline_features.py: This scipt is used on the data to generate the baseline features

To run:
python3 create_baseline_features.py ./data/test/0001.csv > baseline_features.txt

The "hw3_corpus_tool.py" file provided with the assignment has been used in this script to read csv data. 
4 baseline features are generated that can be used to train the CRFSuite. The script can handle training 
and testing data.

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
        #print new line betweeen every two dialgues
        print()
        for x in DialogUtterance:
            feature=''
            pos=''
            token=''
            #First attribute: act of speech tag for training data or 'UNK' for testing data
            if(x[0] is not None):
                feature+=x[0]+'\t'
            else:
                feature+='UNK'+'\t'
            #First feature : Represents the first utterance of the dialogue.
            if(firstline):
                feature+='FIRST_LINE'+'\t'
                speaker=x[1]
                firstline=False
            #Second feature: Represents whether or not the speaker has changed in comparision with the previous utterance.
            else:
                if(x[1]!=speaker):
                    feature+='CHANGE_SPEAKER'+'\t'
                speaker=x[1]
            #Third feature : every token in the utterance 
            #Fourth feature : every part of speech tag in the utterance
            #CRF cannot handle ':' and '\' in feature names, hence have been replaced with 'COLON' and 'BACKSLASH'
            if(x[2] is not None):
                for y in x[2]:
                    token+='TOKEN_'+y[0]+'\t'
                    pos+='POS_'+y[1]+'\t'
                token=token.replace(':','COLON')
                token=token.replace('\\','BACKSLASH')
                pos=pos.replace(':','COLON')
                pos=pos.replace('\\','BACKSLASH')
            feature+=pos
            feature+=token
            print(feature)

if __name__ == "__main__": main()
