import re
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet, stopwords

lemmatizer = WordNetLemmatizer()
def get_lemma(word):
    pos_tags = [wordnet.VERB, wordnet.ADJ, wordnet.ADV, wordnet.NOUN]
    for tag in pos_tags:
        lemma = lemmatizer.lemmatize(word, tag)
        if lemma != word:
            return lemma
    return word

        

class Document():
    stopwords = stopwords.words('english')
    with open('./stopwords.txt', 'r', newline='') as file:
        for word in file.readlines():
            word = word.replace('\n', '')
            if word not in stopwords:
                stopwords.append(word)
    
    def __init__(self, text):
        self.text = text
        self.terms_frequency = {}

    def preprocess(self):
        self.text = self.text.replace('\n', ' ') # 移除換行

        # 移除特殊（標點）符號
        self.text = re.sub(r'[^a-zA-Z0-9]', ' ', self.text)

        # 移除 single character
        self.text = re.sub(r'\s+[a-zA-Z]\s+', ' ', self.text)

        for word in word_tokenize(self.text):
            token = word.lower()
            if token in Document.stopwords:
                continue
            if bool(re.search(r'\d', token)):
                continue
            token = get_lemma(token)
            if token not in self.terms_frequency:
                self.terms_frequency[token] = 1
            else:
                self.terms_frequency[token] += 1
    
    def get_terms_frequency(self):
        return self.terms_frequency