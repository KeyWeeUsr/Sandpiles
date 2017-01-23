from libc.math cimport sqrt, floor
from libc.stdlib cimport malloc, free
from cpython cimport PyList_GET_SIZE


cdef class Sandpile:
    cdef list _grid
    cdef unsigned int _size, grid_len, grid_width

    def __init__(self,
                 list grid=[],
                 unsigned int single=0,
                 unsigned int times=1,
                 unsigned int custom=0):

        cdef unsigned int multiply, size, i, j
        cdef double size_d

        # protect grid from None
        if grid is None:
            raise ValueError(
                'Grid cannot be None!'
            )

        # check kwargs first
        if custom and (times != 1 or single != 0):
            return
        elif not custom and single == 0:
            return
        elif custom and times == 1:
            self.grid_len = PyList_GET_SIZE(grid)
            size_d = sqrt(self.grid_len)
            self.grid_width = <unsigned int>size_d
        else:
            self.grid_width = times
            self.grid_len = times * times
            size_d = times

        if size_d * 10 - floor(size_d * 10) > 0:
            raise ValueError(
                'Square grids only!'
            )
        else:
            size = <unsigned int> size_d

        self._size = size

        # manual range(start, end, inc)
        cdef unsigned int range_len
        cdef unsigned int * range_offset
        range_len = self.grid_len / size
        range_offset = self.range_offset(0, self.grid_len, size, range_len)

        # make sublists
        cdef list new_grid
        if custom:
            self._grid = []
            for i in range(range_len):
                self._grid.append(grid[range_offset[i]:range_offset[i] + size])
        else:
            self._grid = grid
            for i in range(times):
                new_grid = []
                for j in range(times):
                    new_grid.append(single)
                self._grid.append(new_grid)

        free(range_offset)

        self._check()

    cdef void _check(self):
        cdef list copy_grid
        cdef unsigned int run = 0
        cdef unsigned int loop = 1
        cdef unsigned int end = self._size
        cdef unsigned int x, y
        end -= 1

        while loop:
            copy_grid = self._grid[:]
            for y in range(self.grid_width):
                for x in range(<unsigned int> (end + 1)):
                    # because PyObject_RichCompare is evil
                    if <unsigned int>self._grid[y][x] > 3:
                        run = 1
                        # topple start, because I can
                        if x >= 0 and x < self._size:
                            if y + 1 >= 0 and y + 1 < self._size:
                                copy_grid[y + 1][x] += 1
                        if x >= 0 and x < self._size:
                            if y - 1 >= 0 and y - 1 < self._size:
                                copy_grid[y - 1][x] += 1
                        if x - 1 >= 0 and x - 1 < self._size:
                            if y >= 0 and y < self._size:
                                copy_grid[y][x - 1] += 1
                        if x + 1 >= 0 and x + 1 < self._size:
                            if y >= 0 and y < self._size:
                                copy_grid[y][x + 1] += 1
                        copy_grid[y][x] -= 4
                        # topple end
                    elif not run and x == end and y == end:
                        loop = 0
            self._grid = copy_grid
            run = 0

    cdef unsigned int * range_offset(self,
                                     unsigned int start,
                                     unsigned int end,
                                     unsigned int offset,
                                     unsigned int size):

        cdef unsigned int i, value = 0
        cdef unsigned int * array = <unsigned int * > malloc(
            sizeof(unsigned int) * size
        )

        for i in range(size):
            array[i] = value
            i += 1
            value += offset
        return array

    @property
    def grid(self):
        return self._grid

    @property
    def size(self):
        return self._size
