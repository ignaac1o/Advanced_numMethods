from pyomo.environ import *
opt = SolverFactory("glpk")
from pyomo.opt import SolverFactory
import numpy as np

modelcv = AbstractModel()

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
supplyer_c

n_sc=2

modelcv.k = RangeSet(0,n_sc-1)#scenarios
modelcv.I = RangeSet(0,X.shape[0]-1) #Provinces
modelcv.J = RangeSet(0,X.shape[1]-1) #Day

pi=np.array([0.5,0.5])

#model variables: continuous
modelcv.Q = Var(modelcv.I,modelcv.J,domain=NonNegativeReals) 
modelcv.Qc = Var(modelcv.k,modelcv.I,modelcv.J,domain=NonNegativeReals) 

def Obj_rule_cv(modelcv):
	return (sum(sum( modelcv.Q[i,j]*X[i,j] for i in modelcv.I) for j in modelcv.J)) + (sum(pi[k]*(sum(sum( modelcv.Qc[k,i,j]*X[i,j] for i in modelcv.I)for j in modelcv.J)) for k in modelcv.k))
modelcv.Obj = Objective(rule=Obj_rule_cv, sense=maximize)

#constraint min vaccines per day and city
def min_vac_day_city_Q(modelcv, i,j,k): 
	return (modelcv.Q[i,j] + modelcv.Qc[k,i,j] >= 50) 
modelcv.min_vac_day_city_Q = Constraint(modelcv.I, modelcv.J,modelcv.k,rule=min_vac_day_city_Q)


#constraint max vaccines per day and city
def max_vac_day_city_Q(modelcv, i,j,k): 
 	return (modelcv.Q[i,j]+modelcv.Qc[k,i,j] <= 300) 
modelcv.max_vac_day_city_Q = Constraint(modelcv.I, modelcv.J,modelcv.k,rule=max_vac_day_city_Q)


#Min per city
def min_city_all_Q(modelcv, i,k): 
 	return sum(modelcv.Q[i,j]+modelcv.Qc[k,i,j] for j in modelcv.J) >= 2000  
modelcv.min_city_all_Q = Constraint(modelcv.I,modelcv.k,rule=min_city_all_Q)

#Supply
#def supply_Q(modelcv, j): 
# 	return sum(modelcv.Q[i,j] +  for i in modelcv.I) == supplyer_c[0,j]  
#modelcv.supply_Q = Constraint(modelcv.J, rule=supply_Q)

def supply_Qc(modelcv, j,k): 
 	return sum(modelcv.Qc[k,i,j]+modelcv.Q[i,j] for i in modelcv.I) == supplyer_c[k+1,j] +  supplyer_c[0,j] 
modelcv.supply_Qc = Constraint(modelcv.J, modelcv.k,rule=supply_Qc)
