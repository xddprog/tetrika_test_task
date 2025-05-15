def strict(func):
    def wrapper(*args):
        annotations = func.__annotations__
        param_types = list(annotations.values())[:-1]
        
        for arg, expected_type in zip(args, param_types):
            if not isinstance(arg, expected_type):
                raise TypeError
                
        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # 3
try:
    print(sum_two(1, 2.4))  # TypeError
except TypeError:
    print("TypeError")
