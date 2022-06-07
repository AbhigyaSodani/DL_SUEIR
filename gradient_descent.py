from pickletools import long1
import torch
from torch.optim import SGD
import time
from data import NYTimes, Hospital_US
import pickle
import threading
from threading import Lock
import numpy
data1 = NYTimes(level='states')
STATE_NUM=5
N = 4e7
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
states=list(us_state.values())
print(states)


All_E=[]
All_deltas=[]
locks1=[]
locks2=[]

for r in range(200):
    locks2.append([])
    for t in range(200):
        locks2[r].append([])
        for n in range(STATE_NUM):
            locks2[r][t].append(False)
for g in range(200):
    locks1.append([])
    for h in range(STATE_NUM):
        locks1[g].append(False)

for x in range (STATE_NUM):
    
    All_E.append([])
    All_deltas.append(0)
    for y in range (200):
        All_E[x].append(0)
#print(All_E)
def contains_false(list1):
    for i in list1:
        if not i:
            return True
    return False
lock=Lock()
def train_state(state_num,features,threads):
    print(state_num)
    beta = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
    gamma = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
    sigma = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
    mu = torch.tensor(1e-3, dtype=torch.float, requires_grad=True)
    alpha = torch.tensor(2e-1, dtype=torch.float, requires_grad=True)
    rho = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
    theta = torch.tensor(1e-2, dtype=torch.float, requires_grad=True)
    a=torch.rand(STATE_NUM,3,1,dtype=torch.float,requires_grad=True)
    torch.div(a,1000)
    s0 = torch.tensor(1, dtype=torch.float, requires_grad=True)
    e0 = torch.tensor(1e-2, dtype=torch.float, requires_grad=True)
    i0 = torch.tensor(1, dtype=torch.float, requires_grad=True)

    optimizer = SGD([
        {'params': beta, 'lr': 1e-3},
        {'params': gamma, 'lr': 1e-3},
        {'params': sigma, 'lr': 1e-3},
        {'params': mu, 'lr': 1e-5},
        {'params': alpha, 'lr': 1e-5},
        {'params': s0, 'lr': 1e-3},
        {'params': e0, 'lr': 1e-4},
        {'params': i0, 'lr': 1e-4},
        {'params':a,'lr':1e-4}
    ])
    torch.autograd.set_detect_anomaly(True)
    features=torch.from_numpy(features)
    confirm, death = data1.get('2020-03-31', '2020-06-01', states[state_num].lower()) 
    size = len(confirm)
    
    S = [torch.tensor(0) for _ in range(size)]
    E = [torch.tensor(0) for _ in range(size)]
    I = [torch.tensor(0) for _ in range(size)]
    R = [torch.tensor(0) for _ in range(size)]
   
   
    for j in range(100):
        #file=open("states/"+str(states[state_num])+".txt","a")
        deltas=torch.matmul(features.double(),a[state_num].double())
        All_deltas[state_num]=deltas

       
        optimizer.zero_grad()
        
        
        S[0], E[0], I[0], R[0] = s0 * N, e0 * N, i0 * confirm[0], (1 - i0) * confirm[0]
        
        All_E[state_num][0]=E[0].clone().detach()
      
        
        locks1[j][state_num]=True
        
       
        
        while(contains_false(locks1[j])):
           
            continue
        
        
        
        loss = 0
        smooth = 0
        for i in range(size - 30):
            # go for next
            file=open("states/"+str(states[state_num])+".txt","a")
            S[i+1] = S[i] - beta * S[i] * (E[i] + I[i]) / N
            file.write("day "+str(i)+"\n")
            connection_sum=0
            incoming=0
            outgoing=0
            for k in range(0,STATE_NUM):
                
                #print("thing",All_E[j][i]-All_E[j][i-1])
                #print("ref",All_E[k][i])
                #if(state_num==0):
                #    print("num1:",deltas[k]*(All_E[k][i]))
                #    print("num2:",All_deltas[k][state_num]*E[i])
                #    print("final num:",connection_sum)
                file.write("\tstate"+str(k)+"\n")
                incoming+=All_deltas[state_num][k]*(All_E[k][i])
                file.write("\tincoming"+str(deltas[k]*(All_E[k][i]))+"\n")
                outgoing+=All_deltas[k][state_num]*All_E[state_num][i]
                file.write("\toutgoing"+str(All_deltas[k][state_num]*All_E[state_num][i])+"\n")
            connection_sum=incoming-outgoing 
            
            file.write("incoming"+str(incoming)+"\n")
            file.write("outgoing"+str(  outgoing)+"\n")
            file.write("connection"+str(connection_sum)+"\n")
            #file.write(str(S[i]+E[i]+I[i]+R[i])+"\n")
            
                

            
            
            #input()
        
            E[i+1] = connection_sum+E[i] + beta * S[i] * (E[i] + I[i]) / N - sigma * E[i]
            file.write("E:"+str(E[i+1])+"\n")
            file.close()
            All_E[state_num][i+1]=E[i+1].clone().detach()
            """
            if(state_num==0):
               print(All_E)
            print()
            print()
            print()
            """
            I[i+1] = I[i] + mu * sigma * E[i] - gamma * I[i]
            R[i+1] = R[i] + gamma * I[i]
          
            
            loss += torch.reshape(torch.square(1 - (I[i+1] + R[i+1]) / (confirm[i + 1])),())
            
            locks2[j][i][state_num]=True
           
            while(contains_false(locks2[j][i])):
                continue
            if(state_num==0):
                print("All Threads Done on Epoch"+str(j)+" and done with day "+str(i))
            
        loss /= size
        
        loss.backward(retain_graph=True)
        optimizer.step()
        print(str(loss.item()))
        if j % 1 == 0:
            if(state_num==0):
                print('=' * 10, 'Round {} '.format(j), '=' * 10)
            print("Backprop for",states[state_num],"epoch",str(j))
            #file.write("Epoch"+str(j)+"for state"+states[state_num]+"\n")
            #file.write(str(loss.item())+"\n")
            #file.close()
       
       
            
            """
            print('beta: ', beta.item(), beta.grad.item())
            print('gamma: ', gamma.item(), gamma.grad.item())
            print('sigma: ', sigma.item(), sigma.grad.item())
            print('mu: ', mu.item(), mu.grad.item())
            print('alpha: ', alpha.item(), alpha.grad.item())
            print('rho: ', rho.item(), rho.grad.item())
            print('theta: ', theta.item(), theta.grad.item())
            print('s0: ', s0.item(), s0.grad.item())
            print('e0: ', e0.item(), e0.grad.item())
            print('i0: ', i0.item(), i0.grad.item())
        
            """
   
threads=[None]*STATE_NUM
arr_pickle = open ("features.pkl", "rb")
features = pickle.load(arr_pickle)

for i in range(0,STATE_NUM):    
    threads[i] = threading.Thread(target=train_state, args=(i,features[i],threads))
    threads[i].start()  
"""  

threads[0] = threading.Thread(target=train_state, args=(0,features[0]))
threads[0].start()  
threads[1] = threading.Thread(target=train_state, args=(1,features[1]))
threads[1].start()  
"""
