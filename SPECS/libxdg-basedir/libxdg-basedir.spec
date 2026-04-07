# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libxdg-basedir
Version:        1.2.0
Release:        36%{?dist}
Summary:        Implementation of the XDG Base Directory Specifications

License:        MIT
URL:            https://github.com/devnev/libxdg-basedir
Source0:        https://github.com/devnev/%{name}/archive/%{name}-%{version}.tar.gz
Patch0:         libxdg-basedir-leak.patch
Patch1:         libxdg-basedir-valgrind-libtool.patch
Patch2:         libxdg-basedir-basedir-bounds-error.patch 
Patch3:         libxdg-basedir-home-undef.patch
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif
BuildRequires:  libtool

%description
The XDG Base Directory Specification defines where should user files 
be looked for by defining one or more base directories relative in 
with they should be located.

This library implements functions to list the directories according 
to the specification and provides a few higher-level functions.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation files for %{name}
Requires:       %{name} = %{version}-%{release}
BuildRequires:  gcc
BuildRequires:  doxygen
BuildRequires: make

%description    doc
The %{name}-doc package contains doxygen generated files for
developing applications that use %{name}.


%prep
%setup -q

%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%configure --disable-static
make %{?_smp_mflags}
make doxygen-run


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%check
%ifarch %{valgrind_arches}
make check USE_VALGRIND=1
%else
make check
%endif
#env -i make check USE_VALGRIND=1
# Check that we get NULL for all things rooted in ENV{HOME} when running
# with HOME unset
env -i ./tests/testdump | grep null > grep.NULL
env -i ./tests/testdump | grep HOME | grep -v DIRS > grep.HOME
diff -u grep.NULL grep.HOME

%ldconfig_scriptlets


%files
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc doc/html/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-30
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-24
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 01 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-20
- Enhance testing.

* Mon Apr 01 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-19
- Patch correction.

* Mon Apr 01 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-18
- Patch to handle undefined homedir, BZ 1694706.

* Wed Feb 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-17
- Updated valgrind patch.

* Tue Feb 12 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2.0-16
- Relocated upstream, crash patch.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 31 2013 Jon Ciesla <limburgher@gmail.com> - 1.2.0-5
- Patch for memory leak, BZ 1018527.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Jon Ciesla <limburgher@gmail.com> - 1.2.0-1
- New upstream, BZ 783762.
- Temporarily disabling make check tests.  Succeeding locally, failing in RPM.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 16 2010 Michal Nowak <mnowak@redhat.com> - 1.1.1-1
- 1.1.1

* Sun May  9 2010 Michal Nowak <mnowak@redhat.com> - 1.1.0-1
- 1.1.0

* Tue Sep  1 2009 Michal Nowak <mnowak@redhat.com> - 1.0.2-1
- 1.0.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Michal Nowak <mnowak@redhat.com> - 1.0.1-2
- removed bogus ownership of %%{_libdir}/pkgconfig/
- "docs" sub-package renamed to "doc"

* Mon Jun  8 2009 Michal Nowak <mnowak@redhat.com> - 1.0.1-1
- 1.0.1
- -devel: require pkgconfig, own %%{_libdir}/pkgconfig/
- -docs: sub-package
- make check tests
- SPEC cleanups

* Thu May  7 2009 Michal Nowak <mnowak@redhat.com> - 1.0.0-1
- 1.0.0

