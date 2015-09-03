import DataProcessor
import DataBuffer
import time

"""
inputFile = open('twitterdata.csv', 'r')
outputFile = open('twitterinfo.csv', 'w')

dp = DataProcessor.DataProcessor(inputFile, outputFile)

for x in range(1, 10):
    dp.processLine()
"""

#buffer/processor test
try:
    p = DataProcessor.DataProcessor('twitterinfo.csv')
    b = DataBuffer.DataBuffer()
    
    inputFile = open('twitterdata.csv', 'r')
    
    startTime = time.perf_counter()
    ITERATIONS = 40
    BUFFER_MAX_SIZE = 50
    
    
    for j in range(0, ITERATIONS):
        for i in range(0, BUFFER_MAX_SIZE):
            b.pushItem(inputFile.readline())
        
        for i in range(0, BUFFER_MAX_SIZE):
            p.processLine(b.popItem())

    endTime = time.perf_counter()
    
    #print test stats
    timeElapsed = endTime - startTime
    tweetsFiltered = ITERATIONS * BUFFER_MAX_SIZE
    print(str(tweetsFiltered) + " tweets filtered in " + str(timeElapsed) + " seconds.")
    print(str(tweetsFiltered / timeElapsed) + " tweets filtered per second.")
finally:
    p.close()
    inputFile.close()
    
