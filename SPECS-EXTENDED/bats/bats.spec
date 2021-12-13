Vendor:         Microsoft Corporation
Distribution:   Mariner
%global         upstreamname  bats-core

Name:           bats
Version:        1.2.1
Release:        2%{?dist}
Summary:        Bash Automated Testing System

License:        MIT
URL:            https://github.com/%{upstreamname}/%{upstreamname}
Source0:        https://github.com/%{upstreamname}/%{upstreamname}/archive/v%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildArch:      noarch

Requires:       bash
Requires:       parallel
BuildRequires:	parallel

%description
Bats is a TAP-compliant testing framework for Bash. It provides a simple way to
verify that the UNIX programs you write behave as expected. Bats is most useful
when testing software written in Bash, but you can use it to test any UNIX
program.

%prep
%setup -q -n %{upstreamname}-%{version}

%install
./install.sh ${RPM_BUILD_ROOT}%{_prefix}

%check
./bin/bats test/bats.bats
./bin/bats test/parallell.bats
./bin/bats test/suite.bats

%files
%doc README.md AUTHORS
%license LICENSE.md
%{_bindir}/%{name}
%{_libexecdir}/%{upstreamname}
%{_prefix}/lib/%{upstreamname}
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man7/%{name}.7.gz

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Fri Mar 19 2021 Ondřej Míchal <harrymichal@seznam.cz> - 1.2.1-1
- Update to 1.2.1
- new dependency - GNU Parallel
- new upstream test in %check - parallel.bats
- remove the sed in %prep because shebang mangling is done automatically
- change the URL for Source0 so that it does not rely on hardcoded commit

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 02 2018 Piotr Popieluch <piotr1212@gmail.com> - 1.1.0-1
- Change upstream to bats-core
- Update to 1.1.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8.20160219git0360811
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-7.20160219git0360811
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6.20160219git0360811
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5.20160219git0360811
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 05 2016 Piotr Popieluch <piotr1212@gmail.com> - 0.4.0-4.20160219git0360811
- Update to latest git snapshot
- Enable tests
- Remove obsoleted el5 macros
- Move license to %%license
- Add (empty) %%build section
- Add CONDUCT.md to %%doc
- Set correct interpreter in scripts

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3.20141016git3b33a5a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2.20141016git3b33a5a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 François Cami <fcami@redhat.com> - 0.4.0-1.20141016git3b33a5a
- First package version.

