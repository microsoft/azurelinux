# If docs should point to local python3-docs rather than website.
# python3-docs is not shipped in RHEL 9+
%bcond py3docs %{undefined rhel}

%global giturl https://github.com/oneapi-src/oneTBB

Name:    tbb
Summary: The Threading Building Blocks library abstracts low-level threading details
Version: 2021.13.0
Release: 2%{?dist}
License: Apache-2.0 AND BSD-3-Clause
URL:     http://threadingbuildingblocks.org/
VCS:     git:%{giturl}.git

Source0: %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz
# These two are downstream sources.
Source7: tbbmalloc.pc
Source8: tbbmalloc_proxy.pc

# TBB tries to remove -Werror from the compiler flags, which turns
# -Werror=format-security into =format-security
Patch0: tbb-2021-Werror.patch

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: hwloc
BuildRequires: hwloc-devel
BuildRequires: make
BuildRequires: python3-devel
%if %{with py3docs}
BuildRequires: python3-docs
%endif
BuildRequires: %{py3_dist setuptools}
BuildRequires: %{py3_dist sphinx}
BuildRequires: %{py3_dist sphinx-rtd-theme}
BuildRequires: swig

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package bind
Summary: NUMA support library for TBB
Requires: %{name}%{?_isa} = %{version}-%{release}

%description bind
NUMA support library for TBB, allowing the binding of tasks to selected
CPU cores.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-bind%{?_isa} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%package doc
Summary: The Threading Building Blocks documentation
%ifarch %{ix86}
# https://bugzilla.redhat.com/show_bug.cgi?id=2174300
Conflicts: %{name}-doc.x86_64
%endif

%description doc
PDF documentation for the user of the Threading Building Block (TBB)
C++ library.


%package -n python3-%{name}
Summary: Python 3 TBB module
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python 3 TBB module.


%prep
%autosetup -p1 -n oneTBB-%{version}

# Invoke the right python binary directly
for fil in $(grep -Frl %{_bindir}/env python); do
    sed -i.orig 's,env python3,python3,' $fil
    touch -r $fil.orig $fil
    rm $fil.orig
done

%if %{with py3docs}
# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.python\.org/': \)None|\1'%{_docdir}/python3-docs/html/objects.inv'|" \
    -i doc/GSG/conf.py doc/main/conf.py
%endif

%generate_buildrequires
cd python
%pyproject_buildrequires

%build
export TBBROOT=$PWD
export PYTHONPATH=$(sed "s,%{_prefix},$PWD/%{_vpath_builddir}/python/build," <<< %{python3_sitearch})
%cmake \
    -DCMAKE_CXX_STANDARD=17 \
    -DTBB4PY_BUILD:BOOL=ON \
    -DTBB_STRICT:BOOL=OFF \
    -DCMAKE_HWLOC_2_4_LIBRARY_PATH=%{_libdir}/libhwloc.so \
    -DCMAKE_HWLOC_2_4_INCLUDE_PATH=%{_includedir}/hwloc \
%cmake_build

# The python package is not built the Fedora way.  Do it over.
unset PYTHONPATH
export LD_LIBRARY_PATH=$(ls -1d $PWD/%{_vpath_builddir}/*relwithdebinfo)
export LDFLAGS="-L $LD_LIBRARY_PATH %{build_ldflags}"
cd python
%pyproject_wheel
cd -

# Build documentation
export BUILD_TYPE=oneapi
sphinx-build doc/GSG getting-started
sphinx-build doc/main html

%install
%cmake_install

# The python package is not installed the Fedora way.  Do it over.
rm -fr %{buildroot}%{python3_sitearch}
cd python
%pyproject_install
cd -

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
for file in %{SOURCE7} %{SOURCE8}; do
    target=%{buildroot}/%{_libdir}/pkgconfig/$(basename ${file})
    sed 's/_FEDORA_VERSION/%{version}/' $file > $target
    touch -r $file $target
done

# Upstream installs tbb32.pc on 32-bit but it's already in a separate directory
# because %_libdir is different for 32-bit and 64-bit, so rename it to tbb.pc.
if [ -f %{buildroot}/%{_libdir}/pkgconfig/%{name}32.pc ]; then
    mv %{buildroot}/%{_libdir}/pkgconfig/%{name}32.pc %{buildroot}/%{_libdir}/pkgconfig/%{name}.pc
fi

rm -fr %{buildroot}%{_datadir}/doc

%check
# Running the tests in parallel often leads to resource exhaustion.
ctest --output-on-failure --force-new-ctest-process

%files
%doc README.md
%license LICENSE.txt
%{_libdir}/libtbb.so.12*
%{_libdir}/libtbbmalloc.so.2*
%{_libdir}/libtbbmalloc_proxy.so.2*
%{_libdir}/libirml.so.1

%files bind
%{_libdir}/libtbbbind_2_5.so.3*

%files devel
%doc cmake/README.md
%{_includedir}/oneapi/
%{_includedir}/tbb/
%{_libdir}/*.so
%{_libdir}/cmake/TBB/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc getting-started html

%files -n python3-%{name}
%doc python/README.md
%{python3_sitearch}/TBB*
%{python3_sitearch}/tbb/
%{python3_sitearch}/__pycache__/TBB*

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2021.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul  9 2024 Jerry James <loganjerry@gmail.com> - 2021.13.0-1
- Version 2021.13.0
- Add VCS tag
- Drop upstreamed strict aliasing patch

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2021.11.0-6
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Jonathan Wakely <jwakely@fedoraproject.org> - 2021.11.0-5
- Remove Requires:python3-docs for tbb-doc subpackage

* Mon Jan 22 2024 Jonathan Wakely <jwakely@fedoraproject.org> - 2021.11.0-4
- Rename 32-bit arch /usr/lib/pkgconfig/tbb32.pc to tbb.pc

* Fri Jan 19 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2021.11.0-3
- Avoid python3-docs dependency on RHEL

* Wed Jan 17 2024 Jonathan Wakely <jwakely@fedoraproject.org> - 2021.11.0-2
- Add patch for strict aliasing violation

* Thu Dec 28 2023 Jerry James <loganjerry@gmail.com> - 2021.11.0-1
- Rebase to version 2021.11.0
- New -bind subpackage for the NUMA support library
- Build with cmake
- Minor spec file cleanups

* Thu Aug 10 2023 Jonathan Wakely <jwakely@fedoraproject.org> - 2020.3-21
- SPDX migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 2020.3-19
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Jonathan Wakely <jwakely@fedoraproject.org> - 2020.3-18
- Add conflicts tag for tbb-doc (#2174300)
- Remove outdated provides for bundled(jquery)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2020.3-17
- Rebuilt for Python 3.12

* Tue Feb 21 2023 Jonathan Wakely <jwakely@redhat.com> - 2020.3-16
- Add versioned Requires: to python module

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Thomas Rodgers <trodgers@redhat.com> - 2020.3-14
- Fix build failure with GCC13 (bz 2161412)

* Wed Jan 11 2023 Thomas Rodgers <trodgers@redhat.com> - 2020.3-13
- Fix build failure with Python 3.12.0 (bz 2154975)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2020.3-11
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 09 2021 Thomas Rodgers <trodgers@redhat.com> - 2020.3-8
- Merge change to remove baseos-qe.koji-build.scratch-build.validation ahajkova

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2020.3-7
- Rebuilt for Python 3.10

* Thu Jun  3 2021 Thomas Rodgers <trodgers@redhat.com> - 2020.3-6
- Fix ABI regression in tbb::empty_task caused by switch to LTO

* Mon Feb 22 2021 Jerry James <loganjerry@gmail.com> - 2020.3-5
- Fix cmake file installation some more (bz 1930389)

* Thu Feb 18 2021 Jerry James <loganjerry@gmail.com> - 2020.3-4
- Fix cmake file installation (bz 1930389)
- Allow use of RTM instructions when available
- At upstream's suggestion, do not force ITT_NOTIFY support
- Drop -fetchadd64 patch, only needed for forced ITT_NOTIFY support

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Jerry James <loganjerry@gmail.com> - 2020.3-1
- Rebase to version 2020.3

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2020.2-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2020.2-3
- Rebuilt for Python 3.9

* Mon Apr 27 2020 Timm Baeder <tbaeder@redhat.com> - 2020.2-2
- Pass the compiler to when building
- Update the tbb-2019-test-thread-monitor.patch to use std::atomic

* Tue Mar 31 2020 Jerry James <loganjerry@gmail.com> - 2020.2-1
- Rebase to version 2020.2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2020.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Jerry James <loganjerry@gmail.com> - 2020.1-1
- Rebase to version 2020.1

* Tue Dec 31 2019 Jerry James <loganjerry@gmail.com> - 2020-1
- Rebase to version 2020

* Sat Oct 12 2019 Jerry James <loganjerry@gmail.com> - 2019.9-1
- Rebase to 2019 update 9

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.8-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Tue Aug 27 2019 Jerry James <loganjerry@gmail.com> - 2019.8-3
- Add -test-thread-monitor and -test-task-scheduler-init patches to fix FTBFS

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2019.8-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun  8 2019 Jerry James <loganjerry@gmail.com> - 2019.8-1
- Rebase to 2019 update 8

* Thu May 23 2019 Jerry James <loganjerry@gmail.com> - 2019.7-1
- Rebase to 2019 update 7

* Thu May  9 2019 Jerry James <loganjerry@gmail.com> - 2019.6-1
- Rebase to 2019 update 6
- Add -attributes patch to silence gcc warnings

* Mon Mar 25 2019 Jerry James <loganjerry@gmail.com> - 2019.5-1
- Rebase to 2019 update 5

* Mon Mar  4 2019 Jerry James <loganjerry@gmail.com> - 2019.4-1
- Rebase to 2019 update 4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2019.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec  8 2018 Jerry James <loganjerry@gmail.com> - 2019.3-1
- Rebase to 2019 update 3

* Fri Nov 16 2018 Jerry James <loganjerry@gmail.com> - 2019.2-1
- Rebase to 2019 update 2

* Thu Oct  4 2018 Jerry James <loganjerry@gmail.com> - 2019.1-1
- Rebase to 2019 update 1
- Drop special SSE2 build for 32-bit x86 as that is now default
- Drop unneeded -cxxflags patch
- Drop python 2 support (bz 1629761)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul  3 2018 Jerry James <loganjerry@gmail.com> - 2018.5-1
- Rebase to 2018 update 5
- Run check script on all architectures

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2018.4-2
- Rebuilt for Python 3.7

* Thu May 31 2018 Jerry James <loganjerry@gmail.com> - 2018.4-1
- Rebase to 2018 update 4

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2018.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Jerry James <loganjerry@gmail.com> - 2018.2-4
- Build libirml with the correct flags (bz 1540268)
- Do not build with -mrtm

* Mon Jan 29 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2018.2-3
- Fix Python 2 dependency from python3-tbb

* Fri Jan 26 2018 Jerry James <loganjerry@gmail.com> - 2018.2-2
- Install libirml for the python interfaces

* Wed Jan 24 2018 Jerry James <loganjerry@gmail.com> - 2018.2-1
- Rebase to 2018 update 2

* Sat Nov 25 2017 Jerry James <loganjerry@gmail.com> - 2018.1-1
- Rebase to 2018 update 1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun  8 2017 Jerry James <loganjerry@gmail.com> - 2017.7-1
- Rebase to 2017 update 7
- Use the license macro
- Ship the new cmake files in -devel

* Tue May 16 2017 Jerry James <loganjerry@gmail.com> - 2017.6-1
- Rebase to 2017 update 6

* Fri Mar 17 2017 Jerry James <loganjerry@gmail.com> - 2017.5-1
- Rebase to 2017 update 5
- Change version scheme again to match upstream's change
- New source URL on github
- Drop upstreamed patch to fix detection of s390x as 64-bit arch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017-8.20161128
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Dan Horák <dan[at]danny.cz> - 2017-7.20161128
- Fix detection of s390x as 64-bit arch (#1379632)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2017-6.20161128
- Rebuild for Python 3.6

* Fri Dec  2 2016 Jerry James <loganjerry@gmail.com> - 2017-5.20161128
- Rebase to 2017 update 3
- Drop upstreamed s390x patch

* Wed Nov  2 2016 Jerry James <loganjerry@gmail.com> - 2017-4.20161004
- Rebase to 2017 update 2

* Fri Oct 07 2016 Dan Horák <dan[at]danny.cz> - 2017-3.20160916
- Fix detection of s390x as 64-bit arch (#1379632)

* Fri Sep 30 2016 Jerry James <loganjerry@gmail.com> - 2017-2.20160916
- New upstream release

* Thu Sep 22 2016 Jerry James <loganjerry@gmail.com> - 2017-1.20160722
- Rebase to 2017, new upstream version numbering scheme

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-8.20160526
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun  1 2016 Jerry James <loganjerry@gmail.com> - 4.4-7.20160526
- Rebase to 4.4u5
- Build in C++14 mode
- Build the new python module

* Fri May  6 2016 Jerry James <loganjerry@gmail.com> - 4.4-6.20160413
- Rebase to 4.4u4

* Mon Apr  4 2016 Jerry James <loganjerry@gmail.com> - 4.4-5.20160316
- Add -fno-delete-null-pointer-checks to fix optimized code

* Fri Mar 18 2016 Jerry James <loganjerry@gmail.com> - 4.4-4.20160316
- Updated upstream tarball
- Link with RPM_LD_FLAGS

* Sat Feb 20 2016 Jerry James <loganjerry@gmail.com> - 4.4-3.20160128
- Rebase to 4.4u3

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2.20151115
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jerry James <loganjerry@gmail.com> - 4.4-1.20151115
- Rebase to 4.4u2
- Fix the mfence patch to actually emit a memory barrier (bz 1288314)
- Build an sse2 version for i386 for better performance on capable CPUs
- Enable use of C++0x features
- Drop out-of-date CHANGES.txt from git

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-3.20141204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.3-2.20141204
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 19 2015 Petr Machata <pmachata@redhat.com> - 4.3-1.20141204
- Rebase to 4.3u2
- Drop ExclusiveArch

* Thu Sep 25 2014 Karsten Hopp <karsten@redhat.com> 4.1-9.20130314
- enable ppc64le and run 'make test' on that new arch

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-8.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-7.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 Peter Robinson <pbrobinson@fedoraproject.org> 4.1-6.20130314
- Build on aarch64, minor spec cleanups

* Tue Dec  3 2013 Petr Machata <pmachata@redhat.com> - 4.1-5.20130314
- Fix building with -Werror=format-security (tbb-4.1-dont-snip-Wall.patch)

* Thu Oct  3 2013 Petr Machata <pmachata@redhat.com> - 4.1-4.20130314
- Fix %%install to also install include files that are not named *.h

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-3.20130314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Petr Machata <pmachata@redhat.com> - 4.1-3.20130314
- Enable ARM arches

* Wed May 22 2013 Petr Machata <pmachata@redhat.com> - 4.1-2.20130314
- Fix mfence patch.  Since the __TBB_full_memory_fence macro was
  function-call-like, it stole () intended for function invocation.

* Wed May 22 2013 Petr Machata <pmachata@redhat.com> - 4.1-1.20130314
- Rebase to 4.1 update 3

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-7.20120408
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Petr Machata <pmachata@redhat.com> - 4.0-6.20120408
- Fix build on PowerPC

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-5.20120408
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun  7 2012 Petr Machata <pmachata@redhat.com> - 4.0-4.20120408
- Rebase to 4.0 update 4
- Refresh Getting_Started.pdf, Reference.pdf, Tutorial.pdf
- Provide pkg-config files
- Resolves: #825402

* Thu Apr 05 2012 Karsten Hopp <karsten@redhat.com> 4.0-3.20110809
- tbb builds now on PPC(64)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-2.20110809
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Petr Machata <pmachata@redhat.com> - 4.0-1.20110809
- Rebase to 4.0
  - Port the mfence patch
  - Refresh the documentation bundle

* Tue Jul 26 2011 Petr Machata <pmachata@redhat.com> - 3.0-1.20110419
- Rebase to 3.0-r6
  - Port both patches
  - Package Design_Patterns.pdf
  - Thanks to Richard Shaw for initial rebase patch
- Resolves: #723043

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3.20090809
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Petr Machata <pmachata@redhat.com> - 2.2-2.20090809
- Replace mfence instruction with xchg to make it run on ia32-class
  machines without SSE2.
- Resolves: #600654

* Tue Nov  3 2009 Petr Machata <pmachata@redhat.com> - 2.2-1.20090809
- New upstream 2.2
- Resolves: #521571

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3.20080605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2.20080605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 13 2008 Petr Machata <pmachata@redhat.com> - 2.1-1.20080605
- New upstream 2.1
  - Drop soname patch, parallel make patch, and GCC 4.3 patch

* Wed Feb 13 2008 Petr Machata <pmachata@redhat.com> - 2.0-4.20070927
- Review fixes
  - Use updated URL
  - More timestamp preservation
- Initial import into Fedora CVS

* Mon Feb 11 2008 Petr Machata <pmachata@redhat.com> - 2.0-3.20070927
- Review fixes
  - Preserve timestamp of installed files
  - Fix soname not to contain "debug"

* Tue Feb  5 2008 Petr Machata <pmachata@redhat.com> - 2.0-2.20070927
- Review fixes
  - GCC 4.3 patchset
  - Add BR util-linux net-tools
  - Add full URL to Source0
  - Build in debug mode to work around problems with GCC 4.3

* Mon Dec 17 2007 Petr Machata <pmachata@redhat.com> - 2.0-1.20070927
- Initial package.
- Using SONAME patch from Debian.
