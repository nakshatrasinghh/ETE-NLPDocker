#@ Necessary imports and dependancies
import pandas as pd
import numpy as np
from flask import Flask, render_template, url_for, request
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('sentiment.tsv', sep='\t')
df.columns = ["label", "text"]
#@ Features and Labels
df['label'] = df['label'].map({'pos': 1, 'neg': 0})
#@ Convert a collection of text to a matrix of tokens
cv = CountVectorizer()
message_bow = cv.fit_transform(df['text'])

X_train, x_validation, Y_train, y_validation = train_test_split(
    message_bow, df['label'], test_size=0.2, random_state=0)

classifier = MultinomialNB(alpha=0.1).fit(X_train, Y_train)

#@ Main app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
    	message = request.form['message']
    	data = [message]
    	vect = cv.transform(data).toarray()
    	my_prediction = classifier.predict(vect)
    	return render_template('result.html', prediction=my_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)
 