import praw
import re

reddit = praw.Reddit(client_id = '7yoyn3NZ1TCchULU48S9Rw', client_secret = 'tjF-qp0YOwFBjTijj3tI9wl3H1uvQA', username = 'WSB_Developer', password = 'ComputerScience', user_agent = 'none')

wall_street_bets = reddit.subreddit('wallstreetbets')

hot_posts = list(wall_street_bets.hot(limit = 5))


# NVDA = []
# for i in range(len(titles)):
#     flag = re.findall('NVDA', titles[i])
#     if len(flag) > 0:
#         NVDA.append(titles[i])

# x = hot_posts[1].comments[2].body
# print(x)

# def find_stock(stock_name):
#     posts = []
#     for i in range(len(titles)):
#         find_stock = re.findall(stock_name, titles[i])
#         if len(find_stock):
#             posts.append(titles[i])

def get_titles(sub_reddit):
    titles = []
    for post in sub_reddit:
        titles.append(post.title)
    return titles

def get_upvotes(sub_reddit):
    up_votes = []
    for post in sub_reddit:
        up_votes.append(post.score)
    return up_votes

def get_flair(sub_reddit):
    flair_types = []
    for post in sub_reddit:
        if post.link_flair_text != 'Meme':
            flair_types.append(post.link_flair_text)
    return flair_types





print(get_titles(hot_posts))
print(get_upvotes(hot_posts))
print(get_flair(hot_posts))

