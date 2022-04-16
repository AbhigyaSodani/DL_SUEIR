import pandas
import pickle
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
print(internal_flying)
print(x)