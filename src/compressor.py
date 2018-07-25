"""Compressor.

Usage:
  compressor.py compress <read_file> [-o <write_file>] [--lzw|--elias [--divergence <divergence>|--code <code>] [--hp]]
  compressor.py decompress <read_file> [-o <write_file>] (--lzw|--elias --code <code> [--hp])

Options:
  --help                         Show this screen.
  --version                      Show version.
  -o                             Specify output file.
  --lzw                          Use lzw algorithm.
  --elias                        Use elias codes.
  -d --divergence=<divergence>   Specify characters distribution divergence.
  --code=<code>                  Specify elias code type.
  --hp                           Use hyper-threading for high performance.

"""
from docopt import docopt

import execution

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Compressor 1.0')
    print(arguments)
    try:
        execution.execute(arguments)
    except Exception as e:
        print(e.args)
