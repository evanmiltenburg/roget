import glob, lxml, re
from lxml import etree

# clean the input
def clean(l):
    l = l.replace('<size=-1>','')
    l = l.replace('</size>','')
    l = l.replace('<br>','')
    l = l.replace('&','&amp;')
    l = l.replace('"<"','&lt;')
    l = l.replace('">"','&gt;')
    return l.rstrip(',;\n') + '\n'

# get information from the xml
def headword(class_element):
    return re.sub('[0-9#\[\] ]','',class_element.find("headword").find("b").text)

def pos(pos_element):
    return re.sub('[.#]','',pos_element.find("b").text)

def words(paragraph_element):
    return set([word.strip() for i in paragraph_element 
           if not i.text is None 
           for word in i.text.split(',') 
           if not word == ' '
           ])

def index(fn,root):
    return re.sub('[/heads.txt]','',fn + ' ') + headword(root)

# helper generator:
def pospargen(c):
    for a,b in [c[x:x+2] for x in xrange(len(c)-1)]:
        if a.tag == 'pos' and b.tag == 'paragraph':
            yield [a,b]

# get list of [POS, [words,in,entry]]
def pos_words(c):
    return dict([[pos(a),words(b)] for a,b in pospargen(c)])

roget = {}

for fn in glob.glob("./heads/head*.txt"):
    with open(fn,'rb') as f:
        xml = ['<class>']+[clean(l) for l in f.readlines()]+['</class>']
        root = etree.fromstring(''.join(xml), parser=etree.XMLParser(encoding="windows-1252"))
        roget[index(fn,root)] = pos_words(root.getchildren())

parts_of_speech = ['INT', 'VB', 'ADJ', 'N']

from collections import defaultdict

reverse_roget = defaultdict(set)
for category in roget:
    for pos in parts_of_speech:
        if pos in roget[category]:
            for word in roget[category][pos]:
                reverse_roget[word + '_' + pos].add(category)

# INTERFACE COMMANDS
def categories(word,pos):
    "If you want to know which entries a word with a given part of speech occurs in"
    return reverse_roget[word + '_' + pos]

def common_categories(w1,w2,pos):
    "If you want to know which categories are shared by two words with a given part of speech"
    return reverse_roget[w1 + '_' + pos] & reverse_roget[w2 + '_' + pos]

def list_words(category,pos):
    "If you want to list the words with a given part of speech for an entry"
    return roget[category][pos]

def all_entries(word,pos):
    "If you want a list of lists, with each list containing the words for an entry"
    return [list_words(category,pos) for category in categories(word,pos)]

def shared_categories(l,pos):
    "If you want to know which categories are shared by a list of words with a given part of speech"
    return set.intersection(*[categories(w,pos) for w in l])
