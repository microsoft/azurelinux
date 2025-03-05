Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:  Thai language support routines
Name: libthai
Version: 0.1.29
Release: 10%{?dist}
License: LGPL-2.1-or-later
Source0: https://linux.thai.net/pub/thailinux/software/libthai/libthai-%{version}.tar.xz
Patch0: libthai-0.1.9-multilib.patch
URL: http://linux.thai.net

BuildRequires: gcc
BuildRequires: pkgconfig(datrie-0.2)
BuildRequires: doxygen
BuildRequires: make

%description
LibThai is a set of Thai language support routines aimed to ease
developers' tasks to incorporate Thai language support in their applications.
It includes important Thai-specific functions e.g. word breaking, input and
output methods as well as basic character and string supports.

%package devel
Summary:  Thai language support routines
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The libthai-devel package includes the header files and developer docs 
for the libthai package.

Install libthai-devel if you want to develop programs which will use
libthai.

%prep
%autosetup -p1

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# move installed doc files back to build directory to package them
# in the right place
mkdir installed-docs
mv $RPM_BUILD_ROOT%{_docdir}/libthai/* installed-docs
rmdir $RPM_BUILD_ROOT%{_docdir}/libthai

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_scriptlets

%files
%doc README AUTHORS COPYING ChangeLog
%{_libdir}/lib*.so.*
%{_datadir}/libthai

%files devel
%doc installed-docs/*
%{_includedir}/thai
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%changelog
* Wed oNov 13 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 0.1.29-10
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 17 2023 Peng Wu <pwu@redhat.com> - 0.1.29-5
- Migrate to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Peng Wu <pwu@redhat.com> - 0.1.29-1
- Update to 0.1.29

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  2 2018 Peng Wu <pwu@redhat.com> - 0.1.28-1
- Update to 0.1.28

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov  1 2017 Peng Wu <pwu@redhat.com> - 0.1.27-1
- Update to 0.1.27

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct  9 2016 Peng Wu <pwu@redhat.com> - 0.1.25-1
- Update to 1.2.25
- Remove libthai-0.1.24-gcc6.patch, already in upstream tar ball

* Tue Feb 16 2016 Daiki Ueno <dueno@redhat.com> - 0.1.24-1
- Update to 0.1.24
- Apply patch from upstream, which fixes scim-thai FTBFS with GCC6 (Closes: #1308117)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep  2 2014 Daiki Ueno <dueno@redhat.com> - 0.1.21-1
- Update to 0.1.21

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul  4 2014 Daiki Ueno <dueno@redhat.com> - 0.1.20-3
- Unbundle libdatrie (Closes: #1062540)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Daiki Ueno <dueno@redhat.com> - 0.1.20-1
- Update to 0.1.20
- Update bundled libdatrie to 0.2.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Daiki Ueno <dueno@redhat.com> - 0.1.19-1
- Update to 0.1.19
- Fix bogus dates in %%changelog
- Remove libthai-0.1.9-doxygen-segfault.patch, which is no longer
  necessary with the latest Doxygen
- Don't install man pages, as per upstream's default

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Behdad Esfahbod <behdad@redhat.com> - 0.1.14-3
- Update to 0.1.14

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.12-1
- Update to 0.1.12

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com> - 0.1.9-7
- Fix the build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.9-5
- fix license tag

* Mon Mar 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.1.9-4
- Attempt to fix multilib conflict

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.9-3
- Autorebuild for GCC 4.3

* Tue Nov 13 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.9-2
- Add libthai-0.1.9-doxygen-segfault.patch to workaround doxygen segfault

* Tue Aug 28 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.9-1
- Update to 0.1.9
- Adjust patch

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.1.7-6
- Rebuild for build ID

* Mon Jan 22 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-5
- Export _th_*_tbl symbols too.  They are accessed by some of the macros.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-4
- Patch libthai.pc.in to not require datrie.

* Tue Jan 16 2007 Matthias Clasen <mclasen@redhat.com> 0.1.7-3
- Miscellaneous fixes
 
* Tue Jan 16 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-2
- Apply comments from Matthias Clasen (#222611) 
- devel summary improvement
- devel require pkgconfig
- configure --disable-static
- Add comments about the voodoo
- Install docs in the right place

* Sun Jan 14 2007 Behdad Esfahbod <besfahbo@redhat.com> 0.1.7-1
- Initial package based on package by Supphachoke Suntiwichaya
  and Kamthorn Krairaksa for the OLPC.
