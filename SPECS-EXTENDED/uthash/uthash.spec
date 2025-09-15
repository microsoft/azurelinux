Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           uthash
Version:        2.3.0
Release:        9%{?dist}
Summary:        A hash table for C structures

License:        BSD-1-Clause
URL:            https://troydhanson.github.io/%{name}
Source0:        https://github.com/troydhanson/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

%description
Any C structure can be stored in a hash table using uthash.  Just
add a UT_hash_handle to the structure and choose one or more fields
in your structure to act as the key.  Then use these macros to store,
retrieve or delete items from the hash table.


%package devel
Summary:        A hash table for C structures (headers only)

# c-compiled libraries have been dropped upstream.
Obsoletes:      libut          < 2.3.0
Obsoletes:      libut-devel    < 2.3.0

Provides:       %{name}        = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}
Provides:       libut          = %{version}-%{release}
Provides:       libut-devel    = %{version}-%{release}

BuildArch:      noarch

%description devel
Any C structure can be stored in a hash table using uthash.  Just
add a UT_hash_handle to the structure and choose one or more fields
in your structure to act as the key.  Then use these macros to store,
retrieve or delete items from the hash table.


%package tools
Summary:        Command-line utilities for %{name}
Requires:       %{name}        = %{version}-%{release}

%description tools
This package provides the hashscan and keystats utility programs
for %{name}.

The hashscan program examines a running process and reports on the
uthash tables that it finds in that program’s memory.  It can also
save the keys from each table in a format that can be fed into keystats.

The keystats program is able to analyze which hash function has the best
characteristics on the set of keys reported by the hashscan program.


%package doc
Summary:        Documentation-files for %{name}
BuildArch:      noarch
Requires:       %{name}        = %{version}-%{release}

%description doc
This package contains the documentation-files for %{name}.


%prep
%autosetup -p1


%build
%set_build_flags
%make_build -C doc
%make_build -C tests
%make_build -C tests/threads


%install
mkdir -p %{buildroot}{%{_bindir},%{_includedir},%{_pkgdocdir}/html}
install -pm 0755 tests/{hashscan,keystats} %{buildroot}%{_bindir}
install -pm 0644 src/*.h %{buildroot}%{_includedir}
# Install doc.
install -pm 0644 doc/*.txt tests/example.c %{buildroot}%{_pkgdocdir}
install -pm 0644 doc/*.html doc/*.css doc/*.png %{buildroot}%{_pkgdocdir}/html
rm -f %{buildroot}%{_pkgdocdir}/html/google*.html


%files devel
%license LICENSE
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/ChangeLog.txt
%{_includedir}/*.h


%files tools
%{_bindir}/*


%files doc
%doc %{_pkgdocdir}


%changelog
* Tue Jan 20 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.3.0-9
- Initial Azure Linux import from Fedora 41 (license: MIT)
- change the URL and Source from http to https
- License verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Björn Esser <besser82@fedoraproject.org> - 2.3.0-5
- Add tools package
- Add explicit perl BRs
- Add example program to doc package
- Drop google site-verification file from doc package
- Require main package in doc package to avoid file conflicts

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Björn Esser <besser82@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0
- Obsolete libut as it has been dropped upstream

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 04 2017 Björn Esser <besser82@fedoraproject.org> - 2.0.2-1
- New upstream release (rhbz#1429106)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-6
- Fix dir-ownership in %%doc

* Fri Dec 30 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-5
- Introduce doc-subpackage
- Use unified %%_pkgdocdir
- Updated Patch0 and use on el <= 6, only
- Rename Patch0 --> Patch 1000
- Clean-up indentation


* Thu Dec 29 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-4
- Include plain ascii-docs, too

* Thu Dec 29 2016 Björn Esser <bjoern.esser@gmail.com> - 2.0.1-3
- Properly build the documentation

* Sun Dec 18 2016 Björn Esser <fedora@besser82.io> - 2.0.1-2
- Run testsuite with threads, too

* Sat Dec 17 2016 Björn Esser <fedora@besser82.io> - 2.0.1-1
- Update to new upstream release v2.0.1
- Introduce libut / libvector
- Add BR: perl

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-6
- add `%%global debug_package %%{nil}` to avoid empty debuginfo-pkg.

* Thu May 22 2014 Björn Esser <bjoern.esser@gmail.com> - 1.9.9-5
- revert "Root package should be noarch too".
- add provides %%{name} for -devel subpkg.
- add a note about why the mainpkg is arched.

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-4
- Root package should be noarch too

* Wed May 21 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9-3
- Build as noarch

* Sun May 18 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-2
- Move all files to -devel subpkg.

* Sat Mar 29 2014 Christopher Meng <rpm@cicku.me> - 1.9.9-1
- Update to 1.9.9

* Sat Jun 15 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-3
- Add virtual provide.
- Remove 2 wrong tests.

* Fri Jun 14 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-2
- Remove unneeded BR and make files section more clear.

* Sat Jun 01 2013 Christopher Meng <rpm@cicku.me> - 1.9.8-1
- Initial Package.
