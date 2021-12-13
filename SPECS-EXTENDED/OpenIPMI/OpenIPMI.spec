Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

Summary: IPMI (Intelligent Platform Management Interface) library and tools
Name: OpenIPMI

Version:    2.0.31
Release:    2%{?dist}
License:    LGPLv2+ and GPLv2+ or BSD
URL:        http://sourceforge.net/projects/openipmi/
Source:     http://downloads.sourceforge.net/openipmi/%{name}-%{version}.tar.gz
Source1:    openipmi.sysconf
Source2:    openipmi-helper
Source3:    ipmi.service
Patch1:     0001-man.patch

BuildRequires: make
BuildRequires:    gdbm-devel swig glib2-devel net-snmp-devel ncurses-devel
BuildRequires:    openssl-devel python3-devel perl-devel perl-generators
BuildRequires:    pkgconfig
BuildRequires:    readline-devel
BuildRequires:    automake
BuildRequires:    autoconf
BuildRequires:    libtool
%{?systemd_requires}
BuildRequires:    systemd

Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

# Prevent bogus provides of private libs from perl
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^%{perl_vendorarch}/auto/.*\\.so$

%description
The Open IPMI project aims to develop an open code base to allow access to
platform information using Intelligent Platform Management Interface (IPMI).
This package contains the tools of the OpenIPMI project.

%package libs
Summary: The OpenIPMI runtime libraries

%description libs
The OpenIPMI-libs package contains the runtime libraries for shared binaries
and applications.

%package perl
Summary:  IPMI Perl language bindings
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description perl
The OpenIPMI-perl package contains the Perl language bindings for OpenIPMI.

%package -n python3-openipmi
%{?python_provide:%python_provide python3-openipmi}
%{?python_provide:%python_provide python3-OpenIPMI}
# Remove before F30
Provides:  %{name}-python = %{version}-%{release}
Provides:  %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python2 < %{version}-%{release}
Summary:   IPMI Python language bindings
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}

%description -n python3-openipmi
The OpenIPMI-python package contains the Python language bindings for OpenIPMI.

%package devel
Summary:  The development environment for the OpenIPMI project
Requires: pkgconfig
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The OpenIPMI-devel package contains the development libraries and header files
of the OpenIPMI project.

%package lanserv
Summary:  Emulates an IPMI network listener
Requires: %{name}%{?_isa} = %{version}-%{release}

%description lanserv
This package contains a network IPMI listener.


%prep
%autosetup -p1

%build

%configure \
    CFLAGS="-fPIC %{optflags} -z now -fno-strict-aliasing" \
    LDFLAGS="%{__global_ldflags} -Wl,--as-needed" \
    --disable-dependency-tracking \
    --disable-static \
    --with-pythoninstall=%{python3_sitearch} \
    --with-python=%{__python3} \
    --with-tcl=no \
    --with-tkinter=no

# https://fedoraproject.org/wiki/Packaging:Guidelines?rd=Packaging/Guidelines#Beware_of_Rpath
# get rid of rpath still present in OpenIPMI-perl package
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make   # not %%{?_smp_mflags} safe

%install
make install DESTDIR=%{buildroot}

install -d %{buildroot}{%{_sysconfdir}/sysconfig,%{_unitdir},%{_libexecdir}}
install -m 644 %SOURCE1 %{buildroot}%{_sysconfdir}/sysconfig/ipmi
install -m 755 %SOURCE2 %{buildroot}%{_libexecdir}/openipmi-helper
install -m 644 %SOURCE3 %{buildroot}%{_unitdir}/ipmi.service
install -d %{buildroot}%{_sysconfdir}/modprobe.d

rm %{buildroot}/%{_mandir}/man1/openipmigui.1 %{buildroot}%{_libdir}/*.la

# add missing documentation 
echo ".so man1/openipmicmd.1" > %{buildroot}%{_mandir}/man1/ipmicmd.1

echo ".so man1/openipmish.1" > %{buildroot}%{_mandir}/man1/ipmish.1

%post
%systemd_post ipmi.service

%preun
%systemd_preun ipmi.service

%postun
%systemd_postun_with_restart ipmi.service

%ldconfig_scriptlets libs
%ldconfig_scriptlets lanserv

### A sysv => systemd migration contains all of the same scriptlets as a
### systemd package.  These are additional scriptlets

%triggerun -- OpenIPMI < 2.0.18-14
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipmi >/dev/null 2>&1 ||:
/bin/systemctl --no-reload enable ipmi.service >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del ipmi >/dev/null 2>&1 || :
/bin/systemctl try-restart ipmi.service >/dev/null 2>&1 || :

%files
%license COPYING COPYING.BSD COPYING.LIB
%doc CONFIGURING_FOR_LAN FAQ README README.Force README.MotorolaMXP
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%{_libexecdir}/openipmi-helper
%{_bindir}/ipmicmd
%{_bindir}/ipmish
%{_bindir}/ipmi_ui
%{_bindir}/openipmicmd
%{_bindir}/openipmish
%{_bindir}/rmcp_ping
%{_bindir}/solterm
%{_bindir}/openipmi_eventd
%{_unitdir}/ipmi.service
%{_mandir}/man1/ipmi_ui*
%{_mandir}/man1/openipmicmd*
%{_mandir}/man1/openipmish*
%{_mandir}/man1/rmcp_ping*
%{_mandir}/man1/solterm*
%{_mandir}/man1/ipmish*
%{_mandir}/man1/ipmicmd*
%{_mandir}/man1/openipmi_eventd*
%{_mandir}/man7/ipmi_cmdlang*
%{_mandir}/man7/openipmi_conparms*

%files perl
%attr(644,root,root) %{perl_vendorarch}/OpenIPMI.pm
%{perl_vendorarch}/auto/OpenIPMI

%files -n python3-openipmi
%{python3_sitearch}/*OpenIPMI*
%{python3_sitearch}/__pycache__/OpenIPMI.*.pyc

%files libs
%{_libdir}/libOpenIPMI*.so.*

%files devel
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files lanserv
%config(noreplace) %{_sysconfdir}/ipmi/ipmisim1.emu
%config(noreplace) %{_sysconfdir}/ipmi/lan.conf
%dir %{_sysconfdir}/ipmi
%{_bindir}/ipmilan
%{_bindir}/ipmi_sim
%{_bindir}/sdrcomp
%{_libdir}/libIPMIlanserv.so.*
%{_mandir}/man8/ipmilan.8*
%{_mandir}/man1/ipmi_sim.1*
%{_mandir}/man5/ipmi_lan.5*
%{_mandir}/man5/ipmi_sim_cmd.5*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.31-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Jan 25 2021 Josef Ridky <jridky@redhat.com> - 2.0.31-1
- New upstream release 2.0.31 (#1905768)

* Thu Sep 17 2020 Josef Řídký <jridky@redhat.com> - 2.0.29-1
- New upstream release 2.0.29 (#1846675)

* Thu Aug 27 2020 Josef Řídký <jridky@redhat.com> - 2.0.28-7
- Rebuilt for new net-snmp release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.28-5
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.28-4
- Rebuilt for Python 3.9

* Mon Feb 03 2020 Vaclav Dolezal <vdolezal@redhat.com> - 2.0.28-3
- Cleanup of openipmi-helper script; removed no-udev branch (#1579773)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Vaclav Dolezal <vdolezal@redhat.com> - 2.0.28-1
- New upstream release 2.0.28

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.27-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.27-4
- Rebuilt for Python 3.8

* Thu Aug 01 2019 Vaclav Dolezal <vdolezal@redhat.com> - 2.0.27-3
- Prevent bogus Provides of libOpenIPMI.so.0 by OpenIPMI-perl (#1734407)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Vaclav Dolezal <vdolezal@redhat.com> - 2.0.27-1
- New upstream release 2.0.27

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.25-10
- Perl 5.30 rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Josef Ridky <jridky@redhat.com> - 2.0.25-8
- Fix man page self referencing error (#1612159)

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 2.0.25-7
- Rebuild for new net-snmp

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.0.25-5
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.25-4
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.25-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Josef Ridky <jridky@redhat.com> - 2.0.25-2
- Python3 update

* Tue Apr 17 2018 Josef Ridky <jridky@redhat.com> - 2.0.25-1
- New upstream release 2.0.25 (#1568194)
- Replace Python2 with Python3
- Drop OpenIPMI-python2 and set it as Obsolete
- Introduce new OpenIPMI-python3 package

* Tue Mar 06 2018 Josef Ridky <jridky@redhat.com> - 2.0.24-5
- use ldconfig macros
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Josef Ridky <jridky@redhat.com> -2.0.14-3
- remove old systemd dependencies

* Mon Jan 22 2018 Josef Ridky <jridky@redhat.com> -2.0.14-2
- restore removed requirements

* Thu Jan 18 2018 Tomasz Kłoczko <kloczek@fedoraproject.org> - 2.0.24-1
- remove pkgconfig from devel Requires
- remove libedit Requires (it is autogenerated as SONAME dependency)
- remove main package dependecy fron devell Requires (only libs is needed
- add use %%{?_isa} macro in Requires

* Wed Jan 17 2018 Josef Ridky <jridky@redhat.com> - 2.0.24-1
- New upstream release 2.0.24
- spec update (based on Tomasz Kłoczko's pull request)
- reduce the number of SONAME dependencies by use -Wl,--as-needed in LDFLAGS
- change COPYING COPYING.BSD COPYING.LIB files as %%license
- add %%{_sysconfdir}/ipmi directory to lanserv %%files list
- execute /sbin/ldconfig in %%post and %%postun section for lanserv sub-packages
- remove desktop-file-utils and GUI related packages from BuildRequires
- use roff links instead symlinks to gzipped man pages
- use %%autosetup in %%prep
- remove Group tags

* Thu Oct 19 2017 Josef Ridky <jridky@redhat.com> - 2.0.23-6
- Rebuilt for python2 package

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.23-5
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.23-4
- Python 2 binary package renamed to python2-openipmi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Josef Ridky <jridky@redhat.com> - 2.0.23-1
- New upstream release 2.0.23 (#1461606)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.22-6
- Perl 5.26 rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Josef Ridky <jridky@redhat.com> - 2.0.22-4
- Add support for openssl-1.1.0 library (#1383995)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Boris Ranto <branto@redhat.com> - 0:2.0.22-2
- Rebuild for glibc hack

* Thu Jun 02 2016 Boris Ranto <branto@redhat.com> - 0:2.0.22-1
- New version (0:2.0.22-1)
- Apply 'OpenIPMI-2.0.18-pthread-pkgconfig.patch'
- Apply './OpenIPMI-2.0.19-man.patch'
- Apply 'OpenIPMI-2.0.21-nobundle.patch'

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.21-13
- Perl 5.24 rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 Boris Ranto <branto@redhat.com> - 2.0.21-11
- Avoid warning on update/removal (#1256798)

* Tue Nov 24 2015 Boris Ranto <branto@redhat.com> - 2.0.21-10
- Remove duplicities in filelists

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.21-8
- Perl 5.22 rebuild

* Wed Apr 22 2015 Ales Ledvinka <aledvink@redhat.com> - 2.0.21-7
- Remove modalias subpackage.

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.21-6
- Perl 5.20 rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Ledvinka Ales <aledvink@redhat.com> - 2.0.21-4
- Use system libedit instead of the old one bundled with source.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Jaromir Capik <jcapik@redhat.com> - 2.0.21-2
- Fixing FTBFS due to unpackaged files (#1075696)

* Wed Jan 29 2014 Ledvinka Ales <aledvink@redhat.com> - 2.0.21-1
- Update to new upstream (fixed case 2nd) release.

* Tue Jan 14 2014 Ledvinka Ales <aledvink@redhat.com> - 2.0.19-11
- Probe modules on installation. Do not wait until reboot.

* Wed Nov 13 2013 Ledvinka Ales <aledvink@redhat.com> - 2.0.19-10
- Correct aliases matching module strings.

* Tue Nov 05 2013 Fedora Release Engineering <aledvink@redhat.com> - 2.0.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Ledvinka Ales <aledvink@redhat.com> - 2.0.19-7
- Hint compilation to avoid strict aliasing and prevent type-punned pointer issues.
- Fix rPath regression for OpenIPMI-perl library.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.0.19-6
- Perl 5.18 rebuild

* Tue Jun  4 2013 Ledvinka Ales <aledvink@redhat.com> - 2.0.19-5
- Support aarch64 by replicating release toolchain.
- Configuration subpackage with kernel probed wildcard module aliases.
  as workaround for bz#961878 and fesco#1110
- Man pages symlinks same as bin symlinks.
- ipmi_ui command help argument.
- ipmilan missing options.
- Fixed build requirements.

* Thu Apr 25 2013 Ledvinka Ales <aledvink@redhat.com> - 2.0.19-4
- rpmdiff fixes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 27 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.19-2
- Updated RPM scriptlets with latest systemd-rpm macros (#850246)
- Fixed fedora-review tool complaints

* Wed Aug  8 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.19-1
- Update to 2.0.19

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.0.18-15
- Perl 5.16 rebuild

* Mon May  7 2012 Jan Safranek <jsafrane@redhat.com> - 2.0.18-14
- Added ipmi systemd unit

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.0.18-12
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.0.18-11
- Perl mass rebuild

* Fri Jul  8 2011 Jan Safranek <jsafrane@redhat.com> - 2.0.18-10
- Rebuilt for new Net-SNMP

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.18-9
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.18-8
- Perl 5.14 mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-6
- Removed the openipmigui tool, it does not work with TCL without thread
  support (#646184)

* Tue Oct 26 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-5
- Rebuilt for new Net-SNMP

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul  8 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-3
- added lincense files to OpenIPMI-libs subpackage as requested by
  Fedora Licensing Guidelines

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.0.18-2
- Mass rebuild with perl-5.12.0

* Wed May  5 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.18-1
- updated to OpenIPMI-2.0.18
- fixed OpenIPMIpthread pkgconfig file (#468067)

* Mon May  3 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.17-1
- updated to OpenIPMI-2.0.17

* Thu Mar 18 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-12
- implemented mandatory 'force-reload' command in ipmi service

* Thu Mar 11 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-11
- rebuild against new gdbm

* Wed Mar  3 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-10
- add README.initscript describing /etc/init.d/ipmi initscript exit codes
  (#562151)

* Mon Feb 22 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-9
- fix package License: field, there *are* sources with BSD header
- distribute README files and COPYING in package

* Tue Jan  5 2010 Jan Safranek <jsafrane@redhat.com> - 2.0.16-8
- fix package License: field, there is no source with BSD header

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.0.16-7
- rebuild against perl 5.10.1

* Tue Dec  1 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-6
- fix package compilation to remove rpmlint errors

* Wed Sep 30 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-5
- rebuilt with new net-snmp

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.16-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 15 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-2
- fix compilation flags, debuginfo package is correctly generated now

* Thu Mar 19 2009 Jan Safranek <jsafrane@redhat.com> - 2.0.16-1
- new upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.14-10
- rebuild with new openssl

* Thu Dec 11 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-9
- fix linking without rpath, prelink won't screw up the libraries
  anymore (#475265)

* Wed Dec 10 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-8
- shorter probe interval is used in init script, making the service startup
  quicker in most situations (#475101)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.14-7
- Rebuild for Python 2.6

* Thu Oct 30 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-6
- removed static libraries from the -devel subpackage
- fixed openipmigui.desktop file

* Thu Oct 23 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-5
- fixed typos in the descriptions
- added .desktop file for openipmigui tool

* Mon Oct 20 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-4
- fixed description of the package

* Thu Oct 16 2008 Jan Safranek <jsafrane@redhat.com> - 2.0.14-3
- split ipmitool to separate package
- added 'reload' functionality to init script
- added seraparate -gui subpackage

* Wed Jul 30 2008 Phil Knirsch <pknirsch@redhat.com> - 2.0.14-2
- Fixed rpath problem in libOpenIPMIposix.so.0.0.1

* Tue Jul 29 2008 Phil Knirsch <pknirsch@redhat.com> - 2.0.14-1
- Fixed several specfile problems (#453751)
- Update to OpenIPMI-2.0.14

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.13-2
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.13-1
- Updated to OpenIPMI-2.0.13
- Rebuild due to new openssl

* Wed Oct 10 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-3
- Added missing perl-devel buildrequires

* Mon Sep 24 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-2
- Added missing popt-devel buildrequires

* Fri Aug 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-2
- Fix rebuild problems due to glibc change
- License review and fixes

* Tue Apr 24 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.11-1
- Update to OpenIPMI-2.0.11

* Tue Feb 27 2007 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-8
- Update for ipmitool-1.8.9

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.0.6-7
- rebuild for python 2.5

* Tue Nov 28 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-6.fc7
- Update due to new net-snmp-5.4
- Some specfile updates

* Tue Jul 18 2006 Phil Knirsch <pknirsch@redhat.com> - 2.0.6-5
- Fixed check for udev in initscript (#197956)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.6-4.1
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com> 2.0.6-4
- don't include <linux/compiler.h>

* Fri Jun 16 2006 Jon Masters <jcm@redhat.com> 2.0.6-3
- Fix a build requires (needs glibc-kernheaders)

* Thu Jun 15 2006 Jesse Keating <jkeating@redhat.com> 2.0.6-2
- Bump for new glib2

* Tue May 16 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.6-1
- Fixed bug with type conversion in ipmitool (#191091)
- Added python bindings 
- Split off perl and python bindings in separate subpackages
- Dropped obsolete patches
- Added missing buildprereq on readline-devel
- Made it install the python bindings properly on 64bit archs

* Mon May 15 2006 Phil Knirsch <pknirsch@redhat.com>
- Updated ipmitool to 1.8.8
- Updated OpenIPMI to 2.0.6

* Fri Feb 17 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-19
- Added missing PreReq for chkconfig

* Mon Feb 13 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2.1
- rebump for build order issues during double-long bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.14-18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb 06 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-18
- Updated ipmitool to latest upstream version.
- Removed 3 patches for already fixed bugs in latest ipmitool.
- Adapted warning message fix for ipmitool for latest version.

* Tue Jan 24 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-17
- Fixed some minor things in initscripts.

* Mon Jan 09 2006 Phil Knirsch <pknirsch@redhat.com> 1.4.14-16
- Included FRU fix for displaying FRUs with ipmitool
- Included patch for new option to specify a BMC password for IPMI 2.0 sessions

* Tue Jan 03 2006 Radek Vokal <rvokal@redhat.com> 1.4.14-15
- Rebuilt against new libnetsnmp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-14
- Some more initscript and sysconfig updates from Dell.

* Wed Nov 09 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-13
- Rebuilt to link against latest openssl libs.
- Fixed ipmitool not setting session privilege level (#172312)

* Wed Nov 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-11
- Rebuild to link against new net-snmp libs.

* Tue Oct 11 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-10
- Updated initscript to fix missing redhat-lsb bug (#169901)

* Thu Sep 08 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-9
- Another update to latest initscripts from Dell
- Fixed some missing return statements for non-void functions (#164138)

* Thu Sep 01 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-8
- Updated initscript to latest version from Dell

* Fri Aug 12 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-7
- Fixed the unwanted output of failed module loading of the initscript. Behaves
  now like all our other initscripts (#165476)

* Fri Aug 05 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-6
- Fixed build problem on 64bit machines

* Fri Jul 15 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-5
- Fixed missing change to not autostart in the initscript

* Wed Jul 06 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-4
- Made the initscript a replacing configfile

* Mon Jul 04 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-3
- Updated versions of the initscripts and sysconf files
- Fixed typo in preun script and changelog

* Mon Jun 27 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.14-2
- Updated to OpenIPMI-1.4.14
- Split the main package into normal and libs package for multilib support
- Added ipmitool-1.8.2 to OpenIPMI and put it in tools package
- Added sysconf and initscript (#158270)
- Fixed oob subscripts (#149142)

* Wed Mar 30 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-5
- Correctly put libs in the proper packages

* Thu Mar 17 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-4
- gcc4 rebuild fixes
- Added missing gdbm-devel buildprereq

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.4.11-3
- bump release and rebuild with gcc 4

* Tue Feb 08 2005 Karsten Hopp <karsten@redhat.de> 1.4.11-2 
- update

* Tue Oct 26 2004 Phil Knirsch <pknirsch@redhat.com>
- Initial version
