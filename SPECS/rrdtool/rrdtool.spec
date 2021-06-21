Summary:        Round Robin Database Tool to store and display time-series data
Name:           rrdtool
Version:        1.7.0
Release:        5%{?dist}
License:        GPLv2 or GPLv2 with FLOSS License Exception
URL:            https://oss.oetiker.ch/rrdtool/
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/oetiker/rrdtool-1.x/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	pkg-config
BuildRequires:	libpng-devel
BuildRequires:	pango-devel
BuildRequires:	libxml2-devel
BuildRequires:	pixman-devel
BuildRequires:	freetype-devel
BuildRequires:	fontconfig-devel
BuildRequires:	cairo-devel
BuildRequires:	glib-devel
BuildRequires:	systemd
Requires:	    systemd

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}	\
	--disable-tcl		\
	--disable-python 	\
	--disable-perl		\
	--disable-lua		\
	--disable-examples	\
        --with-systemdsystemunitdir=%{_unitdir} \
        --disable-docs 		\
	--disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

#%check
#make %{?_smp_mflags} -k check

%post
/sbin/ldconfig
%systemd_post rrdcached.service

%preun
%systemd_preun rrdcached.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rrdcached.service

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so*
%{_unitdir}/rrdcached.service
%{_unitdir}/rrdcached.socket
%exclude %{_datadir}/locale/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat May 09 00:21:18 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.7.0-5
- Added %%license line automatically

*   Thu Apr 30 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.7.0-4
-   Rename freetype2-devel to freetype-devel.
*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 1.7.0-3
-   Verified license. Removed sha1. Fixed Source0 URL and URL.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 1.7.0-1
-   Updated to version 1.7.0
*   Wed Apr 5 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.0-1
-   Initial version
