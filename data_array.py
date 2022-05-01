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


neighboring_dict={
    "Alabama":	"Mississippi,Tennessee,Florida,Georgia",
	"Alaska":	None,	
   "Arizona": "Nevada,New Mexico,Utah,California,Colorado"	,
	"Arkansas":	"Oklahoma,Tennessee,Texas,Louisiana,Mississippi,Missouri"	,
	"California":	"Oregon,Arizona,Nevada",
   "Colorado":	"New Mexico,Oklahoma,Utah,Wyoming,Arizona,Kansas,Nebraska",	
	"Connecticut":	"New York,Rhode Island,Massachusetts",	
	"Delaware":	"New Jersey,Pennsylvania,Maryland",	
	"Florida":	"Georgia,Alabama",
   "Georgia":	"North Carolina,South Carolina,Tennessee,Alabama,Florida",	
	"Hawaii":	None,	
	"Idaho":	"Utah,Washington,Wyoming,Montana,Nevada,Oregon",	
	"Illinois":	"Kentucky,Missouri,Wisconsin,Indiana,Iowa,Michigan",
	"Indiana":	"Michigan,Ohio,Illinois,Kentucky",	
	"Iowa":	"Nebraska,South Dakota,Wisconsin,Illinois,Minnesota,Missouri",	
	"Kansas":"Nebraska,Oklahoma,Colorado,Missouri",	
	"Kentucky":	"Tennessee,Virginia,West Virginia,Illinois,Indiana,Missouri,Ohio",	
   "Louisiana":	"Texas,Arkansas,Mississippi",	
	"Maine":	"New Hampshire",
	"Maryland":	"Virginia,West Virginia,Delaware,Pennsylvania",	
   "Massachusetts":	"New York,Rhode Island,Vermont,Connecticut,New Hampshire",	
	"Michigan":	"Ohio,Wisconsin,Illinois,Indiana,Minnesota", 
	"Minnesota": "North Dakota,South Dakota,Wisconsin,Iowa,Michigan", 
	"Mississippi":	"Louisiana,Tennessee,Alabama,Arkansas",
	"Missouri": "Nebraska,Oklahoma,Tennessee,Arkansas,Illinois,Iowa,Kansas,Kentucky",	
	"Montana":	"South Dakota,Wyoming,Idaho,North Dakota",	
	"Nebraska":	"Missouri,South Dakota,Wyoming,Colorado,Iowa,Kansas",
	"Nevada": "Idaho,Oregon,Utah,Arizona,California",	
	"New Hampshire": "Vermont,Maine,Massachusetts",
	"New Jersey":	"Pennsylvania,Delaware,New York",	
	"New Mexico":	"Oklahoma,Texas,Utah,Arizona,Colorado",	
	"New York":	"Pennsylvania,Rhode Island,Vermont,Connecticut,Massachusetts,New Jersey",	
	"North Carolina":	"Tennessee,Virginia,Georgia,South Carolina",	
	"North Dakota":	"South Dakota,Minnesota,Montana",	
   "Ohio":	"Michigan,Pennsylvania,West Virginia,Indiana,Kentucky",	
	"Oklahoma":	"Missouri,New Mexico,Texas,Arkansas,Colorado,Kansas",	
	"Oregon":	"Nevada,Washington,California,Idaho",	
	"Pennsylvania":	"New York,Ohio,West Virginia,Delaware,Maryland,New Jersey",	
	"Rhode Island":	"Massachusetts,New York,Connecticut",
	"South Carolina":	"North Carolina,Georgia",	
	"South Dakota":	"Nebraska,North Dakota,Wyoming,Iowa,Minnesota,Montana",
	"Tennessee": "Mississippi,Missouri,North Carolina,Virginia,Alabama,Arkansas,Georgia,Kentucky",	
	"Texas":	"New Mexico,Oklahoma,Arkansas,Louisiana",	
	"Utah":	"Nevada,New Mexico,Wyoming,Arizona,Colorado,Idaho",	
"Vermont":	"New Hampshire,New York,Massachusetts",	
	"Virginia":	"North Carolina,Tennessee,West Virginia,Kentucky,Maryland",
"Washington":	"Oregon,Idaho",	
	"West Virginia": "Pennsylvania,Virginia,Kentucky,Maryland,Ohio",	
	"Wisconsin":	"Michigan,Minnesota,Illinois,Iowa",	
	"Wyoming":	"Nebraska,South Dakota,Utah,Colorado,Idaho,Montana"
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

#print(x)
#print(y)
states=list(us_state.values())
a = np.zeros((50,50,3))

inv_states = {v: k for k, v in us_state.items()}


for v in y.items():
   try:
      for n in neighboring_dict[inv_states[v[0]]].split(","):
         a[states.index(us_state[n])][states.index(v[0])][2]+=v[1]
   except:
      continue

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

print(a[states.index("TN")])


