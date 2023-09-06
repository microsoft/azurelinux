%global _description %{expand:
Python's itertools library is a gem - you can compose elegant solutions for
a variety of problems with the functions it provides. In more-itertools we
collect additional building blocks, recipes, and routines for working with
Python iterables.}
Summary:        More routines for operating on Python iterables, beyond itertools
Name:           python-more-itertools
Version:        8.13.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/erikrose/more-itertools
Source0:        %{pypi_source more-itertools}
BuildRequires:  python3-devel
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildArch:      noarch

%description %{_description}

%package -n python3-more-itertools
Summary:        %{summary}

%description -n python3-more-itertools %{_description}

%prep
%autosetup -p1 -n more-itertools-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files more_itertools

%check
pip3 install tox
tox -e py%{python3_version_nodots}

%files -n python3-more-itertools -f %{pyproject_files}
%doc README.rst
%license LICENSE

%changelog
* Tue Aug 22 2023 Osama Esmail <osamaesmail@microsoft.com> - 8.13.0-3
- Fixing tests by adding 'tox'

* Wed Jan 11 2023 Riken Maharjan <rmaharjan@microsoft.com> - 8.13.0-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Tue Sep 13 2022 Lumír Balhar <lbalhar@redhat.com> - 8.13.0-1
- Update to 8.13.0
Resolves: rhbz#2082756

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 8.12.0-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 8.12.0-3
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Paul Wouters <paul.wouters@aiven.io> - 8.12.0-1
- Update to 8.12.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 8.5.0-4
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 8.5.0-3
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Lumír Balhar <lbalhar@redhat.com> - 8.5.0-1
- Update to 8.5.0 (#1873653)

* Wed Jul 29 2020 Miro Hrončok <mhroncok@redhat.com> - 8.4.0-1
- Update to 8.4.0
- Fixes rhbz#1778332

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-2
- Rebuilt for Python 3.8

* Tue Aug 13 2019 Thomas Moschny <thomas.moschny@gmx.de> - 7.2.0-1
- Update to 7.2.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 aarem AT fedoraproject DOT org - 7.0.0-1
- Update to 7.0.0
- Drop python-2

* Sun Apr 01 2018 aarem AT fedoraproject DOT org - 4.1.0-1
- rebuit for 4.1.0 using Thomas Moschny modification to spec file

* Sat Mar 24 2018 Thomas Moschny <thomas.moschny@gmx.de> - 4.1.0-1
- Update to 4.1.0.
- Do not do  package tests.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3-2
- Rebuild for Python 3.6

* Wed Nov 09 2016 aarem AT fedoraproject DOT org - 2.3-1
- update to 2.3

* Fri Oct 14 2016 aarem AT fedoraproject DOT org - 2.2-4
- fixed missing sum in line 9 of spec file, per BZ #138195

* Sat Oct 8 2016 aarem AT fedoraproject DOT org - 2.2-3
- renamed spec file to match package as per BZ #1381029
-fixed bug (incorrect python3_provides) as per BZ #1381029
- use common macro for description as per suggestion in BZ #1381029

* Wed Oct 05 2016 aarem AT fedoraproject DOT org - 2.2-2
- separated python and python3 cases as per BZ #1381029

* Sun Oct 02 2016 aarem AT fedoraproject DOT org - 2.2-1
- initial packaging of 2.2 version
