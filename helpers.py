def _head(x: str) -> str:
    return x[0]

def _tail(x: str) -> str:
    return x[1:]

def levenstein(a: str, b: str) -> int:
    if len(a) == 0:
        return len(b)
    elif len(b) == 0:
        return len(a)
    else:
        return 1 + min([levenstein(_tail(a), b),
                        levenstein(a, _tail(b)),
                        levenstein(_tail(a), _tail(b))])