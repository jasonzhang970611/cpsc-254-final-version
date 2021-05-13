"""Algorithm Basement"""


from typing import Any, Iterable, List, Tuple, Union


def transpose(obj: Iterable[Union[List, Tuple]]) -> List[List[Any]]:
    """
    Calculate transpose of a data strcture like matrix:
    Input:
        [
            [1, 2, 3],
            [2, 3, 4, 5],
            [6, 7],
            [8, 9, 10]
        ]
    Output:
        [
            [1, 2, 6, 8],
            [2, 3, 7, 9],
            [3, 4, 10],
            [5]
        ]
    """
    result: List[List[Any]] = list()
    maxlen = max(map(lambda obj: len(obj), obj))

    for index in range(maxlen):
        layer: List[Any] = list()
        for line in obj:
            if len(line) - 1 >= index:
                layer.append(line[index])
        result.append(layer)

    return result


if __name__ == "__main__":

    from pprint import pprint

    # Test for transpose
    assert(transpose(
        [
            [1, 2, 3],
            [2, 3, 4, 5],
            [6, 7],
            [8, 9, 10]
        ]
    ) == [
        [1, 2, 6, 8], 
        [2, 3, 7, 9], 
        [3, 4, 10], 
        [5]
    ])
