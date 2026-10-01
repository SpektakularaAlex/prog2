""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean
from time import perf_counter as pc
import numpy as np
# from numba import njit
# import multiprocessing as mp
import concurrent.futures as future 

# Exc1


def approximate_pi(n):
    # n is the number of points

    n_random_points = []
    for i in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        n_random_points.append([x, y])

    nc_points = []
    ns_points = []
    for i in n_random_points:
        # print(i)
        if ((i[0])**2 + (i[1])**2) <= 1:
            nc_points.append(i)
        else:
            ns_points.append(i)
    nc_amount = len(nc_points)
    pi_approx = 4 * (nc_amount/n)


    for i in nc_points:
        plt.plot(i[0], i[1], 'o', color="red")
        # print(f"nc_point={i}")
    for i in ns_points:
        plt.plot(i[0], i[1], 'o', color="blue")
        # print(f"ns_point={i}")

    plt.title(f"Monte Carlo approximation of pi ≈ {pi_approx}")
    plt.grid(True)
    plt.axis('equal')
    plt.show()


    return pi_approx

    # Write your code here
    # return

# print(f"nc_points = {approximate_pi(10**5)}")



# Exc2, approximation


def sphere_volume(n, d):
    # n is the number of points

    # d is the number of dimensions of the sphere
    n_random_points = [[random.uniform(-1, 1) for j in range(d)] for i in range(n) ]

    f_sq = lambda x: x**2

    def sum_squared_element_list(some_lst):
        summed_values = 0
        list_sq_element_val = list(map(f_sq, some_lst))
        # summed_values += (k for k in list_sq_element_val)
        # for i in range(len(some_lst)):
        for i in list_sq_element_val:
            summed_values += i
            # summed_values += f_sq(some_lst[i])
        return summed_values
    
    # nc_list = list(filter(sum_squared_element_list <= 1, n_random_points))
    nc_list = []
    for i in n_random_points:
        if sum_squared_element_list(i) <= 1:
            nc_list.append(i)
    
    # V_approx = (len(nc_list) / len(n_random_points))
    V_approx = 2**d *(len(nc_list) / len(n_random_points))


    return V_approx
    # nc_list = list(filter( , n_random_points))

    


# Exc2, real value


def hypersphere_exact(n, d):
    # n is the number of points

    # d is the number of dimensions of the sphere
    denom = m.gamma((d/2)+ 1 )

    return ((np.pi)**(d/2)) / denom





# Exc3: numba version

# @njit
def sphere_volume_numba(n: int, d: int) -> float:

    n_random_points = [[random.uniform(-1, 1) for j in range(d)] for i in range(n) ]

    f_sq = lambda x: x**2

    def sum_squared_element_list(some_lst):
        summed_values = 0
        list_sq_element_val = list(map(f_sq, some_lst))
        # summed_values += (k for k in list_sq_element_val)
        # for i in range(len(some_lst)):
        for i in list_sq_element_val:
            summed_values += i
            # summed_values += f_sq(some_lst[i])
        return summed_values
    
    # nc_list = list(filter(sum_squared_element_list <= 1, n_random_points))
    nc_list = []
    for i in n_random_points:
        if sum_squared_element_list(i) <= 1:
            nc_list.append(i)
    
    # V_approx = (len(nc_list) / len(n_random_points))
    V_approx = 2**d *(len(nc_list) / len(n_random_points))


    return V_approx



# Exc3

def running_sequential_thing(n, d):
    print(f"V_approx={sphere_volume(10**5, 11)}")
    print(f"V_approx_numba={sphere_volume_numba(10**5, 11)}")
    print(f"V_exact={hypersphere_exact(10**5, 11)}")

    for i in range(3):
        print(f"run={i+1}")
        start = pc()
        V_app = sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of standard approx dimension:{d} and {n} points: {stop-start} seconds, with V_approx={V_app}")
        start = pc()
        V_app_numba = sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of numba approx dimension:{d} and {n} points: {stop-start} seconds, with V_approx_numba={V_app_numba}")

n = 10**6
d = 11
# running_sequential_thing(n, d)

# Exc4: parallel code - parallelize actual computations by splitting data


def sphere_volume_parallel(n, d, number_process=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes


    print("Began the parallel copmuting")
    with future.ProcessPoolExecutor() as ex:
        # processes_list = [[n, d] for j in range(np)]
        # print(f"processes_list={processes_list}")

        # processes_list = [1, 2, 3]
        results_2_map = ex.map(sphere_volume, [n // number_process]*(number_process), [d]*number_process)

        print("Finished the parallel copmuting")
        # V_par_approx = sum(results_2_map)
        V_par_approx = mean(results_2_map)
        # for r in results_2_map:
        #     print(f"r = {r}")

    
    return V_par_approx


n = 100
d = 11

# print(f"Parallell computed results from sphere_volume_parallel2 = {sphere_volume_parallel2(n, d)}")

def main():
    # # Exc1
    # dots = [1000, 10000, 100000]
    # for n in dots:
    #     approximate_pi(n)

    # # Exc2
    # n = 100000
    # d = 2
    # sphere_volume(n, d)
    # print(
    #     f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # n = 100000
    # d = 11
    # sphere_volume(n, d)
    # print(
    #     f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # # Exc3
    # n = 1000000
    # d = 11
    # start = pc()
    # sphere_volume(n, d)
    # stop = pc()
    # print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    # # print("What is numba time?")

    # Exc4
    n = 10**6
    d = 11

    
    start_normal = pc()
    print(f"sphere_volume={sphere_volume(n, d)}")
    stop_normal = pc()
    print(f"Exc4: Sequential time of d={d} and n={n}: {stop_normal-start_normal}")
    
    start_parallel = pc()
    print(f"sphere_volume_parallel={sphere_volume_parallel(n, d, 10)}")
    stop_parallel = pc()
    print(f"Parallel time = {stop_parallel - start_parallel}")


if __name__ == '__main__':
    main()
    



# V_approx=2.1504
# V_approx_numba=2.10944
# V_exact=1.8841038793898994
# run=1
# Exc3: Sequential time of standard approx dimension:11 and 1000000 points: 4.3059955420321785 seconds, with V_approx=1.882112
# Exc3: Sequential time of numba approx dimension:11 and 1000000 points: 0.7906525420257822 seconds, with V_approx_numba=1.8944
# run=2
# Exc3: Sequential time of standard approx dimension:11 and 1000000 points: 4.306834833987523 seconds, with V_approx=1.906688
# Exc3: Sequential time of numba approx dimension:11 and 1000000 points: 0.7662886250182055 seconds, with V_approx_numba=2.002944
# run=3
# Exc3: Sequential time of standard approx dimension:11 and 1000000 points: 4.526595333009027 seconds, with V_approx=1.929216
# Exc3: Sequential time of numba approx dimension:11 and 1000000 points: 0.7774764170171693 seconds, with V_approx_numba=1.910784



#ssh alcr1041@gullviva.it.uu.se