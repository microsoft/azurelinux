Summary:	File manager
Name:		mc
Version:	4.8.21
Release:        4%{?dist}
License:	GPLv3+
URL:		http://www.midnight-commander.org
Group:		Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	https://ftp.midnight-commander.org/%{name}-%{version}.tar.xz
Patch0:		disable-extfs-test.patch
Requires:	glib pcre slang
BuildRequires:	glib-devel pcre-devel slang-devel

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%setup -q
%patch0 -p1
%build
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=/etc
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%license COPYING
/etc/*
/usr/bin/*
%exclude /usr/lib
/usr/libexec/*
/usr/share/*
%exclude /usr/src

%changelog
* Sat May 09 00:21:37 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.8.21-4
- Added %%license line automatically

*   Tue Apr 21 2020 Eric Li <eli@microsoft.com> 4.8.21-3
-   Fix Source0: and delete sha1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.8.21-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.8.21-1
-   Update to version 4.8.21
*   Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.8.19-2
-   Disable extfs test
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.8.19-1
-   Update package version
*   Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.8.17-1
-   Initial build. First version
