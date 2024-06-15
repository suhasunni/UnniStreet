import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk import word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

class SentimentAnalysis:
    def __init__(self): 
        #initialize vectorizer
        self.vectorizer = TfidfVectorizer(use_idf=True,lowercase=True)
        #create instacne of model
        self.sentiment_analysis = self.create_sentiment_analysis()
        
    #Create and train sentiment analysis model    
    def create_sentiment_analysis(self):
        #read data from csv file
        df = pd.read_csv('best_data.csv')
        #vectorize text, set as independant variable
        x = self.vectorizer.fit_transform(df.text)
        #set dependant variable as sentiment score
        y = df.sentiment 
        #split data - 80% training and 20% testing
        x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2, random_state = 42)

        #create instance of naive bayes model
        jane_streets_secret = MultinomialNB()
        #train model
        jane_streets_secret.fit(x_train,y_train)

        #Commented line below tests accuracy of model with 20% of training data
        #print(roc_auc_score(y_test,jane_streets_secret.predict_proba(x_test), multi_class='ovo'))
        
        #Return model
        return jane_streets_secret
    
    #Returns sentiment value of inputted text
    def get_sentiment(self,text): 
        #remove ascii characters from text and put into list to be proccesed 
        text = [re.sub(r'[^a-zA-Z ]','',text)]
        #vectorize text
        vectorized_text = self.vectorizer.transform(text)
        #return sentiment of text
        return self.sentiment_analysis.predict(vectorized_text)
        
#Test phrases to demonstrate the model
# ob = SentimentAnalysis()
# print(ob.get_sentiment(' the stock is very bad it is not very good, sell it because it is crashing '))
# print(ob.get_sentiment('bull market, stock to the moon'))
# print(ob.get_sentiment('nothing is happening with the stock'))