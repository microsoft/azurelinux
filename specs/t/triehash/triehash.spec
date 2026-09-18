# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with tests

Name:           triehash
Version:        0.3
Release:        16%{?dist}
Summary:        Generator for order-preserving minimal perfect hash functions in C

License:        MIT
URL:            https://jak-linux.org/projects/triehash/
Source0:        https://github.com/julian-klode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%if %{with tests}
BuildRequires:  perl(Devel::Cover)
%endif
BuildRequires:  perl(Pod::Man)
BuildRequires:  perl-generators


%{?perl_default_filter}

%description
TrieHash generates perfect hash functions as C code which then gets
compiled into optimal machine code as part of the usual program compilation.

TrieHash works by translating a list of strings to a trie, and then converting
the trie to a set of recursive switch statements; first switching by length,
and then switching by bytes.

TrieHash has various optimizations such as processing multiple bytes at once
(on GNU C), and shortcuts for reducing the complexity of case-insensitive
matching (ASCII only). Generated code performs substantially faster than
gperf, but is larger.

TrieHash was written for use in APT.


%prep
%autosetup


%build
pod2man triehash.pl triehash.1


%install
install -p -m755 -D triehash.pl %{buildroot}%{_bindir}/%{name}
install -p -m644 -D triehash.1 %{buildroot}%{_mandir}/man1/%{name}.1

%if %{with tests}
%check
./tests/run-tests.sh
%endif

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*



%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.3-9
- Perl 5.36 rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.3-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.3-3
- Perl 5.32 rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Neal Gompa <ngompa13@gmail.com> - 0.3-1
- Initial packaging for Fedora (RH#1764799)
