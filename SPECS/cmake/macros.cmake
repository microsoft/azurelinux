#
# Macros for cmake
#
%_cmake_lib_suffix64 -DLIB_SUFFIX=64
%_cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=ON
%_cmake_version @@CMAKE_VERSION@@
%__cmake /usr/bin/cmake
%__ctest /usr/bin/ctest
%__cmake_in_source_build 1
%__cmake_builddir %{!?__cmake_in_source_build:%{_vpath_builddir}}%{?__cmake_in_source_build:.}

# - Set default install prefixes and library install directories
# - Turn on shared libraries by default
%cmake \
  CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
  CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
  %{?__global_ldflags:LDFLAGS="${LDFLAGS:-%__global_ldflags}" ; export LDFLAGS ;} \
  %__cmake \\\
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \\\
  -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \\\
	-DCMAKE_INSTALL_LIBDIR:PATH=lib \\\
	-DINCLUDE_INSTALL_DIR:PATH=%{_includedir} \\\
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \\\
	-DSYSCONF_INSTALL_DIR:PATH=%{_sysconfdir} \\\
	-DSHARE_INSTALL_PREFIX:PATH=%{_datadir} \\\
%if "%{?_lib}" == "lib64" \
	%{?_cmake_lib_suffix64} \\\
%endif \
	-DBUILD_SHARED_LIBS:BOOL=ON \\\
    %{!?__cmake_in_source_build:-S "%{_vpath_srcdir}"} \\\
    -B "%{__cmake_builddir}" 
%cmake_build \
  %__cmake --build "%{__cmake_builddir}" %{?_smp_mflags} --verbose

%cmake_install \
  DESTDIR="%{buildroot}" %__cmake --install "%{__cmake_builddir}"

%ctest(:-:) \
  cd "%{__cmake_builddir}" \
  %__ctest --output-on-failure --force-new-ctest-process %{?_smp_mflags} %{**} \
  cd -


%cmake@@CMAKE_MAJOR_VERSION@@ %cmake
%cmake@@CMAKE_MAJOR_VERSION@@_build %cmake_build
%cmake@@CMAKE_MAJOR_VERSION@@_install %cmake_install
%ctest@@CMAKE_MAJOR_VERSION@@(:-:) %ctest %{**}
