Summary:        Versatile resource statistics tool
Name:           dstat
Version:        0.7.4
Release:        3%{?dist}
License:        GPLv2
URL:            https://github.com/dstat-real/dstat
#Source0:       %{url}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Dstat gives you detailed selective information in columns and clearly indicates in what magnitude and unit the output is displayed. Less confusion, less mistakes. And most importantly, it makes it very easy to write plugins to collect your own counters and extend in ways you never expected.

%prep
%setup -q

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%license COPYING
%doc %{_mandir}/*
%{_bindir}/dstat
%{_datadir}/dstat/

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.4-3
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.4-2
- Added %%license line automatically

*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.7.4-1
-   Bumping version up to 0.7.4.
-   Fixed 'Source0' and 'URL' tags.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.2-2
-   GA - Bump release of all rpms
*   Mon Nov 30 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
-   Initial build.  First version
