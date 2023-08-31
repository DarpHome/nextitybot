import pkgutil
import os
from typing import Iterator

def search_directory(path: str) -> Iterator[str]:
    """Walk through a directory and yield all modules.

    Parameters
    ----------
    path: :class:`str`
        The path to search for modules

    Yields
    ------
    :class:`str`
        The name of the found module. (usable in load_extension)
    """
    relpath = os.path.relpath(path)  # relative and normalized
    if ".." in relpath:
        raise ValueError("Modules outside the cwd require a package to be specified")

    abspath = os.path.abspath(path)
    if not os.path.exists(relpath):
        raise ValueError(f"Provided path '{abspath}' does not exist")
    if not os.path.isdir(relpath):
        raise ValueError(f"Provided path '{abspath}' is not a directory")

    prefix = relpath.replace(os.sep, ".")
    if prefix in ("", "."):
        prefix = ""
    else:
        prefix += "."

    for _, name, ispkg in pkgutil.iter_modules([path]):
        if ispkg:
            yield from search_directory(os.path.join(path, name))
        else:
            yield prefix + name


DEFAULT_ALPHABET: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'

def atoi(target: str, *, radix: int = 10, alphabet: str = DEFAULT_ALPHABET, case_sensitive: bool = False) -> int:
    result: int = 0
    looped: bool = False
    sign: bool = False
    success: bool = False
    assert 2 <= radix <= len(alphabet), f"2 <= radix <= {len(alphabet)}"
    for character in target:
        if character == '-':
            sign = True
        if character in '-\t\n\v\f\r +_':
            continue
        looped = True
        position: int = alphabet.find(character.upper() if case_sensitive else character)
        if position == -1 or position >= radix:
            break
        success = True
        result = result * radix + position
    if sign:
        result = -result
    if not looped:
        raise EOFError('Empty string')
    if not success:
        raise ValueError('Invalid character at start')
    return result


def itoa(n: int, *, radix: int = 10, alphabet: str = DEFAULT_ALPHABET) -> str:
    if len(alphabet) < 2:
        raise ValueError('alphabet')
    if radix > len(alphabet):
        raise ValueError('radix')
    sign: bool = False
    if n < 0:
        n = -n
        sign = True
    result: str = ''
    while True:
        result += alphabet[n % radix]
        n //= radix
        if n == 0:
            break
    if sign:
        result += '-'
    return result[::-1]
