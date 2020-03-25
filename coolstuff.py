from typing import *
__all__ = ["Array"]


class Array():
    """
        It's a Multi dimensional array based on dictionary data structure.
        and it will stored stuff in a dictionary,
        with tuple matching with the values.

        Features:
            * Easy to instantiate
            * Memory efficient for huge array.
            * slicing; like matlab, or nparray.

        not a feature:
            * Indexing with negative integers.
    """
    def __init__(self, Indexranges: Tuple[int], defaultvalue = None):
        """

        :param Indexranges:
            It's a tuple, the length of the tuple is the dimension of the array
            the integer value in side the tuple is the range for that specific dimension.
        :param defaultvalue:
            If the index is not yet set, what is the default value you want to get from it?
        """
        for I in Indexranges:
            assert I > 0, "range of a certain dimension cannot be negative nor zero."
        self.__DefaultValue = defaultvalue
        self.__Dimension = len(Indexranges)
        self.__IndexRange = Indexranges
        self.__Map = {}
        return

    def size(self):
        return self.__IndexRange

    def get_specific_element(self, indices: Tuple[int]):
        """
            Receives a tuple with length matching the dimension of the array.
        :return:
            that specific element at that index of the array.
        """
        assert len(indices) == self.__Dimension, "Dimension mismatch"
        return self.__DefaultValue if indices not in self.__Map else self.__Map[indices]

    def set_specific_element(self, indices: Tuple[int], value):
        """
            Given a tuple representing a multi-dimensional index, it will return
            the value at the specific index.
        :param indices:
            A tuple
        :param value:
            The value,
        :return:
            the value, if not set before, the default value will be returned.
        """
        for I, J in zip(self.__IndexRange, indices):
            assert I > J >= 0, f"Index out of range: J:{J}, I:{I}"
        self.__Map[indices] = value
        return

    def slice(self, slicer: Tuple[int]):
        """
            Slice a sub array inside the array.
            example:
                Let's say that the array "Arr" is 2d, m by n, then
                indices: (-1, 3)
                then it will slice (?, 3) and put then into an array with dimension (Arr.size()[0], 1)
                which is basically the third column, but as a m by 1 array.
        :param slicer:
            A list of tuple with dimension less than or equal to the dimension of the
            array.
        :return:
            Another instance of the Array class.
        """
        # check if the slicing index is valid:
        for I, E in enumerate(slicer):
            assert -1 <= E <= self.__IndexRange[I], "Invalid index for slicing."

        # Flatten the dimension from the slicing index:'
        NewDimension = []
        for I, E in enumerate(slicer):
            NewDimension.append(self.__IndexRange[I] if E == -1 else 1)

        # Copying to a new multi-dimensional Array.
        NewArr = Array(tuple(NewDimension), self.__DefaultValue)

        def should_transfer(slicing, indices):
            for E1, E2, I in zip(slicing, indices, range(len(indices))):
                if E1 == -1:
                    continue
                if E1 != E2:
                    return False
            return True

        for I in self.__Map.keys():
            if should_transfer(slicer, I):
                I = tuple([(E2 if E1 == -1 else 0) for E1, E2 in zip(slicer, I)])  # Collapse that slice with -1
                NewArr.set_specific_element(I, self.get_specific_element(I))
        return NewArr


    def collapse(self):
        """
            Collpase unecessary dimensions of the multi-dimension array.
            e.g.
                Say the array has dimension (1,100), then it will reduced to (100),
                Which is just a 1d array.
                Say the array has dimension (1,1,1), then it will reduced to (1), which is just a scaler.
        :return:
            None
        """

        pass

    def filter(self, fxn:Callable, mode = 0):
        """
            filter out a sub array from this array, using a conditional function given as a parameter.
        :param fxn:
            The conditional function used to filter out elements in the multi-dimension array.
        :param mode:
            if it's set to 0 then we are filtering by elements in the array, meaning that
            the elements will be passed as a parameters into the function.
            if it's set to 1, then it will be filtering by indices in the multidimensional array.
        :return:
            In instance of the Array class.
        """
        pass  # TODO: IMPLEMENT THIS SHIT.

    def __getitem__(self, item: Tuple[int]):
        """
            * Getting an specific item from a specific index
                e.g. (0,0)
                    Return the element in the first row and first column.
            * Slicing the array.
                e.g. (None, 0)
                    Return the first column as a n by 1 array.
            * Slicing the array with a boolean function (Could be filering with tuples OR value of the tuples...):
                ???? TODO: DO THIS SHIT
            * Slicing the array with list of indices:
                ??? TODO: DO THIS SHIT.
        :param item:
            A Tuple of integers or None, other stuff is not allowed.
        :return:
            It really depends on the context.
        """
        assert len(item) == self.__Dimension, f"Can't index a {self.size()} with the index {item}"

        if -1 not in item:
            return self.get_specific_element(item)

        # Slicing the Array:
        for I in range(len(item)):
            if item[I] is None:
                item[I] = -1

        return self.slice(item)

    def __setitem__(self, key: Tuple[int], value):
        if len(key) == self.__Dimension:
            self.set_specific_element(key, value)
            return
        raise Exception("Not Implemented yet")

    def empty_array(*integers):
        """
            A static method that construct the thing, with None in it.
        :param integers:
            Integers, the index ranges and dimension of the multi-dimension array.
        :return:
            An instance of the
        """
        return Array(integers)

    def __repr__(self):
        return str(self.__Map)


def brief_test1():
    print("Setting and getting specif elements")
    arr = Array((3, 3, 3))
    assert arr[2, 2, 2] is None
    arr[1, 1, 1] = 9
    assert arr[1, 1, 1] == 9
    assert arr.size() == (3, 3, 3)
    print("brief_test1 END")


def brief_test2():
    print("Testing slicing the multidimensional array. ")
    arr = Array((3, 3, 3))
    arr[1,1,1] = "fuck you"
    print(f"arr_size{arr.size()}")
    print(arr[1, -1, -1])



def main():
    print("main method run")
    brief_test1()
    brief_test2()
    pass


if __name__ == "__main__":
    main()