#!/usr/bin/python3

import configparser 

myIniFile="./azureAccountDetails.ini"
Outfile="../myLibForAzure/SelectAccount.py"

class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d

if __name__ == "__main__":
    fileToParseObject = MyParser()
    fileToParseObject.read(myIniFile)
    myDict = fileToParseObject.as_dict()
    
    i = 0
    myCompanyNameDict = dict();
    for key in myDict.keys():
        myCompanyNameDict[i] = key
        i = i + 1
   
    for key,value in myCompanyNameDict.items():
        print("{} - {}".format(key, value))
   
    while True:
        try:
            selectedCompanyKey = None
            while selectedCompanyKey not in myCompanyNameDict.keys():
                selectedCompanyKey = int(input("select number of you company:"))
        except KeyboardInterrupt:
            exit()
        except:
            continue
        break
    selectedCompany = myCompanyNameDict[selectedCompanyKey]
    selectedCompanyValues=myDict[selectedCompany]
    with open(Outfile,'w') as OutfilePy:
        for key,value in selectedCompanyValues.items():
             OutfilePy.write(key)
             OutfilePy.write('="')
             OutfilePy.write(value)
             OutfilePy.write('"\n')
