%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.22.0
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/cri-tools
#Source0:       https://github.com/kubernetes-sigs/cri-tools/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         no-git-in-build.patch
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

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
%{_datadir}/doc/%{name}

%clean
rm -rf %{buildroot}/*

%changelog
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.22.0-5
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.22.0-4
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.22.0-3
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.22.0-2
- Increment release for force republishing using golang 1.16.9

*   Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.22.0-1
-   Move to version 1.22.0 and build using golang 1.16.7.
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
