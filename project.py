import os
import re
from nltk import word_tokenize, sent_tokenize, pos_tag_sents,ne_chunk_sents, RegexpParser

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
    return output


def read_answers():
    output = []
    data_file = os.path.abspath("developset/answers/ans_merged.txt")

    with open(data_file, 'r') as f:
        content = f.readlines()
    file = [1]
    for c in content:
        if "ID:" in c:
            if file[0] != 1:
                file = "".join(file)
                output.append(file)
            file = list()
            file.append(c)
        else:
            file.append(c)

    for i,o in enumerate(output):
        new_o = {}
        last_key = ""
        for x in o.split('\n'):
            x = x.split(':')
            if len(x) < 2:
                new_o[last_key].append(x[0].strip())
            else:
                new_o[x[0]] = [x[1].strip()]
                last_key = x[0]
        output[i] = new_o
    return output


def create_proper_noun_dictionary():
    proper_nouns = []
    answers = read_answers()
    keys = ["VICTIM", "PERP ORG", "PERP INDIV"]
    for answer in answers:
        for key in keys:
            if answer[key] != '-' and answer[key] is not None:
                add = [[x for x in y.split('/')] for y in answer[key]][0]
                if '/' in add:
                    add = add.split('/')
                proper_nouns.extend(add)

    return set(proper_nouns)


def tokenize_text(text, lower_all=False):
    text = sent_tokenize(text)
    for i,t in enumerate(text):
        text[i] = word_tokenize(t)
    if lower_all:
        text = [[word.lower() for word in sent] for sent in text]
    return text


def true_case_text(text, proper_noun):
    proper_tokens = [word_tokenize(pn) for pn in proper_noun]
    proper_tokens = list(set([word.capitalize() for word_list in proper_tokens for word in word_list]))
    for i,sent in enumerate(text):
        for j, word in enumerate(sent):
            if j == 0:
                sent[j] = word.capitalize()
            if word in proper_tokens:
                sent[j] = word.capitalize()
        text[i] = sent
    return text

def ner_chunker(tagged_sentence):
    grammar = "NP: {<DT>?<NN|NNS|NNP|NNPS>+}"
    parser = RegexpParser(grammar)
    ner_tagged = parser.parse(tagged_sentence)
    return ner_tagged

input_files = read_files()
proper_noun = create_proper_noun_dictionary()
for file in input_files:
    tokens = tokenize_text(file, lower_all=True)
    tokens = true_case_text(tokens, proper_noun)
    pos_tagged = pos_tag_sents(tokens)
    print(file)
    for x in pos_tagged:
        a = ner_chunker(x)
        print(a)
    print()
    print("##########################################################################################################################################")
    print()
