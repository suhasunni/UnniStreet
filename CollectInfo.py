import praw
import re
from textblob import TextBlob

class Collect:
    def __init__(self, stock_name):
        #create stock name attribute
        self.__stock_name = stock_name 
        
        #create reddit instance
        self.__reddit = praw.Reddit(client_id = '7yoyn3NZ1TCchULU48S9Rw', client_secret = 'tjF-qp0YOwFBjTijj3tI9wl3H1uvQA', username = 'WSB_Developer', password = 'ComputerScience', user_agent = 'none')
        
        #create desired subreddit instance
        self.__wall_street_bets = self.__reddit.subreddit('wallstreetbets')
        
        #create list of posts mentioning stock_name
        self.__posts = self.filter_posts()
        
        #sentiment value
        self.__sentiment = self.create_simple_sentiment()

    def get_up_votes(self, post):
        return post.score

    #return posts that mention stock_name
    def filter_posts(self):
        #initialise return list
        relevant_posts = []
        
        #iterate through each post in r/wallstreetbets
        for post in self.__wall_street_bets.hot(limit = 1000):
            #disregard pinned posts 
            if not post.stickied:
                #disregard meme posts
                if not post.link_flair_text == 'Meme':
                    #find all instances of stock_name appearing in title of post
                    check_title = re.findall(self.__stock_name, post.title)
                    #append if instance exists
                    if len(check_title) > 0:
                        relevant_posts.append(post)
        for post in relevant_posts:
            print(post.title)
        
        if len(relevant_posts) > 0:
            #return array
            return relevant_posts
        else:
            return False
    
    #simple sentiment analysis using TextBlob method
    def create_simple_sentiment(self):
        average_score = 0
        if self.__posts != False:
            for post in self.__posts:
                temp_score_obj = TextBlob(post.title)
                average_score += temp_score_obj.sentiment.polarity   

            return average_score / len(self.__posts)

    
    #enhance simple sentiment analysis using keywords/common phrases
    def create_enhanced_sentiment(self, simple_score):
        #create return variable, currently equal to original simple-score
        new_sentiment_score = simple_score
        
        for post in self.__posts:
            
        #Add/Subtract sentiment score based on hard-coded key words
        #Implement weightage of upvotes/downvotes

        #hardcode negative result
            if post.link_flair_text == 'Gain':
                new_sentiment_score = abs(new_sentiment_score)
            elif post.link_flair_text == 'Loss':
                new_sentiment_score = -abs(new_sentiment_score)

         
    def get_sentiment(self):
        return self.__sentiment
        
    def get_posts(self):
        return self.__posts       
     
        