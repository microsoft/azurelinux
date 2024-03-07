%global srcname distlib
Summary:        Low-level components of distutils2/packaging, augmented with higher-level APIs
Name:           python-distlib
Version:        0.3.6
Release:        3%{?dist}
License:        Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://readthedocs.org/projects/distlib/
Source0:        https://files.pythonhosted.org/packages/source/d/%{srcname}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildArch:      noarch

%description
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Low-level components of distutils2/packaging, augmented with higher-level APIs

%description -n python%{python3_pkgversion}-%{srcname}
Distlib contains the implementations of the packaging PEPs and other low-level
features which relate to packaging, distribution and deployment of Python
software. If Distlib can be made genuinely useful, then it is possible for
third-party packaging tools to transition to using it. Their developers and
users then benefit from standardised implementation of low-level functions,
time saved by not having to reinvent wheels, and improved interoperability
between tools.

%prep
%setup -q -n %{srcname}-%{version}

rm distlib/*.exe


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
export PYTHONHASHSEED=0

# test_sequencer_basic test fails due to relying
# on the ordering of the input, hence disabling it.
# https://github.com/pypa/distlib/issues/161

# test_is_writable assumes we're not the root user
# and does not like that we have write access to /etc

%pytest -k "not (test_sequencer_basic or test_is_writable)"

%files -n python%{python3_pkgversion}-%{srcname} -f %pyproject_files
%license LICENSE.txt
%doc README.rst

%changelog
* Fri Dec 01 2023 Olivia Crain <oliviacrain@microsoft.com> - 0.3.6-3
- Skip test_is_writable during check builds

* Tue Dec 21 2021 Riken Maharjan <rmaharjan@microsoft.com> - 0.3.6-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified.

* Thu Oct 27 2022 Lumír Balhar <lbalhar@redhat.com> - 0.3.6-1
- Update to 0.3.6

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.4-4
- Rebuilt for Python 3.11

* Wed Mar 23 2022 Charalampos Stratakis <cstratak@redhat.com> - 0.3.4-3
- Disable a flaky test
Fixes: rhbz#2033200

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 08 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.3.4-1
- Update to 0.3.4 (#2030405)

* Thu Dec 02 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.3.3-1
- Update to 0.3.3 (#2006679)

* Tue Aug 03 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.3.2-1
- Update to 0.3.2 (#1965756)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.3.1-5
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.3.1-3
- Convert the package to pyproject macros

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.3.1-1
- Update to 0.3.1 (#1851644)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.9

* Thu Mar 19 2020 Tomas Hrnciar <thrnciar@redhat.com> - 0.3.0-1
- Update to 0.3.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.7-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.7-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 02 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.2.7-2
- Remove the python2 subpackage

* Mon Jul 30 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.7-1
- Update to 0.2.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-8
- Rebuilt for Python 3.7

* Sat Apr 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-7
- Fix the license tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 16 2016 Charalampos Stratakis <cstratak@redhat.com> 0.2.3-1
- Update to 0.2.3
- Add the license tag
- Use modern python RPM macros
- Provide a python 2 subpackage
- Use the python provides macros
- Changed to newest pypi URL format

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Matej Stuchlik <mstuchli@redhat.com> - 0.2.1-2
- Update to 0.2.1

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 05 2014 Matej Stuchlik <mstuchli@redhat.com> - 0.1.9-1
- Initial spec
