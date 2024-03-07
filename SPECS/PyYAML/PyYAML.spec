Summary:        YAML parser and emitter for Python
Name:           PyYAML
Version:        5.4.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/yaml/pyyaml
Source0:        https://github.com/yaml/pyyaml/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  libyaml-devel
BuildRequires:  python3
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       libyaml
Requires:       python3
Requires:       python3-libs
Provides:       python3-%{name} = %{version}-%{release}
Provides:       python3-yaml = %{version}-%{release}

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that allow
to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistence.

%prep
%autosetup -p1 -n pyyaml-%{version}
find -type f -name "*.c" -delete -print

%build
export PYYAML_FORCE_CYTHON=1
%py3_build

%install
mkdir -p %{buildroot}%{_bindir}
%py3_install
chmod a-x examples/yaml-highlight/yaml_hl.py

%check
%python3 setup.py test

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README examples
%{python3_sitelib}/*

%changelog
* Tue Nov 07 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4.1-1
- Upgrade to 5.4 to fix CVE-2020-1747 and CVE-2020-14343.

* Fri Oct 27 2023 Xiaohong Deng <xiaohongdeng@microsoft.com> - 5.2-1
- Upgrade to 5.2

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 3.13-8
- Rebuild C source files using Cython for Python 3.9 compatibility

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 3.13-7
- Remove python2 package, have main package contain python3 version
- Add license to python3 package
- Lint spec
- License verified

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 3.13-6
- Provide python3-yaml
- Update URLs to https

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.13-5
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.13-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 16 2019 Tapas Kundu <tkundu@vmware.com> 3.13-3
- Added lib3 changes for CVE-2017-18342
- change default loader for yaml.add_constructor
- Add custom constructors to multiple loaders

* Thu Mar 28 2019 Ankit Jain <ankitja@vmware.com> 3.13-2
- Fix for CVE-2017-18342

* Thu Sep 20 2018 Tapas Kundu <tkundu@vmware.com> 3.13-1
- Updated to release 3.13

* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> 3.12-2
- Adding python3 support.

* Tue Apr 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.12-1
- Updated version to 3.12

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11-2
- GA - Bump release of all rpms

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
