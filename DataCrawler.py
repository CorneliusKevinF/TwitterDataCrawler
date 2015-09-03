'''
    Direct various types of responses into different files
    create a database of user profiles with the unique id as the identifier to eliminate redundant data in the tweets db
    properly handle nested json data
'''
import requests
from requests_oauthlib import OAuth1
import time

HTTP_STATUS_CODES = {'SUCCESS': 200}
URL = 'https://stream.twitter.com/1.1/statuses/sample.json'
CONSUMER_KEY = 'PjRG9bHsijcZTCo8a9OB1Fkvj'
CONSUMER_SECRET = 'WXykLT9uO3Vv8JKrT0PbpzJLxHPjUaHmMFOeudpbzRuhrdMkwt'
ACCESS_TOKEN = '3073073152-8U608uIPZdmlGBLdGTFZqJv56nNUpwQJ6N1k2rD'
ACCESS_TOKEN_SECRET = 'iYClOXdLVOS6C9KjHbFVGX0cnaotjOOVX0VrfLPobjGwB'
TARGET_FILE = 'twitterdata.csv'
NUMBER_OF_TWEETS = 2000 #number of tweets to be collected
MAX_WAIT_TIME = 11   #maximum number of seconds to wait before aborting process
DELAY = 5   #time to wait in seconds if there are no incoming tweets

auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
httpConnection = requests.get(URL, auth=auth, stream=True)

#Still need to handle the various other status codes returned by the request
print("Status Code: " + str(httpConnection.status_code) + " returned by " + URL + ".")

start = time.perf_counter()

if(httpConnection.status_code == HTTP_STATUS_CODES['SUCCESS']):
    tweetsGathered = 0
    timeWaited = 0
    # only works if the file isn't already in use
    
    print("Opening " + TARGET_FILE + "...")
    
    try:
        saveFile = open(TARGET_FILE, 'x')
    except FileExistsError:
        try: 
            saveFile = open(TARGET_FILE, 'a')
        except PermissionError: 
            print("Unable to open the target file. Please close the file and try again.")
            raise
        finally: 
            httpConnection.close()
        
    print("Successfully opened " + TARGET_FILE + ".")
    
    print("Gathering tweets...")
    for line in httpConnection.iter_lines():
        if line:
            tweetsGathered += 1
            json_string = line.decode('utf-8')
            saveFile.write(json_string)
            saveFile.write('\n')
        else:
            if timeWaited >= MAX_WAIT_TIME:
                print(str(timeWaited) + " seconds waited with no incoming tweet. Process aborted.")
                break
            timeWaited += DELAY
            time.sleep(DELAY)
        if tweetsGathered >= NUMBER_OF_TWEETS:
            break

elapsedTime = time.perf_counter() - start

print(str(tweetsGathered) + " entries written to " + TARGET_FILE + ".")
print("Time elapsed: " + str(elapsedTime))
print("Tweets processed per second: " + str(tweetsGathered / elapsedTime) + ".")

saveFile.close()
httpConnection.close()