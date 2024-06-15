import praw
import re
from Sentiment import SentimentAnalysis

class Stock:
    def __init__(self, stock_name):
        
        self.stock_name = stock_name
        
        #create instance of Reddit API
        self.reddit_API = praw.Reddit(client_id = '7yoyn3NZ1TCchULU48S9Rw', client_secret = 'tjF-qp0YOwFBjTijj3tI9wl3H1uvQA', username = 'WSB_Developer', password = 'ComputerScience', user_agent = 'none')
        
        #create instance of r/wallstreetbets subreddit
        self.wall_street_bets = self.reddit_API.subreddit('wallstreetbets') 
        
        #obtain relevant posts objects
        self.posts = self.get_posts()

    #function to retrieve titles of reddit posts
    def get_posts(self):
        #initialize return array
        posts = []
        #check every post in subreddit - limit to first n posts to save time
        for post in self.wall_street_bets.hot(limit = 500):
            #omit pinned posts
            if not post.stickied:
                #omit posts labelled as memes
                if not post.link_flair_text == 'Meme':
                    check_title = re.findall(self.stock_name, post.title)
                    #append if instance exists  
                    if len(check_title) > 0:   
                        posts.append(post) 
        #return list of post objects 
        return posts
    
    #Returns array of post titles
    def get_titles(self):
        titles = []
        for post in self.posts:
            titles.append(post.title)
            
        #print(titles)
        return titles
    
    #Returns average score of every post for a stock
    def get_overall_score(self,list_of_scores):
        overall_score = 0
        for score in list_of_scores:
            overall_score+=score
        
        overall_score=[overall_score/len(list_of_scores)]
        return overall_score
    
    #Returns list of sentiment scores for each post
    def get_scores(self):
        #initialize return variable
        scores = []
        #initialize model 
        sentiment_analyzer = SentimentAnalysis()

        for post in self.posts:
            #Initialise score varibale for induvidual post
            post_score = 0 
            #Hard-code sentiment scores based on user-given post tags
            if post.link_flair_text == 'Gain':
                post_score = 1
            elif post.link_flair_text == 'Loss':
                post_score = -1
            #For posts without tags, calculate sentiment using model
            else:
                #run text through sentiment analysis 
                post_score += sentiment_analyzer.get_sentiment(post.title)   
            #Scale score based on number of upvotes (post.score !=0 since that would create a neutral score of 0)
            if post.score > 0:
                post_score *= post.score
                         
            #Append to return list
            scores.append(int(post_score))
        
        #Check if list is empty, if empty return false
        if len(self.posts) > 0:
            return scores
        else:
            return False
        
     #Returns sentiment of single text input   
    def get_induvidual_sentiment(self,text): 
        sentiment_analyzer = SentimentAnalysis()
        return sentiment_analyzer.get_sentiment(text)
    