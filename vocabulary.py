import math
class Vocabulary():
    def __init__(self):
        '''Initialize

        Params:
        doc_counts (int): document 數量
        '''
        self.document_counts = 0
        self.terms_document_frequency = {}    # 存放各個 terms 的 document frequency

    def add_terms(self, terms):
        '''將 documents 的 terms 加到 vocabulary 中

        Params:
        terms ([str]): 該 document 的 terms (after preprocessed)
        
        Returns: None
        '''
        for term in terms:
            if term not in self.terms_document_frequency:
                self.terms_document_frequency[term] = 1
            else:
                self.terms_document_frequency[term] += 1
        self.document_counts += 1
            
    def get_terms(self):
        return list(sorted(self.terms_document_frequency.keys()))

    def get_idf(self, term):
        '''回傳指定 term 的 idf

        Params:
        term (str): 要取得 idf 的 term
        '''
        return math.log10(self.document_counts/self.terms_document_frequency[term])
