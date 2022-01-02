import time
from api.utils import threaded, wait_until_done, remove_duplicates


def test_threaded_no_wait():
    test_dict = {}

    @threaded
    def func():
        time.sleep(2)
        test_dict['value'] = True

    func()
    time.sleep(2.1)
    assert 'value' in test_dict
    assert test_dict['value'] == True


def test_threaded_wait():
    values = list(range(10))

    @threaded
    def func(val):
        return val

    results = wait_until_done(func(val) for val in values)

    assert results == values


def test_remove_duplicates():
    values = ["test", 1, 2, 3, "yes"] * 2

    val1 = set(values)
    val2 = remove_duplicates(values)

    assert val1 == set(val2)
