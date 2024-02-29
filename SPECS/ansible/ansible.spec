Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.14.12
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://www.ansible.com
Source0:        https://github.com/ansible/ansible/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-devel
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-libs
Requires:       python3-yamlloader
Requires:       python3-jinja2
Requires:       python3-resolvelib

BuildArch:      noarch

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install -O1 --skip-build \
    --root %{buildroot}

%check
python3 setup.py test

%files
%defattr(-, root, root)
%license licenses
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Tue Dec 26 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 2.14.12-1
- Update to v2.14.12 to fix CVE-2023-5764

* Mon Jun 26 2023 Sam Meluch <sammeluch@microsoft.com> - 2.12.1-3
- add python-resolvelib dependency to fix ansible-galaxy

* Mon Jan 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.12.1-2
- Remove python-setuptools in favor of python3-setuptools

* Tue Jan 04 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.12.1-1
- Upgrade to version 2.12.1

* Tue Jun 15 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.9.18-1
- Upgrade to version 2.9.18, which resolves CVE-2021-20191 and CVE-2021-20178

* Wed Dec 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.9.12-1
- Upgrade to version 2.9.12, which resolves CVE-2020-10744

*   Tue Jun 02 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.9.9-1
-   Upgrade to version 2.9.9, which resolves CVE-2020-1733 and CVE-2020-1738.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.9.5-2
-   Added %%license line automatically

*   Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> 2.9.5-1
-   Version update to 2.9.5. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.7.6-1
-   Version update to 2.7.6, fix CVE-2018-16876

*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.6.4-1
-   Version update to 2.6.4

*   Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
-   Version update to 2.4.0.0

*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
-   Use python2 explicitly

*   Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
-   Version update

*   Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
-   Initial build. First version
