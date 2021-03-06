import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)

terminology_list = [u"Barack Obama", u"Angela Merkel", u"Washington, D.C."]
# Only run nlp.make_doc to speed things up
patterns = [nlp.make_doc(text) for text in terminology_list]
print(patterns)
matcher.add("TerminologyList", None, *patterns)

doc = nlp(u"German Chancellor Angela Merkel and US President Barack Obama "
          u"converse in the Oval Office inside the White House in Washington, D.C.")
print(doc)
matches = matcher(doc)
print(matches)
for match_id, start, end in matches:
    span = doc[start:end]
    print(span.text)