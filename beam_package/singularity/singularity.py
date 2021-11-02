import numpy as np
import matplotlib.pyplot as plt

# issue: fails when triangular load ie: uvl loading is given

# for the project use this concept: file:///C:/Users/User/Downloads/lecture17.pdf
# make different functions for different loadings then superposition in the Beam object

def singular_unit(x, a, n):
    """
        format: <x-a>^n
        logic: by definition http://www.eng.uwaterloo.ca/~syde06/singularity-functions.pdf#page=1
    """
    if n < 0:
        if x != a:
            return 0
        elif x == a:
            return 0  # mathematically np.NaN though!
    elif n >= 0:
        if x < a:
            return 0
        elif x >= a:
            return (x - a) ** n  # possibility of 0**0


def singular_x(arr, a, n):
    """
        broadcasting singular_unit to array ie, linspace x
    """
    return np.array(list(map(lambda x: singular_unit(x, a, n), arr)))


# def integrate(arr, a, n):
#     '''
#         combining integration logic recursively.
#         logic: http://www.eng.uwaterloo.ca/~syde06/singularity-functions.pdf#page=1
#     '''
#     if n == -2:
#         return singular_x(arr, a, -1)
#     elif n == -1:
#         return singular_x(arr, a, 0)
#     elif n >= 0:
#         return singular_x(arr, a, n + 1) / (n + 1)


def integrate(arr, a, n):
    '''
        combining integration logic recursively.
        logic: http://ruina.tam.cornell.edu/Courses/Tam202-Fall10/hwsoln/Singularityfns.pdf
    '''
    if n <= 0:
        return singular_x(arr, a, n+1)
    elif n >= 0:
        return singular_x(arr, a, n+1)/(n + 1)

def s(arr, a, n, depth=0):
    '''
        combining singularity and integration recursively for 
        convenience.
    '''
    if depth == 0:
        return singular_x(arr, a, n)
    if depth == 1:
        return integrate(arr, a, n)
    return s(arr, a, n + 1, depth - 1)



def singularity_order(x, distances, order=0):
    '''<x-a>^A do it with respect to q [(pos0, exp)]'''
    s_matrix = []
    for pos0, exp in distances:
        s_matrix.append(s(x, pos0, exp, order))
    return np.array(s_matrix, dtype=np.float64)

def enq(loads, distances, order, x):
    which = {
        'w': 0,
        'V': 1,
        'M': 2,
        'theta': 3,
        'def': 4,
    }
    return (loads * singularity_order(x, distances, which[order])).sum(0)


def show_plot(x:np.array, length:int, distances:list, loads:np.array):
    '''
        todo:
            * Later prepare a render module or something to prepare the plot then use that in Beam class
            * Just use the eqn() function in Beam Class
    '''
    # x = np.linspace(0, length, length * 1000)
    fig, (sfd, bmd) = plt.subplots(2, 1, figsize=(20, 25))
    sfd.set_title('SFD')
    bmd.set_title('BMD')
    sfd.spines['bottom'].set_position('zero')

    sfd.spines['left'].set_position('zero')
    sfd.spines['right'].set_color('none')
    sfd.spines['top'].set_color('none')

    bmd.spines['bottom'].set_position('zero')
    bmd.spines['left'].set_position('zero')
    bmd.spines['right'].set_color('none')
    bmd.spines['top'].set_color('none')

    sfd.set_xlim(0, length+5)
    bmd.set_xlim(0, length + 5)

    p = enq(loads, distances, 'w', x)
    V = enq(loads, distances, 'V', x)
    # print(V[-1])
    M = enq(loads,distances, 'M', x)
    theta = enq(loads, distances,  'theta', x)
    defl = enq(loads, distances, 'def', x)
    sfd.plot(x, V)

    max_moment = np.max(M)
    distance = x[np.argmax(M)]
    bmd.text(10, 100, f"Max bending moment: {max_moment:.2f} k-in")
    bmd.plot(x, M)
    bmd.text(distance, max_moment, f"{max_moment:.2f}")
    bmd.plot(distance, max_moment, '*')
    plt.show()


if __name__ == '__main__':
    length = 20
    distances = [
        # (pos, exp)
        (0,-1),
        (5,-1),
        (6,0),
        (12,0),
        (15,-2),
        (20,-1),
    ]
    loads = np.array([
        # load
        33,
        -20,
        -5,
        5,
        -30,
        17
    ])
    loads = loads.reshape(len(loads), 1)
    x = np.linspace(0, length, length * 1000)
    
    show_plot(x, length, distances, loads)