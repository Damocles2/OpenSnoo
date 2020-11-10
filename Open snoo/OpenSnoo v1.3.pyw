#OpenSnoo v1.3 
#Github release 1.2
#Special thanks to schulstreamer12 for json support

#Licenced under the AGPL 3.0 licence
#https://github.com/TryTurningOffAndOnAgain

#V1.3 features: A ton of small bugfixes and major code organisation/logical rearangement

from tkinter import *
import praw
import json
import time

subreddit = "all"
LoadedPosts = []
content = ""
submission = ""
seperate_for_processing = ''
comments_loaded = []

#read in login info from json file
with open("login_data.json", "r") as handler:
    reddit_logindata = json.load(handler)

client_id_im = reddit_logindata["client_id"]
client_secret_im = reddit_logindata["client_secret"]
password_im = reddit_logindata["password"]
user_agent_im = reddit_logindata["user_agent"]
username_im = reddit_logindata["username"]

#put ye login info here
reddit = praw.Reddit(client_id=client_id_im,
                     client_secret=client_secret_im,
                     password=password_im,
                     user_agent=user_agent_im,
                     username=username_im)

#setup (feel free to use for setup related stuff its empty)
window = Tk()
window.title("OpenSnoo v1.2 Pre-Alpha release")

#----------------definitions----------------
def clicked():

    #change subreddits and load post ids into list
    subreddit = SubredditInput.get()
    poop = 'r/' + subreddit
    lbl.configure(text=poop)
    subreddit_true = reddit.subreddit(subreddit)
    LoadedPosts.clear()
    for submission in subreddit_true.hot(limit=45): #set how many posts you want loaded and if you want new or hot here
        LoadedPosts.append(submission.id)
    
    #load newest submission instantly:
    seperate_for_processing = reddit.submission(id=LoadedPosts.pop(0))
    submission = seperate_for_processing
    postname.configure(text=submission.title)
    post_text.configure(text=submission.selftext)
    link = seperate_for_processing.url
    ismature.configure(text="SWF")
    if submission.over_18 == True:
        ismature.configure(text="NSWF")
    author.configure(text='u/' + submission.author.name)

    #load post comments:
    comment.configure(text='')
    comments_loaded.clear()
    for top_level_comment in seperate_for_processing.comments:
        current_processed_comment = top_level_comment.body
        comments_loaded.append(current_processed_comment)
    
    #instantly load newest comment:
    time.sleep(0.2)
    next_comment()

def next_comment():
    current_viewing = comments_loaded.pop(0)
    comment.configure(text=current_viewing)

def next_post():
    #load newest submission instantly:
    seperate_for_processing = reddit.submission(id=LoadedPosts.pop(0))
    submission = seperate_for_processing
    postname.configure(text=submission.title)
    post_text.configure(text=submission.selftext)
    link = seperate_for_processing.url
    ismature.configure(text="SWF")
    if submission.over_18 == True:
        ismature.configure(text="NSWF")
    author.configure(text='u/' + submission.author.name)

    #load post comments:
    comments_loaded.clear()
    for top_level_comment in seperate_for_processing.comments:
        current_processed_comment = top_level_comment.body
        comments_loaded.append(current_processed_comment)
    
    #instantly load newest comment:
    current_viewing = comments_loaded.pop(0)
    comment.configure(text=current_viewing)


def copy_post_link():
    window.clipboard_append(submission.url)
    window.update() # now it stays on the clipboard after the window is closed

#----------------gui design----------------
lbl = Label(window, text='No subreddit selected', font=("Arial Bold", 50))
lbl.grid(column=0, row=0)

postname = Label(window, text='', font=("Arial Bold", 12))
postname.grid(column=0, row=2)

comment = Message(window, text=' ')
comment.grid(column=1, row=3)

SubredditInput = Entry(window,width=20)
SubredditInput.grid(column=1, row=1)

ismature = Label(window, text=' ')
ismature.grid(column=1, row=2)

author = Label(window, text=' ')
author.grid(column=2, row=2)

finished = seperate_for_processing
btn = Button(window, text="Select subreddit", command=clicked)
btn.grid(column=2, row=1)

next_comment = Button(window, text="Next comment", command=next_comment)
next_comment.grid(column=4, row=1)

post_text=Message(window,text = "")
post_text.grid(row=3,column=0)

btn_next = Button(window, text="Next", command=next_post)
btn_next.grid(column=3, row=1)

window.mainloop()
