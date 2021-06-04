Summary:        ITS XML document translation tool
Name:           itstool
Version:        2.0.6
Release:        3%{?dist}
License:        GPLv3+
URL:            http://itstool.org
Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2

Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  docbook-dtd-xml >= 4.5
BuildRequires:  libxml2
BuildRequires:  libxml2-python
BuildRequires:  python2 >= 2.7.8
BuildRequires:  python2-libs >= 2.7.8
Requires:       python2
Requires:       libxml2-python
BuildArch:      noarch

%description
Itstool extracts messages from XML files and outputs PO template files, then merges
translations from MO files to create translated XML files. It determines what
to translate and how to chunk it into messages using the W3C Internationalization Tag Set (ITS).
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
/usr/share/%{name}/*
%{_mandir}/man1/*
%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.6-3
- Added %%license line automatically

*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 2.0.6-2
-   Renaming docbook-xml to docbook-dtd-xml
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.0.6-1
-   Update to 2.0.4. Fix Source0 URL. Fix summary. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.0.2-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Mon May 1 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.2-5
-	Added runtime dependencies for itstool
*	Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-4
-	Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-3
-	GA - Bump release of all rpms
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.0.2-2
-   Updated group.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.2-1
-	Initial build. First version
