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
                request = comm.isend(part_integral, dest=i, tag=11)
                request.wait()
            else:
                integral = part_integral
            tmp.append(part_points)
        
        result = 0

        integral.calculate_result()
        result += integral.result

        for x in range(1, numProcesses):
            request = comm.irecv(source=x, tag=11)
            tmp_data = request.wait()
            result += tmp_data
        
        print(result)
        end_time = time.time()
        print(end_time-start_time)
    else:
        request = comm.irecv(source = 0, tag = 11)
        integral = request.wait()
        integral.calculate_result()
        request1 = comm.isend(integral.result, dest=0, tag = 11)
        request1.wait()

if __name__ == "__main__":
    main(*sys.argv[1:])