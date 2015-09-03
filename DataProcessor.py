import json

class DataProcessor:
    #TODO extract user info later from nested json object
    #TODO should make code tolerant of missing names in the json data
    relevantNames = ['id_str', 'lang', 'created_at', 'text', 'source']
    
    def __init__(self, outputFile):
        try:
            self.targetFile = open(outputFile, 'x')
        except FileExistsError:
            self.targetFile = open(outputFile, 'a')
        
        print("New DataProcessor instantiated.")
        
    def processLine(self, line):
        rawJsonData = json.loads(line)
        
        if 'created_at' not in rawJsonData:
            return
        else:
            filteredData = {}
            
            for name in self.relevantNames:
                filteredData[name] = rawJsonData[name]
            
            jsonOutput = json.dumps(filteredData)

            self.targetFile.write(jsonOutput)
            self.targetFile.write('\n')
        
    def close(self):
        self.targetFile.close()