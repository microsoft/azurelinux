%bcond_with bundled_libpfm
# rdma is not available
%ifarch %{arm}
%{!?with_rdma: %global with_rdma 0}
%else
%{!?with_rdma: %global with_rdma 1}
%endif
Summary: Performance Application Programming Interface
Name: papi
Version: 5.7.0
Release: 5%{?dist}
License: BSD
Requires: papi-libs = %{version}-%{release}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://icl.cs.utk.edu/papi/
Source0: https://icl.cs.utk.edu/projects/papi/downloads/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: doxygen
BuildRequires: ncurses-devel
BuildRequires: gcc-gfortran
BuildRequires: kernel-headers >= 2.6.32
BuildRequires: chrpath
BuildRequires: lm_sensors-devel
%if %{without bundled_libpfm}
BuildRequires: libpfm-devel >= 4.6.0-1
BuildRequires: libpfm-static >= 4.6.0-1
%endif
# Following required for net component
BuildRequires: net-tools
%if  %{with_rdma}
# Following required for inifiband component
BuildRequires: rdma-core-devel
%endif
BuildRequires: perl-generators
#Right now libpfm does not know anything about s390 and will fail
ExcludeArch: s390 s390x

%description
PAPI provides a programmer interface to monitor the performance of
running programs.

%package libs
Summary: Libraries for PAPI clients
%description libs
This package contains the run-time libraries for any application that wishes
to use PAPI.

%package devel
Summary: Header files for the compiling programs with PAPI
Requires: papi = %{version}-%{release}
Requires: papi-libs = %{version}-%{release}
Requires: pkgconfig
%description devel
PAPI-devel includes the C header files that specify the PAPI user-space
libraries and interfaces. This is required for rebuilding any program
that uses PAPI.

%package testsuite
Summary: Set of tests for checking PAPI functionality
Requires: papi = %{version}-%{release}
Requires: papi-libs = %{version}-%{release}
%description testsuite
PAPI-testsuite includes compiled versions of papi tests to ensure
that PAPI functions on particular hardware.

%package static
Summary: Static libraries for the compiling programs with PAPI
Requires: papi = %{version}-%{release}
%description static
PAPI-static includes the static versions of the library files for
the PAPI user-space libraries and interfaces.

%prep
%setup -q

%build
%if %{without bundled_libpfm}
# Build our own copy of libpfm.
%global libpfm_config --with-pfm-incdir=%{_includedir} --with-pfm-libdir=%{_libdir}
%endif

cd src
autoconf
%configure --with-perf-events \
%{?libpfm_config} \
--with-static-lib=yes --with-shared-lib=yes --with-shlib --with-shlib-tools \
--with-components="appio coretemp example infiniband lmsensors lustre micpower mx net rapl stealtime"
# implicit enabled components: perf_event perf_event_uncore
#components currently left out because of build configure/build issues
# --with-components="bgpm coretemp_freebsd cuda host_micpower nvml vmware"

pushd components
#pushd cuda; ./configure; popd
#pushd host_micpower; ./configure; popd
%if  %{with_rdma}
pushd infiniband_umad; %configure; popd
%endif
pushd lmsensors; \
 %configure --with-sensors_incdir=/usr/include/sensors \
 --with-sensors_libdir=%{_libdir}; \
 popd
#pushd vmware; ./configure; popd
popd

#DBG workaround to make sure libpfm just uses the normal CFLAGS
DBG="" make %{?_smp_mflags}

#generate updated versions of the documentation
#DBG workaround to make sure libpfm just uses the normal CFLAGS
pushd ../doc
DBG="" make
DBG="" make install
popd

%install
rm -rf $RPM_BUILD_ROOT
cd src
make DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true install-all

chrpath --delete $RPM_BUILD_ROOT%{_libdir}/*.so*

%files
%{_bindir}/*
%dir /usr/share/papi
/usr/share/papi/papi_events.csv
%doc INSTALL.txt README LICENSE.txt RELEASENOTES.txt
%doc %{_mandir}/man1/*

%ldconfig_scriptlets libs

%files libs
%{_libdir}/*.so.*
%doc INSTALL.txt README LICENSE.txt RELEASENOTES.txt

%files devel
%{_includedir}/*.h
%if %{with bundled_libpfm}
%{_includedir}/perfmon/*.h
%endif
%{_libdir}/*.so
%{_libdir}/pkgconfig/papi*.pc
%doc %{_mandir}/man3/*

%files testsuite
/usr/share/papi/run_tests*
/usr/share/papi/ctests
/usr/share/papi/ftests
/usr/share/papi/validation_tests
/usr/share/papi/components
/usr/share/papi/testlib

%files static
%{_libdir}/*.a

%changelog
* Tue Mar 23 2021 Henry Li <lihl@microsoft.com> - 5.7.0-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove infiniband-diags-devel from build requirement since it's already obsoleted
  by rdma-core-devel from CBL-Mariner. 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 William Cohen <wcohen@redhat.com> - 5.7.0-2
- Rebase to official papi-5.7.0.

* Mon Feb 18 2019 William Cohen <wcohen@redhat.com> - 5.7.0-1
- Rebase to papi-5.7.0.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 7 2019 William Cohen <wcohen@redhat.com> - 5.6.0-9
- Correct typo in papi-testsuite description.
- Add papi-libs for papi-testsuite and papi-devel.

* Fri Nov 2 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-8
- Pull in patch to avoid division-by-0.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 William Cohen <wcohen@redhat.com> - 5.6.0-6
- Dynamically link utilities and tests to papi libraries.

* Mon Apr 30 2018 William Cohen <wcohen@redhat.com> - 5.6.0-5
- Include various LDFLAGS/CFLAGS.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 William Cohen <wcohen@redhat.com> - 5.6.0-3
- Bump and rebuild.

* Thu Dec 21 2017 William Cohen <wcohen@redhat.com> - 5.6.0-2
- Correct infiniband buildrequires.

* Thu Dec 21 2017 William Cohen <wcohen@redhat.com> - 5.6.0-1
- Rebase to papi-5.6.0.

* Mon Aug 28 2017 Honggang LI <honli@redhat.com> - 5.5.1-6
- Disable RDMA support on ARM32

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 2 2017 William Cohen <wcohen@redhat.com> - 5.5.1-2
- Bump version and rebuild due to new libgfortan.so version.

* Fri Nov 18 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-1
- Rebase to papi-5.5.1.

* Wed Sep 14 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-1
- Rebase to papi-5.5.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 William Cohen <wcohen@redhat.com> - 5.4.3-1
- Rebase to papi-5.4.3.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 6 2015 William Cohen <wcohen@redhat.com> - 5.4.1-2
- Make sure using libpfm-4.6.0.

* Tue Mar 3 2015 William Cohen <wcohen@redhat.com> - 5.4.1-1
- Rebase to papi-5.4.1.

* Wed Feb 11 2015 William Cohen <wcohen@redhat.com> - 5.4.0-3
- Bump version and rebuild.

* Thu Dec 18 2014 William Cohen <wcohen@redhat.com> - 5.4.0-2
- Split out papi-libs as separate subpackage. (#1172875)

* Mon Nov 17 2014 William Cohen <wcohen@redhat.com> - 5.4.0-1
- Rebase to papi-5.4.0.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 4 2014 William Cohen <wcohen@redhat.com> - 5.3.2-1
- Rebase to 5.3.2.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2.16.ga7f6159
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 17 2014 Lukas Berk <lberk@redhat.com> - 5.3.0-1.16.ga7f6159
- Automated weekly rawhide release

* Thu Jan 16 2014 William Cohen <wcohen@redhat.com> - 5.3.0-1
- Rebase to 5.3.0.

* Tue Jan 14 2014 William Cohen <wcohen@redhat.com> - 5.2.0-5
- Add presets for Intel Silvermont.

* Mon Jan 13 2014 William Cohen <wcohen@redhat.com> - 5.2.0-4
- Add presets for Haswell and Ivy Bridge.

* Wed Aug 14 2013 William Cohen <wcohen@redhat.com> - 5.2.0-2
- Enable infiniband and stealtime components.

* Wed Aug 07 2013 William Cohen <wcohen@redhat.com> - 5.2.0-1
- Rebase to 5.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 William Cohen <wcohen@redhat.com> - 5.1.1-7
- rhbz830275 - Add support for POWER8 processor to PAPI

* Mon Jul 22 2013 William Cohen <wcohen@redhat.com> - 5.1.1-6
- Add autoconf buildrequires.

* Mon Jul 22 2013 William Cohen <wcohen@redhat.com> - 5.1.1-5
- rhbz986673 - /usr/lib64/libpapi.so is unowned
- Package files in /usr/share/papi only once.
- Avoid dependency problem with parallel make of man pages.

* Fri Jul 19 2013 William Cohen <wcohen@redhat.com> - 5.1.1-4
- Correct changelog.

* Fri Jul 5 2013 William Cohen <wcohen@redhat.com> - 5.1.1-3
- Add man page corrections/updates.

* Fri Jun 28 2013 William Cohen <wcohen@redhat.com> - 5.1.1-2
- Add testsuite subpackage.

* Thu May 30 2013 William Cohen <wcohen@redhat.com> - 5.1.1-1
- Rebase to 5.1.1

* Mon Apr 15 2013 William Cohen <wcohen@redhat.com> - 5.1.0.2-2
- Fix arm FTBS rhbz 951806.

* Tue Apr 9 2013 William Cohen <wcohen@redhat.com> - 5.1.0.2-1
- Rebase to 5.1.0.2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 William Cohen <wcohen@redhat.com> - 5.0.1-5
- Add armv7 cortex a15 presets.

* Tue Dec 04 2012 William Cohen <wcohen@redhat.com> - 5.0.1-4
- Disable ldconfig on install.

* Thu Nov 08 2012 William Cohen <wcohen@redhat.com> - 5.0.1-3
- Avoid duplicated shared library.

* Wed Oct 03 2012 William Cohen <wcohen@redhat.com> - 5.0.1-2
- Make sure using compatible version of libpfm.

* Thu Sep 20 2012 William Cohen <wcohen@redhat.com> - 5.0.1-1
- Rebase to 5.0.1.

* Mon Sep 10 2012 William Cohen <wcohen@redhat.com> - 5.0.0-6
- Back port fixes for Intel Ivy Bridge event presets.

* Thu Aug 30 2012 William Cohen <wcohen@redhat.com> - 5.0.0-5
- Fixes to make papi with unbundled libpfm.

* Mon Aug 27 2012 William Cohen <wcohen@redhat.com> - 5.0.0-2
- Keep libpfm unbundled.

* Fri Aug 24 2012 William Cohen <wcohen@redhat.com> - 5.0.0-1
- Rebase to 5.0.0.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-4
- Use siginfo_t rather than struct siginfo.

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-3
- Correct build requires.

* Mon Jun 11 2012 William Cohen <wcohen@redhat.com> - 4.4.0-2
- Unbundle libpfm4 from papi.
- Correct description spellings.
- Remove unused test section.

* Fri Apr 20 2012 William Cohen <wcohen@redhat.com> - 4.4.0-1
- Rebase to 4.4.0.

* Fri Mar 9 2012 William Cohen <wcohen@redhat.com> - 4.2.1-2
- Fix overrun in lmsensor component. (rhbz797692)

* Tue Feb 14 2012 William Cohen <wcohen@redhat.com> - 4.2.1-1
- Rebase to 4.2.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 02 2011 William Cohen <wcohen@redhat.com> - 4.2.0-3
- Remove unwanted man1/*.c.1 files. (rhbz749725)

* Mon Oct 31 2011 William Cohen <wcohen@redhat.com> - 4.2.0-2
- Include appropirate man pages with papi rpm. (rhbz749725)
- Rebase to papi-4.2.0, fixup for coretemp component. (rhbz746851)

* Thu Oct 27 2011 William Cohen <wcohen@redhat.com> - 4.2.0-1
- Rebase to papi-4.2.0.

* Fri Aug 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-3
- Provide papi-static.

* Thu May 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-2
- Use corrected papi-4.1.3.

* Thu May 12 2011 William Cohen <wcohen@redhat.com> - 4.1.3-1
- Rebase to papi-4.1.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 William Cohen <wcohen@redhat.com> - 4.1.2.1-1
- Rebase to papi-4.1.2.1

* Fri Oct 1 2010 William Cohen <wcohen@redhat.com> - 4.1.1-1
- Rebase to papi-4.1.1

* Tue Jun 22 2010 William Cohen <wcohen@redhat.com> - 4.1.0-1
- Rebase to papi-4.1.0

* Mon May 17 2010 William Cohen <wcohen@redhat.com> - 4.0.0-5
- Test run with upstream cvs version.

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-4
- Resolves: rhbz562935 Rebase to papi-4.0.0 (correct ExcludeArch).

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-3
- Resolves: rhbz562935 Rebase to papi-4.0.0 (bump nvr).

* Wed Feb 10 2010 William Cohen <wcohen@redhat.com> - 4.0.0-2
- correct the ctests/shlib test
- have PAPI_set_multiplex() return proper value
- properly handle event unit masks
- correct PAPI_name_to_code() to match events
- Resolves: rhbz562935 Rebase to papi-4.0.0 

* Wed Jan 13 2010 William Cohen <wcohen@redhat.com> - 4.0.0-1
- Generate papi.spec file for papi-4.0.0.
