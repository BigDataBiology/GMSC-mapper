from contextlib import contextmanager
import shutil

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


def version_comment(prefix='#'):
    from gmsc_mapper.gmsc_mapper_version import __version__

    return f'{prefix} GMSC-mapper version {__version__}'


def write_version_comment(out, prefix='#'):
    out.write(f'{version_comment(prefix)}\n')


def prepend_version_comment(ofile, prefix='#'):
    comment = f'{version_comment(prefix)}\n'
    with open(ofile, 'rt') as src:
        first = src.readline()
        if first == comment:
            return
        try:
            from atomicwrites import atomic_write
        except ImportError:
            remainder = first + src.read()
            with open(ofile, 'wt') as out:
                out.write(comment)
                out.write(remainder)
            return

        with atomic_write(ofile, overwrite=True) as out:
            out.write(comment)
            out.write(first)
            shutil.copyfileobj(src, out)

def ask(string, valid_values=None, default=0, case_sensitive=False):
    """ Asks for a keyboard answer """
    if not valid_values:
        valid_values = ['y', 'n']
    v = None
    if not case_sensitive:
        valid_values = [value.lower() for value in valid_values]
    prompt_values = [val.upper() if i == default else val
                     for i, val in enumerate(valid_values)]
    while v not in valid_values:
        v = input(f"{string} [{'/'.join(prompt_values)}] ")
        if v == '' and default >= 0:
            v = valid_values[default]
        if not case_sensitive:
            v = v.lower()
    return v
