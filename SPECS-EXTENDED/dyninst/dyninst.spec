Summary: An API for Run-time Code Generation
License: LGPL-2.1-or-later AND GPL-3.0-or-later WITH Bison-exception-2.2 AND LicenseRef-Fedora-Public-Domain AND BSD-3-Clause
Name: dyninst
Group: Development/Libraries
Release: 7%{?dist}
URL: http://www.dyninst.org
Version: 12.3.0
ExclusiveArch: %{ix86} x86_64 ppc64le aarch64

%define __testsuite_version 12.3.0
Source0: https://github.com/dyninst/dyninst/archive/v%{version}/dyninst-%{version}.tar.gz
Source1: https://github.com/dyninst/testsuite/archive/v%{__testsuite_version}/testsuite-%{__testsuite_version}.tar.gz

Patch1: dwarf-error.patch
Patch2: onetbb.patch
# Support cmake 3.27 - https://github.com/dyninst/dyninst/pull/1438
Patch3: dyninst-cmake3.27.patch

%global dyninst_base dyninst-%{version}
%global testsuite_base testsuite-%{__testsuite_version}

BuildRequires: gcc-c++
BuildRequires: elfutils-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: elfutils-debuginfod-client-devel
BuildRequires: boost-devel
BuildRequires: binutils-devel
BuildRequires: cmake
BuildRequires: libtirpc-devel
BuildRequires: tbb tbb-devel
BuildRequires: tex-latex

# Extra requires just for the testsuite
BuildRequires: gcc-gfortran libxml2-devel
BuildRequires: make

# Testsuite files should not provide/require anything
%{?filter_setup:
%filter_provides_in %{_libdir}/dyninst/testsuite/
%filter_requires_in %{_libdir}/dyninst/testsuite/
%filter_setup
}

%description

Dyninst is an Application Program Interface (API) to permit the insertion of
code into a running program. The API also permits changing or removing
subroutine calls from the application program. Run-time code changes are
useful to support a variety of applications including debugging, performance
monitoring, and to support composing applications out of existing packages.
The goal of this API is to provide a machine independent interface to permit
the creation of tools and applications that use run-time code patching.

%package doc
Summary: Documentation for using the Dyninst API
Group: Documentation
%description doc
dyninst-doc contains API documentation for the Dyninst libraries.
License: LGPL-2.1-or-later

%package devel
Summary: Header files for compiling programs with Dyninst
Group: Development/System
Requires: dyninst = %{version}-%{release}
Requires: boost-devel
Requires: tbb-devel
License: LGPL-2.1-or-later AND BSD-3-Clause AND MIT
# FindTBB.cmake: presumed MIT, removed in next version of dyninst

%description devel
dyninst-devel includes the C header files that specify the Dyninst user-space
libraries and interfaces. This is required for rebuilding any program
that uses Dyninst.

%package testsuite
Summary: Programs for testing Dyninst
Group: Development/System
Requires: dyninst = %{version}-%{release}
Requires: dyninst-devel = %{version}-%{release}
License: BSD-3-Clause AND LGPL-2.1-or-later


%description testsuite
dyninst-testsuite includes the test harness and target programs for
making sure that dyninst works properly.

%prep
%setup -q -n %{name}-%{version} -c
%setup -q -T -D -a 1

pushd %{dyninst_base}
%patch -P1 -p1 -b .dwerr
%patch -P2 -p1 -b .onetbb
%patch -P3 -p1 -b .cmake3.27
popd

# cotire seems to cause non-deterministic gcc errors
# https://bugzilla.redhat.com/show_bug.cgi?id=1420551
sed -i.cotire -e 's/USE_COTIRE true/USE_COTIRE false/' \
  %{dyninst_base}/cmake/shared.cmake

%build

cd %{dyninst_base}

CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
%ifarch %{ix86}
    CFLAGS="$CFLAGS -fno-lto -march=i686"
    LDFLAGS="$LDFLAGS -fno-lto"
%endif    
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS LDFLAGS

%cmake \
 -DENABLE_DEBUGINFOD=1 \
 -DINSTALL_LIB_DIR:PATH=%{_libdir}/dyninst \
 -DINSTALL_INCLUDE_DIR:PATH=%{_includedir}/dyninst \
 -DINSTALL_CMAKE_DIR:PATH=%{_libdir}/cmake/Dyninst \
 -DCMAKE_BUILD_TYPE=None \
 -DCMAKE_SKIP_RPATH:BOOL=YES
%cmake_build

# Hack to install dyninst nearby, so the testsuite can use it
DESTDIR="../install" %__cmake --install "%{__cmake_builddir}"
find ../install -name '*.cmake' -execdir \
     sed -i -e "s!%{_prefix}!$PWD/../install&!" '{}' '+'
# cmake mistakenly looks for libtbb.so in the dyninst install dir
sed -i '/libtbb.so/ s/".*usr/"\/usr/' $PWD/../install%{_libdir}/cmake/Dyninst/commonTargets.cmake

cd ../%{testsuite_base}
# testsuite build sometimes encounters dependency issues with -jN
%define _smp_mflags -j1
%cmake \
 -DDyninst_DIR:PATH=$PWD/../install%{_libdir}/cmake/Dyninst \
 -DINSTALL_DIR:PATH=%{_libdir}/dyninst/testsuite \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_SKIP_RPATH:BOOL=YES
%cmake_build

%install

cd %{dyninst_base}
%cmake_install

cd ../%{testsuite_base}
%cmake_install

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/dyninst" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Ugly hack to mask testsuite files from debuginfo extraction.  Running the
# testsuite requires debuginfo, so extraction is useless.  However, debuginfo
# extraction is still nice for the main libraries, so we don't want to disable
# it package-wide.  The permissions are restored by attr(755,-,-) in files.
find %{buildroot}%{_libdir}/dyninst/testsuite/ \
  -type f '!' -name '*.a' -execdir chmod 644 '{}' '+'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/dyninst
%{_libdir}/dyninst/*.so.*
# dyninst mutators dlopen the runtime library
%{_libdir}/dyninst/libdyninstAPI_RT.so
%{_libdir}/dyninst/libdyninstAPI_RT.a

%doc %{dyninst_base}/COPYRIGHT
%doc %{dyninst_base}/LICENSE.md

%config(noreplace) /etc/ld.so.conf.d/*

%files doc
%doc %{dyninst_base}/dataflowAPI/doc/dataflowAPI.pdf
%doc %{dyninst_base}/dynC_API/doc/dynC_API.pdf
%doc %{dyninst_base}/dyninstAPI/doc/dyninstAPI.pdf
%doc %{dyninst_base}/instructionAPI/doc/instructionAPI.pdf
%doc %{dyninst_base}/parseAPI/doc/parseAPI.pdf
%doc %{dyninst_base}/patchAPI/doc/patchAPI.pdf
%doc %{dyninst_base}/proccontrol/doc/proccontrol.pdf
%doc %{dyninst_base}/stackwalk/doc/stackwalk.pdf
%doc %{dyninst_base}/symtabAPI/doc/symtabAPI.pdf

%files devel
%{_includedir}/dyninst
%{_libdir}/dyninst/*.so
%{_libdir}/cmake/Dyninst

%files testsuite
%{_bindir}/parseThat
%dir %{_libdir}/dyninst/testsuite/
%attr(755,root,root) %{_libdir}/dyninst/testsuite/*[!a]
%attr(644,root,root) %{_libdir}/dyninst/testsuite/*.a

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 12.3.0-4
- Rebuilt for Boost 1.83

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Frank Ch. Eigler <fche@redhat.com> - 12.3.0-2
- side-tag respin

* Tue Jul 04 2023 Frank Ch. Eigler <fche@redhat.com> - 12.3.0-1
- migrated to SPDX license

* Tue Jul 04 2023 Orion Poplawski <orion@nwra.com> - 12.3.0-1
- Update to 12.3.0
- Add patch for cmake 3.27 support

* Tue Jun 27 2023 Jonathan Wakely <jwakely@fedoraproject.org> - 12.2.0-5
- Patch for oneTBB (#2036372)

* Thu Feb 23 2023 Frank Ch. Eigler <fche@redhat.com> - 12.2.0-4
- rhbz2173030: ftbfs with gcc 13

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 12.2.0-3
- Rebuilt for Boost 1.81

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 4 2022 William Cohen <wcohen@redhat.com> - 12.2.0-1
- Update to 12.2.0

* Wed Aug 03 2022 Stan Cox <scox@redhat.com> - 12.1.0-4
- Explicitly include time.h as <string> no longer pulls it in

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 12.1.0-2
- Rebuilt for Boost 1.78

* Thu Mar 10 2022 William Cohen <wcohen@redhat.com> - 12.1.0-1
- Update to 12.1.0

* Sat Mar 05 2022 Orion Poplawski <orion@nwra.com> - 12.0.1-4
- Fix cmake build dir

* Mon Feb 07 2022 Stan Cox <scox@redhat.com> - 12.0.1-3
- Quiesce dwarf 5 warnings

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Stan Cox <scox@redhat.com> - 12.0.1-1
- Update to 12.0.1

* Tue Nov 09 2021 Stan Cox <scox@redhat.com> - 11.0.1-4
- Do not create reloc for aarch64 static calls

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 11.0.1-3
- Rebuilt for Boost 1.76

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Stan Cox <scox@redhat.com> - 11.0.1
- Update to 11.0.1

* Fri Apr 30 2021 Stan Cox <scox@redhat.com> - 11.0.0
- Update to 11.0.0

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 10.2.1-6
- Rebuilt for removed libstdc++ symbol (#1937698)

* Fri Jan 29 2021 Frank Ch. Eigler <fche@redhat.com> - 10.2.1-5
- Rebuilt for Boost 1.75 for sure, via buildrequire version constraints

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 10.2.1-3
- Rebuilt for Boost 1.75

* Tue Nov 10 2020 Stan Cox <scox@redhat.com> - 10.2.1-2
- Enable debuginfod

* Wed Oct 28 2020 Stan Cox <scox@redhat.com> - 10.2.1-1
- Update to 10.2.1

* Tue Oct 27 2020 Jeff Law <law@redhat.com> - 10.2.0-2
- Fix C++17 issue caught by gcc-11

* Tue Sep 01 2020 Stan Cox <scox@redhat.com> - 10.2.0-1
- Update to 10.2.0

* Mon Aug 10 2020 Orion Poplawski <orion@nwra.com> - 10.1.0-10
- Use new cmake macros (FTBFS bz#1863463)
- Add BR tex-latex for doc build

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Stan Cox <scox@redhat.com> - 10.1.0-7
- Do not build static versions of the dyninst libraries.

* Fri May 29 2020 Jonathan Wakely <jwakely@redhat.com> - 10.1.0-6
- Rebuilt for Boost 1.73

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Stan Cox <scox@redhat.com> - 10.1.0-4
- Fix rhbz963475 dyninst must be ported to aarch64 

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Stan Cox <scox@redhat.com> - 10.1.0-2
- Use PRIx64 to fix i386 build

* Wed May 29 2019 Stan Cox <scox@redhat.com> - 10.1.0-1
- Update to 10.1.0

* Mon Feb 4  2019 William Cohen <wcohen@redhat.com> - 10.0.0-7
- Fix FTBFS due to move to boost 1.69 and tribool changes.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 10.0.0-5
- Append curdir to CMake invokation. (#1668512)

* Wed Dec 05 2018 Stan Cox <scox@redhat.com> - 10.0.0-4
- Use PRIx64

* Wed Dec 05 2018 Stan Cox <scox@redhat.com> - 10.0.0-3
- Patch Result.h for i386.

* Mon Dec 03 2018 Frank Ch. Eigler <fche@redhat.com> - 10.0.0-2
- Add tbb-devel Requires:
- Add ppc64le into ExclusiveArch:

* Tue Nov 13 2018 Stan Cox <scox@redhat.com> - 10.0.0-1
- Update to 10.0.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 9.3.2-11
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Than Ngo <than@redhat.com> - - 9.3.2-10
- fix FTBS with gcc8
- fix for using libtirpc, Sun RPC Interfaces is removed in latest glibc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Stan Cox <scox@redhat.com> - 9.3.2-8
- Rebuild for Boost 1.64

* Wed Oct 04 2017 Stan Cox <scox@redhat.com> - 9.3.2-7
- Fix swbz22248, handle R_*_IRELATIV, swbz22004, ignore linux-vdso64.so.1

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 9.3.2-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 9.3.2-3
- Rebuilt for Boost 1.64

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 9.3.2-2
- Rebuild due to bug in RPM (RHBZ #1468476)

* Wed Jul 05 2017 Stan Cox <scox@redhat.com> - 9.3.2-1
- Update to 9.3.2

* Mon Mar 06 2017 Stan Cox <scox@redhat.com> - 9.3.1-1
- Update to 9.3.1

* Wed Feb 8 2017 William Cohen <wcohen@redhat.com> - 9.3.0-2
- Rebuild for boost 1.63

* Mon Jan 09 2017 Josh Stone <jistone@redhat.com> - 9.3.0-1
- Update to 9.3.0

* Tue Nov 22 2016 Josh Stone <jistone@redhat.com> - 9.2.0-5
- Backport fixes for rhbz1373197, attach thread races.

* Wed Sep 14 2016 Josh Stone <jistone@redhat.com> - 9.2.0-4
- Fix rhbz1373239, process attach without exe specified.

* Mon Aug 15 2016 Josh Stone <jistone@redhat.com> - 9.2.0-3
- Revert aarch64 and ppc64le support until they're more complete.

* Fri Aug 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 9.2.0-2
- aarch64 and ppc64le are now supported

* Thu Jun 30 2016 Josh Stone <jistone@redhat.com> - 9.2.0-1
- Update to 9.2.0

* Tue Jun 21 2016 Josh Stone <jistone@redhat.com> - 9.1.0-5
- Use static TLS for libdyninstAPI_RT.so

* Thu Mar 10 2016 William Cohen <wcohen@redhat.com> - 9.1.0-4
- Export libdyninstAPI_RT_init_maxthreads (ref rhbz1315841)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Orion Poplawski <orion@cora.nwra.com> - 9.1.0-2
- Rebuild for boost 1.60

* Fri Dec 18 2015 Josh Stone <jistone@redhat.com> - 9.1.0-1
- Update to 9.1.0

* Fri Sep 04 2015 Josh Stone <jistone@redhat.com> - 9.0.3-1
- Update to 9.0.3

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 8.2.1-9
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Thu Jul 23 2015 Josh Stone <jistone@redhat.com> - 8.2.1-7
- Patch use of boost::bind for boost 1.58.

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 8.2.1-6
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Frank Ch. Eigler <fche@redhat.com> - 8.2.1-4
- Rebuild with gcc 5.0.1 for abitag-equipped cxx11 symbols.

* Sat Feb 14 2015 Frank Ch. Eigler <fche@redhat.com> - 8.2.1-3
- Rebuild with gcc 5 for std::__cxx11::basic_string etc. ABI

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 8.2.1-2
- Rebuild for boost 1.57.0

* Fri Oct 31 2014 Josh Stone <jistone@redhat.com> - 8.2.1-1
- Update to point release 8.2.1.

* Wed Aug 20 2014 Josh Stone <jistone@redhat.com> - 8.2.0-1
- rebase to 8.2.0, using upstream tag "v8.2.0.1"

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Josh Stone <jistone@redhat.com> - 8.1.2-10
- Flip from ExcludeArch to ExclusiveArch (ref rhbz1113991)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 8.1.2-8
- Rebuild for boost 1.55.0

* Thu May 22 2014 Josh Stone <jistone@redhat.com> - 8.1.2-7
- Rebuild for libdwarf.so.1

* Wed Dec 11 2013 Josh Stone <jistone@redhat.com> 8.1.2-6
- Fix rhbz1040715 (testsuite g++ optimization)

* Tue Dec 03 2013 Josh Stone <jistone@redhat.com> 8.1.2-5
- Fix rhbz1037048 (-Werror=format-security FTBFS)

* Mon Aug 05 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-4
- Fix rhbz991889 (FTBFS).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 8.1.2-2
- Rebuild for boost 1.54.0

* Tue Jun 18 2013 Josh Stone <jistone@redhat.com> 8.1.2-1
- Update to release 8.1.2.

* Fri Mar 15 2013 Josh Stone <jistone@redhat.com> 8.1.1-1
- Update to release 8.1.1.
- Drop the backported dyninst-test2_4-kill-init.patch.
- Drop the now-upstreamed dyninst-unused_vars.patch.
- Update other patches for context.
- Patch the installed symlinks to be relative, not $(DEST) filled.

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-7
- testsuite: Require dyninst-devel for the libdyninstAPI_RT.so symlink

* Tue Feb 26 2013 Josh Stone <jistone@redhat.com> 8.0-6
- Fix the testsuite path to include libtestlaunch.so

* Mon Feb 25 2013 Josh Stone <jistone@redhat.com> 8.0-5
- Add a dyninst-testsuite package.
- Patch test2_4 to protect against running as root.
- Make dyninst-static require dyninst-devel.

* Thu Feb 14 2013 Josh Stone <jistone@redhat.com> 8.0-4
- Patch make.config to ensure rpm build flags are not discarded.

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 8.0-2
- Rebuild for Boost-1.53.0

* Tue Nov 20 2012 Josh Stone <jistone@redhat.com>
- Tweak the configure/make commands
- Disable the testsuite via configure.
- Set the private includedir and libdir via configure.
- Set VERBOSE_COMPILATION for make.
- Use DESTDIR for make install.

* Mon Nov 19 2012 Josh Stone <jistone@redhat.com> 8.0-1
- Update to release 8.0.
- Updated "files doc" to reflect renames.
- Drop the unused BuildRequires libxml2-devel.
- Drop the 7.99.x version-munging patch.

* Fri Nov 09 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.29
- Rebase to git e99d7070bbc39c76d6d528db530046c22681c17e

* Mon Oct 29 2012 Josh Stone <jistone@redhat.com> 7.99.2-0.28
- Bump to 7.99.2 per abi-compliance-checker results

* Fri Oct 26 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.27
- Rebase to git dd8f40b7b4742ad97098613876efeef46d3d9e65
- Use _smp_mflags to enable building in parallel.

* Wed Oct 03 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.26
- Rebase to git 557599ad7417610f179720ad88366c32a0557127

* Thu Sep 20 2012 Josh Stone <jistone@redhat.com> 7.99.1-0.25
- Rebase on newer git tree.
- Bump the fake version to 7.99.1 to account for ABI differences.
- Enforce the minimum libdwarf version.
- Drop the upstreamed R_PPC_NUM patch.

* Wed Aug 15 2012 Karsten Hopp <karsten@redhat.com> 7.99-0.24
- check if R_PPC_NUM is defined before using it, similar to R_PPC64_NUM

* Mon Jul 30 2012 Josh Stone <jistone@redhat.com> 7.99-0.23
- Rebase on newer git tree.
- Update license files with upstream additions.
- Split documentation into -doc subpackage.
- Claim ownership of {_libdir}/dyninst.

* Fri Jul 27 2012 William Cohen <wcohen@redhat.com> - 7.99-0.22
- Correct requires for dyninst-devel.

* Wed Jul 25 2012 Josh Stone <jistone@redhat.com> - 7.99-0.21
- Rebase on newer git tree
- Update context in dyninst-git.patch
- Drop dyninst-delete_array.patch
- Drop dyninst-common-makefile.patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.99-0.20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 William Cohen <wcohen@redhat.com> - 7.99-0.19
- Patch common/i386-unknown-linux2.4/Makefile to build.

* Fri Jul 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.18
- Rebase on newer git tree the has a number of merges into it.
- Adjust spec file to allow direct use of git patches
- Fix to eliminate unused varables.
- Proper delete for array.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.17
- Rebase on newer git repo.

* Thu Jun 28 2012 William Cohen <wcohen@redhat.com> - 7.99-0.16
- Eliminate dynptr.h file use with rebase on newer git repo.

* Mon Jun 25 2012 William Cohen <wcohen@redhat.com> - 7.99-0.14
- Rebase on newer git repo.

* Tue Jun 19 2012 William Cohen <wcohen@redhat.com> - 7.99-0.12
- Fix static library and header file permissions.
- Use sources from the dyninst git repositories.
- Fix 32-bit library versioning for libdyninstAPI_RT_m32.so.

* Wed Jun 13 2012 William Cohen <wcohen@redhat.com> - 7.99-0.11
- Fix library versioning.
- Move .so links to dyninst-devel.
- Remove unneded clean section.

* Fri May 11 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.9
- Clean up Makefile rules.

* Sat May 5 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.8
- Clean up spec file.

* Wed May 2 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.7
- Use "make install" and do staged build.
- Use rpm configure macro.

* Thu Mar 15 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.5
- Nuke the bundled boost files and use the boost-devel rpm instead.

* Mon Mar 12 2012 William Cohen <wcohen@redhat.com> - 7.0.1-0.4
- Initial submission of dyninst spec file.
