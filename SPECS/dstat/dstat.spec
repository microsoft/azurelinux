Summary:        Versatile resource statistics tool
Name:           dstat
Version:        0.7.4
Release:        3%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/dstat-real/dstat
Source0:        https://github.com/dstat-real/dstat/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         fix-py3-deprecation-warning.patch
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-six

%description
Dstat gives you detailed selective information in columns and clearly indicates in what magnitude and unit the output is displayed.
Less confusion, less mistakes. And most importantly, it makes it very easy to write plugins to collect your own counters and extend
in ways you never expected.

%prep
%autosetup -p1

%install
%make_install
# Installed scripts use "/usr/bin/env python"- we want to explicitly specify python3 here
%{_bindir}/pathfix.py -pni %{_bindir}/python3 %{buildroot} %{buildroot}%{_bindir}/dstat

%files
%defattr(-, root, root, 0755)
%license COPYING
%{_mandir}/*
%{_bindir}/dstat
%{_datadir}/dstat/

%changelog
* Thu Jan 06 2022 Thomas Crain <thcrain@microsoft.com> - 0.7.4-3
- Use python3 in place of ambiguous "/usr/bin/env python" in installed scripts
- Add patch to fix DeprecationWarning
- Add explicit dependency on python3-six
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.4-2
- Added %%license line automatically

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.7.4-1
- Bumping version up to 0.7.4.
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.2-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.2-2
- GA - Bump release of all rpms

* Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
- Initial build.  First version
