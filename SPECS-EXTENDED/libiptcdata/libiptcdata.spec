Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: libiptcdata
Version: 1.0.5
Release: 5%{?dist}
Summary: IPTC tag library

License: LGPLv2+
URL: https://github.com/ianw/%{name}
Source0: https://github.com/ianw/%{name}/releases/download/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  gtk-doc
BuildRequires:  python3-devel


%description
libiptcdata is a library for parsing, editing, and saving IPTC data
stored inside images.  IPTC is a standard for encoding metadata such
as captions, titles, locations, etc. in the headers of an image file.
libiptcdata also includes a command-line utility for modifying the
metadata.

%package -n python3-%{name}
Summary:        Python bindings for libiptcdata
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel

%description -n python3-%{name}
The libiptcdata-python package contains a Python module that allows Python
applications to use the libiptcdata API for reading and writing IPTC
metadata in images.

%package devel
Summary:        Headers and libraries for libiptcdata application development
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The libiptcdata-devel package contains the libraries and include files
that you can use to develop libiptcdata applications.


%prep
%autosetup
# fix compatibility with gtk-doc 1.26
gtkdocize
autoreconf -fiv


%build
#configure --enable-gtk-doc --disable-python --disable-static
export PYTHON_VERSION=%python3_version
%configure --enable-gtk-doc --enable-python --disable-static
%make_build


%install
%make_install
find %{buildroot} -name "*.la" -exec rm -f {} \;
%find_lang %{name} --all-name


%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/*
%{_libdir}/lib*.so.*

%files -n python3-%{name}
%doc python/README
%doc python/examples/*
%{python3_sitearch}/*.so

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libiptcdata
%{_datadir}/gtk-doc/html/libiptcdata


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.5-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.5-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Richard Shaw <hobbes1069@gmail.com> - 1.0.5-1
- Update to 1.0.5.
- Modernize spec file.
- Enable python3 package.

* Fri Jan 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.4-24
- Remove the Python 2 subpackage (#1628188)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.0.4-22
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-20
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.4-19
- Python 2 binary package renamed to python2-libiptcdata
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-15
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.0.4-6
- Mark translations with %%lang.

* Wed Nov 16 2011 David Moore <david.moore@gmail.com> 1.0.4-5
- Removed 'Requires: gtk-doc', updated python sitearch.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 05 2009 David Moore <dcm@acm.org> 1.0.4-1
- New upstream version

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-3
- Added 'BuildRequires: gtk-doc'

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-2
- Added 'Requires: gtk-doc' and 'BuildRequires: libtool' and gettext

* Sun Apr 12 2009 David Moore <dcm@acm.org> 1.0.3-1
- New upstream version
- Added translation to file list

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.2-4
- Rebuild for Python 2.6

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.2-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-2
- Autorebuild for GCC 4.3

* Tue May 15 2007 David Moore <dcm@acm.org> 1.0.2-1
- New upstream version

* Fri Mar 23 2007 David Moore <dcm@acm.org> 1.0.1-1
- New upstream version

* Thu Mar 22 2007 David Moore <dcm@acm.org> 1.0.0-2
- Fixed URL, removed INSTALL file, fixed python path and timestamps

* Wed Mar 21 2007 David Moore <dcm@acm.org> 1.0.0-1
- Updated spec file to better match Fedora guidelines

* Sun Jan 28 2007 David Moore <dcm@acm.org>
- Added libiptcdata-python package

* Wed Apr 12 2006 David Moore <dcm@acm.org>
- Removed *.mo from spec file since there are no translations yet

* Mon Feb 28 2005 David Moore <dcm@acm.org>
- Initial version
