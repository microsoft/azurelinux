Summary:        Terminal multiplexer
Name:           tmux
Version:        2.7
Release:        4%{?dist}
License:        GPLv3+
URL:            https://tmux.github.io/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    tmux=a12bb094bf0baf0275b6d5cc718c938639712e97
Patch0:         CVE-2022-47016.patch
Requires:       libevent ncurses
BuildRequires:  libevent-devel ncurses-devel
%description
Terminal multiplexer
%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
/usr/bin/*
%exclude /usr/lib
/usr/share/*
%exclude /usr/src
%changelog
* Wed Feb 08 2023 Dan Streetman <ddstreet@microsoft.com> - 2.7-4
- CVE-2022-47016

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.7-1
-   Updated to version 2.7.
*   Tue May 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4-1
-   Updated to version 2.4. Added make check.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
-   Updated to version 2.3.
*   Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
-   Initial build.  First version
