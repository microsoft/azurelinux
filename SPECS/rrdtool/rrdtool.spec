	
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}


Summary:        Round Robin Database Tool to store and display time-series data
Name:           rrdtool
Version:        1.7.0
Release:        6%{?dist}
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
	
%package -n python3-rrdtool
%{?python_provide:%python_provide python3-rrdtool}
Summary: Python RRDtool bindings
BuildRequires: python3-devel, python3-setuptools, python-setuptools
%{?__python3:Requires: %{__python3}}
Requires: %{name} = %{version}-%{release}
 
%description -n python3-rrdtool
Python RRDtool bindings.

%package ruby
Summary: Ruby RRDtool bindings
BuildRequires: ruby, ruby-devel
Requires: %{name} = %{version}-%{release}
 
%description ruby
The %{name}-ruby package includes RRDtool bindings for Ruby.

%package tcl
Summary: Tcl RRDtool bindings
BuildRequires: tcl-devel >= 8.0
Requires: tcl >= 8.0
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}
 
%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.

%package lua
Summary: Lua RRDtool bindings
BuildRequires: lua, lua-devel
%if "%{luaver}" != ""
Requires: lua(abi) = %{luaver}
%endif
Requires: %{name} = %{version}-%{release}
 
%description lua
The %{name}-lua package includes RRDtool bindings for Lua.


%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}	\
	--enable-tcl-site \
    --with-tcllib=%{_libdir} \
	--enable-python 	\
	--enable-ruby \
	--disable-perl		\
	--disable-examples	\
        --with-systemdsystemunitdir=%{_unitdir} \
        --disable-docs 		\
	--disable-static
	
perl -pi.orig -e 's|-Wl,--rpath -Wl,\$\(EPREFIX\)/lib||g' \
    bindings/ruby/extconf.rb
sed -i 's|extconf.rb \\|extconf.rb --vendor \\|' bindings/Makefile

make %{?_smp_mflags}

pushd bindings/python
%py3_build
popd

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

pushd bindings/python
%py3_install
popd

rm -rf %{buildroot}%{_libdir}/python2.7
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
	
%files -n python3-rrdtool
%doc bindings/python/COPYING bindings/python/README.md
%{python3_sitearch}/rrdtool*.so
%{python3_sitearch}/rrdtool-*.egg-info

%files tcl
%doc bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir}/rrdtool/*.tcl

%files lua
%doc bindings/lua/README
%{lualibdir}/*

%files ruby
%doc bindings/ruby/README
%{_libdir}/ruby

%changelog
* Mon Jan 11 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.7.0-6
- Build with lua, python3, and ruby support.

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
