Summary:        A library for retrieving information onrunning processes and system utilization
Name:           python-psutil
Version:        5.6.3
Release:        5%{?dist}
Url:            https://pypi.python.org/pypi/psutil
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         disable-tests-python-psutil.patch

%description
psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.

%package -n     python3-psutil
Summary:        A library for retrieving information onrunning processes and system utilization
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  ncurses-term
BuildRequires:  coreutils
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-six
BuildRequires:  python3-test
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pbr
%endif
Requires:       python3
Requires:       python3-libs

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
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 linecache2
$easy_install_3 pytest
$easy_install_3 mock
$easy_install_3 unittest2
LANG=en_US.UTF-8 make test PYTHON=python%{python3_version}

%files -n python3-psutil
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 5.6.3-5
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

* Fri Aug 10 2017 Xiaolin Li <xiaolinl@vmware.com> - 5.2.2-2
- Fixed make check error.

* Wed Apr 26 2017 Xialin Li <xiaolinl@vmware.com> - 5.2.2-1
- Initial packaging for Photon
