#OpenSnoo v2.0
#Github release 2.0
#Special thanks to schulstreamer12 for json support

#Licenced under the AGPL 3.0 licence
#https://github.com/TryTurningOffAndOnAgain

#V2.0 features:
#- Back buttons for comments and posts
#- Image support
#- Titles automatically shortenedwith "..." added if they are over 80 characters

#Minor additions:
#- Icons added to buttons
#- Fixed comment loading glitch

from tkinter import *
import praw
import json
from PIL import Image, ImageTk
from io import BytesIO
from io import StringIO
import requests
from PIL import Image

subreddit = "all"
LoadedPosts = []
content = ""
submission = ""
seperate_for_processing = ''
comments_loaded = []
#cache for the new back feature
viewedcache = []
current_temporary_cache = ""
current_comment_location = 0
#loaded items
old_comments = []
size = 400, 400 #max size of image
img_loaded = False
run_once = True

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

#-------------------setup-------------------
window = Tk()
window.title("OpenSnoo v2.0 Alpha release")
#------------------imports------------------
back_ = PhotoImage(file="back.png")
next_ = PhotoImage(file="next.png")
back_comment = PhotoImage(file="back_comment.png")
next_comment_ = PhotoImage(file="next_comment.png")
search = PhotoImage(file="search.png")
image_unavailable = PhotoImage(file="no_image.png")

#----------------definitions----------------
def back():
    #back button function placeholder
    print('placeholder')

def stallfunction():
    #for actually loading new stuff, currently placeholder
    print('placeholder')

def last_comment():
    global current_comment_location
    current_comment_location -= 1
    comment.configure(text=comments_loaded[current_comment_location])

def next_comment():
    global current_comment_location
    current_comment_location += 1
    comment.configure(text=comments_loaded[current_comment_location])

def next_comment_public():
    current_comment_location = 0
    current_comments_temp_cache = comments_loaded.pop(0)
    comment.configure(text=current_comments_temp_cache)
    old_comments.append(current_comments_temp_cache)
 
def clicked():

    #change subreddits and load post ids into list
    subreddit = SubredditInput.get()
    poop = 'r/' + subreddit
    lbl.configure(text=poop)
    subreddit_true = reddit.subreddit(subreddit)
    LoadedPosts.clear()
    for submission in subreddit_true.hot(limit=200): #set how many posts you want loaded and if you want new or hot here
        LoadedPosts.append(submission.id)
    
    #load newest submission instantly:
    global image_url_cache
    seperate_for_processing = reddit.submission(id=LoadedPosts.pop(0))
    submission = seperate_for_processing
    if len(submission.title) > 80:
        shortened_name = submission.title[:80] + '...'
        postname.configure(text=shortened_name)
    else:
        postname.configure(text=submission.title)
    image_url_cache = submission.url
    post_text.configure(text=submission.selftext)
    link = seperate_for_processing.url
    ismature.configure(text="SWF")
    if submission.over_18 == True:
        ismature.configure(text="NSWF")
    author.configure(text='u/' + submission.author.name)
    print(image_url_cache)

    #load post comments:
    current_comment_location = 0
    comment.configure(text='')
    comments_loaded.clear()
    for top_level_comment in seperate_for_processing.comments:
        current_processed_comment = top_level_comment.body
        comments_loaded.append(current_processed_comment)
    
    #instantly load newest comment:
    next_comment_public()

    #load image
    if submission.is_self == False:
        image_downloaded = requests.get(image_url_cache)
        img = Image.open(BytesIO(image_downloaded.content))
        img.thumbnail(size, Image.ANTIALIAS)
        window.img = ImageTk.PhotoImage(img)
        canvas.itemconfig(window.imgArea, image = window.img)
    else:
         img = image_unavailable
         canvas.itemconfig(window.imgArea, image = window.img)

def next_post():
    #load newest submission instantly:
    global image_url_cache
    seperate_for_processing = reddit.submission(id=LoadedPosts.pop(0))
    submission = seperate_for_processing
    if len(submission.title) > 80:
        shortened_name = submission.title[:80] + '...'
        postname.configure(text=shortened_name)
    else:
        postname.configure(text=submission.title)
    image_url_cache = submission.url
    post_text.configure(text=submission.selftext)
    link = seperate_for_processing.url
    ismature.configure(text="SWF")
    if submission.over_18 == True:
        ismature.configure(text="NSWF")
    author.configure(text='u/' + submission.author.name)
    print(image_url_cache)

    #load post comments:
    current_comment_location = 0
    comment.configure(text='')
    comments_loaded.clear()
    for top_level_comment in seperate_for_processing.comments:
        current_processed_comment = top_level_comment.body
        comments_loaded.append(current_processed_comment)
    
    #instantly load newest comment:
    next_comment_public()

    #load image
    if submission.is_self == False:
        image_downloaded = requests.get(image_url_cache)
        img = Image.open(BytesIO(image_downloaded.content))
        img.thumbnail(size, Image.ANTIALIAS)
        window.img = ImageTk.PhotoImage(img)
        canvas.itemconfig(window.imgArea, image = window.img)
    else:
         img = image_unavailable
         canvas.itemconfig(window.imgArea, image = window.img)

if run_once == True:
    img = image_unavailable
    run_once == False

#----------------gui design----------------

if img_loaded == True:
    img = ImageTk.PhotoImage(img)  

canvas = Canvas(window, width=400, height=400)
canvas.grid(column=0, row=3)
 
window.imgArea = canvas.create_image(0, 0, anchor='nw')

imagesprite = canvas.create_image(400,400,image=img)

lbl = Label(window, text='No subreddit selected', font=("Arial Bold", 25))
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
btn = Button(window, text="Select subreddit", command=clicked, image = search, 
                    compound = LEFT)
btn.grid(column=2, row=1)

next_comment = Button(window, text="Next comment", command=next_comment, image = next_comment_, 
                    compound = LEFT)
next_comment.grid(column=4, row=1)

last_comment = Button(window, text=" Last comment", command=last_comment, image = back_comment, 
                    compound = LEFT)
last_comment.grid(column=4, row=2)

post_text=Message(window,text = "")
post_text.grid(row=3,column=0)

btn_next = Button(window, text="Next", command=next_post, image = next_, 
                    compound = LEFT)
btn_next.grid(column=3, row=1)

btn_back = Button(window, text="Back", command=back, image = back_, 
                    compound = LEFT)
btn_back.grid(column=3, row=2)

window.mainloop()
