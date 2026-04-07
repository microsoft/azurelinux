import os
import sys

src = os.path.abspath('waf')
dst = os.path.abspath(sys.argv[1])

sys.dont_write_bytecode = True

try:
    from importlib.machinery import SourceFileLoader
    waf = SourceFileLoader('waf', src).load_module()
except ImportError:
    import imp
    waf = imp.load_source('waf', src)

waf.unpack_wafdir(dst, src)
