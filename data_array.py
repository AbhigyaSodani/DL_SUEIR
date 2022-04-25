import pandas
import pickle
import numpy as np

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
"""
neighboring_dict=
{
    "Alabama":	"Mississippi, Tennessee, Florida, Georgia",
2.	"Alaska":	None,	
3.	"Arizona"	:Nevada, New Mexico, Utah, California, Colorado	
4.	Arkansas	Oklahoma, Tennessee, Texas, Louisiana, Mississippi, Missouri	
5.	California	Oregon, Arizona, Nevada
3
6.	Colorado	New Mexico, Oklahoma, Utah, Wyoming, Arizona, Kansas, Nebraska	
7.	Connecticut	New York, Rhode Island, Massachusetts	
8.	Delaware	New Jersey, Pennsylvania, Maryland	
9.	Florida	Georgia, Alabama
2
10.	Georgia	North Carolina, South Carolina, Tennessee, Alabama, Florida	
11.	Hawaii	None	
12.	Idaho	Utah, Washington, Wyoming, Montana, Nevada, Oregon	
13.	Illinois	Kentucky, Missouri, Wisconsin, Indiana, Iowa, Michigan	
14.	Indiana	Michigan, Ohio, Illinois, Kentucky	
15.	Iowa	Nebraska, South Dakota, Wisconsin, Illinois, Minnesota, Missouri	
16.	Kansas	Nebraska, Oklahoma, Colorado, Missouri	
17.	Kentucky	Tennessee, Virginia, West Virginia, Illinois, Indiana, Missouri, Ohio	
18.	Louisiana	Texas, Arkansas, Mississippi	
19.	Maine
(The state which borders only one other U.S. state.)	New Hampshire
1
20.	Maryland	Virginia, West Virginia, Delaware, Pennsylvania	
21.	Massachusetts	New York, Rhode Island, Vermont, Connecticut, New Hampshire	5
22.	Michigan	Ohio, Wisconsin, Illinois, Indiana, Minnesota (water border)	5
23.	Minnesota	North Dakota, South Dakota, Wisconsin, Iowa, Michigan (water border)	5
24.	Mississippi	Louisiana, Tennessee, Alabama, Arkansas	4
25.	Missouri
(The state which touches the most other states.)	Nebraska, Oklahoma, Tennessee, Arkansas, Illinois, Iowa, Kansas, Kentucky	8
26.	Montana	South Dakota, Wyoming, Idaho, North Dakota	4
27.	Nebraska	Missouri, South Dakota, Wyoming, Colorado, Iowa, Kansas,	6
28.	Nevada	Idaho, Oregon, Utah, Arizona, California	5
29.	New Hampshire	Vermont, Maine, Massachusetts
3
30.	New Jersey	Pennsylvania, Delaware, New York	3
31.	New Mexico	Oklahoma, Texas, Utah, Arizona, Colorado	5
32.	New York	Pennsylvania, Rhode Island (water border), Vermont, Connecticut, Massachusetts, New Jersey	6
33.	North Carolina	Tennessee, Virginia, Georgia, South Carolina	4
34.	North Dakota	South Dakota, Minnesota, Montana	3
35.	Ohio	Michigan, Pennsylvania, West Virginia, Indiana, Kentucky	5
36.	Oklahoma	Missouri, New Mexico, Texas, Arkansas, Colorado, Kansas	6
37.	Oregon	Nevada, Washington, California, Idaho	4
38.	Pennsylvania	New York, Ohio, West Virginia, Delaware, Maryland, New Jersey	6
39.	Rhode Island	Massachusetts, New York (water border), Connecticut
3
40.	South Carolina	North Carolina, Georgia,	2
41.	South Dakota	Nebraska, North Dakota, Wyoming, Iowa, Minnesota, Montana	6
42.	Tennessee
(The state which touches the most other states.)	Mississippi, Missouri, North Carolina, Virginia, Alabama, Arkansas, Georgia, Kentucky	8
43.	Texas	New Mexico, Oklahoma, Arkansas, Louisiana	4
44.	Utah	Nevada, New Mexico, Wyoming, Arizona, Colorado, Idaho	6
45.	Vermont	New Hampshire, New York, Massachusetts	3
46.	Virginia	North Carolina, Tennessee, West Virginia, Kentucky, Maryland	5
47.	Washington	Oregon, Idaho	2
48.	West Virginia	Pennsylvania, Virginia, Kentucky, Maryland, Ohio	5
49.	Wisconsin	Michigan, Minnesota, Illinois, Iowa	4
50.	Wyoming	Nebraska, South Dakota, Utah, Colorado, Idaho, Montana
}
"""

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

norm_factor_internal=0
for i in internal_flying.items():
   if(i[1]>norm_factor_internal):
      norm_factor_internal=i[1]
for i in internal_flying.items():
   internal_flying[i[0]]/=norm_factor_internal

#print(internal_flying)

car_pickle = open ("rti_dict.pkl", "rb")
y = pickle.load(car_pickle)
norm_factor_road=0
for i in y.items():
   if(i[1]>norm_factor_road):
      norm_factor_road=i[1]
for i in y.items():
   y[i[0]]/=norm_factor_road

print(x)
#print(y)
states=list(us_state.values())
a = np.zeros((50,50,2))

counter1=0
counter2=0

while counter2<50:
   counter1=0
  
   while counter1<50:
      a[counter2][counter1][0]=internal_flying[states[counter2]]
      if(states[counter1]+"-"+states[counter2] in x.keys()):
         
         a[counter2][counter1][1]=x[states[counter1]+"-"+states[counter2]]
      counter1+=1
         
   counter2+=1

print(a[states.index("FL")])

