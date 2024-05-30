Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:			rasdaemon
Version:		0.8.0
Release:		1%{?dist}
Summary:		Utility to receive RAS error tracings
License:		GPLv2
URL:			http://git.infradead.org/users/mchehab/rasdaemon.git
Source0:		http://www.infradead.org/~mchehab/rasdaemon/%{name}-%{version}.tar.bz2

ExcludeArch:		s390 s390x
BuildRequires:		make
BuildRequires:		gcc
BuildRequires:		autoconf automake libtool
BuildRequires:		gettext-devel
BuildRequires:		perl-generators
BuildRequires:		sqlite-devel
BuildRequires:		systemd
BuildRequires:		libtraceevent-devel
Provides:		bundled(kernel-event-lib)
Requires:		hwdata
Requires:		perl-DBD-SQLite
Requires:		libtraceevent
%ifarch %{ix86} x86_64
Requires:		dmidecode
%endif

Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
%{name} is a RAS (Reliability, Availability and Serviceability) logging tool.
It currently records memory errors, using the EDAC tracing events.
EDAC is drivers in the Linux kernel that handle detection of ECC errors
from memory controllers for most chipsets on i386 and x86_64 architectures.
EDAC drivers for other architectures like arm also exists.
This userspace component consists of an init script which makes sure
EDAC drivers and DIMM labels are loaded at system startup, as well as
an utility for reporting current error counts from the EDAC sysfs files.

%prep
%setup -q
autoreconf -vfi

%build
%ifarch %{arm} aarch64
%configure --enable-sqlite3 --enable-aer --enable-non-standard --enable-arm \
	   --enable-mce --enable-extlog --enable-devlink --enable-diskerror \
	   --enable-memory-failure --enable-abrt-report --enable-hisi-ns-decode \
	   --enable-memory-ce-pfa --enable-amp-ns-decode --enable-cpu-fault-isolation \
	   --with-sysconfdefdir=%{_sysconfdir}/sysconfig
%else
%configure --enable-sqlite3 --enable-aer \
	   --enable-mce --enable-extlog --enable-devlink --enable-diskerror \
	   --enable-memory-failure --enable-abrt-report --enable-cpu-fault-isolation \
	   --with-sysconfdefdir=%{_sysconfdir}/sysconfig
%endif
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
install -D -p -m 0644 misc/rasdaemon.service %{buildroot}%{_unitdir}/rasdaemon.service
install -D -p -m 0644 misc/ras-mc-ctl.service %{buildroot}%{_unitdir}/ras-mc-ctl.service
install -D -p -m 0655 misc/rasdaemon.env %{buildroot}%{_sysconfdir}/sysconfig/%{name}
rm INSTALL %{buildroot}/usr/include/*.h

%files
%doc AUTHORS ChangeLog COPYING README.md TODO
%{_sbindir}/rasdaemon
%{_sbindir}/ras-mc-ctl
%{_mandir}/*/*
%{_unitdir}/*.service
%{_sysconfdir}/ras/dimm_labels.d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Wed May 22 2024 Chris Co <chrco@microsoft.com> - 0.8.0-1
- Update to version 0.8.0. From Fedora 40. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.4-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Thu Oct 10 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.4-1
- Bump to version 0.6.4 with some DB changes for hip08 and some fixes

* Fri Aug 23 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.3-1
- Bump to version 0.6.3 with new ARM events, plus disk I/O and netlink support

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.2-1
- Bump to version 0.6.2 with improvements for PCIe AER parsing and at ras-mc-ctl tool

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org>  0.6.1-1
- Bump to version 0.6.1 adding support for Skylake Xeon MSCOD, a bug fix and some new DELL labels

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 14 2017 Mauro Carvalho Chehab <mchehab@osg.samsung.com>  0.6.0-1
- Bump to version 0.6.0 adding support for Arm and Hisilicon events and update Dell Skylate labels

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.8-3
- Add a virtual provide, per BZ#104132

* Fri Apr 15 2016 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.8-2
- Bump to version 0.5.8 with support for Broadwell EP/EX MSCOD/DE MSCOD

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 03 2015 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.6-1
- Bump to version 0.5.6 with support for LMCE and some fixes

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Mauro Carvalho Chehab <mchehab@osg.samsung.com> 0.5.5-1
- Bump to version 0.5.5 with support for newer Intel platforms & some fixes

* Tue Sep 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.4-3
- aarch64/ppc64 have edac capabilities
- spec cleanups
- No need to run autoreconf

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.4-1
- Bump to version 0.5.4 with some fixes, mainly for amd64

* Sun Aug 10 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.3-1
- Bump to version 0.5.3 and enable ABRT and ExtLog

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.2-1
- fix and enable ABRT report support

* Fri Mar 28 2014 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.1-1
- Do some fixes at the service files and add some documentation for --record

* Sun Feb 16 2014  Mauro Carvalho Chehab <m.chehab@samsung.com> 0.5.0-1
- Add experimental ABRT support

* Tue Sep 10 2013 Mauro Carvalho Chehab <m.chehab@samsung.com> 0.4.2-1
- Fix ras-mc-ctl layout filling

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.4.1-4
- Perl 5.18 rebuild

* Sun Jun  2 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.1-3
- ARM has EDMA drivers (currently supported in Calxeda highbank)

* Wed May 29 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.1-2
- Fix the name of perl-DBD-SQLite package

* Wed May 29 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.1-1
- Updated to version 0.4.1 with contains some bug fixes

* Tue May 28 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.4.0-1
- Updated to version 0.4.0 and added support for mce, aer and sqlite3 storage

* Mon May 20 2013 Mauro Carvalho Chehab <mchehab@redhat.com> 0.3.0-1
- Package created