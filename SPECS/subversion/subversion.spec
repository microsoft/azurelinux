Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.14.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Utilities/System
URL:            https://subversion.apache.org/
Source0:        https://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  expat-devel
BuildRequires:  libserf-devel
BuildRequires:  libtool
BuildRequires:  lz4
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  sqlite-devel
BuildRequires:  swig
BuildRequires:  utf8proc-devel
%if %{with_check}
BuildRequires:  python3
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif
Requires:       apr
Requires:       apr-util
Requires:       libserf
Requires:       utf8proc

%description
The Apache version control system.

%package    devel
Summary:        Header and development files for mesos
Requires:       %{name} = %{version}

%description    devel
 subversion-devel package contains header files, libraries.

%package    perl
Summary:        Allows Perl scripts to directly use Subversion repositories.
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       %{name} = %{version}

%description    perl
Provides Perl (SWIG) support for Subversion version control system.

%prep
%autosetup -p1

%build
export CFLAGS="%{build_cflags} -Wformat"
sh configure --prefix=%{_prefix}        \
        --disable-static                \
        --with-apache-libexecdir        \
        --with-serf=%{_prefix}          \
        --with-lz4=internal

make %{?_smp_mflags}

# For Perl bindings
make  %{?_smp_mflags} swig-pl

%install
make -j1 DESTDIR=%{buildroot} install
%find_lang %{name}

# For Perl bindings
make install-swig-pl-lib DESTDIR=%{buildroot}
make pure_vendor_install -C subversion/bindings/swig/perl/native \
        PERL_INSTALL_ROOT=%{buildroot}

%check
# subversion expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f

%files -f %{name}.lang
%defattr(-,root,root)
%license LICENSE
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man[158]/*
%{_datadir}/locale/*
%exclude %{_libdir}/libsvn_swig_perl*so*

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.*a
%{_libdir}/libsvn_*.so
%{_datadir}/pkgconfig/*.pc
%exclude %{_libdir}/debug/

%files perl
%defattr(-,root,root)
%{perl_vendorarch}/SVN
%{perl_vendorarch}/auto/SVN
%{_libdir}/libsvn_swig_perl*so*
%{_libdir}/perl5/*
%{_mandir}/man3/SVN*

%changelog
* Mon Jun 06 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.2-1
- Updating to 1.14.2 to fix CVE-2021-28544.

* Mon Apr 25 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.14.1-3
- Fix duplicate packaging of libsvn_swig_perl so

* Mon Jan 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.14.1-2
- Use python3 during %%check section instead of python2

* Fri Jan 14 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.14.1-1
- Update to version 1.14.1.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.14.0-4
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 1.14.0-3: Adding 'BuildRequires' on 'python', 'shadow-utils' and 'sudo' to fix the package tests.
- henry.beberman@microsoft.com, 1.14.0-4: Patch CVE-2020-17525.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.14.0-3
- Use new perl package names.
- Add perl(ExtUtils::Embed) build requirement.
- Update perl installation and packaging to perl_vendorarch directory.

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> 1.14.0-2
- Add -Wformat to fix the build because -Werror=format-security is enabled.

* Tue Jun 09 2020 Andrew Phelps <anphel@microsoft.com> 1.14.0-1
- Update to 1.14.0 to fix: CVE-2019-0203, CVE-2018-11782, CVE-2018-11803

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.10.2-7
- Added %%license line automatically

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> 1.10.2-6
- Rename serf to libserf.
- Update Source0 and URL to use https. Update License. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.10.2-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Mar 05 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.10.2-4
- Excluding conflicting perllocal.pod

* Tue Oct 02 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.10.2-3
- Added Perl bindings

* Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-2
- Added utf8proc as Requires.

* Wed Sep 19 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-1
- Updated to version 1.10.2

* Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-2
- Compile subversion with https repository access module support

* Mon Aug 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-1
- Update to version 1.9.7.

* Thu Jun 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.5-2
- Fix make check issues.

* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.5-1
- Update to version 1.9.5

* Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-2
- Moved pkgconfig/*.pc to devel subpackage.

* Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-1
- Upgraded to version 1.9.4, fixes CVE-2016-2167  CVE-2016-2168

* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.9.3-8
- Use sqlite-{devel,libs}

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.9.3-7
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.3-6
- GA - Bump release of all 

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.3-1
- Updated to version 1.9.3

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-5
- Handled locale files with macro find_lang

* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.13-4
- Updated build-requires after creating devel package for apr.

* Mon Sep 21 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-3
- Move .a, and .so files to devel pkg.

* Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.13-2
- Move headers into devel pkg.

* Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 1.8.13-1
- Initial build. First version
