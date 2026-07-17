# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: High-performance implementation of a colorful cat
Name:    lolcat
Version: 1.5
Release: 5%{?dist}
Source:  https://github.com/jaseg/lolcat/archive/v%{version}/%{name}-%{version}.tar.gz
URL:     https://github.com/jaseg/lolcat/

Patch1:  lolcat-Makefile.patch

License: WTFPL
BuildRequires: make
BuildRequires: gcc

%description
lolcat is a colorful version of 'cat'. It is faster than python-lolcat 
and much faster than ruby-lolcat. It works well with "non-binary" 
characters, but who would want to display binary data!

%prep
%autosetup

%build
%set_build_flags
%make_build all

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
%make_install DESTDIR=$RPM_BUILD_ROOT/%{_bindir}

%files
%{_bindir}/lolcat
%{_bindir}/censor
%doc README.md
%license LICENSE

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 josef radinger <cheese@nosuchhost.net> - 1.5-1
- bump version

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 josef radinger <cheese@nosuchhost.net> - 1.4-1
- bump version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 josef radinger <cheese@nosuchhost.net> - 1.3-1
- bump version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 17 2021 josef radinger <cheese@nosuchhost.net> - 1.2-0
- bump version
- massage patch1
- remove patch2

* Sun Dec 27 2020 josef radinger <cheese@nosuchhost.net> - 1.1-1
- bump version
- add patch2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 josef radinger <cheese@nosuchhost.net> - 1.0-6
- modify description

* Mon Aug 26 2019 josef radinger <cheese@nosuchhost.net> - 1.0-5
- use a better source-url
- use %%autosetup
- use %%make_build
- use %%make_install (plus patch1 to preserve timestamps)
- better Summary

* Sat Aug 17 2019 josef radinger <cheese@nosuchhost.net> - 1.0-4
- use %%{_bindir} instead of /usr/bin
- invoke %%set_build_flags before make

* Fri Aug 16 2019 josef radinger <cheese@nosuchhost.net> - 1.0-3
- correct license
- small cleanup in spec-file

* Wed Aug 07 2019 josef radinger <cheese@nosuchhost.net> - 1.0-2
- add URL

* Tue Aug 06 2019 josef radinger <cheese@nosuchhost.net> - 1.0-1
- initial package

