Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1
%global testsuite_ver ff37e2
%global clknetsim_ver 9ed48d
%global selinuxtype targeted
%bcond_with selinux

Name:		linuxptp
Version:	3.1.1
Release:	7%{?dist}
Summary:	PTP implementation for Linux

License:	GPLv2+
URL:		http://linuxptp.sourceforge.net/

Source0:	https://sourceforge.net/projects/%{name}/files/v3.1/%{name}-%{version}.tgz
Source1:	phc2sys.service
Source2:	ptp4l.service
Source3:	timemaster.service
Source4:	timemaster.conf
Source5:	ptp4l.conf
# external test suite
Source10:	linuxptp-testsuite-%{testsuite_ver}.tar.gz
# simulator for test suite
Source11:	clknetsim-%{clknetsim_ver}.tar.gz
# selinux policy
Source20:	linuxptp.fc
Source21:	linuxptp.if
Source22:	linuxptp.te

# fix handling of zero-length messages
Patch1:		linuxptp-zerolength.patch
# revert phc2sys options needed by the older version of test suite
Patch2:		clknetsim-phc2sys.patch

# The following patches are for HA in linuxptp
# https://review.opendev.org/c/starlingx/integ/+/891638
Patch3:         0001-clock-Reset-state-when-switching-port-with-same-best.patch
Patch4:         0002-clock-Reset-clock-check-on-best-clock-port-change.patch
Patch5:         0003-port-Don-t-check-timestamps-from-non-slave-ports.patch
Patch6:         0004-port-Don-t-renew-raw-transport.patch
Patch7:         0005-clockcheck-Increase-minimum-interval.patch
Patch8:         0006-Add-option-to-disable-default-port-selection-in-phc2.patch
Patch9:         0007-sysoff-Change-sysoff_measure-to-return-errno.patch
Patch10:        0008-sysoff-Change-log-level-of-ioctl-error-messages.patch
Patch11:        0009-sysoff-Retry-on-EBUSY-when-probing-supported-ioctls.patch
Patch12:        0010-phc2sys-Don-t-exit-when-reading-of-PHC-fails-with-EB.patch
Patch13:        0011-phc2sys-extract-PMC-functionality-into-a-smaller-str.patch
Patch14:        0012-phc2sys-make-PMC-functions-non-static.patch
Patch15:        0013-phc2sys-break-out-pmc-code-into-pmc_common.c.patch
Patch16:        0014-Introduce-the-PMC-agent-module.patch
Patch17:        0015-pmc_agent-Rename-pmc_node-to-something-more-descript.patch
Patch18:        0016-pmc_agent-Hide-the-implementation.patch
Patch19:        0017-Find-a-better-home-for-the-management-TLV-ID-helper-.patch
Patch20:        0018-Find-a-better-home-for-the-management-TLV-data-helpe.patch
Patch21:        0019-Introduce-error-codes-for-the-run_pmc-method.patch
Patch22:        0020-pmc_agent-Convert-the-subscribe-method-into-the-cano.patch
Patch23:        0021-pmc_agent-Simplify-the-update-method.patch
Patch24:        0022-pmc_agent-Simplify-logic-in-update-method.patch
Patch25:        0023-pmc_agent-Remove-bogus-comparison-between-last-updat.patch
Patch26:        0024-pmc_agent-Perform-time-comparison-using-positive-log.patch
Patch27:        0025-pmc_agent-Rename-the-update-method-and-attempt-to-do.patch
Patch28:        0026-phc2sys-Fix-null-pointer-de-reference-in-manual-mode.patch
Patch29:        0027-pmc_agent-Convert-the-method-that-queries-TAI-UTC-of.patch
Patch30:        0028-pmc_agent-Convert-the-method-that-queries-the-port-p.patch
Patch31:        0029-pmc_agent-Generalize-the-method-that-queries-the-loc.patch
Patch32:        0030-pmc_agent-Simplify-the-method-that-gets-of-the-numbe.patch
Patch33:        0031-pmc_agent-Let-the-update-method-poll-for-push-events.patch
Patch34:        0032-phc2sys-Fix-regression-in-the-automatic-mode.patch
Patch35:        0033-Implement-push-notification-for-TIME_STATUS_NP.patch
Patch36:        0034-clock-Rename-UDS-variables-to-read-write.patch
Patch37:        0035-clock-Add-read-only-UDS-port-for-monitoring.patch
Patch38:        0036-Rename-management-ID-macros.patch
Patch39:        0037-Enhance-phc2sys-to-accept-multiple-ptp4l-inputs.patch
Patch40:        0038-Best-source-selection-algorithm.patch
Patch41:        0039-Select-best-source-clock-after-state-changes.patch
Patch42:        0040-Forced-lock-a-clock-source-in-configuration.patch
Patch43:        0041-HA-phc2sys-com-socket.patch
Patch44:        0042-Commands-enable-lock-and-disable-lock.patch
Patch45:        0043-Commands-enable-source-and-disable-source.patch
Patch46:        0044-Stream-type-phc2sys-com-socket.patch
Patch47:        0045-Functions-starts_with-and-str_at_column.patch
Patch48:        0046-Robustness-improvements-to-phc2sys-socket.patch
Patch49:        0047-phc2sys-without-w-option.patch

BuildRequires:	gcc gcc-c++ make systemd

%{?systemd_requires}

%if 0%{?with_selinux}
Requires:	(%{name}-selinux if selinux-policy-%{selinuxtype})
%endif

%description
This software is an implementation of the Precision Time Protocol (PTP)
according to IEEE standard 1588 for Linux. The dual design goals are to provide
a robust implementation of the standard and to use the most relevant and modern
Application Programming Interfaces (API) offered by the Linux kernel.
Supporting legacy APIs and other platforms is not a goal.

%if 0%{?with_selinux}
%package selinux
Summary:	linuxptp SELinux policy
BuildArch:	noarch
Requires:	selinux-policy-%{selinuxtype}
Requires(post):	selinux-policy-%{selinuxtype}
BuildRequires:	selinux-policy-devel
%{?selinux_requires}

%description selinux
linuxptp SELinux policy module

%endif

%prep
%setup -q -a 10 -a 11 -n %{name}-%{!?gitfullver:%{version}}%{?gitfullver}
%patch1 -p1 -b .zerolength
mv linuxptp-testsuite-%{testsuite_ver}* testsuite
mv clknetsim-%{clknetsim_ver}* testsuite/clknetsim

pushd testsuite/clknetsim
%patch2 -p1 -R -b .phc2sys
popd

mkdir selinux
cp -p %{SOURCE20} %{SOURCE21} %{SOURCE22} selinux

%build
%{make_build} \
	EXTRA_CFLAGS="$RPM_OPT_FLAGS" \
	EXTRA_LDFLAGS="$RPM_LD_FLAGS"

%if 0%{?with_selinux}
make -C selinux -f %{_datadir}/selinux/devel/Makefile linuxptp.pp
bzip2 -9 selinux/linuxptp.pp
%endif

%install
%makeinstall

mkdir -p $RPM_BUILD_ROOT{%{_sysconfdir}/sysconfig,%{_unitdir},%{_mandir}/man5}
install -m 644 -p %{SOURCE1} %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}
install -m 644 -p %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}

echo 'OPTIONS="-f /etc/ptp4l.conf"' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ptp4l
echo 'OPTIONS="-a -r"' > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/phc2sys

echo '.so man8/ptp4l.8' > $RPM_BUILD_ROOT%{_mandir}/man5/ptp4l.conf.5
echo '.so man8/timemaster.8' > $RPM_BUILD_ROOT%{_mandir}/man5/timemaster.conf.5

%if 0%{?with_selinux}
install -D -m 0644 selinux/linuxptp.pp.bz2 \
	$RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{selinuxtype}/linuxptp.pp.bz2
install -D -p -m 0644 selinux/linuxptp.if \
	$RPM_BUILD_ROOT%{_datadir}/selinux/devel/include/distributed/linuxptp.if
%endif

%check
cd testsuite
# set random seed to get deterministic results
export CLKNETSIM_RANDOM_SEED=26743
%{make_build} -C clknetsim
PATH=..:$PATH ./run

%post
%systemd_post phc2sys.service ptp4l.service timemaster.service

%preun
%systemd_preun phc2sys.service ptp4l.service timemaster.service

%postun
%systemd_postun_with_restart phc2sys.service ptp4l.service timemaster.service

%if 0%{?with_selinux}
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/linuxptp.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
	%selinux_modules_uninstall -s %{selinuxtype} linuxptp
	%selinux_relabel_post -s %{selinuxtype}
fi

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/linuxptp.pp.*
%{_datadir}/selinux/devel/include/distributed/linuxptp.if
%ghost %verify(not md5 size mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/linuxptp

%endif

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
%{_sbindir}/timemaster
%{_sbindir}/ts2phc
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%changelog
* Thu Nov 16 2023 Harshit Gupta <guptaharshit@microsoft.com> - 3.1.1-7
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License Verified.

* Wed Jan 11 2023 Miroslav Lichvar <mlichvar@redhat.com> 3.1.1-6
- update selinux policy (#2159919)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Apr 26 2022 Miroslav Lichvar <mlichvar@redhat.com> 3.1.1-4
- fix tests on ppc64le (#2046706)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Miroslav Lichvar <mlichvar@redhat.com> 3.1.1-2
- package selinux policy

* Wed Jul 07 2021 Miroslav Lichvar <mlichvar@redhat.com> 3.1.1-1
- update to 3.1.1 (CVE-2021-3570, CVE-2021-3571)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Feb 25 2021 Miroslav Lichvar <mlichvar@redhat.com> 3.1-3
- fix handling of zero-length messages
- minimize default configuration
- remove obsolete build requirement

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 2020 Miroslav Lichvar <mlichvar@redhat.com> 3.1-1
- update to 3.1

* Mon Jul 27 2020 Miroslav Lichvar <mlichvar@redhat.com> 3.0-1
- update to 3.0

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
