import tempfile

compiler = '%(libomp_compiler)s' % lit_config.params
config.test_filecheck = '%(bindir)s/FileCheck' % lit_config.params
config.omp_header_directory = '%(includedir)s' % lit_config.params
config.libomp_obj_root = tempfile.mkdtemp()
config.library_dir = '%(libdir)s' % lit_config.params
test_root = '%(libomp_test_root)s' % lit_config.params

# Lit will default to the compiler used to build openmp, which is gcc, but we
# want to run the tests using clang.
config.test_compiler_features = ['clang']
config.test_c_compiler = 'clang'
config.test_cxx_compiler = 'clang++'
lit_config.load_config(config, '%(libomp_test_root)s/lit.cfg' % lit_config.params)
