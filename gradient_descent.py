import torch
from torch.optim import SGD
from data import NYTimes, Hospital_US
import pickle
import threading
import numpy
data1 = NYTimes(level='states')
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
beta = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
gamma = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
sigma = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
mu = torch.tensor(1e-3, dtype=torch.float, requires_grad=True)
alpha = torch.tensor(2e-1, dtype=torch.float, requires_grad=True)
rho = torch.tensor(1e-1, dtype=torch.float, requires_grad=True)
theta = torch.tensor(1e-2, dtype=torch.float, requires_grad=True)
a=torch.rand(50,3,1,dtype=torch.float,requires_grad=True)
torch.div(a,1000)
s0 = torch.tensor(1, dtype=torch.float, requires_grad=True)
e0 = torch.tensor(1e1, dtype=torch.float, requires_grad=True)
i0 = torch.tensor(1, dtype=torch.float, requires_grad=True)

optimizer = SGD([
    {'params': beta, 'lr': 1e-5},
    {'params': gamma, 'lr': 1e-5},
    {'params': sigma, 'lr': 1e-5},
    {'params': mu, 'lr': 1e-8},
    {'params': alpha, 'lr': 1e-5},
    {'params': s0, 'lr': 1e-4},
    {'params': e0, 'lr': 1e-4},
    {'params': i0, 'lr': 1e-4},
    {'params':a,'lr':1e-4}
])

All_E=[[0]*200]*50
#print(All_E)

def train_state(state_num,features):
    torch.autograd.set_detect_anomaly(True)
    features=torch.from_numpy(features)
    confirm, death = data1.get('2020-03-31', '2020-06-01', states[state_num].lower()) 
    size = len(confirm)
    
    S = [torch.tensor(0) for _ in range(size)]
    E = [torch.tensor(0) for _ in range(size)]
    I = [torch.tensor(0) for _ in range(size)]
    R = [torch.tensor(0) for _ in range(size)]
    file=open(str(states[state_num])+".txt","a")
   
    for j in range(1000):
        deltas=torch.matmul(features.double(),a[state_num].double())
        #print(deltas)
        optimizer.zero_grad()
        S[0], E[0], I[0], R[0] = s0 * N, e0 * confirm[0], i0 * confirm[0], (1 - i0) * confirm[0]
        All_E[state_num][0]=E[0]
      
        loss = 0
        smooth = 0
        for i in range(size - 1):
            # go for next
            S[i+1] = S[i] - beta * S[i] * (E[i] + I[i]) / N
           
            connection_sum=0
            for j in range(0,50):
                #print("thing",All_E[j][i]-All_E[j][i-1])
                connection_sum+=deltas[j]*(All_E[j][i])
            #print(connection_sum)
            #input()
            E[i+1] =E[i] + beta * S[i] * (E[i] + I[i]) / N - sigma * E[i]
            All_E[state_num][i+1]=E[i+1]
            I[i+1] = I[i] + mu * sigma * E[i] - gamma * I[i]
            R[i+1] = R[i] + gamma * I[i]
          
            
            loss += torch.reshape(torch.square(1 - (I[i+1] + R[i+1]) / (confirm[i + 1])),())
            
        loss /= size
        print("Backprop for",states[state_num],"epoch",str(j))
        loss.backward()
        optimizer.step()
        
        if j % 100 == 99:
            #print('=' * 10, 'Round {} '.format(j), '=' * 10)
            file.write("Epoch"+str(j)+"for state"+states[state_num]+"\n")
            file.write(str(loss.item())+"\n")
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
    file.close()
threads=[None]*50
arr_pickle = open ("features.pkl", "rb")
features = pickle.load(arr_pickle)

for i in range(0,50):    
    threads[i] = threading.Thread(target=train_state, args=(i,features[i]))
    threads[i].start()
