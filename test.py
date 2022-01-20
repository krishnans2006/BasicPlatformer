from contextlib import suppress

with suppress(ZeroDivisionError):
    print(10/0)