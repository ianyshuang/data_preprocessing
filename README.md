# 資料預處理

1. 確保 `raw.csv` 存在，若尚未存在則加到專案的根目錄，此處的 `raw.csv` 只是示範用。第一列不要有 column name（`name`|`state`|`content`），如果有的話，請先手動移除。
2. 執行 `python/python3 main.py`
3. 會產生六個檔案，分別代表 training、validation、testing 的 tf / tf-idf 資料。
    - training_tf.csv
    - training_tfidf.csv
    - validation_tf.csv
    - validation_tfidf.csv
    - testing_tf.csv
    - testing_tfidf.csv