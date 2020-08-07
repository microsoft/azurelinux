#
# Macros for cmake
#
%_cmake_lib_suffix64 -DLIB_SUFFIX=64
%_cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=ON
%_cmake_version @@CMAKE_VERSION@@
%__cmake /usr/bin/cmake
# - Set default install prefixes and library install directories
# - Turn on shared libraries by default
%cmake \
  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
  CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
  %{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
  %__cmake \\\
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \\\
	-DCMAKE_INSTALL_LIBDIR:PATH=lib \\\
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \\\
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \\\
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \\\
	-DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \\\
%if "%{?_lib}" == "lib64" \
	%{?_cmake_lib_suffix64} \\\
%endif \
	-DBUILD_SHARED_LIBS:BOOL=ON

