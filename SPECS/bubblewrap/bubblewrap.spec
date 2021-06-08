Summary:        setuid implementation of a subset of user namespaces.
Name:           bubblewrap
Version:        0.3.0
Release:        5%{?dist}
License:        LGPLv2+
URL:            https://github.com/containers/bubblewrap/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/containers/bubblewrap/releases/download/v%{version}/bubblewrap-%{version}.tar.xz
# This vulnerability only applies to version >= 0.4.0. Ignore the warnings against it.
Patch0:         CVE-2020-5291.nopatch
Patch1:         CVE-2019-12439.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libcap-devel
Requires:       libcap
%description
Bubblewrap could be viewed as setuid implementation of a subset of user namespaces. Emphasis on subset - specifically relevant to the above CVE, bubblewrap does not allow control over iptables.

The original bubblewrap code existed before user namespaces - it inherits code from xdg-app helper which in turn distantly derives from linux-user-chroot.

%prep
%setup -q
%patch1 -p1
%build

./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --disable-silent-rules \
    --with-priv-mode=none
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/bwrap
%{_datadir}/bash-completion/completions/bwrap

%changelog
* Thu May 21 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.3.0-5
- Fixed CVE-2019-12439

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.3.0-4
- Added %%license line automatically

*   Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> 0.3.0-3
-   Ignore CVE-2020-5291.
-   Update Source0 and URL.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.3.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 0.3.0-1
-   Updated to version 0.3.0.
*   Thu Aug 03 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.8-1
-   Initial build.  First version
