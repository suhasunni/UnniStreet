import praw
import re
from textblob import TextBlob

class Collect:
    def __init__(self, stock_name):
        self.__stock_name = stock_name 
        
        #create reddit instance
        self.__reddit = praw.Reddit(client_id = '7yoyn3NZ1TCchULU48S9Rw', client_secret = 'tjF-qp0YOwFBjTijj3tI9wl3H1uvQA', username = 'WSB_Developer', password = 'ComputerScience', user_agent = 'none')
        
        #create desired subreddit instance
        self.__wall_street_bets = self.__reddit.subreddit('wallstreetbets')
        
        #create list of posts mentioning stock_name
        self.__posts = self.filter_posts()
        

    def get_up_votes(self, post):
        return post.score

    #return posts that mention stock_name
    def filter_posts(self):
        relevant_posts = []
        #iterate through each post in r/wallstreetbets
        for post in self.__wall_street_bets.hot(limit = 100):
            #find all instances of stock_name appearing in title of post
            check_title = re.findall(self.__stock_name, post.title)
            #append if instance exists
            if len(check_title) > 0:
                relevant_posts.append(post)
        for post in relevant_posts:
            print(post.title)
        #return array
        return relevant_posts
    
    def get_sentiment(self):
        average_score = 0
        for post in self.__posts:
            temp_score_obj = TextBlob(post.title)
            average_score += temp_score_obj.sentiment.polarity   

        return average_score / len(self.__posts)

    def enhance_sentiment(self):
        #Add/Subtract sentiment score based on hard-coded key words
        #Implement weightage of upvotes/downvotes
        #hello
        pass   
         
        
           
     
        