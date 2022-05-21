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

supplyer=np.empty(20)
i=0
while(i<20):
    supplyer[i]=np.random.randint(900,1100)
    i+=1
supplyer = supplyer.astype(int)

model = ConcreteModel()

model.I = RangeSet(0,X.shape[0]-1) #Cities
model.J = RangeSet(0,X.shape[1]-1) #Days

#variable
model.x = Var(model.I,model.J, domain=NonNegativeReals)
#model.X = Param(model.n,model.m,initialize=X)

def Obj_rule(model):
	return sum(sum( model.x[i,j]*X[i,j] for i in model.I) for j in model.J)

model.Obj = Objective(rule=Obj_rule, sense=maximize)

#constraint min vaccines per day and city
def min_vac_day_city(model, i,j): 
	return (model.x[i,j] >= 50) 
model.min_vac_day_city = Constraint(model.I, model.J,rule=min_vac_day_city)

#constraint max vaccines per day and city
def max_vac_day_city(model, i,j): 
	return (model.x[i,j] <= 200) 
model.max_vac_day_city = Constraint(model.I, model.J,rule=max_vac_day_city)

#Min per city
def min_city_all(model, i): 
	return sum(model.x[i,j] for j in model.J) >= 2000  
model.min_city_all = Constraint(model.I, rule=min_city_all)

#Min per city
def supply(model, j): 
	return sum(model.x[i,j] for i in model.I) == supplyer[j]  
model.supply = Constraint(model.J, rule=supply)



