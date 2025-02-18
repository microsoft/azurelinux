%global maj 0

Name:           serd
Version:        0.32.4
Release:        1%{?dist}
Summary:        A lightweight C library for RDF syntax

License:        ISC
URL:            https://drobilla.net/software/%{name}.html
Source0:        https://download.drobilla.net/%{name}-%{version}.tar.xz
Source1:        https://download.drobilla.net/%{name}-%{version}.tar.xz.sig
Source2:        https://drobilla.net/drobilla.gpg

BuildRequires:  meson
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_lv2_theme
BuildRequires:  python-sphinxygen

%description
%{name} is a lightweight C library for RDF syntax which supports reading and 
writing Turtle, TRiG, NTriples, and NQuads.

Serd is suitable for performance-critical or resource-limited applications,
such as serialising very large data sets, network protocols, or embedded
systems that require minimal dependencies and lightweight deployment.

%package devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for RDF syntax which supports reading and 
writing Turtle, TRiG, NTriples, and NQuads.

This package contains the headers and development libraries for %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%meson -Dman_html=disabled
%meson_build

%install
%meson_install
# Move devel docs to the right directory
install -d %{buildroot}%{_docdir}/%{name}
mv %{buildroot}%{_docdir}/%{name}-%{maj} %{buildroot}%{_docdir}/%{name}

%check
%meson_test

%files
%license COPYING
%doc AUTHORS NEWS README.md
%doc %{_mandir}/man1/serdi.1*
%{_libdir}/lib%{name}-%{maj}.so.%{maj}*
%{_bindir}/serdi

%files devel
%doc %{_docdir}/%{name}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_includedir}/%{name}-%{maj}/

%changelog
* Sun Jan 19 2025 Guido Aulisi <guido.aulisi@inps.it> - 0.32.4-1
- Update to 0.32.4

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.32.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Guido Aulisi <guido.aulisi@gmail.com> - 0.32.2-1
- Update to 0.32.2
- Verify sources

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jan 31 2023 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.16-1
- Update to 0.30.16

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.12-1
- Update to 0.30.12

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.10-1
- Update to 0.30.10

* Sun Oct 04 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.6-1
- Update to 0.30.6

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.4-1
- Update to 0.30.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.2-1
- Update to 0.30.2
- Use python3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.30.0-1
- Update to 0.30.0
- Remove ldconfig scriptlets
- Minor spec cleanup

* Sun Jul 15 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.28.0-5
- Fix FTBFS due to the move of /usr/bin/python into a separate package

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Kalev Lember <klember@redhat.com> - 0.28.0-2
- Bump and rebuild for an rpm signing issue

* Thu Aug 10 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.28.0-1
- Update to 0.28.0
- Use license macro

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.26.0-2
- Fix unowned mid-level directory

* Mon Mar 13 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.26.0-1
- Update to 0.26.0
- Use hardened LDFLAGS
- Remove deprecated Groups tags

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Brendan Jones <brendan.jones.it@gmail.com> - 0.22.0-1
- Update to 0.22.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-1
- Update to 0.20.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.18.2-3
- Install docs to %%{_pkgdocdir} where available (#994091).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.18.2-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-1
- New upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-1
- New upstream release. 

* Sat Jan 14 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Move man1 file, furtherqualify wildcards. 

* Sat Jan 14 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- License to ISC, remove tabs

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
