%define libedit_version 3.1
%define libedit_release 20230828

Summary:        The NetBSD Editline library
Name:           libedit
Version:        3.1.20230828
Release:        1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.thrysoee.dk/editline/libedit-%{libedit_release}-%{libedit_version}.tar.gz
License:        BSD
Url:            https://www.thrysoee.dk/editline/
Group:          Applications/Libraries
Requires:       ncurses
BuildRequires:  ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD
Editline library. It provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

%package        devel
Summary:        The NetBSD Editline library
Group:          Development/Libraries
Requires:       libedit = %{version}-%{release}

%description devel
Development files for libedit

%prep
%setup -qn libedit-%{libedit_release}-%{libedit_version}

%build
./configure \
--prefix=%{_prefix} \
--disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}/%{_mandir}/man3/history.3*

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
%license COPYING
    %defattr(-,root,root,0755)
    %exclude %{_libdir}/debug
    %{_libdir}/*.so.*
    %{_mandir}/*

%files devel
    %defattr(-,root,root,0755)
    %{_libdir}/*.so
    %{_libdir}/pkgconfig
    %{_includedir}/*

%changelog
*   Thu Mar 01 2024 Suresh Thelkar <sthelkaro@microsoft.com> - 3.1.20230828-1
-   Upgrade to 3.1.20230828-1

*   Fri Mar 11 2022 Jon Slobodzian <joslobo@microsoft.com> - 3.1.20210910-1
-   Upgrade to 3.1.20210910-1

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.20180525-6
-   Removing the explicit %%clean stage.

*   Wed Aug 05 2020 Andrew Phelps <anphel@microsoft.com> 3.1.20180525-5
-   Remove conflicting file _mandir/man3/history.3*

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.1.20180525-4
-   Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 3.1.20180525-3
-   Verified license. Removed sha1. Fixed Source0 URL.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1.20180525-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.20180525-1
-   Initial
