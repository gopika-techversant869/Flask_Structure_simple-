import cProfile

def test_function():
    total = 0
    for i in range(10000):
        total += i
    return total

cProfile.run('test_function()')
