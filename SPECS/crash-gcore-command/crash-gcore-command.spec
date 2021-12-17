Name:          crash-gcore-command
Version:       1.5.1
Release:       2%{?dist}
Summary:       gcore extension module for crash utility
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/crash-utility/crash-extensions
Source0:       https://github.com/crash-utility/crash-extensions/raw/master/%{name}-%{version}.tar.gz
Source1:       gcore_defs.patch
License:       GPLv2+
BuildRequires: zlib-devel
BuildRequires: crash-devel >= 7.2.5
Requires:      crash >= 7.2.5
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
Command for creating a core dump file of a user-space task that was
running in a kernel dumpfile.

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch x86_64
make -f gcore.mk ARCH=SUPPORTED TARGET=X86_64
%endif
%ifarch aarch64
patch -p1 < %{SOURCE1}
make -f gcore.mk ARCH=SUPPORTED TARGET=ARM64
%endif

%install
mkdir -p %{buildroot}%{_libdir}/crash/extensions/
install -pm 755 gcore.so %{buildroot}%{_libdir}/crash/extensions/

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/crash/extensions/gcore.so
%doc COPYING

%changelog
*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.1-2
-   Removing the explicit %%clean stage.
-   License verified.

*   Wed Jun 17 2020 Joe Schmitt <joschmit@microsoft.com> 1.5.1-1
-   Update version to 1.5.1.
-   Update URL.
-   Update Source0.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.4.0-2
-   Added %%license line automatically
*   Wed Mar 25 2020 Emre Girgin <mrgirgin@microsoft.com> 1.4.0-1
-   Split the crash.spec into two 'crash.spec' and 'crash-gcore-command.spec'.
-   Updated URL and Source0 links. Updated license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.2.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 7.2.3-1
-   Upgrading to version 7.2.3
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-2
-   Aarch64 support
*   Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-1
-   Update version to 7.1.8 (it supports linux-4.9)
-   Disable a patch - it requires a verification.
*   Fri Oct 07 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-2
-   gcore-support-linux-4.4.patch
*   Fri Sep 30 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-1
-   Update version to 7.1.5 (it supports linux-4.4)
-   Added gcore plugin
-   Remove zlib-devel requirement from -devel subpackage
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1.4-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1.4-1
-   Updated to version 7.1.4
*   Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 7.1.3-1
-   Initial build. First version
