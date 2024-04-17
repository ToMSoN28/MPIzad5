import sys
from mpi4py import MPI
from integral import Integral
import time

function = lambda x: x**2 + x + 1

def main(start, end, points):
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    numProcesses = comm.Get_size()

    start = float(start)
    end = float(end)
    points = int(points)
    
    integral: Integral
    if (id == 0):
        start_time = time.time()
        size = (end - start) / points
        more_points = points % numProcesses
        tmp = []
        for i in range(numProcesses):
            part_points = int(points/numProcesses)
            if i < more_points:
                part_points += 1
            part_start = start + (size * sum(tmp))
            part_end = part_start + part_points * size
            part_integral = Integral(part_start, part_end, part_points)
            if i != 0: 
                comm.send(part_integral, dest=i)
            else:
                integral = part_integral
            tmp.append(part_points)
        
        result = 0

        integral.calculate_result()
        result += integral.result

        for x in range(1, numProcesses):
            result += comm.recv(source=x)
        
        print(result)
        end_time = time.time()
        print(end_time-start_time)
    else:
        integral = comm.recv(source = 0)
        integral.calculate_result()
        comm.send(integral.result, dest=0)

if __name__ == "__main__":
    main(*sys.argv[1:])