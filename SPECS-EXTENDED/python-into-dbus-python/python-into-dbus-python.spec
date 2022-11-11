Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname into-dbus-python

Name:           python-%{srcname}
Version:        0.07
Release:        6%{?dist}
Summary:        Transformer to dbus-python types

License:        ASL 2.0
URL:            https://github.com/stratis-storage/into-dbus-python
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%if %{with_check}
BuildRequires:  python3-pip
%endif

%global _description \
Facilities for converting an object that inhabits core Python types, e.g.,\
lists, ints, dicts, to an object that inhabits dbus-python types, e.g.,\
dbus.Array, dbus.UInt32, dbus.Dictionary based on a specified dbus signature.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-dbus-signature-pyparsing
BuildRequires:  python3-dbus
BuildRequires:  python3-hypothesis
BuildRequires:  python3-hs-dbus-signature
Requires:       python3-dbus-signature-pyparsing
Requires:       python3-dbus

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest==7.1.3 sortedcontainers
pip3 install .
pytest -v tests

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/into_dbus_python/
%{python3_sitelib}/into_dbus_python-*.egg-info/

%changelog
* Tue Nov 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.07-6
- Freezing "pytest" deps to version 7.1.3 to avoid regressions.

* Thu Apr 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.07-5
- Drop BR on pytest & pip install latest deps to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.07-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 6 2019 mulhern <amulhern@redhat.com> - 0.07-2
- Use tracing profile for tests

* Fri Sep 6 2019 mulhenr <amulhern@redhat.com> - 0.07-1
- New version: 0.07

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.06-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.06-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Ilya Gradina <ilya.gradina@gmail.com> - 0.06-1
- Initial package
