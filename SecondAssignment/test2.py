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


model = ConcreteModel()

model.I = RangeSet(0,X.shape[0]-1) #Provinces
model.J = RangeSet(0,X.shape[1]-1) #Days

#variable
#model.x = Var(model.I,model.J, domain=Binary)
model.x = Var(model.I,model.J, domain=NonNegativeReals, bounds=(0,1))

def Obj_rule(model):
	return sum(sum( 8000*model.x[i,j]*X[i,j] for i in model.I) for j in model.J)

model.Obj = Objective(rule=Obj_rule, sense=maximize)

#Send vaccines to maximum 3 provinces per day
def max_vaccines_province(model,j):
    return(sum(model.x[i,j] for i in model.I)<=3)
model.max_vaccines_provinve=Constraint(model.J,rule=max_vaccines_province)

#Min per city
def min_city_binary(model, i): 
	return sum(model.x[i,j]*8000 for j in model.J) >= 32000  
model.min_city_binay = Constraint(model.I, rule=min_city_binary)

#No receiving vaccines two days in a row
def no_two_row(model,i,j):
    if (j!=19):
        return (model.x[i,j] + model.x[i,j+1] <=1)
    else:
        return (model.x[i,j] + model.x[i,j-1] <= 1)
model.no_two_row=Constraint(model.I,model.J,rule=no_two_row)
