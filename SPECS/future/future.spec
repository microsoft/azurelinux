%global with_python3 1
%global _description \
future is the missing compatibility layer between Python 2 and \
Python 3. It allows you to use a single, clean Python 3.x-compatible \
codebase to support both Python 2 and Python 3 with minimal overhead. \
\
It provides ``future`` and ``past`` packages with backports and forward \
ports of features from Python 3 and 2. It also comes with ``futurize`` and \
``pasteurize``, customized 2to3-based scripts that helps you to convert \
either Py2 or Py3 code easily to support both Python 2 and 3 in a single \
clean Py3-style codebase, module by module.
Summary:        Easy, clean, reliable Python 2/3 compatibility
Name:           future
Version:        0.18.2
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://python-future.org/
Source0:        https://files.pythonhosted.org/packages/source/f/%{name}/%{name}-%{version}.tar.gz
# https://github.com/PythonCharmers/python-future/issues/165
Patch0:         %{name}-skip_tests_with_connection_errors.patch
# Python 3.9 support
# https://github.com/PythonCharmers/python-future/pull/544
Patch1:         %{name}-python39.patch
BuildArch:      noarch
%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-devel
%endif

%description
%{_description}

%if 0%{?with_python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary:        Easy, clean, reliable Python 2/3 compatibility
BuildRequires:  python2-devel
BuildRequires:  python2-numpy
BuildRequires:  python2-pytest
BuildRequires:  python2-requests
BuildRequires:  python2-setuptools
Provides:       future = 0:%{version}-%{release}
%if 0%{?el6}
BuildRequires:  python-argparse
BuildRequires:  python-importlib
BuildRequires:  python-unittest2
Requires:       python-argparse
Requires:       python-importlib
%endif

%description -n python2-%{name}
%{_description}
%endif

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Summary:        Easy, clean, reliable Python 2/3 compatibility
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-requests
BuildRequires:  python%{python3_pkgversion}-setuptools
Provides:       future-python3 = 0:%{version}-%{release}
Obsoletes:      python2-%{name} < 0:%{version}-%{release}
Obsoletes:      %{name}-python2 < 0:%{version}-%{release}
Provides:       future = 0:%{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} < 8
Obsoletes:      python34-%{name} < 0:%{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-%{name}
%{_description}
%endif
# with_python3

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-%{name}
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{name}}
Summary:        Easy, clean, reliable Python 2/3 compatibility
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-numpy
BuildRequires:  python%{python3_other_pkgversion}-pytest
BuildRequires:  python%{python3_other_pkgversion}-requests
BuildRequires:  python%{python3_other_pkgversion}-setuptools
Provides:       future-python%{python3_other_pkgversion} = 0:%{version}-%{release}

%description -n python%{python3_other_pkgversion}-%{name}
%{_description}
%endif

%prep
%setup -qc -n future-%{version}

pushd future-%{version}
%patch0
%patch1 -p1
popd

%if 0%{?with_python3}
cp -a future-%{version} python3
find python3 -name '*.py' | xargs pathfix.py -pn -i %{__python3}
%endif
# with_python3

%if 0%{?with_python3_other}
cp -a future-%{version} python%{python3_other_pkgversion}
find python%{python3_other_pkgversion} -name '*.py' | xargs pathfix.py -pn -i %{__python3}
%endif

%build
%if 0%{?with_python3}
pushd python3
%py3_build
popd
%endif
# with_python3

%if 0%{?with_python3_other}
pushd python%{python3_other_pkgversion}
%{py3_other_build}
popd
%endif

%install

%if 0%{?with_python3}
pushd python3
%py3_install
mv %{buildroot}%{_bindir}/futurize %{buildroot}%{_bindir}/futurize-%{python3_version}
mv %{buildroot}%{_bindir}/pasteurize %{buildroot}%{_bindir}/pasteurize-%{python3_version}
ln -sf ./futurize-%{python3_version} %{buildroot}%{_bindir}/futurize-3
ln -sf ./pasteurize-%{python3_version} %{buildroot}%{_bindir}/pasteurize-3

ln -sf ./futurize-%{python3_version} %{buildroot}%{_bindir}/futurize
ln -sf ./pasteurize-%{python3_version} %{buildroot}%{_bindir}/pasteurize

sed -i -e '/^#!\//, 1d' %{buildroot}%{python3_sitelib}/future/backports/test/pystone.py
popd

chmod a+x %{buildroot}%{python3_sitelib}/future/backports/test/pystone.py
%endif

%if 0%{?with_python3_other}
pushd python%{python3_other_pkgversion}
%{py3_other_install}
mv %{buildroot}%{_bindir}/futurize %{buildroot}%{_bindir}/futurize-%{python3_other_version}
mv %{buildroot}%{_bindir}/pasteurize %{buildroot}%{_bindir}/pasteurize-%{python3_other_version}
sed -i -e '/^#!\//, 1d' %{buildroot}%{python3_other_sitelib}/future/backports/test/pystone.py
popd

chmod a+x %{buildroot}%{python3_other_sitelib}/future/backports/test/pystone.py
%endif

## This packages ships PEM certificates in future/backports/test directory.
## It's for testing purpose, i guess. Ignore them.
%check

# Bugs
# https://github.com/PythonCharmers/python-future/issues/474
# https://github.com/PythonCharmers/python-future/issues/508
%if 0%{?with_python3}
pushd python3
%if 0%{?python3_version_nodots} > 37
PYTHONPATH=$PWD/build/lib py.test-%{python3_version} -k "not test_pow and not test_urllib2"
%endif
%if 0%{?python3_version_nodots} <= 37
PYTHONPATH=$PWD/build/lib py.test-%{python3_version}
%endif
popd
%endif
# with_python3

%if 0%{?with_python3_other}
pushd python%{python3_other_pkgversion}
PYTHONPATH=$PWD/build/lib py.test-%{python3_other_version}
popd
%endif
# with_python3

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{name}
%license python3/LICENSE.txt
%doc python3/README.rst
%{_bindir}/futurize-3
%{_bindir}/pasteurize-3

%{_bindir}/futurize
%{_bindir}/pasteurize

%{_bindir}/futurize-%{python3_version}
%{_bindir}/pasteurize-%{python3_version}
%{python3_sitelib}/future/
%{python3_sitelib}/past/
%{python3_sitelib}/libfuturize/
%{python3_sitelib}/libpasteurize/
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{name}
%license python3/LICENSE.txt
%doc python3/README.rst
%{_bindir}/futurize-%{python3_other_version}
%{_bindir}/pasteurize-%{python3_other_version}
%{python3_other_sitelib}/future/
%{python3_other_sitelib}/past/
%{python3_other_sitelib}/libfuturize/
%{python3_other_sitelib}/libpasteurize/
%{python3_other_sitelib}/*.egg-info
%endif


%changelog
* Mon Jan 23 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.18.2-7
- Move from extended to core
- Remove python2 bits from the spec
- License verified

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 0.18.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Tue Feb 11 2020 Antonio Trande <sagitterATfedoraproject.org> - 0.18.2-5
- Fix Python 3.9 builds

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Antonio Trande <sagitterATfedoraproject.org> - 0.18.2-3
- Fix Python2 executable on Fedora 30

* Fri Jan 24 2020 Antonio Trande <sagitterATfedoraproject.org> - 0.18.2-2
- Build Python2 version on Fedora 30

* Fri Jan 24 2020 Antonio Trande <sagitterATfedoraproject.org> - 0.18.2-1
- Release 0.18.2

* Sat Oct 12 2019 Antonio Trande <sagitterATfedoraproject.org> - 0.18.0-2
- Use python3_version_nodots macro

* Sat Oct 12 2019 Antonio Trande <sagitterATfedoraproject.org> - 0.18.0-1
- Release 0.18.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.17.1-0.5.20190506git23989c4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.17.1-0.4.20190506git23989c4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-0.3.20190506git23989c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Antonio Trande <sagitterATfedoraproject.org> - 0.17.1-0.2.20190506git23989c4
- Bump to a pre-release 0.17.1, commit #23989c4
- Unversioned commands point to Python3 on Fedora
- Obsolete Python2 version on Fedora

* Tue Apr 09 2019 Antonio Trande <sagitterATfedoraproject.org> - 0.17.1-0.1.20190313gitc423752
- Bump to a pre-release 0.17.1 (fix rhbz#1698160, upstream bug #488)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.17.0-1
- Release 0.17.0

* Wed Oct 24 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.17.0-0.1.20181019gitbee0f3b
- Bump to a pre-release 0.17.0

* Wed Oct 24 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-13.20181019gitbee0f3b
- Update to the commit #bee0f3b
- Perform all Python3 tests

* Fri Sep 21 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-12.20180917gitaf02ef6
- Update to the commit #af02ef6

* Sun Aug 26 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-11
- Prepare SPEC file for deprecation of Python2 on fedora 30+
- Prepare SPEC file for Python3-modules packaging on epel7

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.16.0-9
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 14 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-7
- Use versioned Python2 packages

* Fri Dec 15 2017 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-6
- Python3 built on epel7

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.16.0-3
- Rebuild for Python 3.6

* Tue Dec 13 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-2
- BR Python2 dependencies unversioned on epel6

* Tue Dec 13 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.16.0-1
- Update to 0.16.0

* Wed Aug 17 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-10
- Rebuild for Python 3.5.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-7
- Renamed Python2 package

* Thu Dec 10 2015 Antonio Trande <sagitterATfedoraproject.org> - 0.15.2-6
- SPEC file adapted to recent guidelines for Python

* Fri Nov 13 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-5
- Rebuild

* Fri Nov 13 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-4
- Python3 tests temporarily disabled with Python35

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 0.15.2-3 - Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Sep 14 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-2
- Patch0 updated

* Fri Sep 11 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.2-1
- Update to 0.15.2

* Wed Sep 02 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-4
- Added patch to exclude failed tests (patch0)

* Wed Aug 26 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-3
- Added python-provides macro

* Thu Jul 30 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-2
- Fixed Python3 packaging on Fedora
- Removed configparser backport (patch1)

* Tue Jul 28 2015 Antonio Trande <sagitter@fedoraproject.org> 0.15.0-1
- Initial build
