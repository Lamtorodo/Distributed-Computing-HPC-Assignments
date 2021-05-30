import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import time

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()



def compute_integrale_trapeze(x, y, nbi):

    integrale = 0.
    for i in range(nbi):
        trap = (x[i+1]-x[i])/2 * (y[i]+y[i+1])
        integrale = integrale + trap
                
    return integrale

def plot_integrale(x, y, nbi):
    for i in range(nbi):
        # dessin du rectangle
        x_trap = [x[i], x[i], x[i+1], x[i+1], x[i]] # abscisses des sommets
        y_trap = [0   , y[i], y[i+1],      0,        0   ] # ordonnees des sommets
        plt.plot(x_trap, y_trap,"r")
    
    return 0

t0 = time.process_time()
Xmin = 0
Xmax = 3*np.pi/2
nbx = 20  # max nbr of iterations
dx = (Xmax-Xmin)/(nbx-1) # space step

## distributing automatically the interval [xmin; xmax] between processors
nbi = int((nbx-1)/SIZE) 

if SIZE == RANK+1:
	nbi += (nbx-1)%SIZE

## [xmin; xmax] in each processor
if RANK == (SIZE-1):
   xmax = 3*np.pi/2
   xmin = Xmax-nbi*dx
else:
   xmin =Xmin+RANK*nbi*dx
   xmax =Xmin+(RANK+1)*nbi*dx 

nbxloc = nbi+1
x = np.linspace(xmin, xmax, nbxloc)
y = np.cos(x)

integrale = compute_integrale_trapeze(x, y, nbi)
integrale_sum=COMM.reduce(integrale,op=MPI.SUM, root=0)
t1 = time.process_time()

#print("integrale in {rank} is {integ} :".format(rank=RANK,integ=integrale))

if RANK==0:
	print('\n')
	print("Integrale =", integrale_sum)
	print("Time spent is",t1 - t0)
	

