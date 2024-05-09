Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		sassist
Version:	0.8.5
Release:	5%{?dist}
Summary:	Dell SupportAssist log collector

License:	MIT
URL:		https://www.dell.com/en-us/work/learn/supportassist
Source0:	https://github.com/dell/sassist/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:	systemd

%if 0%{?suse_version}
Requires: supportutils
%else
Requires: sos
%endif
Requires: freeipmi
Requires: zip

BuildArch: noarch
%{?systemd_requires}

%description
Dell SupportAssist log collector for Linux.

%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}

install -p -m755 src/sassist.sh %{buildroot}%{_bindir}
install -p -m644 src/systemd/sassist.service %{buildroot}%{_unitdir}
install -p -m644 src/systemd/sassist-collect.service %{buildroot}%{_unitdir}
install -p -m644 src/systemd/run-media-iDRAC_NATOSC.mount %{buildroot}%{_unitdir}

%files
%license COPYING
%{_bindir}/sassist.sh
%{_unitdir}/sassist.service
%{_unitdir}/sassist-collect.service
%{_unitdir}/run-media-iDRAC_NATOSC.mount

%post
%systemd_post sassist.service

%preun
%systemd_preun sassist.service

%postun
%systemd_postun_with_restart sassist.service

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.5-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 01 2018 Charles Rose <charles_rose@dell.com> - 0.8.5-1
- Retain all content in zip file. Created Makefile.

* Fri Oct 19 2018 Charles Rose <charles_rose@dell.com> - 0.8.4-1
- PrivateTmp, better error handling, sos plugin changes

* Fri Aug 24 2018 Charles Rose <charles_rose@dell.com> - 0.8.3-1
- move mount point, enable all sos plugins, some cleanup

* Mon Jun 18 2018 Charles Rose <charles_rose@dell.com> - 0.8.2-1
- incorporate spec file suggestions from Robert-André Mauchin

* Thu Jun 14 2018 Charles Rose <charles_rose@dell.com> - 0.8.2
- guess paths for log collectors. fix error handling.

* Thu Jun 14 2018 Charles Rose <charles_rose@dell.com> - 0.8.1
- add dependency on zip. fix temp dir creation bug

* Mon Apr 02 2018 Charles Rose <charles_rose@dell.com> - 0.8.0
- add support for supportconfig

* Mon Apr 02 2018 Charles Rose <charles_rose@dell.com> - 0.7.1
- support multi-distro

* Mon Aug 28 2017 Charles Rose <charles_rose@dell.com> - 0.7.0-1
- first RPM release
