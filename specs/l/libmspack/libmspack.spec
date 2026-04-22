# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libmspack
Version:        0.10.1
Release: 1.15.alpha%{?dist}
Summary:        Library for CAB and related files compression and decompression

# CRC32 is LicenseRef-Fedora-UltraPermissive
License:        LGPL-2.1-only AND LicenseRef-Fedora-UltraPermissive AND MIT
URL:            http://www.cabextract.org.uk/libmspack/
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}alpha.tar.gz
#Source0:        https://github.com/kyz/libmspack/archive/v%{version}alpha/%{name}-v%{version}alpha.tar.gz

BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires: make

# Temporarily while building from github tarball:
#BuildRequires:  autoconf, automake, libtool


%description
The purpose of libmspack is to provide both compression and decompression of 
some loosely related file formats used by Microsoft.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-doc < 0.2

%description    devel
The %{name}-devel package contains libraries, header files and documentation
for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}alpha

chmod a-x mspack/mspack.h

# Temporarily while building from github tarball:
#autoreconf -fi


%build
%configure --disable-static --disable-silent-rules

# disable rpath the hard way
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

rm $RPM_BUILD_ROOT%{_libdir}/libmspack.la

iconv -f ISO_8859-1 -t utf8 ChangeLog --output Changelog.utf8
touch -r ChangeLog Changelog.utf8
mv Changelog.utf8 ChangeLog

pushd doc
doxygen
find html -type f | xargs touch -r %{SOURCE0}
rm -f html/installdox
popd


%ldconfig_scriptlets

%files
%doc README TODO ChangeLog AUTHORS
%license COPYING.LIB
%{_libdir}/%{name}.so.0*

%files devel
%doc doc/html
%{_includedir}/mspack.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.15.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.14.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.13.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.12.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.11.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.10.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.9.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.8.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.7.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.6.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.5.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Dan Horák <dan[at]danny.cz> - 0.10.1-0.1.alpha
- updated to 0.10.1alpha (fixes CVE-2019-1010305)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.9.1-0.1.alpha
- 0.9.1alpha
- libmspack-0.8-0.1.alpha corrupts extracted cab files (#1647033)
- examples no longer installed (by default)

* Tue Oct 30 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.8-0.1.alpha
- 0.8alpha
- use %%make_build %%make_install %%ldconfig_scriptlets %%license
- devel: use %%{?_isa} to tighten dep on main pkg
- drop deprecated Group: tag
- %%files: tighten to include library soname

* Wed Aug 01 2018 Richard W.M. Jones <rjones@redhat.com> - 0.7-0.1.alpha
- New upstream version 0.7alpha.
- No tarball was uploaded so temporarily use tarball from github.
- Fixes CVE-2018-14679 libmspack: off-by-one error in the CHM PMGI/PMGL
  chunk number validity checks

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Dan Horák <dan[at]danny.cz> - 0.6-0.1.alpha
- updated to 0.6alpha (fixes CVE-2017-6419 and CVE-2017-11423)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.10.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.9.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.8.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 27 2016 Dan Horák <dan[at]danny.cz> - 0.5-0.7.alpha
- install the actual expand binary

* Wed Jul 27 2016 Dan Horák <dan[at]danny.cz> - 0.5-0.6.alpha
- install the expand tool as msexpand (#1319357)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-0.5.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 0.5-0.4.alpha
- Avoid 'test/md5.c:126:3: warning: dereferencing type-punned pointer
  will break strict-aliasing rules' by adding -fno-strict-aliasing flag.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Dan Horák <dan[at]danny.cz> - 0.5-0.1.alpha
- updated to 0.5alpha

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Dan Horák <dan[at]danny.cz> - 0.4-0.1.alpha
- updated to 0.4alpha

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.3.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.2.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Dan Horák <dan[at]danny.cz> - 0.3-0.1.alpha
- updated to 0.3alpha

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.20100723alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Dan Horák <dan[at]danny.cz> - 0.2-0.1.20100723alpha
- updated to 0.2alpha released 2010/07/23
- merged the doc subpackage with devel

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.7.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.6.20060920alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.5-20060920alpha
- Rebuild for gcc4.3

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.4.20060920alpha
- installed documentation into html subdir
- manually installed doc's for main package

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.3.20060920alpha
- Got source using wget -N
- Removed some doc's
- Shifted doc line for doc package
- Added install -p

* Sun Jan 20 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 0.0-0.2.20060920alpha
- Changed install script for doc package
- Fixed rpmlint issue with debug package

* Fri Jan 18 2008 Marc Wiriadisastra <marc@mwiriadi.id.au> - 20060920cvs.a-1
- Initial release
