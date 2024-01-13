Summary:        A library for retrieving information onrunning processes and system utilization
Name:           python-psutil
Version:        5.9.7
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/psutil
Source0:        https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# A small number of tests do not reliably run in Mariner chroots- we can skip these tests
Patch0:         disable-tests-python-psutil.patch
BuildRequires:  gcc
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  coreutils
BuildRequires:  curl-devel
BuildRequires:  ncurses-term
BuildRequires:  openssl-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-test
%endif

%description
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.

%package -n     python3-psutil
Summary:        A library for retrieving information onrunning processes and system utilization
Requires:       python3

%description -n python3-psutil
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.
It is useful mainly for system monitoring, profiling and limiting process resources and management of running processes. It implements many functionalities offered by command line tools
such as: ps, top, lsof, netstat, ifconfig, who, df, kill, free, nice, ionice, iostat, iotop, uptime, pidof, tty, taskset, pmap. It currently supports Linux, Windows, OSX, Sun Solaris,
FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures, with Python versions from 2.6 to 3.6 (users of Python 2.4 and 2.5 may use 2.1.3 version). PyPy is also known to work.

%prep
%autosetup -p 1 -n psutil-release-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install linecache2 pytest mock unittest2
LANG=en_US.UTF-8 PYTHONPATH=%{buildroot}%{python3_sitelib} make test PYTHON=python%{python3_version}

%files -n python3-psutil
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Jan 12 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 5.9.7-1
- Upgrade to latest upstream version (v5.9.7)
- Remove the disable-tests-python-psutil.patch

* Tue Jan 25 2022 Thomas Crain <thcrain@microsoft.com> - 5.9.0-1
- Upgrade to latest upstream version
- Update skipped tests patch
- Lint spec
- License verified

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 5.6.3-6
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 5.6.3-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.6.3-4
- Added %%license line automatically

* Tue Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.6.3-3
- Rename ncurses-terminfo to ncurses-term.

* Tue Apr 07 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.6.3-2
- Remove python-enum from build requires.

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 5.6.3-1
- Update to version 5.6.3. Source0 fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 5.4.7-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> - 5.4.7-2
- Fix makecheck

* Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> - 5.4.7-1
- Updated to version 5.4.7

* Thu Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.2.2-2
- Fixed make check error.

* Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> - 5.2.2-1
- Initial packaging for Photon
