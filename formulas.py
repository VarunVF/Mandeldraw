from collections.abc import Callable


def mandelbrot(x: float, y: float, n: int) -> bool:
    """
    Determine whether a complex number is in the Mandelbrot set
    for a given number of iterations.
    :param x: real part
    :param y: imaginary part
    :param n: number of iterations to perform
    :return: whether the point is an element of the Mandelbrot set
    """
    c = complex(x, y)
    z = 0j
    for _ in range(n):
        z = z**2 + c
        if abs(z) > 2:
            return False

    return abs(z) < 2


def get_multibrot_func(power: float) -> Callable[[float, float, int], bool]:
    def multibrot(x, y, n):
        c = complex(x, y)
        z = 0j
        for _ in range(n):
            z = z ** power + c
            if abs(z) > 2:
                return False
        return abs(z) < 2

    return multibrot
