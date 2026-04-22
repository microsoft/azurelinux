# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    tbb2020.3
Summary: The Threading Building Blocks library abstracts low-level threading details
Version: 2020.3
Release: 8%{?dist}
License: Apache-2.0 AND BSD-3-Clause
URL:     http://threadingbuildingblocks.org/

Source0: https://github.com/intel/tbb/archive/v%{version}/tbb-%{version}.tar.gz
# These three are downstream sources.
Source6: tbb.pc
Source7: tbbmalloc.pc
Source8: tbbmalloc_proxy.pc

# Don't snip -Wall from C++ flags.  Add -fno-strict-aliasing, as that
# uncovers some static-aliasing warnings.
# Related: https://bugzilla.redhat.com/show_bug.cgi?id=1037347
Patch0: tbb-2019-dont-snip-Wall.patch

# Make attributes of aliases match those on the aliased function.
Patch1: tbb-2020-attributes.patch

# Fix test-thread-monitor, which had multiple bugs that could (and did, on
# ppc64le) result in a hang.
Patch2: tbb-2019-test-thread-monitor.patch

# Fix a test that builds a 4-thread barrier, but cannot guarantee that more
# than 2 threads will be available to use it.
Patch3: tbb-2019-test-task-scheduler-init.patch

# Fix ABI break resulting from tbb::empty_task being removed from libtbb.so's
# exported symbols
Patch4: tbb-mark-empty_task-execute-with-gnu-used.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2161412
# https://github.com/oneapi-src/oneTBB/pull/833
Patch5: tbb-2020-task-namespace.patch

# For compat package - only build tbb
Patch6: tbb2020.3-compat.patch

BuildRequires: cmake
BuildRequires: doxygen
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: swig
BuildRequires: tbb

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: tbb%{?_isa}
Conflicts: tbb-devel

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%prep
%autosetup -p1 -n oneTBB-%{version}

# For repeatable builds, don't query the hostname or architecture
sed -i 's/"`hostname -s`" ("`uname -m`"/fedorabuild (%{_arch}/' \
    build/version_info_linux.sh

# Insert --as-needed before the libraries to be linked.
sed -i "s/-fPIC/& -Wl,--as-needed/" build/linux.gcc.inc

%build
compiler=""
if [[ %{__cc} == *"gcc"* ]]; then
    compiler="gcc"
elif [[ %{__cc} == *"clang"* ]]; then
    compiler="clang"
else
    compiler="%{__cc}"
fi

%make_build tbb_build_prefix=obj stdver=c++14 \
    compiler=${compiler} \
    CXXFLAGS="%{optflags} -DUSE_PTHREAD" \
    LDFLAGS="$RPM_LD_FLAGS -lpthread" tbb
for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    base=$(basename ${file})
    sed 's/_FEDORA_VERSION/%{version}/' ${file} > ${base}
    touch -r ${file} ${base}
done

%check
# This test assumes it can create thread barriers for arbitrary numbers of
# threads, but tbb limits the number of threads spawned to a function of the
# number of CPUs available.  Some of the koji builders have a small number of
# CPUs, so the test hangs waiting for threads that have not been created to
# arrive at the barrier.  Skip this test until upstream fixes it.
sed -i '/test_task_scheduler_observer/d' build/Makefile.test

make test tbb_build_prefix=obj stdver=c++14 CXXFLAGS="%{optflags}"

%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}

pushd build/obj_release
    for file in libtbb; do
        install -p -D -m 755 ${file}.so.2 $RPM_BUILD_ROOT/%{_libdir}
        ln -s $file.so.2 $RPM_BUILD_ROOT/%{_libdir}/$file.so
    done
popd
ln -s libtbbmalloc.so.2 $RPM_BUILD_ROOT/%{_libdir}/libtbbmalloc.so
ln -s libtbbmalloc_proxy.so.2 $RPM_BUILD_ROOT/%{_libdir}/libtbbmalloc_proxy.so
ln -s libirml.so.1 $RPM_BUILD_ROOT/%{_libdir}/libirml.so

pushd include
    find tbb -type f ! -name \*.htm\* -exec \
        install -p -D -m 644 {} $RPM_BUILD_ROOT/%{_includedir}/{} \
    \;
popd

for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    install -p -D -m 644 $(basename ${file}) \
        $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/$(basename ${file})
done

# Install the rml headers
mkdir -p $RPM_BUILD_ROOT%{_includedir}/rml
cp -p src/rml/include/*.h $RPM_BUILD_ROOT%{_includedir}/rml

# Install the cmake files
cmake \
  -DINSTALL_DIR=$RPM_BUILD_ROOT%{_libdir}/cmake/TBB \
  -DSYSTEM_NAME=Linux \
  -DLIB_REL_PATH=../.. \
  -P cmake/tbb_config_installer.cmake

%files
%doc doc/Release_Notes.txt README.md
%license LICENSE
%{_libdir}/libtbb.so.2

%files devel
%doc CHANGES cmake/README.rst
%{_includedir}/rml/
%{_includedir}/tbb/
%{_libdir}/libtbb.so
%{_libdir}/libtbbmalloc.so
%{_libdir}/libtbbmalloc_proxy.so
%{_libdir}/libirml.so
%{_libdir}/cmake/TBB/
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Jonathan Wakely <jwakely@fedoraproject.org> - 2020.3-3
- Add BSD-3-Clause to License tag

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 10 2023 Orion Poplawski <orion@nwra.com> - 2020.3-1
- Compat package for TBB 2020.3
