import nltk
nltk.download('stopwords')

import matplotlib.pyplot as plt
import seaborn as sns
import json 
import pickle
import random
import re
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


class ChatBot:
    def __init__(self):
        self.tags = []
        self.patterns = []
        self.responses = {} 
        self.data = None
        self.model = None
    
        # intialize the lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        
        # get the stop words from the nltk library
        self.stop_words = set(stopwords.words('english'))

    def laod_data(self, file_path=None):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print("File Not found")
        
        intends = self.data.get('intents')
        if not intends:
            print("No 'intents' key found in the JSON file.")
            return

        self.patterns = []
        self.tags = []
        self.responses = {}
        

        for intent in intends:
            tag = intent['tag']

            self.responses[tag] = intent['responses']


            for pattern in intent.get('patterns', []):
                processed_text = self.preprocess_text(pattern)

                self.patterns.append(processed_text)
                self.tags.append(tag)

        print("Data extracted from intents.json")
        print("Number of patterns:", len(self.patterns))
        print("Number of unique tags:", len(set(self.tags))) 
        print("Tags:", set(self.tags))

    def preprocess_text(self, text):
        # lower the text {Hi -> hi}
        text = text.lower()

        # removes the links {http://amazon.com}
        text = re.sub(r'http\S+', '', text)

        # remove any html tags {<br>}
        text = re.sub(r'[<?*>]', '', text)

        # split the words into tokens
        tokens = word_tokenize(text)


        # remove the stop words from the tokens {is, no, yes, read} -> {yes, no, read}
        tokens = [token for token in tokens if token not in self.stop_words]

        # lemmatize each words in the token { reading -> read }
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        # Join tokens back into text
        processed_text = ' '.join(tokens)

        return processed_text 
    
    def evaluate_model(self, x_test, y_test):
        if not self.model:
            print("Model not built yet.")
            return
        
        # predict the x_test
        y_pred = self.model.predict(x_test)

        # calculate the accuracy_score
        accuracy = accuracy_score(y_test, y_pred)

        # build a confussion matrix for sns heatmap 
        confusion = confusion_matrix(y_test, y_pred)

        # generate a classification report
        classification_rep = classification_report(y_test, y_pred)

        print("Accuracy:", accuracy)
        print("Confusion Matrix:\n", confusion)
        print("Classification Report:\n", classification_rep)

        # plot the confusion matrix using seaborn
        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion, annot=True, fmt='d', cmap='Blues', xticklabels=set(self.tags), yticklabels=set(self.tags))
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.show()


    def build(self, test_size=0.2):
        print("Building and training the model...")
        x_train, x_test, y_train, y_test = train_test_split(self.patterns, self.tags, test_size=test_size)

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', SVC(kernel='linear'))
        ])

        self.model.fit(x_train, y_train)
        print("Model training complete.")
        self.evaluate_model(x_test, y_test)
    
        with open('ChatBot.pkl', 'wb') as model_file:
            pickle.dump(self.model, model_file)

    def load_model(self, model_path):
        if os.path.isfile(model_path):
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
            print("Model loaded from disk.")
            return True
        else:
            print(f"Model file '{model_path}' not found.")
            return False
        
    def predict(self, user_input):
        if not self.model:
            return "Error: Model not loaded."
        
        process_input = self.preprocess_text(user_input)
        predicted_tag = self.model.predict([process_input])[0]
        
        if predicted_tag in self.responses:
            return random.choice(self.responses[predicted_tag])
        else:
            return "I'm sorry, I don't understand that."