""" MA3.py

Student: Alexander Cremer
Mail: alexander.cremer.1041@student.uu.se
Reviewed by: Andre
Date reviewed: 07/10/26

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean
from time import perf_counter as pc
import numpy as np
from numba import njit
# import multiprocessing as mp
import concurrent.futures as future 

# Exc1


def approximate_pi(n):
    # n is the number of points
    # Write your code here

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
    plt.savefig(f"MC_approx-n{n}.png")
    # plt.show()


    return pi_approx






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


    


# Exc2, real value


def hypersphere_exact(n, d):
    # n is the number of points

    # d is the number of dimensions of the sphere
    denom = m.gamma((d/2)+ 1 )

    return ((np.pi)**(d/2)) / denom


# print(f"Difference between approx and exact for (n,d) = (100 000, 2) -> {np.abs(hypersphere_exact(100000, 2) - sphere_volume(100000, 2))}")
# print(f"Difference between approx and exact for (n,d) = (100 000, 11) -> {np.abs(hypersphere_exact(100000, 11) - sphere_volume(100000, 11))}")

# Difference between approx and exact for (n,d) = (100 000, 2) -> 0.0037273464102067777
# Difference between approx and exact for (n,d) = (100 000, 11) -> 0.12293612061010051


# Exc3: numba version

@njit
def sphere_volume_numba(n: int, d: int) -> float:

    n_random_points = [[random.uniform(-1, 1) for j in range(d)] for i in range(n) ]

    f_sq = lambda x: x**2

    def sum_squared_element_list(some_lst):
        summed_values = 0
        list_sq_element_val = list(map(f_sq, some_lst))
        for i in list_sq_element_val:
            summed_values += i

        return summed_values
    

    nc_list = []
    for i in n_random_points:
        if sum_squared_element_list(i) <= 1:
            nc_list.append(i)
    
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

# n = 10**6
# d = 11
# running_sequential_thing(n, d)

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





# Exc4: parallel code - parallelize actual computations by splitting data


def sphere_volume_parallel(n, d, number_process=10):


    with future.ProcessPoolExecutor() as ex:
        results_2_map = ex.map(sphere_volume, [n // number_process]*(number_process), [d]*number_process)

        V_par_approx = mean(results_2_map)

    return V_par_approx


def running_sequential_thing_parallel(n, d):


    for i in range(3):
        start_normal = pc()
        print(f"sphere_volume={sphere_volume(n, d)}")
        stop_normal = pc()
        print(f"Exc4: Sequential time of d={d} and n={n}: {stop_normal-start_normal}")
        
        start_parallel = pc()
        print(f"sphere_volume_parallel={sphere_volume_parallel(n, d, 10)}")
        stop_parallel = pc()
        print(f"Parallel time = {stop_parallel - start_parallel}")



# sphere_volume=1.951744
# Exc4: Sequential time of d=11 and n=1000000: 4.365607458006707
# sphere_volume_parallel=1.859584
# Parallel time = 2.8699822499911534
# sphere_volume=1.820672
# Exc4: Sequential time of d=11 and n=1000000: 4.408299624992651
# sphere_volume_parallel=1.861632
# Parallel time = 2.7323789579968434
# sphere_volume=1.900544
# Exc4: Sequential time of d=11 and n=1000000: 4.296994125004858
# sphere_volume_parallel=1.806336
# Parallel time = 2.8463344580086414




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

    running_sequential_thing_parallel(n, d)
    
    # start_normal = pc()
    # print(f"sphere_volume={sphere_volume(n, d)}")
    # stop_normal = pc()
    # print(f"Exc4: Sequential time of d={d} and n={n}: {stop_normal-start_normal}")
    
    # start_parallel = pc()
    # print(f"sphere_volume_parallel={sphere_volume_parallel(n, d, 10)}")
    # stop_parallel = pc()
    # print(f"Parallel time = {stop_parallel - start_parallel}")


if __name__ == '__main__':
    main()
    







#ssh alcr1041@gullviva.it.uu.se