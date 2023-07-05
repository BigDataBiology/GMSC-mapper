from contextlib import contextmanager

@contextmanager
def open_output(ofile, mode='wt'):
    if ofile == '-' or ofile == '/dev/stdout':
        with open('/dev/stdout', mode=mode) as out:
            yield out
    else:
        try:
            from atomicwrites import atomic_write
        except ImportError:
            with open(ofile, mode=mode) as out:
                yield out
            return

        with atomic_write(ofile, mode=mode, overwrite=True) as out:
            yield out

def ask(string, valid_values=None, default=-1, case_sensitive=False):    
    """ Asks for a keyborad answer """
    if not valid_values:
        valid_values = ['y', 'n']
    v = None
    if not case_sensitive:
        valid_values = [value.lower() for value in valid_values]
    while v not in valid_values:
        v = input("%s [%s] " % (string,','.join(valid_values) ))
        if v == '' and default >= 0:
            v = valid_values[default]
        if not case_sensitive:
            v = v.lower()
    return v