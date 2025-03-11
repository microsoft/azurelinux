%global         maj 0

Name:           zix
Version:        0.6.2
Release:        2%{?dist}
Summary:        A lightweight C library of portability wrappers and data structures
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://gitlab.com/drobilla/%{name}
Source0:        https://download.drobilla.net/%{name}-%{version}.tar.xz
Source1:        https://download.drobilla.net/%{name}-%{version}.tar.xz.sig
Source2:        https://drobilla.net/drobilla.gpg

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  doxygen
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxygen
BuildRequires:  gnupg2

%description
%{name} is a lightweight C library of portability wrappers and data structures.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Provides:       bundled(js-jquery) = 3.6.0
Buildarch:      noarch

%description    doc
The %{name}-doc package contains documentation files for
developing applications that use %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
# Do not build benchmarks
%meson -Dbenchmarks=disabled
%meson_build

%install
%meson_install
# Delete duplicated sphinx docs
rm -rf %{buildroot}%{_docdir}/%{name}-%{maj}/singlehtml
# Delete sphinx buildinfo
rm -f %{buildroot}%{_docdir}/%{name}-%{maj}/html/.buildinfo
# Move devel docs to the right directory
install -d %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_docdir}/%{name}-%{maj} %{buildroot}%{_docdir}/%{name}

%check
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}-%{maj}.so.%{maj}*

%files devel
%{_includedir}/%{name}-%{maj}
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc

%files doc
%license COPYING
%doc %{_docdir}/%{name}/%{name}-%{maj}

%changelog
* Tue Feb 25 2025 Jyoti kanase <v-jykanase@microsoft.com> - 0.6.2-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Sun Jan 19 2025 Guido Aulisi <guido.aulisi@inps.it> - 0.6.2-1
- Update to 0.6.2
- Verify sources

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 11 2024 Guido Aulisi <guido.aulisi@gmail.com> - 0.4.2-1
- Update to 0.4.2

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 17 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.4.0-1
- Update to 0.4.0
- Use releases

* Sat Aug 12 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-7
- Drop dependency from doc package

* Sun Apr 16 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-6
- Delete single html documetation
- Make doc package noarch

* Sun Mar 19 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-5
- Put documentation files into separate package

* Sat Mar 11 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-4
- Fix BRs

* Sun Feb 26 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-3
- Enable docs

* Sun Feb 05 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-2
- Remove unneeded BR glib2-devel

* Sun Feb 05 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.3.1-1
- Initial import
