output = []


def collect_sents(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start: end]
    sent = span.sent
    match_ents = {'start': span.start - sent.start, 'end': span.end - sent.start,
                  'label': doc.vocab.strings[match_id]}
    output.append({'text': sent.text, 'ents': match_ents})
    return output


def get_victim(line_l, nlp, Matcher):
    global output
    output = []
    line = line_l.lower().replace('\n', ' ')

    matching_rules = [
        ('murder_passive', [{'LEMMA': 'be'}, {'LEMMA': 'murder', 'OP': '*'}, {'POS': 'ADP', 'OP': '*'}]),
        ('kidnap', [{'LEMMA': 'be'}, {'LEMMA': 'kidnap'}]),
        ('killed', [{'LEMMA': 'be'}, {'LEMMA': 'killed'}]),
        ('murder_active', [{'LEMMA': 'be', 'OP': '!'}, {'ORTH': 'murdered'}]),
        ('massacre', [{'ORTH': 'to', 'OP': '!'}, {'ORTH': 'massacre'}])
    ]

    matcher = Matcher(nlp.vocab)
    [matcher.add(rule[0], collect_sents, rule[1]) for rule in matching_rules]

    doc = nlp(line)
    noun_chunk = []
    for noun in doc.noun_chunks:
        noun_chunk.append(noun.text)
    matcher(doc)
    final_nouns = []
    if len(output) > 0:
        rule_label = output[0]['ents']['label']
        noun_clauses = []

        for token in doc:
            if 'murder' in token.text:
                if rule_label == 'murder_active':
                    noun_clauses.extend([x.text for x in token.rights])

        if 'murder' in line:
            for ent in doc.ents:
                if ent.label_ == 'PERSON':
                    for x in noun_chunk:
                        if ent.text in x or x in ent.text:
                            final_nouns.append(ent.text)

        for n in noun_clauses:
            for x in noun_chunk:
                if n in x:
                    final_nouns.append(x)
        if len(final_nouns) > 0:
            return final_nouns[0].upper().replace('THE ', '')