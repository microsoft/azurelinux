Summary:        CRI tools
Name:           cri-tools
Version:        1.23.0
Release:        13%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/kubernetes-sigs/cri-tools
#Source0:       https://github.com/kubernetes-sigs/cri-tools/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         no-git-in-build.patch
%define debug_package %{nil}
BuildRequires:  glib-devel
BuildRequires:  glibc-devel
BuildRequires:  golang

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup -p1

%build
export VERSION="v%{version}"
make %{?_smp_mflags}


%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./build/bin/crictl
install -p -m 755 -t %{buildroot}%{_bindir} ./build/bin/critest

install -m 755 -d %{buildroot}%{_docdir}/%{name}
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./CHANGELOG.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./CONTRIBUTING.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./OWNERS
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./README.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./code-of-conduct.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./docs/validation.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./docs/roadmap.md
install -p -m 644 -t %{buildroot}%{_docdir}/%{name} ./docs/crictl.md

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_docdir}/%{name}

%changelog
* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.23.0-2
- Bump release to rebuild with golang 1.18.3

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - 1.23.0-1
- Update to version 1.23.0

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22.0-2
-   Removing the explicit %%clean stage.

*   Thu Sep 16 2021 Andrew Phelps <anphel@microsoft.com> 1.22.0-1
-   Update version to 1.22.0

*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.11.1-8
-   Increment release to force republishing using golang 1.15.13.

*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.11.1-7
-   Increment release to force republishing using golang 1.15.11.

*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.11.1-6
-   Increment release to force republishing using golang 1.15.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.11.1-5
-   Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.11.1-4
-   Renaming go to golang

*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.11.1-3
-   Fixed "Source0" and "URL" tags.
-   License verified.
-   Removed "%%define sha1".

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-   Initial build added for Photon.
