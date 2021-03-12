#!/usr/bin/python3

import cffi

# ------------------------------------------------------------------------------- #

ffibuilder = cffi.FFI()

ffibuilder.embedding_api(
    """
    char *getURL(char url[]);
    """
)

ffibuilder.set_source("helheim_cffi", "")
with open('template.tpl', 'r') as code:
    ffibuilder.embedding_init_code(code.read())

ffibuilder.compile(target="helheim_cffi.so", verbose=True)

