Summary:        C++ interface to the glib
Name:           glibmm24
%define BaseVersion 2.56
Version:        %{BaseVersion}.0
Release:        7%{?dist}
License:        LGPLv2+
URL:            https://developer.gnome.org/glibmm/stable/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnome.org/pub/GNOME/sources/glibmm/%{BaseVersion}/glibmm-%{version}.tar.xz
BuildRequires:  python2 >= 2.7
BuildRequires:  libsigc++20 >= 2.10.0
BuildRequires:  glib-devel glib-schemas
%if %{with_check}
BuildRequires:  glib-networking
%endif

Requires:	libsigc++20 >= 2.10.0
Requires:	glib >= 2.50.0
Requires:	gobject-introspection >= 1.50.0
Requires:	perl-XML-Parser

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.

%package devel
Summary: Header files for glibmm
Group: Applications/System
Requires: %{name} = %{version}
Requires:	glib-devel libsigc++20
%description devel
These are the header files of glibmm.

%prep
%setup -q -n glibmm-%{version}
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%check
#need read content from /etc/fstab, which couldn't be empty
echo '#test' > /etc/fstab
export GIO_EXTRA_MODULES=/usr/lib/gio/modules; make check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/glibmm-2.4/proc/*
%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/glibmm-2.4/include/*
%{_libdir}/giomm-2.4/include/*
%{_includedir}/*
%{_datadir}/*

%changelog
* Sat May 09 00:20:49 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-6
-   Renaming glibmm to glibmm24
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-5
-   Renaming XML-Parser to perl-XML-Parser
*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 2.56.0-4
-   Renaming libsigc++ to libsigc++20
*   Tue Apr 21 2020 Eric Li <eli@microsoft.com> 2.56.0-3
-   Fix Source0: and delete sha1. Verified License. Fixed URL.  Fixed formatting.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.56.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.56.0-1
-   Update to version 2.56.0
*   Thu Aug 24 2017 Rongrong Qiu <rqiu@vmware.com> 2.50.1-2
-   add buildrequires for make check for bug 1900286
*   Thu May 26 2017 Harish Udaiya Kumar <hudaiykumar@vmware.com> 2.50.1-1
-   Downgrade to stable version 2.50.1
*   Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.53.1-1
-   Update to version 2.53.1
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.1-2
-   Modified %check
*   Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.1-1
-   Updated to version 2.48.1-1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.3.1-2
-   GA - Bump release of all rpms
*   Thu Apr 14 2016	Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.3.1-1
    Updated to version 2.47.3.1
*   Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.46.3-1
-   Updated to version 2.46.3
*   Tue Jul 7 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
-   Created devel subpackage. Added Summary.
*   Tue Jun 23 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
-   Added glib-schemas to build requirements.
*   Fri Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
-   Initial version
