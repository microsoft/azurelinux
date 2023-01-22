%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.9.27
Release:        2%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://www.ansible.com
Source0:        https://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
BuildRequires:  python3-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  python3-devel
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-yamlloader
Requires:       python3-jinja2

BuildArch:      noarch

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root %{buildroot}

%check
pip3 install 'tox>=3.27.1,<4.0.0'
cd build/lib/ansible_test/_data && tox

%files
%defattr(-, root, root)
%license licenses
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Thu Jan 12 2023 Sam Meluch <sammeluch@microsoft.com> - 2.9.27-2
- Update version of tox for package tests

* Mon May 02 2022 Nick Samson <nisamson@microsoft.com> - 2.9.27-1
- Upgraded to 2.9.27-1 to fix CVE-2021-3620

* Thu Oct 21 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.9.23-2
- Add missing runtime dependencies.

* Fri Oct 15 2021 Bala <balakumaran.kannan@microsoft.com> - 2.9.23-1
- Upgrade to version 2.9.23, which resolves CVE-2021-3583, CVE-2020-14330 and CVE-2021-20228
- Switching to building with Python 3 to fix tests.

* Tue Jun 15 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.9.18-1
- Upgrade to version 2.9.18, which resolves CVE-2021-20191 and CVE-2021-20178

* Wed Dec 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.9.12-1
- Upgrade to version 2.9.12, which resolves CVE-2020-10744

* Tue Jun 02 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9.9-1
- Upgrade to version 2.9.9, which resolves CVE-2020-1733 and CVE-2020-1738.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.9.5-2
- Added %%license line automatically

* Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> 2.9.5-1
- Version update to 2.9.5. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.7.6-1
- Version update to 2.7.6, fix CVE-2018-16876

* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.6.4-1
- Version update to 2.6.4

* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
- Version update to 2.4.0.0

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
- Use python2 explicitly

* Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
- Version update

* Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
- Initial build. First version
