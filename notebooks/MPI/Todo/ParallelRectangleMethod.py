import numpy as np
import matplotlib.pyplot as plt
from mpi4py import MPI
import time

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

def compute_integrale_rectangle(x, y, nbi):
    
    integrale =0.
    for i in range(nbi):
        integrale = integrale + y[i]*(x[i+1]-x[i])
        
    return integrale

def plot_integrale(x, y, nbi):
  
    for i in range(nbi):
         # dessin du rectangle
        x_rect = [x[i], x[i], x[i+1], x[i+1], x[i]] # abscisses des sommets
        y_rect = [0   , y[i], y[i]  , 0     , 0   ] # ordonnees des sommets
        plt.plot(x_rect, y_rect,"r")
        
t0 = time.process_time()
Xmin = 0
Xmax = 3*np.pi/2
nbx = 15  # nombre maximum d'itérations
dx = (Xmax-Xmin)/(nbx-1) 

## on calcule l'intervalle concernant chaque processeur
nbi = int((nbx-1)/SIZE) 
if SIZE == (RANK+1):
	nbi += (nbx-1)%SIZE

if RANK == (SIZE-1):
   xmax = 3*np.pi/2
   xmin = Xmax-nbi*dx
else:
   xmin =Xmin+RANK*nbi*dx
   xmax =Xmin+(RANK+1)*nbi*dx 

nbxloc = nbi+1
x = np.linspace(xmin, xmax, nbxloc)
y = np.cos(x)

integrale = compute_integrale_rectangle(x, y, nbi)
#faire la somme des calculs des intégrales venant de chaque processeur dans le processeur 1
integrale_sum=COMM.reduce(integrale,op=MPI.SUM, root=0)
t1 = time.process_time()

#print("integrale in {rank} is {integ} :".format(rank=RANK,integ=integrale))

if RANK==0:
	print('\n')
	print("Integrale =", integrale_sum)
	print("Temps",t1 - t0 , "secondes")
	
plt.plot(x,y,"bo-")
plot_integrale(x, y, nbi)   
plt.show()
