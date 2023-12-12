Summary:        Multithreaded IO generation tool
Name:           fio
Version:        3.30
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.kernel.dk/?p=fio.git;a=summary
Source0:        https://brick.kernel.dk/snaps/%{name}-%{version}.tar.bz2
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libaio-devel
BuildRequires:  libcurl-devel
BuildRequires:  libnbd-devel
BuildRequires:  librbd1-devel
BuildRequires:  librdmacm-devel
BuildRequires:  numactl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  zlib-devel
%ifarch x86_64
BuildRequires:  libpmem-devel
BuildRequires:  libpmemblk-devel
%endif
%if %{with_check}
BuildRequires:  CUnit-devel
%endif

# Main fio package has soft dependencies on all the engine
# subpackages, but allows the engines to be uninstalled if not needed
# or if the dependencies are too onerous.
Recommends:     %{name}-engine-libaio
Recommends:     %{name}-engine-http
Recommends:     %{name}-engine-nbd
Recommends:     %{name}-engine-rados
Recommends:     %{name}-engine-rbd
Recommends:     %{name}-engine-rdma
%ifarch x86-64
Recommends:     %{name}-engine-dev-dax
Recommends:     %{name}-engine-pmemblk
Recommends:     %{name}-engine-libpmem
%endif

%description
fio is an I/O tool that will spawn a number of threads or processes doing
a particular type of io action as specified by the user.  fio takes a
number of global parameters, each inherited by the thread unless
otherwise parameters given to them overriding that setting is given.
The typical use of fio is to write a job file matching the io load
one wants to simulate.

%package engine-libaio
Summary:        Linux libaio engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-libaio
Linux libaio engine for %{name}.

%package engine-http
Summary:        HTTP engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-http
HTTP engine for %{name}.

%package engine-nbd
Summary:        Network Block Device engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-nbd
Network Block Device (NBD) engine for %{name}.

%ifarch x86_64
%package engine-dev-dax
Summary:        PMDK dev-dax engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-dev-dax
dev-dax engine for %{name}.
Read and write using device DAX to a persistent memory device
(e.g., /dev/dax0.0) through the PMDK libpmem library.
%endif

%ifarch x86_64
%package engine-pmemblk
Summary:        PMDK pmemblk engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-pmemblk
pmemblk engine for %{name}.
Read and write using filesystem DAX to a file on a filesystem mounted with
DAX on a persistent memory device through the PMDK libpmemblk library.
%endif

%ifarch x86_64
%package engine-libpmem
Summary:        PMDK pmemblk engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-libpmem
libpmem engine for %{name}.
Read and write using mmap I/O to a file on a filesystem mounted with DAX
on a persistent memory device through the PMDK libpmem library.
%endif

%package engine-rados
Summary:        Rados engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-rados
Rados engine for %{name}.

%package engine-rbd
Summary:        Rados Block Device engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-rbd
Rados Block Device (RBD) engine for %{name}.

%package engine-rdma
Summary:        RDMA engine for %{name}.
Requires:       %{name} = %{version}-%{release}

%description engine-rdma
RDMA engine for %{name}.

%prep
%autosetup -p1

%py3_shebang_fix \
 tools/fio_jsonplus_clat2csv \
 tools/fiologparser.py \
 tools/hist/*.py \
 tools/plot/fio2gnuplot \
 t/steadystate_tests.py

# Edit /usr/local/lib path in os/os-linux.h to match Mariner conventions.
sed -e 's,/usr/local/lib/,%{_libdir}/,g' -i os/os-linux.h

%build
./configure --disable-optimizations --enable-libnbd --dynamic-libengines
EXTFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" %make_build

%install
%make_install prefix=%{_prefix} mandir=%{_mandir} libdir=%{_libdir}/fio INSTALL="install -p"

%check
%make_build test

%files
%license COPYING MORAL-LICENSE
%doc README.rst REPORTING-BUGS HOWTO.rst examples
%doc GFIO-TODO SERVER-TODO STEADYSTATE-TODO
%dir %{_datadir}/%{name}
%dir %{_libdir}/fio/
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}/*

%ifarch x86_64
%files engine-dev-dax
%{_libdir}/fio/fio-dev-dax.so
%endif

%files engine-http
%{_libdir}/fio/fio-http.so

%files engine-libaio
%{_libdir}/fio/fio-libaio.so

%ifarch x86_64
%files engine-libpmem
%{_libdir}/fio/fio-libpmem.so
%endif

%files engine-nbd
%{_libdir}/fio/fio-nbd.so

%ifarch x86_64
%files engine-pmemblk
%{_libdir}/fio/fio-pmemblk.so
%endif

%files engine-rados
%{_libdir}/fio/fio-rados.so

%files engine-rbd
%{_libdir}/fio/fio-rbd.so

%files engine-rdma
%{_libdir}/fio/fio-rdma.so

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.30-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri July 15 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.30-1
- Promote to Mariner base repo
- Update to latest upstream version and remove upstreamed patches
- Remove provides filtering- fixed upstream
- Remove references to architectures Mariner does not support
- Add package test
- Lint spec

* Tue Mar 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.29-1
- Updating to version 3.29 using Fedora 36 specs (license: MIT) as guidance.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.21-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jul 28 2020 Eric Sandeen <sandeen@redhat.com> 3.21-1
- New upstream version

* Fri May 15 2020 Martin Bukatovic <mbukatov@redhat.com> 3.19-3
- Enable http engine. (#1836323)

* Thu Apr 16 2020 Eric Sandeen <sandeen@redhat.com> 3.19-2
- Bugfix update: stat: eliminate extra log samples

* Thu Mar 12 2020 Eric Sandeen <sandeen@redhat.com> 3.19-1
- New upstream version

* Thu Feb 13 2020 Eric Sandeen <sandeen@redhat.com> 3.18-1
- New upstream version
- Fix gcc10 build

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Eric Sandeen <sandeen@redhat.com> 3.17-1
- New upstream version

* Wed Nov 06 2019 Richard W.M. Jones <rjones@redhat.com> 3.16-2
- Enable Network Block Device (libnbd) engine.

* Sat Sep 21 2019 Eric Sandeen <sandeen@redhat.com> 3.16-1
- New upstream version

* Fri Aug 16 2019 Eric Sandeen <sandeen@redhat.com> 3.15-1
- New upstream version

* Thu Aug 08 2019 Eric Sandeen <sandeen@redhat.com> 3.14-3
- Make all scripts explicitly call python3 (#1738819)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Eric Sandeen <sandeen@redhat.com> 3.14-1
- New upstream version

* Thu Feb 14 2019 Eric Sandeen <sandeen@redhat.com> 3.13-1
- New upstream version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Eric Sandeen <sandeen@redhat.com> 3.12-1
- New upstream version

* Wed Aug 22 2018 Eric Sandeen <sandeen@redhat.com> 3.8-1
- New upstream version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Eric Sandeen <sandeen@redhat.com> 3.7-1
- New upstream version

* Fri Jun 01 2018 Eric Sandeen <sandeen@redhat.com> 3.6-3
- Complete the conversion to python3

* Wed May 16 2018 Eric Sandeen <sandeen@redhat.com> 3.6-2
- Make all python scripts python3 compliant and explicit

* Wed Apr 18 2018 Eric Sandeen <sandeen@redhat.com> 3.6-1
- New upstream version

* Mon Feb 26 2018 Eric Sandeen <sandeen@redhat.com> 3.4-2
- BuildRequires: gcc

* Fri Feb 16 2018 Eric Sandeen <sandeen@redhat.com> 3.4-1
- New upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 3.3-2
- Build with linker flags from redhat-rpm-config

* Wed Dec 27 2017 Eric Sandeen <sandeen@redhat.com> 3.3-1
- New upstream version

* Mon Nov 06 2017 Eric Sandeen <sandeen@redhat.com> 3.2-1
- New upstream version

* Wed Oct 25 2017 Dan Horák <dan[at]danny.cz> 3.1-3
- Add build deps for s390x

* Tue Oct 24 2017 Eric Sandeen <sandeen@redhat.com> 3.1-2
- Add new build deps for more features

* Wed Oct 18 2017 Eric Sandeen <sandeen@redhat.com> 3.1-1
- New upstream version

* Fri Aug 25 2017 Adam Williamson <awilliam@redhat.com> - 3.0-3
- Re-enable ceph deps on ppc64 (it's building again)
- Disable RDMA support on 32-bit ARM (#1484155)

* Thu Aug 17 2017 Eric Sandeen <sandeen@redhat.com> 3.0-2
- Include more files as doc (#1482372)

* Wed Aug 16 2017 Eric Sandeen <sandeen@redhat.com> 3.0-1
- New upstream version

* Mon Jul 31 2017 Eric Sandeen <sandeen@redhat.com> 2.99-3
- Exclude ceph-related deps on ppc64

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Eric Sandeen <sandeen@redhat.com> 2.99-1
- New upstream version

* Fri Jun 16 2017 Eric Sandeen <sandeen@redhat.com> 2.21-1
- New upstream version

* Wed Apr 05 2017 Eric Sandeen <sandeen@redhat.com> 2.19-2
- Enable dev-dax engine on x86_64

* Wed Apr 05 2017 Eric Sandeen <sandeen@redhat.com> 2.19-1
- New upstream version

* Thu Feb 23 2017 Eric Sandeen <sandeen@redhat.com> 2.18-1
- New upstream version

* Thu Feb 23 2017 Eric Sandeen <sandeen@redhat.com> 2.17-1
- New upstream version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Eric Sandeen <sandeen@redhat.com> 2.16-1
- New upstream version

* Sat Nov 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.15-2
- Rebuild (Power64)

* Thu Oct 27 2016 Eric Sandeen <sandeen@redhat.com> 2.15-1
- New upstream version

* Tue Oct 04 2016 Eric Sandeen <sandeen@redhat.com> 2.14-1
- New upstream version

* Mon Aug 29 2016 Eric Sandeen <sandeen@redhat.com> 2.13-1
- New upstream version

* Wed Jun 15 2016 Eric Sandeen <sandeen@redhat.com> 2.12-1
- New upstream version

* Wed May 25 2016 Eric Sandeen <sandeen@redhat.com> 2.11-1
- New upstream version

* Fri Apr 29 2016 Eric Sandeen <sandeen@redhat.com> 2.9-1
- New upstream version

* Thu Mar 17 2016 Eric Sandeen <sandeen@redhat.com> 2.8-1
- New upstream version

* Fri Mar 11 2016 Eric Sandeen <sandeen@redhat.com> 2.7-1
- New upstream version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Eric Sandeen <sandeen@redhat.com> 2.6-1
- New upstream version

* Thu Jan 14 2016 Eric Sandeen <sandeen@redhat.com> 2.3-1
- New upstream version

* Mon Dec 21 2015 Eric Sandeen <sandeen@redhat.com> 2.2.13-1
- New upstream version
- Add librdmacm-devel as build dependency (enable RDMA)

* Tue Nov 10 2015 Eric Sandeen <sandeen@redhat.com> 2.2.11-1
- New upstream version
- Add zlib-devel as build dependency

* Tue Sep 22 2015 Eric Sandeen <sandeen@redhat.com> 2.2.10-1
- New upstream version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Eric Sandeen <sandeen@redhat.com> 2.2.8-1
- New upstream version

* Wed Apr 15 2015 Eric Sandeen <sandeen@redhat.com> 2.2.7-1
- New upstream version
- Add librbd ioengine support

* Fri Apr 10 2015 Eric Sandeen <sandeen@redhat.com> 2.2.6-1
- New upstream version

* Tue Feb 17 2015 Eric Sandeen <sandeen@redhat.com> 2.2.5-1
- New upstream version

* Mon Jan 05 2015 Eric Sandeen <sandeen@redhat.com> 2.2.4-1
- New upstream version

* Fri Jan 02 2015 Eric Sandeen <sandeen@redhat.com> 2.2.3-1
- New upstream version

* Wed Nov 12 2014 Eric Sandeen <sandeen@redhat.com> 2.1.14-1
- New upstream version

* Wed Sep 17 2014 Eric Sandeen <sandeen@redhat.com> 2.1.12-1
- New upstream version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Eric Sandeen <sandeen@redhat.com> 2.1.11-1 
- New upstream version

* Mon Jun 16 2014 Eric Sandeen <sandeen@redhat.com> 2.1.10-1 
- New upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Eric Sandeen <sandeen@redhat.com> 2.1.9-1 
- New upstream version

* Mon Apr 14 2014 Eric Sandeen <sandeen@redhat.com> 2.1.8-1 
- New upstream version

* Mon Apr 07 2014 Eric Sandeen <sandeen@redhat.com> 2.1.7-1 
- New upstream version

* Wed Feb 12 2014 Eric Sandeen <sandeen@redhat.com> 2.1.5-1 
- New upstream version

* Wed Sep 25 2013 Eric Sandeen <sandeen@redhat.com> 2.1.3-1 
- New upstream version

* Thu Aug 08 2013 Eric Sandeen <sandeen@redhat.com> 2.1.2-1 
- New upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Eric Sandeen <sandeen@redhat.com> 2.1-1 
- New upstream version

* Wed Apr 17 2013 Eric Sandeen <sandeen@redhat.com> 2.0.15-1 
- New upstream version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  9 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.13-1
- New upstream 2.0.13 release

* Tue Jan 01 2013 Dan Horák <dan[at]danny.cz> - 2.0.12.2-2
- fix build on arches without ARCH_HAVE_CPU_CLOCK (arm, s390)

* Fri Dec 21 2012 Eric Sandeen <sandeen@redhat.com> 2.0.12.2-1 
- New upstream version

* Sat Nov 24 2012 Eric Sandeen <sandeen@redhat.com> 2.0.11-1 
- New upstream version

* Thu Nov 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.10-2
- Merge latest from F16 to master, bump release

* Fri Oct 12 2012 Eric Sandeen <sandeen@redhat.com> 2.0.10-1 
- New upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Eric Sandeen <sandeen@redhat.com> 2.0.8-1
- New upstream version

* Fri Mar 23 2012 Eric Sandeen <sandeen@redhat.com> 2.0.6-1
- New upstream version

* Tue Feb 28 2012 Eric Sandeen <sandeen@redhat.com> 2.0.5-1
- New upstream version

* Mon Jan 23 2012 Eric Sandeen <sandeen@redhat.com> 2.0.1-1
- New upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Eric Sandeen <sandeen@redhat.com> 2.0-1
- New upstream version

* Fri Nov 11 2011 Eric Sandeen <sandeen@redhat.com> 1.99.12-1
- New upstream version

* Tue Sep 27 2011 Eric Sandeen <sandeen@redhat.com> 1.58-1
- New upstream version

* Thu Aug 11 2011 Eric Sandeen <sandeen@redhat.com> 1.57-1
- New upstream version

* Tue May 31 2011 Eric Sandeen <sandeen@redhat.com> 1.55-1
- New upstream version

* Mon May 09 2011 Eric Sandeen <sandeen@redhat.com> 1.53-1
- New upstream version

* Fri Apr 29 2011 Eric Sandeen <sandeen@redhat.com> 1.52-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Eric Sandeen <sandeen@redhat.com> 1.50.2-1
- New upstream version

* Wed Jan 26 2011 Eric Sandeen <sandeen@redhat.com> 1.50-1
- New upstream version

* Wed Dec 15 2010 Eric Sandeen <sandeen@redhat.com> 1.44.3-1
- New upstream version

* Fri Oct 22 2010 Eric Sandeen <sandeen@redhat.com> 1.44.1-1
- New upstream version

* Fri Oct 22 2010 Eric Sandeen <sandeen@redhat.com> 1.44-1
- New upstream version

* Thu Sep 23 2010 Eric Sandeen <sandeen@redhat.com> 1.43.2-1
- New upstream version

* Tue Jun 29 2010 Eric Sandeen <sandeen@redhat.com> 1.41.5-1
- New upstream version

* Tue Jun 22 2010 Eric Sandeen <sandeen@redhat.com> 1.41.3-1
- New upstream version

* Tue Jun 22 2010 Eric Sandeen <sandeen@redhat.com> 1.41-1
- New upstream version

* Fri Jun 18 2010 Eric Sandeen <sandeen@redhat.com> 1.40-1
- New upstream version

* Thu Jun 03 2010 Eric Sandeen <sandeen@redhat.com> 1.39-1
- New upstream version

* Tue Mar 23 2010 Eric Sandeen <sandeen@redhat.com> 1.38-1
- New upstream version

* Tue Feb 23 2010 Eric Sandeen <sandeen@redhat.com> 1.37-1
- New upstream version

* Tue Dec 15 2009 Eric Sandeen <sandeen@redhat.com> 1.36-1
- New upstream version

* Thu Nov 05 2009 Eric Sandeen <sandeen@redhat.com> 1.35-1
- New upstream version

* Mon Sep 14 2009 Eric Sandeen <sandeen@redhat.com> 1.34-1
- New upstream version

* Thu Sep 10 2009 Eric Sandeen <sandeen@redhat.com> 1.33.1-1
- New upstream version

* Tue Sep 08 2009 Eric Sandeen <sandeen@redhat.com> 1.33-1
- New upstream version

* Fri Jul 31 2009 Eric Sandeen <sandeen@redhat.com> 1.32-1
- New upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Eric Sandeen <sandeen@redhat.com> 1.31-1
- Much newer upstream version

* Fri Mar 06 2009 Eric Sandeen <sandeen@redhat.com> 1.24-1
- New upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Eric Sandeen <sandeen@redhat.com> 1.23-1
- New upstream version, several bugs fixed.

* Mon Oct 13 2008 Eric Sandeen <sandeen@redhat.com> 1.22-1
- New upstream version, several bugs fixed.

* Thu Jun 19 2008 Eric Sandeen <sandeen@redhat.com> 1.21-1
- New upstream version
- Build verbosely and with RPM cflags

* Fri Apr 25 2008 Eric Sandeen <sandeen@redhat.com> 1.20-1
- New upstream version

* Thu Apr 10 2008 Eric Sandeen <sandeen@redhat.com> 1.19-1
- New upstream version

* Wed Feb 13 2008 Eric Sandeen <sandeen@redhat.com> 1.18-1
- Initial build
