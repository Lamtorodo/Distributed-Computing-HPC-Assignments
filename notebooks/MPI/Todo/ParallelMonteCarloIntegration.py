import random
import numpy as np
import timeit
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

def f(x):
    return np.cos(x)
    
a=0
b=np.pi # b>a
N=1000
x=np.linspace(a,b,N)
y=f(x)
fmin=min(y)
fmax=max(y)
Area_rectangle=abs(b-a)*abs(fmax-fmin)
nbi=int(N/SIZE)+(SIZE==(RANK+1))*(N%SIZE)

random.seed(45)
def MonteCarloIntegration():
    random.seed(45)
    m=0
    for i in range(nbi):
        # 0<= random.random() <=1
        x_random=a+(b-a)*random.random()
        y_random=fmin+(fmax-fmin)*random.random()
        if y_random<=f(x_random):
            m+=1
    return m

start = timeit.default_timer()
M=MonteCarloIntegration()
sum_M=COMM.reduce(M,op=MPI.SUM,root=0)
end = timeit.default_timer()

if RANK==0:
	integral=(sum_M/N)*Area_rectangle
	print("Integral of cos(x) between {a} and {b} = {L}".format(a=a,b=b,L=integral))
	print("Run time:",end-start) 
