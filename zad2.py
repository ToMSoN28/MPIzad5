from mpi4py import MPI
import sys
from integral import Integral
import time

def main(start, end, points):
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()            #number of the process running the code
    numProcesses = comm.Get_size()  #total number of processes running
    myHostName = MPI.Get_processor_name()  #machine name running the code
    
    start = float(start)
    end = float(end)
    points = int(points)
    
    if id == 0:
        start_time = time.time()
        data = []
        step = (end-start)/points
        more_points = points % numProcesses
        tmp = []
        for i in range(numProcesses):
            if i < more_points:
                tmp.append(int(points/numProcesses)+1)
            else:
                tmp.append(int(points/numProcesses))
                
        for i in range(numProcesses):
            if len(data) == 0:
                s = start
            else:
                s = data[i-1][1]
            e = s + (step*tmp[i])
            data.append((s, e, tmp[i]))   
            
        # print(data)
    else:
        data = None    
                
    data_to_calculate = comm.scatter(data, root=0)        
    integral = Integral(data_to_calculate[0], data_to_calculate[1], data_to_calculate[2])
    integral.calculate_result()
    gathered_data = comm.gather(integral.result, root=0)
    
    if id == 0:
        # print(gathered_data)
        # sum = 0
        # for partial_result in gathered_data:
        #     sum += partial_result
        print(sum(gathered_data))
        end_time = time.time()
        print(end_time-start_time)
            
if __name__ == "__main__":
    main(*sys.argv[1:])