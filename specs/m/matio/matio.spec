# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           matio
Version:        1.5.29
Release:        1%{?dist}
Summary:        Library for reading/writing Matlab MAT files

License:        BSD-2-Clause
URL:            http://sourceforge.net/projects/matio
Source0:        http://downloads.sourceforge.net/matio/matio-%{version}.tar.gz

BuildRequires: make
BuildRequires:  doxygen
#According to the README - zlib 1.2.2 is possible but require a patch
BuildRequires:  zlib-devel >= 1.2.3
BuildRequires:  hdf5-devel >= 1.8
# 1.5.3 was released without configure
BuildRequires:  libtool
Requires:       hdf5 = %{_hdf5_version}
     

%description
matio is an open-source library for reading/writing Matlab MAT files.  This
library is designed for use by programs/libraries that do not have access or
do not want to rely on Matlab's libmat shared library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       hdf5-devel
Requires:       zlib-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1

sed -i -e '/Requires\.private/d' matio.pc.in


%build
sh ./autogen.sh
%configure \
  --enable-shared \
  --disable-static \
  --enable-mat73=yes \
  --enable-extended-sparse=yes

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}



%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

#Fix timestamp
touch -r $RPM_BUILD_ROOT%{_includedir}/matio_pubconf.h NEWS

rm -rf $RPM_BUILD_ROOT%{_datadir}/info/dir


%check
%ifnarch s390x
fail=1
#Needed to avoid rpath
export LD_LIBRARY_PATH=%{_builddir}/%{?buildsubdir}/src/.libs/
make check || ( cat test/testsuite.log && exit $fail )
%endif

%ldconfig_scriptlets


%files
%license COPYING
%doc NEWS README
%{_bindir}/matdump
%{_libdir}/*.so.13*

%files devel
%{_includedir}/matio*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/Mat_*.3.*


%changelog
* Mon Nov 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.5.29-1
- 1.5.29

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 13 2025 Orion Poplawski <orion@nwra.com> - 1.5.28-3
- Rebuild with hdf5 1.14.6

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.5.28-1
- 1.5.28

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 1.5.27-3
- Rebuild for hdf5 1.14.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.5.27-1
- 1.5.27

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.26-1
- 1.5.26

* Fri Nov 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.24-2
- Patch out static requires

* Mon Oct 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.24-1
- 1.5.24

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Florian Weimer <fweimer@redhat.com> - 1.5.23-5
- Port configure script to C99

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.5.23-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.5.23-1
- 1.5.23

* Tue Apr 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.5.22-1
- 1.5.22

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 1.5.21-4
- Rebuild for hdf5 1.12.1

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 1.5.21-3
- Rebuild for hdf5 1.10.7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.21-1
- 1.5.21

* Mon Mar 22 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.20-1
- 1.5.20

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 06 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.19-1
- 1.5.19

* Thu Sep 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.5.18-1
- 1.5.18

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 1.5.17-3
- Rebuild for hdf5 1.10.6

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.5.17-1
- 1.5.17

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 30 2019 Orion Poplawski <orion@nwra.com> - 1.5.15-1
- Update to 1.5.15

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 1.5.14-1
- Update to 1.5.14

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 12 2018 Sandro Mani <manisandro@gmail.com> - 1.5.7-8
- Rebuild (hdf5)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 06 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.7-3
- Rebuild for hdf5 1.8.18

* Fri Jul 01 2016 Dan Horák <dan[at]danny.cz> - 1.5.7-2
- fix build on big endian arches

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.7-1
- Update to 1.5.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.3-1
- Update to 1.5.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-6
- Rebuild for hdf5 1.8.15

* Wed Jan 07 2015 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-5
- Rebuild for hdf5 1.8.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-3
- Rebuild for hdf 1.8.13

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 1.5.2-1
- Update to 1.5.2

* Sat Sep 14 2013 Dan Horák <dan[at]danny.cz> - 1.5.1-4
- Rebuilt to resolve broken deps on s390(x)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-2
- Rebuild for hdf5 1.8.11

* Thu Mar 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1
- Spec file clean-up

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Dan Horák <dan[at]danny.cz> - 1.5.0-5
- fix build on big endian platforms

* Wed Dec 05 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5.0-4
- Rebuild for hdf5 1.8.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5.0-2
- Rebuild for hdf5 1.8.9
- Add Requires on specific version of hdf5 built with

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.5.0-1
- Update to 1.5.0
- Enable mat73 support
- License change from LGPLv2+ to BSD

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4
- Remove uneeded patches.

* Wed Sep 30 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.3.3-5
- Fix location of Fortran module.
- Add Requires: pkgconfig on -devel.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 kwizart < kwizart at gmail.com > - 1.3.3-3
- Remove the test subpackage 
- Enable make check
- Various typo and clean-up

* Wed Sep 24 2008 kwizart < kwizart at gmail.com > - 1.3.3-2
- Fix undefined-non-weak-symbol 
- Fix missing f90 files in the debuginfo package

* Wed Sep 24 2008 kwizart < kwizart at gmail.com > - 1.3.3-1
- Initial package for fedora


