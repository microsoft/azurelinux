Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           systemd-bootchart
Version:        233
Release:        8%{?dist}
Summary:        Boot performance graphing tool

License:        GPLv2+ and LGPLv2+
URL:            https://github.com/systemd/systemd-bootchart
Source0:        https://github.com/systemd/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  docbook-style-xsl
%{?systemd_requires}

%description
This package provides a binary which can be started during boot early boot to
capture informations about processes and services launched during bootup.
Resource utilization and process information are collected during the boot
process and are later rendered in an SVG chart. The timings for each services
are displayed separately.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE.GPL2
%license LICENSE.LGPL2.1
%doc README
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%{_unitdir}/systemd-bootchart.service
%{_unitdir}/../%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/bootchart.conf.5*
%{_mandir}/man5/bootchart.conf.d.5*

%changelog
* Tue Sep 19 2023 Jon Slobodzian <joslobo@microsoft.com> - 233-8
- Fix build issue for systemd/systemd-bootstrap confusion
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 233-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 233-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 233-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 233-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 233-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 233-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 233-1
- Update to 233

* Sun Sep 10 2017 Peter Robinson <pbrobinson@fedoraproject.org> 232-1
- new upstream 232 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 231-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 231-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 231-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 231-2
- Improve SPEC file thanks to suggestions during review

* Tue Sep 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 231-1
- Initial packaging
