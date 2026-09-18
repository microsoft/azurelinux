# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Unbundle Apache-Reload
%{bcond_with mod_perl_enables_bundled_Apache_Reload}
# Run optional test
%{bcond_without mod_perl_enables_optional_test}

%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

%global regenerate_xs 0

Name:           mod_perl
Version:        2.0.13
Release:        11%{?dist}
Summary:        An embedded Perl interpreter for the Apache HTTP Server
# other files:                  ASL 2.0
## Not in binary packages
# docs/os/win32/distinstall:    GPL+ or Artistic
# docs/os/win32/mpinstall:      GPL+ or Artistic
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://perl.apache.org/

Source0:        https://www.apache.org/dist/perl/mod_perl-%{version}.tar.gz
Source1:        https://www.apache.org/dist/perl/mod_perl-%{version}.tar.gz.asc
Source2:        https://www.apache.org/dist/perl/KEYS
Source3:        perl.conf
Source4:        perl.module.conf

# Normalize documentation encoding
Patch0:         mod_perl-2.0.12-Convert-documentation-to-UTF-8.patch
Patch1:         mod_perl-2.0.4-inline.patch
Patch2:         mod_perl-32bit-ftbs.patch

BuildRequires:  lmdb-devel
BuildRequires:  openldap-devel
BuildRequires:  apr-devel >= 1.2.0
BuildRequires:  apr-util-devel
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  gdbm-devel
BuildRequires:  gnupg2
BuildRequires:  httpd
BuildRequires:  httpd-devel >= 2.4.0
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DirHandle)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::Embed)
BuildRequires:  perl(ExtUtils::Install)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
# Module::CoreList not helpful
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Win32 not used
BuildRequires:  sed
%if %{regenerate_xs}0
BuildRequires:  perl(Data::Flow) >= 0.05
BuildRequires:  perl(Tie::IxHash)
%endif
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.6.1
BuildRequires:  perl(base)
BuildRequires:  perl(BSD::Resource)
BuildRequires:  perl(Carp::Heavy)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Getopt::Long)
# IO::Dir not used at tests
BuildRequires:  perl(Linux::Pid)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Socket)
BuildRequires:  perl(subs)
# TAP::Formatter::Console not use at tests
# TAP::Harness not used at tests
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Harness)
# Tests:
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::testlib)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(locale)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(threads)
BuildRequires:  perl(Test::More)
%if %{with mod_perl_enables_optional_test}
# Optional tests:
BuildRequires:  perl(CGI) >= 2.93
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(LWP::UserAgent)
%endif

Requires:       httpd-mmn = %{_httpd_mmn}
# For Apache::SizeLimit::Core
Requires:       perl(Linux::Pid)

%{?perl_default_filter}

%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Apache2::Connection\\)$
%global __provides_exclude %__provides_exclude|perl\\(Apache2::RequestRec\\)$
%global __provides_exclude %__provides_exclude|perl\\(warnings\\)$
%global __provides_exclude %__provides_exclude|perl\\(HTTP::Request::Common\\)$
%global __provides_exclude %__provides_exclude|mod_perl\\.so\\(.*$
%global __provides_exclude %__provides_exclude|mod_perl\\.so$
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Apache::Test.*\\)
%global __requires_exclude %__requires_exclude|perl\\(Data::Flow\\)
%global __requires_exclude %__requires_exclude|perl\\(Apache2::FunctionTable\\)
%global __requires_exclude %__requires_exclude|perl\\(Apache2::StructureTable\\)

# Hide dependencies on broken provides
%global __requires_exclude %__requires_exclude|^perl\\(Apache2::MPM\\)

%description
Mod_perl incorporates a Perl interpreter into the Apache web server,
so that the Apache web server can directly execute Perl code.
Mod_perl links the Perl run-time library into the Apache web server and
provides an object-oriented Perl interface for Apache's C language
API.  The end result is a quicker CGI script turnaround process, since
no external Perl interpreter has to be started.

Install mod_perl if you're installing the Apache web server and you'd
like for it to directly incorporate a Perl interpreter.


%package devel
Summary:        Files needed for building XS modules that use mod_perl
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       httpd-devel%{?_isa}
Requires:       perl(IO::Dir)

%description devel 
The mod_perl-devel package contains the files needed for building XS
modules that use mod_perl.


%if %{with mod_perl_enables_bundled_Apache_Reload}
%package -n perl-Apache-Reload
Version:        0.13
Summary:        Reload changed Perl modules
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
# The mod_perl2 1.99022 is not used, pick for example ModPerl::Util to
# constrain the version.
Requires:       perl(ModPerl::Util) >= 1.99022
Conflicts:      mod_perl < 2.0.10-4
Provides:       bundled(Apache-Reload) = %{version}

# Fiter-underspecified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(ModPerl::Util\\)$

%description -n perl-Apache-Reload
This mod_perl extension allows to reload Perl modules that changed on the disk.
%endif


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p 1

# Remove docs/os. It's only win32 info with non-ASL-2.0 license. Bug #1199044.
rm -rf docs/os
# Remove bundled Apache-Reload
%if %{without mod_perl_enables_bundled_Apache_Reload}
rm -rf Apache-Reload
sed -i -e '/Apache-Reload/d' Makefile.PL MANIFEST
%endif
# Remove failing tests, CPAN RT#118919, CPAN RT#132919
for F in \
    ModPerl-Registry/t/closure.t \
    ModPerl-Registry/t/special_blocks.t \
    ModPerl-Registry/t/perlrun_extload.t \
    t/filter/in_bbs_inject_header.t \
    t/filter/TestFilter/in_bbs_inject_header.pm \
;do
    rm "$F"
    sed -i -e '\,^'"$F"',d' MANIFEST
done

%build
CFLAGS="$RPM_OPT_FLAGS -fpic" perl Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{_httpd_apxs} \
         MP_APR_CONFIG=%{_bindir}/apr-1-config

# This is not needed now when we are using httpd24 branch, but I will keep
# it here in case someone will have to regenerate *.xs files again.
%if %{regenerate_xs}0
%{make_build} source_scan
%{make_build} xs_generate
CFLAGS="$RPM_OPT_FLAGS -fpic" perl Makefile.PL </dev/null \
         PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
         INSTALLDIRS=vendor \
         MP_APXS=%{_httpd_apxs} \
         MP_APR_CONFIG=%{_bindir}/apr-1-config
%endif

%{make_build} -C src/modules/perl OPTIMIZE="$RPM_OPT_FLAGS -fpic"
%{make_build}

%install
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_moddir}
# Not parallel-safe
make install \
    MODPERL_AP_LIBEXECDIR=$RPM_BUILD_ROOT%{_httpd_moddir} \
    MODPERL_AP_INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}/httpd

# Remove files not suitable for distribution.
find $RPM_BUILD_ROOT -type f -name .packlist -delete
find $RPM_BUILD_ROOT -type f -name perllocal.pod -delete
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -delete
# Remove empty vendor_perl/auto/mod_perl2 directory.
find $RPM_BUILD_ROOT -depth -type d -empty -delete

# Fix permissions to avoid strip failures on non-root builds.
%{_fixperms} $RPM_BUILD_ROOT/*

# Install the config file
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_confdir}
install -d -m 755 $RPM_BUILD_ROOT%{_httpd_modconfdir}
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_httpd_confdir}
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_httpd_modconfdir}/02-perl.conf

# Move set of modules to -devel
devmods="ModPerl::Code ModPerl::BuildMM ModPerl::CScan \
          ModPerl::TestRun ModPerl::Config ModPerl::WrapXS \
          ModPerl::BuildOptions ModPerl::Manifest \
          ModPerl::MapUtil ModPerl::StructureMap \
          ModPerl::TypeMap ModPerl::FunctionMap \
          ModPerl::ParseSource ModPerl::MM \
          Apache2::Build Apache2::ParseSource Apache2::BuildConfig \
          Bundle::ApacheTest"
for m in $devmods; do
   test -f $RPM_BUILD_ROOT%{_mandir}/man3/${m}.3pm &&
     echo "%{_mandir}/man3/${m}.3pm*"
   fn=${m//::/\/}
   test -f $RPM_BUILD_ROOT%{perl_vendorarch}/${fn}.pm &&
        echo %{perl_vendorarch}/${fn}.pm
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/${fn} && 
        echo %{perl_vendorarch}/${fn}
   test -d $RPM_BUILD_ROOT%{perl_vendorarch}/auto/${fn} && 
        echo %{perl_vendorarch}/auto/${fn}
done | tee devel.files | sed 's/^/%%exclude /' > exclude.files
echo "%%exclude %{_mandir}/man3/Apache::Test*.3pm*" >> exclude.files

# perl build script generates *.orig files, they get installed and later they
# break provides so mod_perl requires mod_perl-devel. We remove them here.
find "$RPM_BUILD_ROOT" -type f -name *.orig -delete

%check
make test TEST_VERBOSE=1 && RETVAL=$?
if test "$RETVAL" != 0; then
    # Echo both error_log files if make test returns failure.
    echo BEGIN t/logs/error_log
    cat t/logs/error_log
    echo END t/logs/error_log

    echo BEGIN ModPerl-Registry/t/logs/error_log
    cat ModPerl-Registry/t/logs/error_log
    echo END ModPerl-Registry/t/logs/error_log

    exit 1
fi

%files -f exclude.files
%license LICENSE
%doc Changes CONTRIBUTING.md NOTICE README* STATUS SVN-MOVE docs/
%config(noreplace) %{_httpd_confdir}/perl.conf
%config(noreplace) %{_httpd_modconfdir}/02-perl.conf
%{_bindir}/*
%{_httpd_moddir}/mod_perl.so
%{perl_vendorarch}/auto/*
%dir %{perl_vendorarch}/Apache/
%{perl_vendorarch}/Apache/SizeLimit*
%{perl_vendorarch}/Apache2/
%exclude %{perl_vendorarch}/Apache2/Reload.pm
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/APR/
%{perl_vendorarch}/ModPerl/
%{perl_vendorarch}/*.pm
%{_mandir}/man3/*.3*
%exclude %{_mandir}/man3/Apache::Reload.3pm*
%exclude %{_mandir}/man3/Apache2::Reload.3pm*

%files devel -f devel.files
%{_includedir}/httpd/*
%{perl_vendorarch}/Apache/Test*.pm
%{_mandir}/man3/Apache::Test*.3pm*

%if %{with mod_perl_enables_bundled_Apache_Reload}
%files -n perl-Apache-Reload
%dir %{perl_vendorarch}/Apache/
%{perl_vendorarch}/Apache/Reload.pm
%dir %{perl_vendorarch}/Apache2/
%{perl_vendorarch}/Apache2/Reload.pm
%{_mandir}/man3/Apache::Reload.3pm*
%{_mandir}/man3/Apache2::Reload.3pm*
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.13-10
- Perl 5.42 rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 05 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 2.0.13-8
- Add lmdb and openldap devel buildrequires, fixes RHBZ#2302876

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.13-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.13-5
- Perl 5.40 rebuild

* Fri Feb 02 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 2.0.13-4
- fix ftbs on i686, BZ 2261386

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 22 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 2.0.13-1
- 2.0.13 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.12-8
- Perl 5.38 rebuild

* Thu Jun 01 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.12-7
- Do not use deprecated do_open9() (CPAN RT#148451)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.12-4
- Perl 5.36 rebuild

* Wed Feb 23 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 2.0.12-3
- remove perlrun_extload test
- use autosetup macro

* Sat Feb 12 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 2.0.12-2
- Echo both error_log files in the event of a make test failure

* Wed Feb 02 2022 Petr Pisar <ppisar@redhat.com> - 2.0.12-1
- 2.0.12 bump

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Petr Pisar <ppisar@redhat.com> - 2.0.11-9
- Fix detecting APR features broken by a multilib-sanitized apr.h (bug #1981927)

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.11-8
- Perl 5.34 rebuild

* Mon May 17 2021 Petr Pisar <ppisar@redhat.com> - 2.0.11-7
- Fix a crash due to wrong use of perl_parse()
- Fix building with perl 5.34 (Perl GH#18617)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Petr Pisar <ppisar@redhat.com> - 2.0.11-4
- Enable tests
- Do not use deprecated ap_get_server_version() (CPAN RT#124972)
- Use httpd 2.4 access rules in an example in perl.conf
- Disable ModPerl-Registry/t/closure.t and ModPerl-Registry/t/special_blocks.t
  tests (CPAN RT#132919)

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.11-3
- Perl 5.32 rebuild
- Disable tests

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.11-1
- 2.0.11 bump

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.10-16
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.0.10-14
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Aug 29 2018 Petr Pisar <ppisar@redhat.com> - 2.0.10-13
- Fix CVE-2011-2767 (arbitrary Perl code execution in the context of the user
  account via a user-owned .htaccess) (bug #1623267)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.10-11
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.0.10-9
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Petr Pisar <ppisar@redhat.com> - 2.0.10-6
- Remove bundled Apache-Reload (bug #1225037)

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.10-5
- Perl 5.26 rebuild

* Fri Mar 24 2017 Petr Pisar <ppisar@redhat.com> - 2.0.10-4
- Sub-package Apache::Reload and Apache2::Reload into perl-Apache-Reload
  (bug #1225037)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Petr Pisar <ppisar@redhat.com> - 2.0.10-2
- Adapt tests to httpd-2.4.25 (bug #1409610)

* Tue Nov 22 2016 Petr Pisar <ppisar@redhat.com> - 2.0.10-1
- 2.0.10 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.9-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 19 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.9-2
- fix #1272901 - add perl(Test) to BuildRequires

* Fri Jun 19 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.9-1
- update to 2.0.9

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-14.20150311svn1665777
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.8-13.20150311svn1665777
- Perl 5.22 rebuild

* Wed Mar 11 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-12.20150311svn1665777
- update to latest revision from trunk to backport latest upstream fixes

* Fri Mar 06 2015 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-11.20140624svn1602105
- remove docs/os from documentation because of its license (#1199044)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.0.8-10.20140624svn1602105
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-9.20140624svn1602105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-8.20140624svn1602105
- update to latest revision from trunk to backport latest upstream fixes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-7.20140430svn1590627
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-6.20140430svn1590627
- update to latest revision of httpd24threading branch to backport latest upstream fixes

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 2.0.8-5.20131031svn1537408
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Oct 21 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-3.20131031svn1537408
- update to latest revision of httpd24 branch to backport new upstream fixes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3.20130709svn1498417
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.0.8-2.20130709svn1498417
- Perl 5.18 rebuild

* Tue Jul 09 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.8-1.20130709svn1498417
- update to latest revision of httpd24 branch to backport important fixes
  in httpd-2.4 compatibility

* Thu Feb 21 2013 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-12.20130221svn1448242
- update to httpd24 svn branch which provides much more better compatibility
  with httpd-2.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-10
- do not install .orig file generated by make xs_generate
- filter unversioned mod_perl.so from provides

* Mon Nov 19 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-9
- clean up spec file
- do not require -devel when installing main package

* Mon Nov 19 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-8
- add wrappers for new fields added in httpd-2.4 structures

* Wed Jul 25 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-7
- updated httpd-2.4 patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-5
- Hide dependencies on broken provides

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-4
- Perl 5.16 rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-3
- Rebuild to fix Apache2::MPM dependency on i686

* Fri Jun 29 2012 Petr Pisar <ppisar@redhat.com> - 2.0.7-2
- Perl 5.16 rebuild

* Fri Jun 29 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.7-1
- update to 2.0.7 (#830501)

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 2.0.5-11
- Perl 5.16 rebuild

* Thu Apr 19 2012 Petr Pisar <ppisar@redhat.com> - 2.0.5-10
- Fix dependency declaration on Data::Dumper

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.5-9
- fix compilation with httpd-2.4 (#809142)

* Tue Mar 06 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.5-8
- filter perl(HTTP::Request::Common) Provide from -devel (#247250)
- use short_name as argv[0] (#782369)

* Thu Jan  5 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.0.5-7
- Ship Apache::Reload and Apache::SizeLimit in main package (#748362).
- Require Linux::Pid for Apache::SizeLimit (#766568).
- Move Apache::Test* man pages to -devel.
- Don't filter Module::Build dependency.

* Wed Nov  9 2011 Joe Orton <jorton@redhat.com> - 2.0.5-6
- fudge the LFS test (#730832)

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 2.0.5-5
- RPM 4.9 dependency filtering added

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.5-4
- Perl mass rebuild

* Mon Apr 11 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.5-3
- filter warnings from provides

* Sat Mar 26 2011 Joe Orton <jorton@redhat.com> - 2.0.5-2
- ship NOTICE file

* Sat Mar 26 2011 Joe Orton <jorton@redhat.com> - 2.0.5-1
- update to 2.0.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.0.4-13
- fix missing requirements, add filter_setup macro, remove double provides

* Thu Nov 04 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.0.4-12
- Spec cleanup for the merge review

* Fri May 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.0.4-11
- Mass rebuild with perl-5.12.0

* Tue Dec  8 2009 Joe Orton <jorton@redhat.com> - 2.0.4-10
- add security fix for CVE-2009-0796 (#544455)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 17 2008 Joe Orton <jorton@redhat.com> 2.0.4-7
- fix inline abuse (#459351)

* Wed Aug  6 2008 Joe Orton <jorton@redhat.com> 2.0.4-5
- rebuild to fix patch fuzz (#427758)

* Mon Jul 14 2008 Joe Orton <jorton@redhat.com> 2.0.4-4
- rebuild for new BDB

* Tue May 13 2008 Joe Orton <jorton@redhat.com> 2.0.4-3
- trim changelog; rebuild

* Fri Apr 18 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- update to 2.0.4

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.3-21
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.3-20
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Joe Orton <jorton@redhat.com> 2.0.3-19
- further fixes for perl 5.10 (upstream r480903, r615751)

* Wed Jan 30 2008 Joe Orton <jorton@redhat.com> 2.0.3-18
- fix build with perl 5.10 (upstream r480890)

* Tue Jan 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-17
- fix perl BR

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.3-16
- rebuild for new perl

* Thu Dec  6 2007 Joe Orton <jorton@redhat.com> 2.0.3-15
- rebuild for new OpenLDAP

* Wed Sep  5 2007 Joe Orton <jorton@redhat.com> 2.0.3-14
- filter perl(HTTP::Request::Common) Provide from -devel (#247250)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 2.0.3-13
- rebuild for fixed 32-bit APR

* Thu Aug 23 2007 Joe Orton <jorton@redhat.com> 2.0.3-12
- rebuild for expat soname bump

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 2.0.3-11
- rebuild for libdb soname bump

* Mon Aug 20 2007 Joe Orton <jorton@redhat.com> 2.0.3-10
- fix License

* Fri Apr 20 2007 Joe Orton <jorton@redhat.com> 2.0.3-8
- filter provide of perl(warnings) (#228429)

* Wed Feb 28 2007 Joe Orton <jorton@redhat.com> 2.0.3-7
- also restore Apache::Test to devel
- add BR for perl-devel

* Tue Feb 27 2007 Joe Orton <jorton@redhat.com> 2.0.3-6
- filter more Apache::Test requirements

* Mon Feb 26 2007 Joe Orton <jorton@redhat.com> 2.0.3-5
- repackage set of trimmed modules, but only in -devel

* Wed Jan 31 2007 Joe Orton <jorton@redhat.com> 2.0.3-4
- restore ModPerl::MM

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 2.0.3-3
- trim modules even more aggressively (#197841)

* Mon Dec  4 2006 Joe Orton <jorton@redhat.com> 2.0.3-2
- update to 2.0.3
- remove droplet in buildroot from multilib patch
- drop build-related ModPerl:: modules and Apache::Test (#197841)
- spec file cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Thu Jun 15 2006 Joe Orton <jorton@redhat.com> 2.0.2-6
- fix multilib conflicts in -devel (#192733)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.2-5.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 2.0.2-3
- rebuild for httpd 2.2

* Wed Oct 26 2005 Joe Orton <jorton@redhat.com> 2.0.2-2
- update to 2.0.2

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 2.0.1-2
- rebuild

* Fri Jun 17 2005 Warren Togami <wtogami@redhat.com> 2.0.1-1
- 2.0.1

* Fri May 20 2005 Warren Togami <wtogami@redhat.com> 2.0.0-3
- dep changes (#114651 jpo and ville)

* Fri May 20 2005 Joe Orton <jorton@redhat.com> 2.0.0-1
- update to 2.0.0 final

* Mon Apr 18 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.0.0-0.rc5.3
- Fix sample configuration.
- Explicitly disable the test suite. (#112563)

* Mon Apr 18 2005 Joe Orton <jorton@redhat.com> 2.0.0-0.rc5.2
- fix filter-requires for new Apache2:: modules

* Sat Apr 16 2005 Warren Togami <wtogami@redhat.com> - 2.0.0-0.rc5.1
- 2.0.0-RC5

* Sun Apr 03 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 2.0.0-0.rc4.1
- Update to 2.0.0-RC4.
- Specfile cleanup. (#153236)
