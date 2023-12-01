Summary:        Pygments is a syntax highlighting package written in Python.
Name:           python-pygments
Version:        2.5.2
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/Pygments
Source0:        https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
BuildArch:      noarch

%description
Pygments is a syntax highlighting package written in Python.

%package -n     python3-pygments
Summary:        Pygments is a syntax highlighting package written in Python.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python3

%description -n python3-pygments
Pygments is a syntax highlighting package written in Python.

It is a generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code. Highlights are:

a wide range of over 300 languages and other text formats is supported
special attention is paid to details, increasing quality by a fair amount
support for new languages and formats are added easily
a number of output formats, presently HTML, LaTeX, RTF, SVG, all image formats that PIL supports and ANSI sequences
it is usable as a command-line tool and as a library.

%prep
%autosetup -p1 -n Pygments-%{version}

%build
%py3_build

%install
%py3_install

%check
#easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
#$easy_install_3 nose
#PYTHON=python3 make test
#test incompatible with python3.7

%files -n python3-pygments
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.5.2-1
- Auto-upgrade to 2.5.2 - Azure Linux 3.0 - package upgrades

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.4.2-7
- Add license to python3 package
- Remove python2 package
- Lint spec

* Fri Mar 26 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.4.2-6
- Patch CVE-2021-20270.

* Wed Mar 24 2021 Henry Beberman <henry.beberman@microsoft.com> - 2.4.2-5
- Patch CVE-2021-27291.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.4.2-4
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.4.2-3
- Renaming python-Pygments to python-pygments

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.4.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jun 13 2019 Tapas Kundu <tkundu@vmware.com> - 2.4.2-1
- Update to release 2.4.2

* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> - 2.2.0-3
- Fix makecheck

* Fri Jul 28 2017 Divya Thaluru <dthaluru@vmware.com> - 2.2.0-2
- Fixed make check errors

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.2.0-1
- Initial packaging for Photon
