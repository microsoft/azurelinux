Vendor:         Microsoft Corporation
Distribution:   Mariner
%global xfceversion 4.14
%bcond_with perl

Name:           xfconf
Version:        4.14.4
Release:        4%{?dist}
Summary:        Hierarchical configuration system for Xfce

License:        GPLv2
URL:            http://www.xfce.org/
#VCS git:git://git.xfce.org/xfce/xfconf
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2

BuildRequires:  glib2-devel
BuildRequires:  perl(File::Find)
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(dbus-1) >= 1.1.0
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.84
%if %{with perl}
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::Depends)
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Glib)
BuildRequires:  perl(Glib::MakeHelper)
%endif
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  gcc-c++
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala

Requires:       dbus-x11

Obsoletes:      libxfce4mcs < 4.4.3-3
Obsoletes:      xfconf-perl < 4.13.8

%description
Xfconf is a hierarchical (tree-like) configuration system where the
immediate child nodes of the root are called "channels".  All settings
beneath the channel nodes are called "properties."

%package        devel
Summary:        Development tools for xfconf
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       dbus-devel
Requires:       dbus-glib-devel
Requires:       glib2-devel
Obsoletes:      libxfce4mcs-devel < 4.4.3-3
Obsoletes:      xfce-mcs-manager-devel < 4.4.3-3

%description devel
This package includes the libraries and header files you will need
to compile applications for xfconf.

%if %{with perl}
%package perl
Summary:        Perl modules for xfconf
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
This package includes the perl modules and files you will need to 
interact with xfconf using perl. 
%endif

%prep
%setup -q

%build
# gobject introspection does not work with LTO.  There is an effort to fix this
# in the appropriate project upstreams, so hopefully LTO can be enabled someday
# Disable LTO.
%define _lto_cflags %{nil}

%configure --disable-static --with-perl-options=INSTALLDIRS="vendor"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH="`pwd`/xfconf/.libs"

%make_build

%install
%make_install

# fix permissions for installed libraries
chmod 755 %{buildroot}/%{_libdir}/*.so

%if %{with perl}
# remove perl temp file
rm -f %{buildroot}/%{perl_archlib}/perllocal.pod

# remove unneeded dynloader bootstrap file
rm -f %{buildroot}/%{perl_vendorarch}/auto/Xfce4/Xfconf/Xfconf.bs

# fix permissions on the .so file
chmod 755 %{buildroot}/%{perl_vendorarch}/auto/Xfce4/Xfconf/Xfconf.so
%endif

# remove .packlist files. 
find %{buildroot} -type f -name .packlist -exec rm -f {} \;

# get rid of .la files
find %{buildroot} -type f -name *.la -exec rm -f {} \;

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS TODO
%{_libdir}/lib*.so.*
%{_bindir}/xfconf-query
%{_libdir}/xfce4/xfconf/
%{_libdir}/girepository-1.0/Xfconf-0.typelib
%{_datadir}/vala/vapi/libxfconf-0.deps
%{_datadir}/vala/vapi/libxfconf-0.vapi
%{_datadir}/dbus-1/services/org.xfce.Xfconf.service
%{_datadir}/gir-1.0/Xfconf-0.gir

%files devel
%doc %{_datadir}/gtk-doc
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4/xfconf-0

%if %{with perl}
%files perl
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Xfce4
%{_mandir}/man3/*.3*
%endif

%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.14.4-4
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.14.4-3
- Adding missing BRs on Perl modules.

* Thu May 27 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.14.4-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Unconditionally use "%%bcond_with perl"

* Tue Nov 10 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.14.4-1
- Update to 4.14.4

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4.14.3-2
Disable LTO

* Wed May 06 2020 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.14.3-1
- Update to 4.14.3

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.14.1-1
- Update to 4.14.1

* Mon Jul 29 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 4.13.8-4
- Enable vala

* Mon Jul 29 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 4.13.8-3
- rebuild for xfce 4.14pre3

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.8-1
- Update to 4.13.8
- Enable gobject introspection
- Following upstream, disable perl bindings and obsolete xfconf-perl sub-pkg

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.13.7-2
- Perl 5.30 rebuild

* Sat May 18 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.7-1
- Update to 4.13.7

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Dan Horák <dan[at]danny.cz> - 4.13.6-3
- Limit the perl subpackage to Fedora, nothing requires it anyway

* Mon Oct 22 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.6-2
- Fix files section
- Spec clean up

* Mon Oct 22 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.6-1
- Update to 4.13.6

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.5-20
- Update to 4.13.5
- Spec cleanup

* Mon Jul 16 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-9
- Add gcc-c++ as BR

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.12.1-7
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.12.1-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 24 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-1
- Update to 4.12.1

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.12.0-5
- Perl 5.24 rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.12.0-2
- Perl 5.22 rebuild

* Sat Feb 28 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.0-1
- Update to stable release 4.12.0
- Fix permissions for installed libraries

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.10.0-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.10.0-9
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 4.10.0-5
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 4.10.0-2
- Perl 5.16 rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.0-1
- Update to 4.9.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Kevin Fenzi <kevin@scrye.com> - 4.8.1-1
- Update to 4.8.1

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 4.8.0-4
- Perl mass rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.8.0-3
- Perl mass rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final. 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4
- Fix directory ownership

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Mon Aug 23 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-3
- Remove unneeded gtk-doc dep. Fixes bug #604423

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.6.2-2
- Mass rebuild with perl-5.12.0

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.6.1-5
- rebuild against perl 5.10.1

* Tue Oct 20 2009 Orion Poplawski <orion@cora.nwra.com> - 4.6.1-4
- Add BR perl(ExtUtils::MakeMaker) and perl(Glib::MakeHelper)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.1-2
- Require dbus-x11 (#505499)

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Fix directory ownership problems
- Move gtk-doc into devel package and mark it %%doc
- Make devel package require gtk-doc

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Thu Jan 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.5.93-3
- Let xfce4-settings Obsolete mcs manager and plugin packages

* Thu Jan 22 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.5.93-2
- Add Obsoletes for mcs devel package

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Fri Jan 02 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.92-4
- Add Obsoletes for mcs packages

* Mon Dec 22 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-3
- Fixes for review ( bug 477732 )

* Mon Dec 22 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-2
- Add gettext BuildRequires

* Sun Dec 21 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Initial version for Fedora
