%global apiver 2.68
%define BaseVersion %(echo %{version} | cut -d. -f1-2)

Summary:        C++ interface to the glib
Name:           glibmm
Version:        2.70.0
Release:        2%{?dist}
License:        LGPLv2+
URL:            https://developer.gnome.org/glibmm/stable/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glibmm/%{BaseVersion}/glibmm-%{version}.tar.xz
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  glib-devel 
BuildRequires:  glib-schemas
BuildRequires:  graphviz
BuildRequires:  libsigc++30
BuildRequires:  libxslt
BuildRequires:  m4
BuildRequires:  meson
BuildRequires:  mm-common
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter

%if %{with_check}
BuildRequires:  glib-networking
%endif

Requires:	libsigc++30
Requires:	glib >= 2.69.1
Requires:	gobject-introspection >= 1.50.0
Requires:	perl-XML-Parser

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.

%package devel
Summary: Header files for glibmm
Group: Applications/System
Requires: 	%{name} = %{version}
Requires:	glib-devel
Requires:   libsigc++30
%description devel
These are the header files of glibmm.

%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++30-doc
 
%description    doc
This package contains the full API documentation for %{name}.

%prep
%setup -q -n glibmm-%{version}

%build
%meson -Dbuild-documentation=true
%meson_build

%install
%meson_install

chmod +x %{buildroot}%{_libdir}/glibmm-%{apiver}/proc/generate_wrap_init.pl
chmod +x %{buildroot}%{_libdir}/glibmm-%{apiver}/proc/gmmproc

%check
#need read content from /etc/fstab, which couldn't be empty
echo '#test' > /etc/fstab
export GIO_EXTRA_MODULES=/usr/lib/gio/modules
%meson_test

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/glibmm-%{apiver}/proc/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/glibmm-%{apiver}/include/*
%{_libdir}/giomm-%{apiver}/include/*
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_datadir}/devhelp/
%doc %{_docdir}/glibmm-%{apiver}/

%changelog
* Mon Feb 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.70.0-2
- Fix %check section

* Thu Feb 03 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.70.0-1
- Update to v2.70.0
- Refactor to support new meson build system
- libsigc++30, instead of libsigc++20
- Renaming glibmm24 to glibmm
- Add doc package

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.56.0-8
- Remove libtool archive files from final packaging

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.56.0-7
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-6
- Renaming glibmm to glibmm

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-5
- Renaming XML-Parser to perl-XML-Parser

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-4
- Renaming libsigc++ to libsigc++20

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> 2.56.0-3
- Fix Source0: and delete sha1. Verified License. Fixed URL.  Fixed formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.56.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.56.0-1
- Update to version 2.56.0

* Thu Aug 24 2017 Rongrong Qiu <rqiu@vmware.com> 2.50.1-2
- add buildrequires for make check for bug 1900286

* Fri May 26 2017 Harish Udaiya Kumar <hudaiykumar@vmware.com> 2.50.1-1
- Downgrade to stable version 2.50.1

* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.53.1-1
- Update to version 2.53.1

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.1-2
- Modified %check

* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.1-1
- Updated to version 2.48.1-1

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.3.1-2
- GA - Bump release of all rpms

* Thu Apr 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.47.3.1-1
- Updated to version 2.47.3.1

* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.46.3-1
- Updated to version 2.46.3

* Tue Jul 7 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
- Created devel subpackage. Added Summary.

* Tue Jun 23 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
- Added glib-schemas to build requirements.

* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
- Initial version
