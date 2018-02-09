import os
import re
from nltk import word_tokenize, sent_tokenize, pos_tag_sents,ne_chunk_sents, RegexpParser
import string
import math

def read_files():
    output = []
    data_file = os.path.abspath("developset/texts/merged-file.txt")
    p = re.compile('[A-Z]{3}[1-9]*-[A-Z]{3}[1-9]*-[0-9]{4}')
    with open(data_file, 'r') as f:
        content = f.readlines()
    file = [1]
    for c in content:
        if p.match(c) is not None:
            if file[0] != 1:
                file = "".join(file)
                output.append(file)
            file = list()
            file.append(c)
        else:
            file.append(c)

    return str("\n".join(output)).lower()


input_files = read_files()

table = str.maketrans({key : None for key in string.punctuation})

stripped_files = input_files.translate(table)
word_list = set([word for sent in sent_tokenize(stripped_files) for word in word_tokenize(sent)])

input_tokens = [[w for w in word_tokenize(sent) if w not in string.punctuation] for sent in sent_tokenize(input_files)]

vocab_size = len(word_list)

embed_size = 300
























