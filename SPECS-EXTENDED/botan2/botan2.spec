Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global major_version 2

Name:           botan2
Version:        2.19.5
Release:        1%{?dist}
Summary:        Crypto and TLS for C++11

License:        BSD-2-Clause
URL:            https://botan.randombit.net/
Source0:        https://botan.randombit.net/releases/Botan-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  make

%description
Botan is a BSD-licensed crypto library written in C++. It provides a
wide variety of basic cryptographic algorithms, X.509 certificates and
CRLs, PKCS \#10 certificate requests, a filter/pipe message processing
system, and a wide variety of other features, all written in portable
C++. The API reference, tutorial, and examples may help impart the
flavor of the library. This is the current stable release branch 2.x
of Botan.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
%{summary}

This package contains HTML documentation for %{name}.


%package -n python3-%{name}
Summary:        Python3 bindings for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
%{summary}

This package contains the Python3 binding for %{name}.


%prep
%autosetup -n Botan-%{version} -p1


%build
export CXXFLAGS="${CXXFLAGS:-%{optflags}}"

# we have the necessary prerequisites, so enable optional modules
%global enable_modules bzip2,zlib

%{__python3} ./configure.py \
        --prefix=%{_prefix} \
        --libdir=%{_lib} \
        --docdir=%{_docdir} \
        --cc=gcc \
        --os=linux \
        --cpu=%{_arch} \
        --enable-modules=%{enable_modules} \
        --with-python-version=%{python3_version} \
        --with-sphinx \
        --with-rst2man \
        --distribution-info="$(source /etc/os-release ; echo "$NAME")" \
        --disable-static-library \
        --with-debug-info

# work around https://github.com/randombit/botan/issues/2130
%make_build PYTHON_EXE=%{__python3}

%install
make install PYTHON_EXE=%{__python3} DESTDIR=%{buildroot}

sed -e '1{/^#!/d}' -i %{buildroot}%{python3_sitearch}/botan2.py
%if "%{python3_sitelib}" != "%{python3_sitearch}"
mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{python3_sitearch}/botan2.py %{buildroot}%{python3_sitelib}/botan2.py
%endif

# doc installation fixups
mv %{buildroot}%{_docdir}/botan-%{version} %{buildroot}%{_pkgdocdir}
rm -r %{buildroot}%{_pkgdocdir}/handbook/{.doctrees,.buildinfo}


%ldconfig_scriptlets


%files
%license license.txt
%dir %{_pkgdocdir}
%{_pkgdocdir}/*.txt
%{_libdir}/libbotan-%{major_version}.so.19*
%{_bindir}/botan
%{_mandir}/man1/botan.1*


%files devel
%license license.txt
%{_includedir}/*
%{_libdir}/libbotan-%{major_version}.so
%{_libdir}/pkgconfig/botan-%{major_version}.pc


%files doc
%license license.txt
%dir %{_pkgdocdir}
%{_pkgdocdir}/handbook


%files -n python3-%{name}
%license license.txt
%pycached %{python3_sitelib}/%{name}.py


%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./botan-test


%changelog
* wed nov 5 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 2.19.5-1
- Upgrade to version 2.19.5
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.14.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat Jun 27 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.14.0-1
- Update to 2.14.0.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.13.0-3
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Benjamin Kircher <bkircher@0xadd.de> - 2.13.0-1
- Update to 2.13

* Wed Oct 16 2019 Benjamin Kircher <bkircher@0xadd.de> - 2.12.1-1
- Update to 2.12.1

* Sat Oct  5 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.0-5
- Allow building on CentOS8 fixing a quoting and a Python path issue.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.11.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.11.0-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.11.0-1
- New upstream release

* Sun Mar 31 2019 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.10.0-1
- New upstream release

* Sat Feb 09 2019 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.9.0-1
- Update to 2.9.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-2
- Rebuilt for Python 3.7

* Mon Jul  2 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.0-1
- Update to 2.7.0.

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-2
- Rebuilt for Python 3.7

* Thu Apr 12 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.6.0-1
- New upstream release

* Sun Apr 01 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-10
- Add patch to fix test suite failure due to expired test certificate

* Mon Mar 19 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-9
- Update empty patch file with the real patch contents.

* Sat Mar 17 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-8
- Add patch to fix test suite failures on ppc64le (see gh#1498).
- Add patch to fix test suite if SIMD instructions are not available (see gh#1495).

* Thu Mar 15 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-7
- Add patch to the Python module, supporting loading via
  libbotan-2.so.X.

* Thu Mar 15 2018 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.0-6
- Set CXXFLAGS before calling configure.py.
- Patch for building on armv7hl (see gh#1495).
- Make dependency on rst2man explicit.
- Don't use Python2 at all.
- Remove shebang from botan2.py.
- Don't build a static library.
- Switch to %%ldconfig_scriptlets.

* Tue Mar 13 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.4.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Mar 06 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-4
- Exclude ppc64le arch, fix linter warnings

* Tue Mar 06 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-3
- Fix macro expansion in changelog section

* Sat Jan 13 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-2
- Remove INSTALL_ variables, not used anymore

* Thu Jan 11 2018 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.4.0-1
- New upstream version; add new man page for botan command line utility

* Fri Dec 15 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.3.0-1
- New upstream version

* Thu Sep 07 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-4
- Backport upstream fix for broken GOST on i686

* Wed Sep 06 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-3
- Fix %%check section after rpath removal, generate debug symbols

* Thu Aug 31 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-2
- Fix issues that came up in review, see RH Bugzilla #1487067

* Sat Aug 12 2017 Benjamin Kircher <benjamin.kircher@gmail.com> - 2.2.0-1
- New package. No need for compat-openssl10-devel anymore with 2.2.0 release
