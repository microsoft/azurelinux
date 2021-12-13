Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           unique3
Version:        3.0.2
Release:        21%{?dist}
Summary:        Single instance support for applications

License:        LGPLv2+
URL:            https://github.com/Distrotech/libunique/tags
# Source0: https://github.com/Distrotech/libunique/archive/refs/tags/3.0.2.tar.gz
Source0:        https://github.com/Distrotech/libunique/archive/refs/tags/libunique-%{version}.tar.xz

BuildRequires:  gnome-doc-utils >= 0.3.2
BuildRequires:  libtool
BuildRequires:  glib2-devel >= 2.25.0
BuildRequires:  gtk3-devel >= 2.99.3
BuildRequires:  gtk-doc >= 1.11

BuildRequires: automake autoconf libtool

%description
Unique is a library for writing single instance applications, that is
applications that are run once and every further call to the same binary
either exits immediately or sends a command to the running instance.

This version of unique works with GTK+ 3.

%package docs
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
API docs for %{name}.

%package devel
Summary: Libraries and headers for unique3
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel
Requires: gtk3-devel

%description devel
Headers and libraries for unique3.

%prep
%setup -q -n libunique-%{?version}
# fix compatibility with gtk-doc 1.26
gtkdocize
autoreconf -i -f -v

%build
%configure --enable-gtk-doc --disable-static --enable-introspection=no
%make_build

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog COPYING README
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/unique-3.0/
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%files docs
%doc %{_datadir}/gtk-doc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.2-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 11 2018 Filipe Rosset <rosset.filipe@gmail.com> - 3.0.2-16
- Rebuilt to fix FTBFS on rawhide, fix compatibility with gtk-doc 1.26
- Spec cleanup / modernization

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Richard Hughes <rhughes@redhat.com> - 3.0.2-6
- Split out a noarch -docs subpackage for multilib.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 3.0.2-2
- Rebuild for new libpng

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-4
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-2
- Rebuild against newer gtk

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-4
- Rebuild against newer gtk

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-3
- Rebuild against newer gtk3

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-2
- Co-own /usr/share/gtk-doc (#604415)

* Thu Jul  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-1
- Initial packaging
