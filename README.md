# Roget.py: a simple python script to access Roget's thesaurus

Does what it says on the tin. It loads the data files, and generates two versions of the thesaurus:

* `roget['entry']['part-of-speech'] = set(['some','words'])`
* `reverse_roget['word']['part-of-speech'] = set(['some','entries'])`

# General functions

These functions show what you can do with this script. If you think I should really add some particular function, please contact me.

```
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
```

## Resource

I used the ELKB version of Roget's thesaurus. You can download it [here](http://www.nzdl.org/ELKB/download.html).