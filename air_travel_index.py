import pandas
import pickle
import numpy as np
"""
ati_dict={}
with open('Airports2.csv', newline='') as csvfile:
     airports = pandas.read_csv("Airports2.csv")
     
     for i in airports.iloc:
       origins=[str(j).replace(" ","") for j in i[2].split(",")]
       destinations=[str(j).replace(" ","") for j in i[3].split(",")]
       print(origins,destinations)
       if(origins[1]+"-"+destinations[1] not in ati_dict.keys()):
          ati_dict.update({origins[1]+"-"+destinations[1]:int(i[4])})
       else:
           ati_dict[origins[1]+"-"+destinations[1]]+=int(i[4])
print(ati_dict)
f=open("ati_dict.pkl","wb")
pickle.dump(ati_dict,f)
f.close()
"""
us_state = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

car_pickle = open ("ati_dict.pkl", "rb")
x = pickle.load(car_pickle)
x={k: v for k, v in sorted(x.items(), key=lambda item: item[1],reverse=True)}
internal_flying={}
remove_list=[]
for i in x.items():
   if(i[0].split("-")[0]==i[0].split("-")[1]):
      internal_flying.update({i[0].split("-")[0]:int(i[1])})
      remove_list.append(i[0])
for j in remove_list:
   del x[j]
norm_factor=0
for i in x.items():
   if(i[1]>norm_factor):
      norm_factor=i[1]
for i in x.items():
   x[i[0]]/=norm_factor
#print(internal_flying)
#print(x)
print(x)
states=list(us_state.values())
a = np.zeros((50,50,2))

counter1=0
counter2=0

while counter2<50:
   counter1=0
   while counter1<50:
      if(states[counter1]+"-"+states[counter2] in x.keys()):
         
         a[counter2][counter1][1]=x[states[counter1]+"-"+states[counter2]]
      counter1+=1
         
   counter2+=1

print(a[states.index("FL")])