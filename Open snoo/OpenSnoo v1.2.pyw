from tkinter import *
import praw
import json

subreddit = "all"
LoadedPosts = []
content = ""
submission = ""
seperate_for_processing = ''
comments_loaded = []

#read in login info from json file
with open("login_data.json", "r") as handler:
    reddit_logindata = json.load(handler)

client_id_imported = reddit_logindata["client_id"]
client_secret_imported = reddit_logindata["client_secret"]
password_imported = reddit_logindata["password"]
user_agent_imported = reddit_logindata["user_agent"]
username_imported = reddit_logindata["username"]

#put ya login info here
reddit = praw.Reddit(client_id=client_id_imported, 
                    client_secret=client_secret_imported, 
                    password=password_imported,
                    user_agent=user_agent_imported,
                    username=username_imported)

#setup
window = Tk()

#script
window.title("OpenSnoo v1.2 Pre-Alpha release")

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

def clicked():

    #change subreddits and load post ids into list
    subreddit = SubredditInput.get()
    poop = 'r/' + subreddit
    lbl.configure(text=poop)
    subreddit_true = reddit.subreddit(subreddit)
    LoadedPosts.clear()
    for submission in subreddit_true.new(limit=45): #set how many posts you want loaded and if you want new or hot here
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
    comments_loaded.clear()
    for top_level_comment in seperate_for_processing.comments:
        current_processed_comment = top_level_comment.body
        comments_loaded.append(current_processed_comment)
    
    #instantly load newest comment:
    current_viewing = comments_loaded.pop(0)
    comment.configure(text=current_viewing)
    
    

finished = seperate_for_processing
btn = Button(window, text="Select subreddit", command=clicked)
btn.grid(column=2, row=1)

def next_comment():
    current_viewing = comments_loaded.pop(0)
    comment.configure(text=current_viewing)

next_comment = Button(window, text="Next comment", command=next_comment)
next_comment.grid(column=4, row=1)

post_text=Message(window,text = "")
post_text.grid(row=3,column=0)

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

btn_next = Button(window, text="Next", command=next_post)
btn_next.grid(column=3, row=1)

window.mainloop()
