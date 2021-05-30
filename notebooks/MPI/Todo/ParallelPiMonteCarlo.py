import random 
import timeit
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

INTERVAL= 1000
nbi=int(INTERVAL/SIZE)+(SIZE==(RANK+1))*(INTERVAL%SIZE)

random.seed(42)  

def compute_points():
    
    random.seed(42)  
    
    circle_points= 0

    # Total Random numbers generated= possible x 
    # values* possible y values 
    for i in range(nbi): 
      
        # Randomly generated x and y values from a 
        # uniform distribution 
        # Rannge of x and y values is -1 to 1 
        
        
        rand_x= random.uniform(-1, 1) 
        rand_y= random.uniform(-1, 1) 
      
        # Distance between (x, y) from the origin 
        origin_dist= rand_x**2 + rand_y**2
      
        # Checking if (x, y) lies inside the circle 
        if origin_dist<= 1: 
            circle_points+= 1
      
        # Estimating value of pi, 
        # pi= 4*(no. of points generated inside the  
        # circle)/ (no. of points generated inside the square) 
    
     
    
    return circle_points

start = timeit.default_timer()
circle_points = compute_points()
total_circle_points=COMM.reduce(circle_points,op=MPI.SUM, root=0)
end = timeit.default_timer()

#print("Circle points number :",circle_points)
if RANK==0:
	pi = 4* total_circle_points/ INTERVAL
	print("Final Estimation of Pi=", pi, "cpu time :",end-start) 
