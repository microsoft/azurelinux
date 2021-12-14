Vendor:         Microsoft Corporation
Distribution:   Mariner
%global gitfullver e0580929f451e685d92cd10d80b76f39e9b09a97
%global gitver %(c=%{gitfullver}; echo ${c:0:6})
%global _hardened_build 1
%global testsuite_ver a7f6e1
%global clknetsim_ver 79ffe4

Name:		linuxptp
Version:	2.0
Release:	8%{?dist}
Summary:	PTP implementation for Linux

License:	GPLv2+
URL:		http://linuxptp.sourceforge.net/

#Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tgz
Source0:	https://github.com/richardcochran/%{name}/archive/%{gitver}/%{name}-%{gitver}.tar.gz
Source1:	phc2sys.service
Source2:	ptp4l.service
Source3:	timemaster.service
Source4:	timemaster.conf
# external test suite
Source10:	https://github.com/mlichvar/linuxptp-testsuite/archive/%{testsuite_ver}/linuxptp-testsuite-%{testsuite_ver}.tar.gz
# simulator for test suite
Source11:	https://github.com/mlichvar/clknetsim/archive/%{clknetsim_ver}/clknetsim-%{clknetsim_ver}.tar.gz

BuildRequires:	gcc gcc-c++ systemd
BuildRequires:	net-snmp-devel

%{?systemd_requires}

%description
This software is an implementation of the Precision Time Protocol (PTP)
according to IEEE standard 1588 for Linux. The dual design goals are to provide
a robust implementation of the standard and to use the most relevant and modern
Application Programming Interfaces (API) offered by the Linux kernel.
Supporting legacy APIs and other platforms is not a goal.

%prep
%setup -q -a 10 -a 11 -n %{name}-%{!?gitfullver:%{version}}%{?gitfullver}
mv linuxptp-testsuite-%{testsuite_ver}* testsuite
mv clknetsim-%{clknetsim_ver}* testsuite/clknetsim

%build
make %{?_smp_mflags} \
	EXTRA_CFLAGS="$RPM_OPT_FLAGS" \
	EXTRA_LDFLAGS="$RPM_LD_FLAGS"

%install
%makeinstall

mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig,%{_unitdir},%{_mandir}/man5}
install -m 644 -p configs/default.cfg $RPM_BUILD_ROOT%{_sysconfdir}/ptp4l.conf
install -m 644 -p %{SOURCE1} %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}

echo 'OPTIONS="-f /etc/ptp4l.conf -i eth0"' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ptp4l
echo 'OPTIONS="-a -r"' > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/phc2sys

echo '.so man8/ptp4l.8' > $RPM_BUILD_ROOT%{_mandir}/man5/ptp4l.conf.5
echo '.so man8/timemaster.8' > $RPM_BUILD_ROOT%{_mandir}/man5/timemaster.conf.5

%check
cd testsuite
# set random seed to get deterministic results
export CLKNETSIM_RANDOM_SEED=26743
make %{?_smp_mflags} -C clknetsim
PATH=..:$PATH ./run

%post
%systemd_post phc2sys.service ptp4l.service timemaster.service

%preun
%systemd_preun phc2sys.service ptp4l.service timemaster.service

%postun
%systemd_postun_with_restart phc2sys.service ptp4l.service timemaster.service

%files
%doc COPYING README.org configs
%config(noreplace) %{_sysconfdir}/ptp4l.conf
%config(noreplace) %{_sysconfdir}/sysconfig/phc2sys
%config(noreplace) %{_sysconfdir}/sysconfig/ptp4l
%config(noreplace) %{_sysconfdir}/timemaster.conf
%{_unitdir}/phc2sys.service
%{_unitdir}/ptp4l.service
%{_unitdir}/timemaster.service
%{_sbindir}/hwstamp_ctl
%{_sbindir}/nsm
%{_sbindir}/phc2sys
%{_sbindir}/phc_ctl
%{_sbindir}/pmc
%{_sbindir}/ptp4l
%{_sbindir}/snmp4lptp
%{_sbindir}/timemaster
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Feb 03 2020 Miroslav Lichvar <mlichvar@redhat.com> 2.0-7.20191225gite05809
- update to 20191225gite05809
- fix testing with new glibc

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-6.20190912git48e605
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 25 2019 Miroslav Lichvar <mlichvar@redhat.com> 2.0-5.20190912git48e605
- update to 20190912git48e605

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Miroslav Lichvar <mlichvar@redhat.com> 2.0-2
- start ptp4l, timemaster and phc2sys after network-online target
- fix building with new kernel headers

* Mon Aug 13 2018 Miroslav Lichvar <mlichvar@redhat.com> 2.0-1
- update to 2.0

* Thu Aug 09 2018 Miroslav Lichvar <mlichvar@redhat.com> 2.0-0.1.20180805gita27407
- update to 20180805gita27407

* Mon Jul 16 2018 Miroslav Lichvar <mlichvar@redhat.com> 1.9.2-3
- add gcc and gcc-c++ to build requirements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Miroslav Lichvar <mlichvar@redhat.com> 1.9.2-1
- update to 1.9.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-7.20180101git303b08
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Miroslav Lichvar <mlichvar@redhat.com> 1.8-6.20180101git303b08
- use macro for systemd scriptlet dependencies

* Thu Jan 11 2018 Miroslav Lichvar <mlichvar@redhat.com> 1.8-5.20180101git303b08
- update to 20180101git303b08

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Miroslav Lichvar <mlichvar@redhat.com> 1.8-1
- update to 1.8

* Fri Jul 22 2016 Miroslav Lichvar <mlichvar@redhat.com> 1.7-1
- update to 1.7
- add delay option to default timemaster.conf

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Miroslav Lichvar <mlichvar@redhat.com> 1.6-1
- update to 1.6
- set random seed in testing to get deterministic results
- remove trailing whitespace in default timemaster.conf

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Miroslav Lichvar <mlichvar@redhat.com> 1.5-1
- update to 1.5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.4-1
- update to 1.4
- replace hardening build flags with _hardened_build
- include test suite

* Fri Aug 02 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.3-1
- update to 1.3

* Tue Jul 30 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.2-3.20130730git7789f0
- update to 20130730git7789f0

* Fri Jul 19 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.2-2.20130719git46db40
- update to 20130719git46db40
- drop old systemd scriptlets
- add man page link for ptp4l.conf

* Mon Apr 22 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.2-1
- update to 1.2

* Mon Feb 18 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.1-1
- update to 1.1
- log phc2sys output

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.0-1
- update to 1.0

* Fri Nov 09 2012 Miroslav Lichvar <mlichvar@redhat.com> 0-0.3.20121109git4e8107
- update to 20121109git4e8107
- install unchanged default.cfg as ptp4l.conf
- drop conflicts from phc2sys service

* Fri Sep 21 2012 Miroslav Lichvar <mlichvar@redhat.com> 0-0.2.20120920git6ce135
- fix issues found in package review (#859193)

* Thu Sep 20 2012 Miroslav Lichvar <mlichvar@redhat.com> 0-0.1.20120920git6ce135
- initial release
