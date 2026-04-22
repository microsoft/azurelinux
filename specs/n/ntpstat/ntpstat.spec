# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		ntpstat
Version:	0.6
Release: 15%{?dist}
Summary:	Utility to print NTP synchronization status

License:	MIT
URL:		https://github.com/mlichvar/ntpstat
Source0:	https://github.com/mlichvar/ntpstat/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	make
Requires:	(ntpsec or chrony)
# ntpstat was split off from the ntp package
Conflicts:	ntp < 4.2.8p10-4

%description
This package contains a script which prints a brief summary of the system
clock's synchronisation status when the ntpd or chronyd daemon is running.

%prep
%setup -q

%build

%install
make install bindir=$RPM_BUILD_ROOT%{_bindir} mandir=$RPM_BUILD_ROOT%{_mandir}

%files
%license COPYING
%doc NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Miroslav Lichvar <mlichvar@redhat.com> 0.6-4
- switch dependency from ntp to ntpsec

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 11 2020 Miroslav Lichvar <mlichvar@redhat.com> 0.6-1
- update to 0.6

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 20 2018 Miroslav Lichvar <mlichvar@redhat.com> 0.5-1
- update to 0.5

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Miroslav Lichvar <mlichvar@redhat.com> 0.4-3
- fix more issues found in package review (#1510565)

* Thu Nov 23 2017 Miroslav Lichvar <mlichvar@redhat.com> 0.4-2
- fix issues found in package review (#1510565)

* Tue Nov 07 2017 Miroslav Lichvar <mlichvar@redhat.com> 0.4-1
- update to 0.4
- split ntpstat off from ntp package
