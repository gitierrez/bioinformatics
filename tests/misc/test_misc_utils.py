from biomics.misc import sort_dict


def test_sort_dict_ascending():
    d = {'a': 5, 'b': 1, 'c': 4, 'd': 3, 'e': 2}
    assert list(sort_dict(d, ascending=True).keys()) == ['b', 'e', 'd', 'c', 'a']


def test_sort_dict_descending():
    d = {'a': 5, 'b': 1, 'c': 4, 'd': 3, 'e': 2}
    assert list(sort_dict(d, ascending=False).keys()) == ['a', 'c', 'd', 'e', 'b']
