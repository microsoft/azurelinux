Summary:        Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.
Name:           iotop
Version:        0.6
Release:        10%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Monitoring
URL:            http://guichaz.free.fr/iotop/
Source0:        http://guichaz.free.fr/iotop/files/%{name}-%{version}.tar.gz
# Fix build issue with Python 3
# https://repo.or.cz/iotop.git/commit/99c8d7cedce81f17b851954d94bfa73787300599
Patch0:         %{name}-itervalues.patch
# Build explicitly with Python 3
# https://repo.or.cz/iotop.git/commit/5bdd01c3b3b1c415c71b00b2374538995f63597c
Patch1:         %{name}-use-py3.patch
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-curses
BuildArch:      noarch

%description
Iotop is a Python program with a top like UI used to show the processes and their corresponding IO activity.

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

# %%check
# This package does not have any tests

%files
%defattr(-,root,root)
%license COPYING
%doc NEWS THANKS
%{python3_sitelib}/%{name}*.egg-info
%{python3_sitelib}/%{name}/
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}*

%changelog
* Wed May 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.6-10
- Add dependency on python3-curses

* Tue Jan 25 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.6-9
- Build with python3 instead of python2
- Add upstream patches for building with python3
- Document lack of tests
- Lint spec

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6-8
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6-7
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.6-6
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jun 16 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-5
- Use python2 explicitly

* Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.6-4
- Add python2 to Requires

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-3
- Fix arch

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6-2
- GA - Bump release of all rpms

* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6-1
- Initial build. First version
