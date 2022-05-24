from pyomo.environ import *

import numpy as np
import pandas as pd

X=np.empty([8,20])
np.asmatrix(X)
np.random.seed(1)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        X[i,j]=np.random.random()

X=np.round(X,2)

supplyer_c=np.empty([3,20])
np.asmatrix(supplyer_c)
i=0
j=0
while(j<3):
    if(j==0):
        for i in range(0,20):
            supplyer_c[j,i]=np.random.randint(900,1100) #This is the daily normal distribution
            i+=1
    elif(j==1):
        for i in range(0,20):
            supplyer_c[j,i]=np.random.randint(100,200) #High Increment of the distribution  for all machines working
            i+=1
    else:
        for i in range(0,20):
            supplyer_c[j,i]=np.random.randint(0,100) #Small increment if some of them break
            i+=1
    j+=1

supplyer_c = supplyer_c.astype(int)
supplyer=supplyer_c[2,:]+supplyer_c[0,:]


model = ConcreteModel()

model.I = RangeSet(0,X.shape[0]-1) #Cities
model.J = RangeSet(0,X.shape[1]-1) #Days

#variable
model.x = Var(model.I,model.J, domain=NonNegativeReals)

def Obj_rule(model):
	return sum(sum( model.x[i,j]*X[i,j] for i in model.I) for j in model.J)

model.Obj = Objective(rule=Obj_rule, sense=maximize)

#constraint min vaccines per day and city
def min_vac_day_city(model, i,j): 
	return (model.x[i,j] >= 50) 
model.min_vac_day_city = Constraint(model.I, model.J,rule=min_vac_day_city)

#constraint max vaccines per day and city
def max_vac_day_city(model, i,j): 
	return (model.x[i,j] <= 300) 
model.max_vac_day_city = Constraint(model.I, model.J,rule=max_vac_day_city)

#Min per city
def min_city_all(model, i): 
	return sum(model.x[i,j] for j in model.J) >= 2000  
model.min_city_all = Constraint(model.I, rule=min_city_all)

#Supply
def supply(model, j): 
	return sum(model.x[i,j] for i in model.I) == supplyer[j]  
model.supply = Constraint(model.J, rule=supply)
