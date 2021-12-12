%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global srcname pytest-relaxed

%global desc  pytest-relaxed provides 'relaxed' test discovery for pytest. \
It is the spiritual successor to https://pypi.python.org/pypi/spec, but \
is built for pytest instead of nosetests, and rethinks some aspects of \
the design (such as a decreased emphasis on the display side of things.)

Summary:   Relaxed test discovery for pytest
Name:      python-%{srcname}
Version:   1.1.5
Release:   11%{?dist}
License:   BSD
URL:       https://github.com/bitprophet/pytest-relaxed
#Source0:  https://github.com/bitprophet/pytest-relaxed/archive/%{version}/%{srcname}-%{version}.tar.gz
Source0:   https://github.com/bitprophet/pytest-relaxed/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch: noarch

%description
%{desc}

%package -n python3-%{srcname}
Summary:       %{summary}
BuildRequires: python3-devel 
BuildRequires: python3-decorator
BuildRequires: python3-pytest < 5
BuildRequires: python-setuptools
BuildRequires: python-six
# No need to specify runtime dependencies because they'll be auto-generated

%description -n python3-%{srcname}
%{desc}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
PYTHONPATH=%{buildroot}%{python3_sitelib} pytest-%{python3_version}

%files -n python3-%{srcname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/pytest_relaxed-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/pytest_relaxed/

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.1.5-11
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sat May 30 2020 Paul Howarth <paul@city-fan.org> - 1.1.5-9
- Avoid FTBFS with pytest 5
* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-8
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Tue Jan 14 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-6
- Make the release strictly bigger than the last two builds (rhbz #1788771)
* Mon Oct 07 2019 Othman Madjoudj <athmane@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5 (rhbz #1697355)
* Sun Oct 06 2019 Othman Madjoudj <athmane@fedoraproject.org> - 1.1.5-5
- Drop python2 subpackage (python2 eol)
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Thu Jun 27 2019 Paul Howarth <paul@city-fan.org> - 1.1.5-1
- Update to 1.1.5
- Re-enable the test suite
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.7
* Thu Jun 28 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-5
- Disable the test suite until a version compatible with pytest > 3.3 is available
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Fri Nov 17 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-2
- Minor packaging fixes
* Thu Nov 16 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-1
- Initial spec