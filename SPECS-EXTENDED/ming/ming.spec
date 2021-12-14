Vendor:         Microsoft Corporation
Distribution:   Mariner
%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh || echo 0.0)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%bcond_without check

%global abi 1
%global commit 50098023446a5412efcfbd40552821a8cba983a6
# https://src.fedoraproject.org/rpms/redhat-rpm-config/blob/master/f/buildflags.md#legacy-fcommon
%define _legacy_common_support 1

Summary: A library for generating Macromedia Flash files
Name: ming
Version: 0.4.9
%global fver %(echo %{version} | tr . _)
Release: 1%{?dist}
URL: http://www.libming.org/
Source0: https://github.com/libming/libming/archive/%{commit}/ming-%{commit}.tar.gz
# make ming-config multilib-compatible
Patch0: ming-multilib.patch
# install perl modules to vendorarch dir and link dynamically with libming.so
Patch1: ming-perl.patch
# fix parallel make calls to bison causing generated code corruption
# https://github.com/libming/libming/issues/49
Patch2: ming-parallel-make.patch
# drop -dev from version, perl doesn't like it
Patch4: ming-version.patch
# https://github.com/libming/libming/pull/145
Patch100: ming-pr145.patch

License: LGPLv2+ and GPLv2+ and MIT and GPL+ or Artistic
BuildRequires: bison
BuildRequires: flex
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: libpng-devel
BuildRequires: libtool
BuildRequires: swig

%description
Ming is a library for generating Macromedia Flash files (.swf), written in C,
and includes useful utilities for working with .swf files.

%package devel
Summary: A library for generating Macromedia Flash files - development files
Requires: %{name}%{_isa} = %{version}-%{release}

%description devel
Ming is a library for generating Macromedia Flash files (.swf), written in C,
and includes useful utilities for working with .swf files.

This package contains the development files.

%package utils
Summary: Utilities for generating Macromedia Flash files
Requires: %{name} = %{version}-%{release}

%description utils
A set of utility programs for generating Macromedia Flash files using the Ming
library.

%package -n perl-ming
Summary: A Perl module for generating Macromedia Flash files using the Ming library
Obsoletes: ming-perl < 0.4.7-1
Provides: ming-perl = %{version}-%{release}
Provides: ming-perl%{_isa} = %{version}-%{release}
Provides: perl-SWF = %{version}-%{release}
Provides: perl-SWF%{_isa} = %{version}-%{release}
BuildRequires: perl-devel
%if %{with check}
BuildRequires: perl(blib)
%endif
BuildRequires: perl-generators
BuildRequires: perl(Cwd)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(strict)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-ming
A perl module for generating Macromedia Flash files using the Ming library.

%package -n php-ming
Summary: A PHP module for generating Macromedia Flash files using the Ming library
BuildRequires: php-devel
Obsoletes: ming-php < 0.4.7-1
Provides: ming-php = %{version}-%{release}
Provides: ming-php%{_isa} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}

%description -n php-ming
A PHP module for generating Macromedia Flash files using the Ming library.

%package -n tcl-ming
Summary: A TCL module for generating Macromedia Flash files using the Ming library
BuildRequires: tcl-devel
Obsoletes: ming-tcl < 0.4.7-1
Provides: ming-tcl = %{version}-%{release}
Provides: ming-tcl%{_isa} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description -n tcl-ming
A TCL module for generating Macromedia Flash files using the Ming library.

%prep
%setup -q -n libming-%{commit}
%patch0 -p1 -b .multilib
%patch1 -p1 -b .p
%patch2 -p1 -b .pmake
%patch4 -p1 -b .ver
%patch100 -p1
pushd src
chmod -x blocks/{matrix,outputblock}.* \
         displaylist.* position.*
popd

./autogen.sh

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-cpp \
  --enable-perl \
  --enable-php \
  --disable-python \
  --enable-tcl \

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build V=1

%install
%make_install
rm %{buildroot}%{_libdir}/libming.la
rm %{buildroot}%{_libdir}/perl5/perllocal.pod
rm -f %{buildroot}%{perl_vendorarch}/auto/SWF/{.packlist,SWF.bs}
chmod 755 %{buildroot}%{perl_vendorarch}/auto/SWF/SWF.so
rm %{buildroot}%{_libdir}/ming/tcl/mingc.la
install -d %{buildroot}%{tcl_sitearch}/ming
mv %{buildroot}%{_libdir}/ming/tcl/mingc.so %{buildroot}%{tcl_sitearch}/ming/
rmdir %{buildroot}%{_libdir}/ming{/tcl,}

%if %{with check}
%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %make_build check
%endif

%ldconfig_scriptlets

%files
%license LICENSE LICENSE_GPL2
%doc AUTHORS HISTORY NEWS README
%{_libdir}/libming.so.%{abi}*

%files devel
%doc docs/libming docs/perl docs/index.html
%doc TODO
%{_bindir}/ming-config
%{_includedir}/ming.h
%{_includedir}/mingpp.h
%{_libdir}/libming.so
%{_libdir}/pkgconfig/libming.pc

%files utils
%doc util/README util/TIPS util/ming.css util/swftoperl.html
%{_bindir}/dbl2png
%{_bindir}/gif2dbl
%{_bindir}/gif2mask
%{_bindir}/listaction
%{_bindir}/listaction_d
%{_bindir}/listfdb
%{_bindir}/listjpeg
%{_bindir}/listmp3
%{_bindir}/listswf
%{_bindir}/listswf_d
%{_bindir}/makefdb
%{_bindir}/makeswf
%{_bindir}/png2dbl
%{_bindir}/raw2adpcm
%{_bindir}/swftocxx
%{_bindir}/swftoperl
%{_bindir}/swftophp
%{_bindir}/swftopython
%{_bindir}/swftotcl

%files -n perl-ming
%dir %{perl_vendorarch}/auto/SWF
%{perl_vendorarch}/auto/SWF/SWF.so
%{perl_vendorarch}/SWF.pm
%dir %{perl_vendorarch}/SWF
%{perl_vendorarch}/SWF/*.pm
%{_mandir}/man3/SWF*.3pm*

%files -n php-ming
%{php_extdir}/ming.so

%files -n tcl-ming
%{tcl_sitearch}/ming

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.9-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon May 11 2020 Dominik Mierzejewski <rpm@greysector.net> - 0.4.9-0.6.20181112git5009802
- work around build issues with gcc-10 (#1793907)
- add missing dependency for running tests
- run tests in parallel

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-0.5.20181112git5009802
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 02 2019 Dominik Mierzejewski <rpm@greysector.net> - 0.4.9-0.4.20181112git5009802
- backport security fixes from PR#145
- fixes: CVE-2018-7866, CVE-2018-7873, CVE-2018-7876, CVE-2018-9009,
         CVE-2018-9132

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-0.3.20181112git5009802
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.9-0.2.20181112git5009802
- Perl 5.30 rebuild

* Mon Feb 25 2019 Dominik Mierzejewski <rpm@greysector.net> - 0.4.9-0.1.20181112git5009802
- sync with upstream git
- fixes: CVE-2018-6358, CVE-2018-7867, CVE-2018-7868, CVE-2018-7870,
         CVE-2018-7871, CVE-2018-7872, CVE-2018-7875, CVE-2018-9165

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.8-12
- Remove python2 subpackage (#1627348)

* Fri Oct 12 2018 Remi Collet <remi@remirepo.net> - 0.4.8-11
- Rebuild for https://fedoraproject.org/wiki/Changes/php73

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.8-9
- Perl 5.28 rebuild

* Wed Mar 07 2018 Dominik Mierzejewski <rpm@greysector.net> - 0.4.8-8
- backport security fixes from upstream repo
- fixes: CVS-2017-8782,  CVE-2017-9988,  CVE-2017-9989,  CVE-2017-11704,
         CVE-2017-11728, CVE-2017-11729, CVE-2017-11730, CVE-2017-11731,
         CVE-2017-11732, CVE-2017-11733, CVE-2017-11734, CVE-2017-16883,
         CVE-2017-16898, CVE-2018-5251,  CVE-2018-5294,  CVE-2018-6315,
         CVE-2018-6359
- call python2 explicitly
- add missing BR on gcc-c++
- cleanup empty unused dirs and tighten file lists
- allow disabling check section
- use ldconfig_scriptlets macro

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 0.4.8-7
- Rebuild (giflib)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Remi Collet <remi@fedoraproject.org> - 0.4.8-5
- rebuild for https://fedoraproject.org/wiki/Changes/php72

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.8-2
- Perl 5.26 rebuild

* Fri Apr 07 2017 Dominik Mierzejewski <rpm@greysector.net> - 0.4.8-1
- update to 0.4.8
- re-enable php extension (upstream is php7 compatible now)
- fixes: CVE-2016-9264, CVE-2016-9265, CVE-2016-9266, CVE-2016-9827,
         CVE-2016-9828, CVE-2016-9829, CVE-2016-9831
- use modern make_build/install macros

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Dominik Mierzejewski <rpm@greysector.net> - 0.4.7-1
- update to 0.4.7
- rename subpackages to follow the guidelines more closely
- work around corruption of bison-generated files due to make -jN
- drop php subpackage on rawhide for now
- add some docs to the devel package

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.5-10
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.5-7
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.4.5-6
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Remi Collet <rcollet@redhat.com> - 0.4.5-4
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Fri Jun 06 2014 Dominik Mierzejewski <rpm@greysector.net> - 0.4.5-3
- add missing perl module Provides and BRs

* Tue May 27 2014 Dominik Mierzejewski <rpm@greysector.net> - 0.4.5-2
- fix ming-config to be multilib-compatible
- enable testsuite
- disable silent rules in configure call
- drop defattr
- build perl, php, python and tcl bindings
- don't change ChangeLog timestamp

* Sun May 25 2014 Dominik Mierzejewski <rpm@greysector.net> - 0.4.5-1
- initial build
