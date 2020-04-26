import fbchat
from fbchat import Client
from fbchat.models import *
import time
import getpass
from os import listdir

def discard_special(word):
    retword = ''
    word = word.lower()
    for letter in word:
        if letter.isalpha():
            retword+=letter
    return retword

username = input("Enter your email id: ")
password = str()
try:
  password = getpass.getpass()
except Exception as error:
  print('ERROR', error)

client = Client(username, password)

friend_name = input("Enter name of friend you want to bother the fuck out of: ")
friend = ''
friends = client.searchForUsers(friend_name)
for i in range(len(friends)):
  print("Is {} the right friend?\nIs this their picture {}?".format(friends[i].name, friends[i].photo))
  resp = input()
  if len(resp) >= 1:
    if resp[0].lower() == 'y':
      friend = friends[i]
      break
    elif resp[0].lower() == 'n':
      continue
    else:
      print("Invalid option! Going to next item in the list of friends")
    if i == len(friends) - 1:
      exit()
    
movies = list()
files = listdir()
for file in files:
  if file.endswith('.script'):
    movies.append(file[:-7])
messages_seen = list()
no_count = 0
print("Enter the name of the script you wanna send word by word\nOptions: {}".format(movies))
movie_name = input()
if movie_name in movies:
  fh = open(movie_name+'.script')
  for line in fh:
    for word in line.split():
      msg_info = client.send(Message(text=word), thread_id=friend.uid, thread_type=ThreadType.USER)
      time.sleep(0.5)
      messages = client.fetchThreadMessages(limit = 3, thread_id = friend.uid)
      for message in messages:
        if message.uid not in messages_seen:
          msg_text = discard_special(message.text)
          if msg_text == 'no' or msg_text == 'stop':
            no_count+=1
          messages_seen.append(message.uid)
      time.sleep(0.5)
      if no_count == 8:
        msg_info = client.send(Message(text="I will stop now"), thread_id=friend.uid, thread_type=ThreadType.USER)
        exit()