Summary:        GIO-based library with Unix/Linux specific API
Name:           libgsystem
Version:        2015.2
Release:        8%{?dist}
Group:          Development/Libraries
Source0:        https://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.xz/e388e3ad3c2b527479cc8512f6ad9a37/%{name}-%{version}.tar.xz
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/LibGSystem
Vendor:         Microsoft Corporation
Distribution:   Mariner

# We always run autogen.sh
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
# For docs
BuildRequires:  gtk-doc
# Core requirements
BuildRequires:  glib-devel
BuildRequires:  pkg-config
BuildRequires:  attr-devel
BuildRequires:  rpm
BuildRequires:  autoconf
BuildRequires:  which
BuildRequires:  pcre-devel
BuildRequires:  libcap-devel
BuildRequires:  libffi-devel
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-gobject-introspection
Requires:   glib
Requires:   libcap
Requires:   libffi
Requires:   pcre
Requires:   gobject-introspection
%description
LibGSystem is a GIO-based library usable as a "git submodule",
targeted primarily for use by operating system components.

%package        devel
Summary:        Development files for libgsystem
Requires:       %{name} = %{version}
Requires:       gobject-introspection-devel

%description    devel
The libgsystem-devel package contains libraries and header files for
developing applications.

%prep
%setup -q

%build
alias python=python3
env NOCONFIGURE=1 ./autogen.sh
%configure  --disable-silent-rules \
            --enable-gtk-doc
make %{?_smp_mflags}

%install
alias python=python3
make install DESTDIR=%{buildroot} INSTALL="install -p -c"
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license COPYING
%doc COPYING README
%{_libdir}/*.so*
%{_libdir}/girepository-1.0/GSystem-1.0.typelib

%files devel
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*
%{_datadir}/gir-*/*.gir

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2015.2-8
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2015.2-7
- Removing the explicit %%clean stage.

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2015.2-6
- Remove unused gobject-introspection-python requirement
- Explicity specify python3-gobject-introspection requirement

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2015.2-5
- Added %%license line automatically

*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2015.2-4
-   Fixed "Source0" tag - switched to an online source.
-   License verified.
-   Removed "%%define sha1".
-   Replaced tabs with spaces.
-   Made sure we have on package per line for (Build)Requires.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2015.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 18 2018 Keerthana K <keerthanak@vmware.com> 2015.2-2
-   Removed % from autosetup in the changelog to address the
-   build break with latest RPM version.
*   Wed Apr 26 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2015.2-1
-   Updated to version 2015.2
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-4
-   BuildRequired attr-devel.
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 2015.1-3
-   Use setup instead of autosetup
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2015.1-2
-   GA - Bump release of all rpms
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 2014.2-1
-   Initial build. First version
