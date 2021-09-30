import numpy as np
import matplotlib.pyplot as plt


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


def integrate(arr, a, n):
    '''
        combining integration logic recursively.
        logic: http://www.eng.uwaterloo.ca/~syde06/singularity-functions.pdf#page=1
    '''
    if n == -2:
        return singular_x(arr, a, -1)
    elif n == -1:
        return singular_x(arr, a, 0)
    elif n >= 0:
        return singular_x(arr, a, n + 1) / (n + 1)


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


def singularity_order(order=0):
    return np.array([
        s(x, 0, -2, order),
        s(x, 15, 0, order),
        s(x, 45, 0, order),
        s(x, 25, -1, order),
        s(x, 50, -2, order),
        # s(x, 50, -1, order),
        s(x, 50, -1, order)
    ])


def enq(loads, order):
    which = {
        'w': 0,
        'V': 1,
        'M': 2,
        'theta': 3,
        'def': 4,
    }
    return (loads * singularity_order(which[order])).sum(0)


Ra = 67.5  # 210
Rb = 42.5  # 90

fig, ((sfd, bmd), (slope, deflection)) = plt.subplots(2, 2)
sfd.set_title('SFD')
bmd.set_title('BMD')
sfd.spines['bottom'].set_position('zero')
sfd.set_xlim(0, 55)
sfd.spines['left'].set_position('zero')
sfd.spines['right'].set_color('none')
sfd.spines['top'].set_color('none')

bmd.spines['bottom'].set_position('zero')
bmd.spines['left'].set_position('zero')
bmd.spines['right'].set_color('none')
bmd.spines['top'].set_color('none')

x = np.linspace(0, 50, 50 * 1000)
loads = np.array([
    125,
    20,
    -20,
    -50,
    -10875,
    -550
]).reshape(6, 1)
print(loads)

p = enq(loads, 'w')
V = enq(loads, 'V')
M = enq(loads, 'M')
theta = enq(loads, 'theta')
defl = enq(loads, 'def')

# plots
print(V)
sfd.plot(x, V)

max_moment = np.max(M)
distance = x[np.argmax(M)]
bmd.text(10, 100, f"Max bending moment: {max_moment:.2f} k-in")
bmd.plot(x, M)
bmd.text(distance, max_moment, f"{max_moment:.2f}")
bmd.plot(distance, max_moment, '*')

slope.plot(x, theta)
deflection.plot(x, defl)
plt.show()
