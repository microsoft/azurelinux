Summary:        Convert flat ASCII text to man page format
Name:           txt2man
Version:        1.7.1
Release:        12%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/mvertes/txt2man
Source0:        https://github.com/mvertes/%{name}/archive/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gawk
BuildRequires:  make

Requires:       gawk

%description
txt2man is a shell script using gnu awk, that should run on any
Unix-like system. The syntax of the ASCII text is very straightforward
and looks very much like the output of the man(1) program.

%prep
# No idea why but github archive is prepending the name twice
%setup -q -n %{name}-%{name}-%{version}

%build
%{make_build}

%install
#manual install
install -p -m 0755 -D bookman $RPM_BUILD_ROOT%{_bindir}/bookman
install -p -m 0755 -D src2man $RPM_BUILD_ROOT%{_bindir}/src2man
install -p -m 0755 -D txt2man $RPM_BUILD_ROOT%{_bindir}/txt2man

install -p -m 0644 -D bookman.1 $RPM_BUILD_ROOT%{_mandir}/man1/bookman.1
install -p -m 0644 -D src2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/src2man.1
install -p -m 0644 -D txt2man.1 $RPM_BUILD_ROOT%{_mandir}/man1/txt2man.1



%files
%doc Changelog README
%license COPYING
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Sun Apr 20 2026 Zhichun Wan <zhichunwan@microsoft.com> - 1.7.1-12
- Initial Azure Linux import from Fedora 45 (license: MIT).
- License verified.

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.1-8
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.1-1
- Update to 1.7.1.
- Specfile updates.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Adam Miller <maxamillion@fedoraproject.org> - 1.6.0-1
- Update to latest upstream release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon May 09 2011 Adam Miller <maxamillion@fedoraproject.org> - 1.5.6-1
- New upstream release, fixes old bugs.
- Upstream release notes claim POSIX shell code, but bookman still relies on
  bash styled syntax so we continue to patch it out.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 04 2009 Sindre Pedersen Bjordal <sindrepb@fedoraproject.org> - 1.5.5-1
- Initial build
- Include debian patch to fix bashisms
