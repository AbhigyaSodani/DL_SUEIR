import pandas
import pickle
import numpy as np

rti_dict={}
with open('Trips_by_distance.csv', newline='') as csvfile:
     airports = pandas.read_csv("Trips_by_distance.csv")
     counter=0
     for i in airports.iloc:
       counter+=1
       
       if i["Level"]=="State":
            if i["State Postal Code"] in rti_dict.keys():
                rti_dict[i["State Postal Code"]]+=int(i["Number of Trips >=500"].replace(",",""))
            else:
                rti_dict.update({i["State Postal Code"]:int(i["Number of Trips >=500"].replace(",",""))})

print(rti_dict)
f=open("rti_dict.pkl","wb")
pickle.dump(rti_dict,f)
f.close()
