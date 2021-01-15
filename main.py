import os
import csv
from document import Document
from vocabulary import Vocabulary

CSV_PATH = './raw.csv'

def write_tf(dataset, filename, vocabulary):
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(['name', 'state', 'TF'])
    
    for data in dataset:
        voc_terms_frequency = []
        doc_terms_frequency = data['document'].get_terms_frequency()

        for term in vocabulary.get_terms():
            if term not in doc_terms_frequency:
                voc_terms_frequency.append(f'"{term}":0')
            else:
                freq = doc_terms_frequency[term]
                voc_terms_frequency.append(f'"{term}":{freq}')

        
        tf_dict = '{' + ','.join(voc_terms_frequency) + '}'
        with open(filename, 'a') as file:
            writer = csv.writer(file, delimiter='|', quotechar='', quoting=csv.QUOTE_NONE)
            writer.writerow([data['name'], data['state'], tf_dict])

def write_tf_idf(dataset, filename, vocabulary):
    with open(filename, 'w') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(['name', 'state', 'TF-IDF'])
    
    for data in dataset:
        voc_terms_frequency = []
        doc_terms_frequency = data['document'].get_terms_frequency()

        for term in vocabulary.get_terms():
            if term not in doc_terms_frequency:
                voc_terms_frequency.append(f'"{term}":0')
            else:
                tf_idf = doc_terms_frequency[term] * vocabulary.get_idf(term)
                voc_terms_frequency.append(f'"{term}":{tf_idf}')

        
        tfidf_dict = '{' + ','.join(voc_terms_frequency) + '}'
        with open(filename, 'a') as file:
            writer = csv.writer(file, delimiter='|', quotechar='', quoting=csv.QUOTE_NONE)
            writer.writerow([data['name'], data['state'], tfidf_dict])

successful_count = failed_count = other_count = 0
training_data = []
validation_data = []
testing_data = []

print('區分資料並預處理中...')
with open(CSV_PATH, 'r', newline='') as file:
    rows = list(csv.reader(file, delimiter='|'))
    # 計算「成功/失敗」的個別個數
    for row in rows:
        if row[1] == 'successful':
            successful_count += 1
        elif row[1] == 'failed':
            failed_count += 1
        else:
            other_count += 1
    
    # 將「成功/失敗」 各以 70/15/15的比例分配到 training/validation/testing 中
    successful_partitions = [int(successful_count * 0.7), int(successful_count * 0.85)]
    failed_partitions = [int(failed_count * 0.7), int(failed_count * 0.85)]

    successful_count = failed_count = 0
    for row in rows:
        data = {
            'document': Document(row[2]),
            'state': row[1],
            'name': row[0]
        }
        if data['state'] != 'successful' and data['state'] != 'failed':
            continue
        data['document'].preprocess()   # 先將文章預處理

        if data['state'] == 'successful':
            if successful_count < successful_partitions[0]:
                training_data.append(data)
            elif successful_count < successful_partitions[1]:
                validation_data.append(data)
            else:
                testing_data.append(data)
            successful_count += 1
        else:
            if failed_count < failed_partitions[0]:
                training_data.append(data)
            elif failed_count < failed_partitions[1]:
                validation_data.append(data)
            else:
                testing_data.append(data)
            failed_count += 1

# 從 training data 建立 vocabulary
print('Training Data Numbers: ', len(training_data))
print('Validation Data Numbers: ', len(validation_data))
print('Testing Data Numbers: ', len(testing_data))
print('Exculding Data Numbers: ', other_count)
print('建立 vocabulary 中...')
vocabulary = Vocabulary()
for data in training_data:
    doc_terms = list(data['document'].get_terms_frequency().keys())
    vocabulary.add_terms(doc_terms)

print('寫入 TF CSV 檔中...')
write_tf(training_data, 'training_tf.csv', vocabulary)
write_tf(validation_data, 'validation_tf.csv', vocabulary)
write_tf(testing_data, 'testing_tf.csv', vocabulary)

print('寫入 TF_IDF CSV 檔中...')
write_tf_idf(training_data, 'training_tfidf.csv', vocabulary)
write_tf_idf(validation_data, 'validation_tfidf.csv', vocabulary)
write_tf_idf(testing_data, 'testing_tfidf.csv', vocabulary)


print(vocabulary.get_terms())