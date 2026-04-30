## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 21;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable to avoid all the test suites
%bcond tests 1

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

%bcond bdb %[0%{?fedora} < 33 && 0%{?rhel} < 9]
# Python 2 for F<32, Python 3 for F>=32 and RHEL>=9
%bcond python2 %[0%{?fedora} < 32 && 0%{?rhel} < 9]
%bcond python3 %{without python2}
%bcond pyswig 1
# Java, Ruby bindings and KWallet are not enabled on RHEL
%bcond kwallet %[0%{?fedora} != 0]
%bcond ruby %[0%{?fedora} != 0]
%ifarch %{java_arches}
%bcond java %[0%{?fedora} != 0]
%else
%bcond java 0
%endif

%if %{with python2} == %{with python3}
%error Pick exactly one Python version
%endif

# set JDK path to build javahl; default for JPackage
%define jdk_path /usr/lib/jvm/java

%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%if %{with python2}
%global svn_python_sitearch %{python2_sitearch}
%global svn_python %{__python2}
%global svn_python_br python2-devel
%else
%global svn_python_sitearch %{python3_sitearch}
%global svn_python %{__python3}
%global svn_python_br python3-devel
%endif

Summary: A Modern Concurrent Version Control System
Name: subversion
Version: 1.14.5
Release: %autorelease
License: Apache-2.0
URL: https://subversion.apache.org/
Source0: https://downloads.apache.org/subversion/subversion-%{version}.tar.bz2
Source1: subversion.conf
Source3: filter-requires.sh
Source4: http://www.xsteve.at/prg/emacs/psvn.el
Source5: psvn-init.el
Source6: svnserve.service
Source7: svnserve.tmpfiles
Source8: svnserve.sysconf
Patch1: subversion-1.12.0-linking.patch
Patch2: subversion-1.14.0-testwarn.patch
Patch3: subversion-1.14.2-soversion.patch
Patch4: subversion-1.8.0-rubybind.patch
Patch5: subversion-1.8.5-swigplWall.patch
Patch6: subversion-1.14.1-testnomagic.patch
Patch7: subversion-1.14.2-modsyms.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2255746
Patch8: subversion-1.14.3-zlib-ng.patch
Patch9: subversion-1.14.5-progenv.patch
# Fix tests with Python 3.14, https://github.com/apache/subversion/pull/30
Patch10: subversion-1.14.5-python314.patch
BuildRequires: make
BuildRequires: libxcrypt-devel
BuildRequires: autoconf, libtool, texinfo, which, gcc, gcc-c++
BuildRequires: swig >= 1.3.24, gettext
%if %{with bdb}
BuildRequires: libdb-devel >= 4.1.25
%endif
BuildRequires: %{svn_python_br}
BuildRequires: apr-devel >= 1.5.0, apr-util-devel >= 1.3.0
BuildRequires: libserf-devel >= 1.3.0, cyrus-sasl-devel
BuildRequires: sqlite-devel >= 3.4.0, file-devel, systemd-units
BuildRequires: utf8proc-devel, lz4-devel
# Any apr-util crypto backend needed
BuildRequires: apr-util-openssl
# For systemctl scriptlets
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: emacs-filesystem
Provides: svn = %{version}-%{release}
Requires: subversion-libs%{?_isa} = %{version}-%{release}

%define __perl_requires %{SOURCE3}

# Put Python bindings in site-packages
%define swigdirs swig_pydir=%{svn_python_sitearch}/libsvn swig_pydir_extra=%{svn_python_sitearch}/svn

%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file.  Subversion is intended to be a
compelling replacement for CVS.

%package libs
Summary: Libraries for Subversion Version Control system
# APR 1.3.x interfaces are required
Conflicts: apr%{?_isa} < 1.5.0
# Enforced at run-time by ra_serf
Conflicts: libserf%{?_isa} < 1.3.0

%description libs
The subversion-libs package includes the essential shared libraries
used by the Subversion version control tools.

%if %{with python2} && %{with pyswig}
%package -n python2-subversion
%{?python_provide:%python_provide python2-subversion}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
BuildRequires: python2-devel
Summary: Python bindings for Subversion Version Control system

%description -n python2-subversion
The python2-subversion package includes the Python 2.x bindings to the
Subversion libraries.
%endif
%if %{with python3} && %{with pyswig}
%package -n python3-subversion
%{?python_provide:%python_provide python3-subversion}
Summary: Python bindings for Subversion Version Control system
BuildRequires: python3-devel py3c-devel
BuildRequires: (python3-setuptools if python3-devel >= 3.12)
Requires: subversion-libs%{?_isa} = %{version}-%{release}

%description -n python3-subversion
The python3-subversion package includes the Python 3.x bindings to the
Subversion libraries.
%endif

%package devel
Summary: Development package for the Subversion libraries
Requires: subversion-libs%{?_isa} = %{version}-%{release}
Requires: apr-devel%{?_isa}, apr-util-devel%{?_isa}

%description devel
The subversion-devel package includes the libraries and include files
for developers interacting with the subversion package.

%package gnome
Summary: GNOME Keyring support for Subversion
Requires: subversion-libs%{?_isa} = %{version}-%{release}
BuildRequires: dbus-devel, libsecret-devel

%description gnome
The subversion-gnome package adds support for storing Subversion
passwords in the GNOME Keyring.

%if %{with kwallet}
%package kde
Summary: KDE Wallet support for Subversion
Requires: subversion-libs%{?_isa} = %{version}-%{release}
BuildRequires: qt5-qtbase-devel >= 5.0.0, kf5-kwallet-devel, kf5-ki18n-devel
BuildRequires: kf5-kcoreaddons-devel

%description kde
The subversion-kde package adds support for storing Subversion
passwords in the KDE Wallet.
%endif

%package -n mod_dav_svn
Summary: Apache httpd module for Subversion server
Requires: httpd-mmn = %{_httpd_mmn}
Requires: subversion-libs%{?_isa} = %{version}-%{release}
BuildRequires: httpd-devel >= 2.0.45

%description -n mod_dav_svn
The mod_dav_svn package allows access to a Subversion repository
using HTTP, via the Apache httpd server.

%package perl
Summary: Perl bindings to the Subversion libraries
BuildRequires: perl-devel >= 2:5.8.0, perl-generators, perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More), perl(ExtUtils::Embed)
Requires: subversion-libs%{?_isa} = %{version}-%{release}

%description perl
This package includes the Perl bindings to the Subversion libraries.

%if %{with java}
%package javahl
Summary: JNI bindings to the Subversion libraries
Requires: subversion = %{version}-%{release}
BuildRequires: java-devel
# JAR repacking requires both zip and unzip in the buildroot
BuildRequires: zip, unzip
# For the tests
BuildRequires: junit
BuildArch: noarch

%description javahl
This package includes the JNI bindings to the Subversion libraries.
%endif

%if %{with ruby}
%package ruby
Summary: Ruby bindings to the Subversion libraries
BuildRequires: ruby-devel >= 1.9.1, ruby >= 1.9.1
BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(csv)
Requires: subversion-libs%{?_isa} = %{version}-%{release}
Requires: rubygem(csv)
Conflicts: ruby-libs%{?_isa} < 1.8.2

%description ruby
This package includes the Ruby bindings to the Subversion libraries.
%endif

%package tools
Summary: Supplementary tools for Subversion
Requires: subversion-libs%{?_isa} = %{version}-%{release}

%description tools
This package includes supplementary tools for use with Subversion.

%prep
%autosetup -p1 -S gendiff

:
: === Building:
: === Python3=%{with python3} Python2=%{with python2} PySwig=%{with pyswig}
: === Java=%{with java} Ruby=%{with ruby}
: === BDB=%{with bdb} Tests=%{with tests} KWallet=%{with kwallet}
:

%build
# Regenerate the buildsystem, so that any patches applied to
# configure, swig bindings etc take effect.
mv build-outputs.mk build-outputs.mk.old
export PYTHON=%{svn_python}

### Force regeneration of swig bindings with the buildroot's SWIG.
# Generated files depend on the build/generator/swig/*.py which
# generates them, so when autogen-standalone.mk's autogen-swig target
# is run by autogen.sh it will regenerate them:
touch build/generator/swig/*.py

### Regenerate everything:
# This PATH order makes the fugly test for libtoolize work...
PATH=/usr/bin:$PATH ./autogen.sh --release

# fix shebang lines, #111498
perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in
# fix python executable
perl -pi -e 's|/usr/bin/env python.*|%{svn_python}|' subversion/tests/cmdline/svneditor.py

# override weird -shrext from ruby
export svn_cv_ruby_link="%{__cc} -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""
%if 0%{?fedora} >= 32 || 0%{?rhel} >= 9
# Fix include path for ruby2.7
export svn_cv_ruby_includes="-I%{_includedir}"
%endif

#export EXTRA_CFLAGS="$RPM_OPT_FLAGS -DSVN_SQLITE_MIN_VERSION_NUMBER=3007012 \
#       -DSVN_SQLITE_MIN_VERSION=\\\"3.7.12\\\""
export APACHE_LDFLAGS="-Wl,-z,relro,-z,now"
export CC=gcc CXX=g++ JAVA_HOME=%{jdk_path}

export CFLAGS="%{build_cflags} -Wno-error=incompatible-pointer-types"
# neccessary for libtool compilation of bindings
export LT_CFLAGS="$CFLAGS"

%configure --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
        --disable-debug \
        --with-swig --with-serf=%{_prefix} \
        --with-ruby-sitedir=%{ruby_vendorarchdir} \
        --with-ruby-test-verbose=verbose \
        --with-apxs=%{_httpd_apxs} --disable-mod-activation \
        --enable-plaintext-password-storage \
        --with-apache-libexecdir=%{_httpd_moddir} \
        --disable-static --with-sasl=%{_prefix} \
        --with-libmagic=%{_prefix} \
        --with-gnome-keyring \
%if %{with java}
        --enable-javahl \
        --with-junit=%{_prefix}/share/java/junit.jar \
%endif
%if %{with kwallet}
        --with-kwallet=%{_includedir}:%{_libdir} \
%endif
%if %{with bdb}
        --with-berkeley-db \
%else
        --without-berkeley-db \
%endif
        || (cat config.log; exit 1)
make %{?_smp_mflags} all tools
%if %{with pyswig}
make swig-py swig-py-lib %{swigdirs}
%endif
make swig-pl swig-pl-lib
%if %{with ruby}
make swig-rb swig-rb-lib
%endif
%if %{with java}
# javahl-javah does not parallel-make with javahl
#make javahl-java javahl-javah
make javahl
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT
%if %{with pyswig}
make install-swig-py %{swigdirs} DESTDIR=$RPM_BUILD_ROOT
%endif

make install-swig-pl-lib DESTDIR=$RPM_BUILD_ROOT
%if %{with ruby}
make install-swig-rb DESTDIR=$RPM_BUILD_ROOT
%endif

make pure_vendor_install -C subversion/bindings/swig/perl/native \
        PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with java}
make install-javahl-java install-javahl-lib javahl_javadir=%{_javadir} DESTDIR=$RPM_BUILD_ROOT
%endif

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/subversion

mkdir -p ${RPM_BUILD_ROOT}{%{_httpd_modconfdir},%{_httpd_confdir}}

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_httpd_confdir}
%else
sed -n /^LoadModule/p %{SOURCE1} > 10-subversion.conf
sed    /^LoadModule/d %{SOURCE1} > example.conf
touch -r %{SOURCE1} 10-subversion.conf example.conf
install -p -m 644 10-subversion.conf ${RPM_BUILD_ROOT}%{_httpd_modconfdir}
%endif

# Remove unpackaged files
rm -rf ${RPM_BUILD_ROOT}%{_includedir}/subversion-*/*.txt \
       ${RPM_BUILD_ROOT}%{svn_python_sitearch}/*/*.{a,la}

# The SVN build system is broken w.r.t. DSO support; it treats
# normal libraries as DSOs and puts them in $libdir, whereas they
# should go in some subdir somewhere, and be linked using -module,
# etc.  So, forcibly nuke the .so's for libsvn_auth_{gnome,kde},
# since nothing should ever link against them directly.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libsvn_auth_*.so

# remove stuff produced with Perl modules
find $RPM_BUILD_ROOT -type f \
    -a \( -name .packlist -o \( -name '*.bs' -a -empty \) \) \
    -print0 | xargs -0 rm -f

# make Perl modules writable so they get stripped
find $RPM_BUILD_ROOT%{_libdir}/perl5 -type f -perm 555 -print0 |
        xargs -0 chmod 755

# unnecessary libraries for swig bindings
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libsvn_swig_*.{so,la,a}

# Remove unnecessary ruby libraries
rm -f ${RPM_BUILD_ROOT}%{ruby_vendorarchdir}/svn/ext/*.*a

# Trim what goes in docdir
rm -rvf tools/*/*.in tools/hook-scripts/mailer/tests

# Install psvn for emacs
for f in emacs/site-lisp; do
  install -m 755 -d ${RPM_BUILD_ROOT}%{_datadir}/$f
  install -m 644 $RPM_SOURCE_DIR/psvn.el ${RPM_BUILD_ROOT}%{_datadir}/$f
done

install -m 644 $RPM_SOURCE_DIR/psvn-init.el \
        ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# Rename authz_svn INSTALL doc for docdir
ln -f subversion/mod_authz_svn/INSTALL mod_authz_svn-INSTALL

# Trim exported dependencies to APR libraries only:
sed -i "/^dependency_libs/{
     s, -l[^ ']*, ,g;
     s, -L[^ ']*, ,g;
     s,%{_libdir}/lib[^a][^p][^r][^ ']*.la, ,g;
     }"  $RPM_BUILD_ROOT%{_libdir}/*.la

# Trim libdir in pkgconfig files to avoid multilib conflicts
sed -i '/^libdir=/d' $RPM_BUILD_ROOT%{_datadir}/pkgconfig/libsvn*.pc

# Install bash completion
install -Dpm 644 tools/client-side/bash_completion \
        $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/svn
for comp in svnadmin svndumpfilter svnlook svnsync svnversion; do
    ln -s svn \
        $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/${comp}
done

# Install svnserve bits
mkdir -p %{buildroot}%{_unitdir} \
      %{buildroot}/run/svnserve \
      %{buildroot}%{_prefix}/lib/tmpfiles.d \
      %{buildroot}%{_sysconfdir}/sysconfig

install -p -m 644 $RPM_SOURCE_DIR/svnserve.service \
        %{buildroot}%{_unitdir}/svnserve.service
install -p -m 644 $RPM_SOURCE_DIR/svnserve.tmpfiles \
        %{buildroot}%{_prefix}/lib/tmpfiles.d/svnserve.conf
install -p -m 644 $RPM_SOURCE_DIR/svnserve.sysconf \
        %{buildroot}%{_sysconfdir}/sysconfig/svnserve

# Install tools ex diff*, x509-parser
make install-tools DESTDIR=$RPM_BUILD_ROOT toolsdir=%{_bindir}
rm -f $RPM_BUILD_ROOT%{_bindir}/diff* $RPM_BUILD_ROOT%{_bindir}/x509-parser

# Don't add spurious dependency in libserf-devel
sed -i "/^Requires.private/s, serf-1, ," \
    $RPM_BUILD_ROOT%{_datadir}/pkgconfig/libsvn_ra_serf.pc

# Make svnauthz-validate a symlink
rm $RPM_BUILD_ROOT%{_bindir}/svnauthz-validate
ln -s svnauthz $RPM_BUILD_ROOT%{_bindir}/svnauthz-validate

for f in svn-populate-node-origins-index fsfs-access-map \
    svnauthz svnauthz-validate svnmucc svnraisetreeconflict svnbench \
    svn-mergeinfo-normalizer fsfs-stats svnmover svnconflict; do
    echo %{_bindir}/$f
    if test -f $RPM_BUILD_ROOT%{_mandir}/man?/${f}.*; then
       echo %{_mandir}/man?/${f}.*
    fi
done | tee tools.files | sed 's/^/%%exclude /' > exclude.tools.files

%find_lang %{name}

cat %{name}.lang exclude.tools.files >> %{name}.files

%if %{with tests}
%check
export LANG=C LC_ALL=C
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
export MALLOC_PERTURB_=171 MALLOC_CHECK_=3
export LIBC_FATAL_STDERR_=1
export PYTHON=%{svn_python}

: Run svnauthz to avoid regeneration during test suite.
tools/server-side/svnauthz --version || exit 1

if ! make check CLEANUP=yes PARALLEL=${RPM_BUILD_NCPUS}; then
   : Test suite failure.
   cat fails.log
   cat tests.log
   exit 1
fi
if ! make check-swig-pl; then
   : Swig test failure.
   exit 1
fi
%if %{with pyswig}
if ! make check-swig-py; then
   : Python swig test failure.
   exit 1
fi
%endif
%if %{with ruby}
if ! make check-swig-rb; then
   : Ruby swig test failure.
   exit 1
fi
%endif
%if %{with java}
make check-javahl
%endif
%endif

%post
%systemd_post svnserve.service

%preun
%systemd_preun svnserve.service

%postun
%systemd_postun_with_restart svnserve.service

%ldconfig_scriptlets libs

%ldconfig_scriptlets perl

%ldconfig_scriptlets ruby

%if %{with java}
%ldconfig_scriptlets javahl
%endif

%files -f %{name}.files
%{!?_licensedir:%global license %%doc}
%license LICENSE NOTICE
%doc BUGS COMMITTERS INSTALL README CHANGES
%doc mod_authz_svn-INSTALL
%{_bindir}/*
%{_mandir}/man*/*
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/bash-completion/
%config(noreplace) %{_sysconfdir}/sysconfig/svnserve
%dir %{_sysconfdir}/subversion
%exclude %{_mandir}/man*/*::*
%{_unitdir}/*.service
%attr(0700,root,root) %dir /run/svnserve
%{_prefix}/lib/tmpfiles.d/svnserve.conf

%files tools -f tools.files
%doc tools/hook-scripts tools/backup tools/examples tools/xslt
%if %{with bdb}
%doc tools/bdb
%endif

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE NOTICE
%{_libdir}/libsvn*.so.*
%exclude %{_libdir}/libsvn_swig_perl*
%exclude %{_libdir}/libsvn_swig_ruby*
%if %{with java}
%{_libdir}/libsvnjavahl-*.so
%endif
%if %{with kwallet}
%exclude %{_libdir}/libsvn_auth_kwallet*
%endif
%exclude %{_libdir}/libsvn_auth_gnome*

%if %{with python2} && %{with pyswig}
%files -n python2-subversion
%{python2_sitearch}/svn
%{python2_sitearch}/libsvn
%endif

%if %{with python3} && %{with pyswig}
%files -n python3-subversion
%{python3_sitearch}/svn
%{python3_sitearch}/libsvn
%endif

%files gnome
%{_libdir}/libsvn_auth_gnome_keyring-*.so.*

%if %{with kwallet}
%files kde
%{_libdir}/libsvn_auth_kwallet-*.so.*
%endif

%files devel
%{_includedir}/subversion-1
%{_libdir}/libsvn*.*a
%{_libdir}/libsvn*.so
%{_datadir}/pkgconfig/*.pc
%exclude %{_libdir}/libsvn_swig_perl*
%exclude %{_libdir}/libsvnjavahl-*.so

%files -n mod_dav_svn
%config(noreplace) %{_httpd_modconfdir}/*.conf
%{_libdir}/httpd/modules/mod_*.so
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%doc example.conf
%endif

%files perl
%{perl_vendorarch}/auto/SVN
%{perl_vendorarch}/SVN
%{_libdir}/libsvn_swig_perl*
%{_mandir}/man*/*::*

%if %{with ruby}
%files ruby
%{_libdir}/libsvn_swig_ruby*
%{ruby_vendorarchdir}/svn
%endif

%if %{with java}
%files javahl
%{_javadir}/svn-javahl.jar
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.14.5-21
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.14.5-20
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.14.5-19
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.5-17
- Perl 5.42 rebuild

* Thu Jun 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.5-16
- Fix tests for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.14.5-15
- Rebuilt for Python 3.14

* Wed Mar 05 2025 Tomas Korbar <tkorbar@redhat.com> - 1.14.5-14
- Add requirement of emacs-filesystem

* Fri Feb 14 2025 Joe Orton <jorton@fedoraproject.org> - 1.14.5-13
- Merge #12 `run the test suite against the installed binaries`

* Wed Feb 05 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.5-12
- Conditionalize ruby tests

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-11
- fix bcond for non-Java architectures

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-10
- fix java bcond.

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-9
- simplify build conditional definitions.

* Mon Feb 03 2025 Tomas Korbar <tkorbar@redhat.com> - 1.14.5-8
- Fix debuginfo building and stop building ruby and java subpackages

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-7
- enable parallelisation in "make check"

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.14.5-6
- Add explicit BR: libxcrypt-devel

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.5-4
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Dec 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.5-3
- Explicitly add dependency for rubygem(csv) for ruby3.4

* Fri Dec 13 2024 Joe Orton <jorton@redhat.com> - 1.14.5-2
- fix ELN build failure

* Wed Dec 11 2024 Joe Orton <jorton@redhat.com> - 1.14.5-1
- update to 1.14.5 (#2331047) use %%autosetup enable tests by default again

* Fri Nov 01 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.4-1
- Rebase to version 1.14.4

* Mon Oct 07 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-12
- Rebuild for utf8proc SONAME bump

* Tue Aug 06 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-11
- Fix debuginfo generation for bindings

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.3-9
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.14.3-8
- Rebuilt for Python 3.13

* Thu Mar 28 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.3-7
- Do not use %%eln macro

* Mon Mar 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.3-6
- Really rebuild for java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.14.3-5
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-3
- Fix building with gcc 14

* Fri Jan 12 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-2
- Fix testing of binary patch

* Fri Jan 05 2024 Richard Lescak <rlescak@redhat.com> - 1.14.3-1
- rebase to version 1.14.3 (#2256062)

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-26
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Mon Nov 20 2023 Joe Orton <jorton@redhat.com> - 1.14.2-25
- fix mod_authz_svn, mod_dontdothat (#2250182)

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-24
- use %%patch -P throughout

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-23
- restore plaintext password storage by default (per upstream)

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-22
- restrict symbols exposed by DSOs built for httpd

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-20
- Perl 5.38 rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 1.14.2-19
- Rebuilt for Python 3.12

* Mon Jul 03 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-18
- temporary disable tests for eln to prevent FTBFS

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.14.2-17
- Rebuilt for Python 3.12

* Mon May 08 2023 Florian Weimer <fweimer@redhat.com> - 1.14.2-16
- Port to C99

* Thu Feb 16 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-15
- SPDX migration

* Fri Jan 27 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-14
- add requirement for python3-setuptools with new Python 3.12 (#2155420)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-12
- Remove perl(MODULE_COMPAT), it will be replaced by generators

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-11
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Mon Oct 10 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-10
- Really apply ruby32 patch

* Sun Oct 09 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-9
- Backport upstream fix for ruby3.2 support

* Wed Oct 05 2022 Richard Lescak <rlescak@redhat.com> - 1.14.2-8
- fix segfault in Python swig test (#2128024)

* Fri Jul 29 2022 Joe Orton <jorton@redhat.com> - 1.14.2-7
- improve library versioning so filenames are unique across releases

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 05 2022 Joe Orton <jorton@redhat.com> - 1.14.2-5
- disable libmagic during test runs

* Tue Jul 05 2022 Joe Orton <jorton@redhat.com> - 1.14.2-4
- update for new Java arches and bump to JDK 17 (#2103909)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.14.2-3
- Rebuilt for Python 3.11

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-2
- Perl 5.36 rebuild

* Wed May 04 2022 Joe Orton <jorton@redhat.com> - 1.14.2-1
- update to 1.14.2 (#2073852, CVE-2021-28544, CVE-2022-24070)

* Sat Feb 05 2022 Jiri <jvanek@redhat.com> - 1.14.1-12
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-11
- F-36: rebuild against ruby31

* Mon Jan 24 2022 Timm Bäder <tbaeder@redhat.com> - 1.14.1-10
- Disable automatic .la file removal

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Richard Lescak <rlescak@redhat.com> - 1.14.1-8
- Replaced deprecated method readfp() in gen_base.py to build with Python
  3.11 (#2019019)

* Wed Dec 01 2021 Joe Orton <jorton@redhat.com> - 1.14.1-7
- fix intermittent FTBFS in tests (#1956806)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.14.1-5
- Rebuilt for Python 3.10

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.1-4
- Perl 5.34 rebuild

* Thu May 20 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.1-3
- Temporary disable the tests for Perl mass rebuil

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.14.1-2
- Rebuilt for updated systemd-rpm-macros

* Wed Feb 10 2021 Joe Orton <jorton@redhat.com> - 1.14.1-1
- update to 1.14.1 (#1927265, #1768698) Resolves: rhbz#1768698 Resolves:
  rhbz#1927265

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Tom Stellard <tstellar@redhat.com> - 1.14.0-20
- Add BuildRequires: make

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-19
- F-34: rebuild against ruby 3.0

* Fri Dec 11 2020 Joe Orton <jorton@redhat.com> - 1.14.0-18
- strip libdir from pkgconfig files add missing -libs dep from
  python3-subversion

* Thu Dec 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-17
- fix KWallet conditional (#1902598) Resolves: rhbz#1902598

* Wed Dec 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-16
- Reorder bconds.

* Mon Nov 30 2020 Jan Grulich <jgrulich@redhat.com> - 1.14.0-15
- Disable KWallet for RHEL and ELN Resolves: bz#1902598

* Tue Sep 29 2020 Joe Orton <jorton@redhat.com> - 1.14.0-14
- bump required apr-devel BR gcc, gcc-c++

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.0-11
- Perl 5.32 rebuild

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-10
- Fix chronology, again.

* Wed Jun 03 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.14.0-9
- Minor conditional fixes for ELN

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-8
- Fix chronology more.

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-7
- use minor version as libtool library revision number

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-6
- Amend changelog.

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-5
- Seems the ruby bindings failure was a false -ve, though libsvn_swig_ruby
  only builds with many mismatched callback pointer types, so looks
  dubious.

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-4
- disable Ruby bindings, failing tests with Ruby 2.7

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-3
- remove duplicated %%changelog entries

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-2
- enable Python swig bindings by default for f32+

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-1
- update to 1.14.0 (#1840565, #1812195) Resolves: rhbz#1812195 Resolves:
  rhbz#1840565

* Mon Jun 01 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-2
- revise %%changelog history to restore chronological order

* Mon Jun 01 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-1
- Merge branch 'unstable'

* Tue Apr 28 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.12.2-9
- fixed the build-requires

* Tue Apr 28 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.12.2-8
- Updated build-requires for java and qt5

* Wed Feb 12 2020 Joe Orton <jorton@redhat.com> - 1.12.2-7
- fix FTBFS on 32-bit arches (#1800120) Resolves: rhbz#1800120

* Wed Feb 12 2020 Joe Orton <jorton@redhat.com> - 1.12.2-6
- conditionally package bdb tools in -tools

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.12.2-4
- F-32: fix include path for ruby 2.7 Rebuild for ruby 2.7

* Mon Jan 06 2020 Joe Orton <jorton@redhat.com> - 1.12.2-3
- update for KDE 5 (Phil O, #1768693) Resolves: rhbz#1768693

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1.12.2-2
- switch to Python 3 for F32+ (#1737928) Resolves: rhbz#1737928

* Thu Jul 25 2019 Joe Orton <jorton@redhat.com> - 1.12.2-1
- update to 1.12.2

* Thu Jul 25 2019 Joe Orton <jorton@redhat.com> - 1.12.0-4
- Catch issues better in markdown conversion.

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.12.0-3
- Perl 5.30 rebuild

* Thu May 02 2019 Joe Orton <jorton@redhat.com> - 1.12.0-2
- merge pie/rpath patches into one; drop PIE stuff which shouldn't be
  needed any more with current Fedora?

* Wed May 01 2019 Joe Orton <jorton@redhat.com> - 1.12.0-1
- update to 1.12.0 (#1702471) Resolves: rhbz#1702471

* Wed Apr 17 2019 Joe Orton <jorton@redhat.com> - 1.11.1-8
- Add pullrev.sh script.

* Wed Apr 17 2019 Joe Orton <jorton@redhat.com> - 1.11.1-7
- fix build with APR 1.7.0 (upstream r1857391)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.11.1-5
- Remove obsolete Group tag

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.11.1-4
- Remove obsolete ldconfig scriptlets

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.1-3
- F-30: rebuild against ruby26

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.11.1-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jan 11 2019 Joe Orton <jorton@redhat.com> - 1.11.1-1
- update to 1.11.1

* Thu Nov 01 2018 Joe Orton <jorton@redhat.com> - 1.11.0-2
- Updated sed script to convert CHANGES to markdown.

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 1.11.0-1
- update to 1.11.0

* Thu Oct 11 2018 Joe Orton <jorton@redhat.com> - 1.10.3-1
- update to 1.10.3

* Fri Jul 20 2018 Joe Orton <jorton@redhat.com> - 1.10.2-2
- Remove obsolete patches.

* Fri Jul 20 2018 Joe Orton <jorton@redhat.com> - 1.10.2-1
- update to 1.10.2 (#1603197) Resolves: rhbz#1603197

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10.0-11
- Perl 5.28 rebuild

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 1.10.0-10
- fix test suite invocation

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 1.10.0-9
- Narrow swig-disabling to just Python bindings.

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 1.10.0-8
- Remove old source.

* Wed Jun 27 2018 Joe Orton <jorton@redhat.com> - 1.10.0-7
- really disable Berkeley DB support if required by bcond add build
  conditional to disable swig binding subpackages

* Tue May 01 2018 Joe Orton <jorton@redhat.com> - 1.10.0-6
- remove build and -devel deps on libgnome-keyring-devel

* Tue May 01 2018 Joe Orton <jorton@redhat.com> - 1.10.0-5
- drop -devel dep on libserf-devel

* Tue Apr 24 2018 Joe Orton <jorton@redhat.com> - 1.10.0-4
- add bdb, tests as build conditional

* Tue Apr 24 2018 Joe Orton <jorton@redhat.com> - 1.10.0-3
- add bdb build conditional

* Tue Apr 17 2018 Joe Orton <jorton@redhat.com> - 1.10.0-2
- move new tools to -tools

* Mon Apr 16 2018 Joe Orton <jorton@redhat.com> - 1.10.0-1
- update to 1.10.0 (#1566493) Resolves: rhbz#1566493

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com> - 1.9.7-11
- more python2 fixes for #1552079

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com> - 1.9.7-10
- add build conditionals for python2, python3 and kwallet Resolves:
  rhbz#1552079

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com>
- More Python2/3 improvements.

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com> - 1.9.7-8
- For Subversion 1.9, only run test suite with Py2 (Py3 supported with
  1.10).

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com> - 1.9.7-7
- add build conditionals for python2, python3 and kwallet

* Fri Feb 09 2018 Joe Orton <jorton@redhat.com> - 1.9.7-6
- force use of Python2 in test suite

* Thu Feb 08 2018 Joe Orton <jorton@redhat.com> - 1.9.7-5
- force use of Python2 in test suite

* Thu Feb 01 2018 Joe Orton <jorton@redhat.com> - 1.9.7-4
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/rpms/subversion

* Tue Jan 02 2018 Joe Orton <jorton@redhat.com> - 1.9.7-3
- trim changelog, remove mailer tests from -tools

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.7-2
- Python 2 binary package renamed to python2-subversion

* Fri Aug 11 2017 Joe Orton <jorton@redhat.com> - 1.9.7-1
- update to 1.9.7 (CVE-2017-9800, #1480402) add Documentation= to
  svnserve.service Resolves: rhbz#1480335 Resolves: rhbz#1480402

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-9
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Joe Orton <jorton@redhat.com> - 1.9.6-7
- move javahl .so to -libs (#1469158) Resolves: rhbz#1469158

* Mon Jul 10 2017 Joe Orton <jorton@redhat.com> - 1.9.6-6
- Merge branch 'f26'

* Mon Jul 10 2017 Joe Orton <jorton@redhat.com> - 1.9.6-5
- disable tests on ppc64

* Thu Jul 06 2017 Joe Orton <jorton@redhat.com> - 1.9.6-4
- fix build.

* Thu Jul 06 2017 Joe Orton <jorton@redhat.com> - 1.9.6-3
- update to 1.9.6 (#1467890) update to latest upstream psvn.el move
  libsvnjavahl to -libs, build -javahl noarch Resolves: rhbz#1467890

* Thu Jul 06 2017 Joe Orton <jorton@redhat.com> - 1.9.6-2
- update to 1.9.6 (#1467890) update to latest upstream psvn.el Resolves:
  rhbz#1467890

* Thu Jul 06 2017 Joe Orton <jorton@redhat.com> - 1.9.6-1
- merge

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.5-6
- Perl 5.26 rebuild

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 1.9.5-5
- Fix to use JIRA links.

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 1.9.5-4
- Remove unnecessary whitespace.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.5-2
- F-26: rebuild for ruby24

* Mon Jan 02 2017 Joe Orton <jorton@redhat.com> - 1.9.5-1
- update to 1.9.5 (#1400040, CVE-2016-8734) Resolves: rhbz#1400040
  Resolves: rhbz#1399871 Resolves: rhbz#888755

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Fri Jun 24 2016 Petr Písař <ppisar@redhat.com> - 1.9.4-4
- Mandatory Perl build-requires added
  <https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl>

* Thu May 26 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.4-3
- Enable tests; Revert one of Ruby 2.2 fixes

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.4-2
- Perl 5.24 rebuild

* Sun May 08 2016 Peter Robinson <pbrobinson@gmail.com> - 1.9.4-1
- Update to 1.9.4 (#1331222) CVE-2016-2167 CVE-2016-2168 - Move tools in
  docs to tools subpackage (rhbz 1171757 1199761) - Disable make check to
  work around FTBFS

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Joe Orton <jorton@redhat.com> - 1.9.3-2
- rebuild for Ruby 2.3

* Tue Dec 15 2015 Joe Orton <jorton@redhat.com> - 1.9.3-1
- update to 1.9.3 (#1291683)
- use private /tmp in svnserve.service Resolves: rhbz#1291683

* Fri Sep 25 2015 Joe Orton <jorton@redhat.com> - 1.9.2-2
- Add script to turn CHANGES into markdown for bodhi.

* Thu Sep 24 2015 Joe Orton <jorton@redhat.com> - 1.9.2-1
- update to 1.9.2 (#1265447)

* Mon Sep 14 2015 Joe Orton <jorton@redhat.com> - 1.9.1-1
- update to 1.9.1 (#1259099)

* Mon Aug 24 2015 Joe Orton <jorton@redhat.com> - 1.9.0-2
- package pkgconfig files

* Mon Aug 24 2015 Joe Orton <jorton@redhat.com> - 1.9.0-1
- update to 1.9.0 (#1207835)

* Tue Jul 14 2015 Joe Orton <jorton@redhat.com> - 1.8.13-8
- restore dep on systemd (#1183873)

* Tue Jul 14 2015 Joe Orton <jorton@redhat.com> - 1.8.13-7
- move svnmucc man page to -tools

* Tue Jul 14 2015 Joe Orton <jorton@redhat.com> - 1.8.13-6
- move svnauthz to -tools; make svnauthz-validate a symlink

* Fri Jul 10 2015 Joe Orton <jorton@redhat.com> - 1.8.13-5
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/subversion

* Fri Jul 10 2015 Joe Orton <jorton@redhat.com> - 1.8.13-4
- rebuild with tests enabled

* Tue Apr 21 2015 Peter Robinson <pbrobinson@gmail.com> - 1.8.13-3
- Disable tests to fix swig test issues

* Wed Apr 08 2015 Vít Ondruch <vondruch@redhat.com> - 1.8.13-2
- Fix Ruby's test suite.

* Wed Apr 08 2015 Joe Orton <jorton@redhat.com> - 1.8.13-1
- update to 1.8.13 (#1207835)
- attempt to patch around SWIG issues Resolves: rhbz#1207835

* Tue Feb 24 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.11-4
- Revert "SWIG Test Rebuild"

* Tue Feb 24 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.11-3
- SWIG Test Rebuild

* Tue Dec 16 2014 Joe Orton <jorton@redhat.com> - 1.8.11-2
- Remove old sources.

* Tue Dec 16 2014 Joe Orton <jorton@redhat.com> - 1.8.11-1
- update to 1.8.11 (#1174521)
- require newer libserf (#1155670) Resolves: rhbz#1155670 Resolves:
  rhbz#1174521

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-7
- prevents assert()ions in library code (#1058693)

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-6
- drop sysv conversion trigger (#1133786)

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-5
- move svn-bench, fsfs-* to -tools

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.10-4
- Perl 5.20 rebuild

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 1.8.10-3
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Joe Orton <jorton@redhat.com> - 1.8.10-2
- Merge.

* Mon Aug 18 2014 Joe Orton <jorton@redhat.com> - 1.8.10-1
- update to 1.8.10 (#1129100, #1128884, #1125800)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-7
- update to 1.8.9 (#1100779)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-6
- update to 1.8.9 (#1100779)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-5
- update to 1.8.9 (#1100779)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-4
- update to 1.8.9 (#1100779)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-3
- update to 1.8.9 (#1100779)

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-2
- merge

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-1
- update to 1.8.9 (#1100779)

* Wed Apr 23 2014 Joe Orton <jorton@redhat.com> - 1.8.8-6
- remove debugging test run

* Wed Apr 23 2014 Joe Orton <jorton@redhat.com> - 1.8.8-5
- require minitest 4 to fix tests for Ruby bindings (#1089252)

* Tue Apr 22 2014 Joe Orton <jorton@redhat.com> - 1.8.8-4
- rebuild with rubygem-test-unit (#1089252)

* Tue Apr 22 2014 Joe Orton <jorton@redhat.com> - 1.8.8-3
- rebuild

* Wed Mar 05 2014 Joe Orton <jorton@redhat.com> - 1.8.8-2
- drop conditional support for db4

* Fri Feb 28 2014 Joe Orton <jorton@redhat.com> - 1.8.8-1
- update to 1.8.8

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 1.8.5-58
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Jan 06 2014 Joe Orton <jorton@redhat.com>
- bump release.

* Mon Jan 06 2014 Joe Orton <jorton@redhat.com>
- fix permissions of /run/svnserve (#1048422)

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com>
- remove empty patches

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com>
- remove empty patch.

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com>
- don't drop -Wall when building swig Perl bindings (#1037341)

* Mon Dec 02 2013 Joe Orton <jorton@redhat.com>
- Fix diff again.

* Mon Dec 02 2013 Joe Orton <jorton@redhat.com>
- rediff

* Mon Dec 02 2013 Joe Orton <jorton@redhat.com>
- update SQLite 3.8 patches, thanks to Andreas Stieger

* Mon Dec 02 2013 Joe Orton <jorton@redhat.com>
- update SQLite 3.8 support patches, thanks to Andreas Stieger

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com>
- Fix spello.

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com>
- update to 1.8.5 (#1034130)
- add fix for wc-queries-test breakage (h/t Andreas Steiger, r1542774)
  Resolves: rhbz#985582 Resolves: rhbz#1034130

* Mon Nov 18 2013 Joe Orton <jorton@redhat.com>
- add fix for ppc breakage (Andreas Stieger, #985582)

* Tue Oct 29 2013 Joe Orton <jorton@redhat.com>
- update to 1.8.4

* Tue Sep 03 2013 Joe Orton <jorton@redhat.com>
- move bash completions out of /etc (#922993)

* Tue Sep 03 2013 Joe Orton <jorton@redhat.com>
- update to 1.8.3

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com>
- rebuild for perl 5.18 (again)

* Thu Jul 25 2013 Joe Orton <jorton@redhat.com>
- update to 1.8.1

* Fri Jul 19 2013 Joe Orton <jorton@redhat.com>
- temporarily ignore test suite failures on ppc* (#985582)

* Thu Jul 18 2013 Joe Orton <jorton@redhat.com>
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/subversion

* Thu Jun 20 2013 Joe Orton <jorton@redhat.com>
- fix serf requirement

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- fix DSO install dir

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- fix BR for apr-util-openssl to be a BR

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- add 1.8.0 sources

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- add 1.8.0 sources

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- use full relro in mod_dav_svn build (#973694)

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- update patches for 1.8.0

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- renumber patches.

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com>
- update to 1.8.0; switch to serf

* Mon Jun 03 2013 Joe Orton <jorton@redhat.com>
- update to 1.7.10 (#970014)
- fix aarch64 build issues (Dennis Gilmore, #926578) Resolves:
  CVE-2013-1968

* Thu May 09 2013 Joe Orton <jorton@redhat.com>
- fix spurious failures in ruby test suite (upstream r1327373)

* Thu May 09 2013 Joe Orton <jorton@redhat.com>
- try harder to avoid svnserve bind failures in ruby binding tests
- enable verbose output for ruby binding tests Resolves: rhbz#960127

* Tue Apr 09 2013 Joe Orton <jorton@redhat.com>
- update to 1.7.9

* Fri Mar 29 2013 Vít Ondruch <vondruch@redhat.com>
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0 Drop Ruby
  version checks from configuration script. Fix and enable Ruby test suite.

* Fri Mar 15 2013 Joe Orton <jorton@redhat.com>
- Merge from master.

* Thu Mar 14 2013 Joe Orton <jorton@redhat.com>
- drop specific dep on ruby(abi)

* Tue Jan 08 2013 Joe Orton <jorton@redhat.com>
- update to latest psvn.el

* Tue Jan 08 2013 Joe Orton <jorton@redhat.com>
- fix %%date

* Tue Jan 08 2013 Joe Orton <jorton@redhat.com>
- Scriptlets replaced with new systemd macros (#850410)

* Fri Jan 04 2013 Joe Orton <jorton@redhat.com>
- update to 1.7.8

* Thu Oct 11 2012 Joe Orton <jorton@redhat.com>
- update to 1.7.7

* Fri Aug 17 2012 Joe Orton <jorton@redhat.com>
- update to 1.7.6

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Joe Orton <jorton@redhat.com>
- merge

* Mon Jul 16 2012 Joe Orton <jorton@redhat.com>
- switch svnserve pidfile to use /run, use /usr/lib/tmpfiles.d (#840195)

* Tue May 22 2012 Joe Orton <jorton@redhat.com>
- remove patches merged upstream.

* Tue May 22 2012 Joe Orton <jorton@redhat.com>
- update to 1.7.5

* Tue Apr 24 2012 Joe Orton <jorton@redhat.com>
- drop strict sqlite version requirement (#815396)

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com>
- switch to libdb-devel (#814090)

* Thu Apr 19 2012 Joe Orton <jorton@redhat.com>
- adapt for conf.modules.d with httpd 2.4
- add possible workaround for kwallet crasher (#810861) Resolves:
  rhbz#810861

* Tue Apr 17 2012 Joe Orton <jorton@redhat.com>
- possible fix/workaround for 810861

* Tue Apr 10 2012 Joe Orton <jorton@redhat.com>
- fix comment grammar

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com>
- re-enable test suite

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com>
- disable tests, enable kwallet

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com>
- fix build with httpd 2.4

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 1.7.4-3
- test w/o kwallet again.

* Mon Mar 12 2012 Joe Orton <jorton@redhat.com> - 1.7.4-2
- restore necessary hashorder fix

* Mon Mar 12 2012 Joe Orton <jorton@redhat.com> - 1.7.4-1
- update to 1.7.4
- fix build with httpd 2.4

* Thu Mar 01 2012 Joe Orton <jorton@redhat.com> - 1.7.3-22
- re-enable kwallet (#791031)

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-21
- update psvn

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-20
- add tools subpackage (#648015)

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-19
- better trim doc dir to avoid breaking svnmucc tests

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-18
- further hash order fix from upstream

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-17
- trim contents of doc dic (#746433)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-16
- re-enable test suite

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-15
- %%files fixes to infinity

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-14
- yet another %%files fix

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-13
- fix %%files

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-12
- fix %%install

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-11
- more hash order fixes

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-10
- build w/o test suite

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-9
- more files list fixes, remove init script

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-8
- correct files list

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-7
- fix ruby sitedir name

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-6
- fix config file location

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-5
- convert svnserve to systemd (#754074)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-4
- use ruby vendorlib directory (#798203)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-3
- add upstream test suite fixes for APR hash change (r1293602, r1293811)

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.3-2
- ship, enable mod_dontdothat#

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.3-1
- update to 1.7.3

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.2-3
- require ruby 1.9.1 abi

* Thu Feb 09 2012 Joe Orton <jorton@redhat.com> - 1.7.2-2
- add Vincent Batts' Ruby 1.9 fixes from dev@

* Thu Feb 09 2012 Joe Orton <jorton@redhat.com> - 1.7.2-1
- update to 1.7.2

* Sun Feb 05 2012 Peter Robinson <pbrobinson@gmail.com> - 1.7.1-4
- fix gnome-keyring build deps

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Joe Orton <jorton@redhat.com> - 1.7.1-2
- fix sans-kwallet build

* Thu Dec 01 2011 Joe Orton <jorton@redhat.com> - 1.7.1-1
- update to 1.7.1 (temporarily) disable failing kwallet support

* Sun Nov 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-7
- Build with libmagic support.

* Sat Oct 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-6
- Fix apr Conflicts syntax in -libs. Fix obsolete chown syntax in
  subversion.conf. Fix use of spaces vs tabs in specfile.

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-5
- more %%install fixes

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-4
- fix installed docs

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-3
- attempt to fix javahl build

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-2
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/subversion

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-1
- update to 1.7.0 drop svn2cl (no longer shipped in upstream tarball)

* Wed Jul 20 2011 Joe Orton <jorton@redhat.com> - 1.6.17-9
- enable javahl correctly

* Wed Jul 20 2011 Joe Orton <jorton@redhat.com> - 1.6.17-8
- run javahl tests (Blair Zajac, #723338)

* Wed Jul 20 2011 Joe Orton <jorton@redhat.com> - 1.6.17-7
- Merge branch 'master' of ssh://pkgs.fedoraproject.org/subversion

* Fri Jun 24 2011 Joe Orton <jorton@redhat.com> - 1.6.17-6
- split out python bindings

* Thu Jun 02 2011 Joe Orton <jorton@redhat.com> - 1.6.17-5
- drop old java patch

* Thu Jun 02 2011 Joe Orton <jorton@redhat.com> - 1.6.17-4
- drop old java patch

* Thu Jun 02 2011 Joe Orton <jorton@redhat.com> - 1.6.17-3
- remove old sources

* Thu Jun 02 2011 Joe Orton <jorton@redhat.com> - 1.6.17-2
- update to 1.6.17 (#709952)

* Thu Jun 02 2011 Joe Orton <jorton@redhat.com> - 1.6.17-1
- update to 1.6.17 (#709952)

* Fri Mar 04 2011 Joe Orton <jorton@redhat.com> - 1.6.16-2
- update to 1.6.16 (#682203) tweak arch-specific requires

* Fri Mar 04 2011 Joe Orton <jorton@redhat.com> - 1.6.16-1
- update to 1.6.16 (#682203) tweak arch-specific requires

* Sun Nov 28 2010 Joe Orton <jorton@redhat.com> - 1.6.15-3
- remove old sources

* Sun Nov 28 2010 Joe Orton <jorton@redhat.com> - 1.6.15-2
- add 1.6.15 sources

* Sun Nov 28 2010 Joe Orton <jorton@redhat.com> - 1.6.15-1
- update to 1.6.15

* Tue Oct 12 2010 Joe Orton <jorton@redhat.com> - 1.6.13-2
- trim tools/buildbot, tools/dist from docdir

* Tue Oct 05 2010 Joe Orton <jorton@redhat.com> - 1.6.13-1
- update to 1.6.13

* Tue Sep 07 2010 Joe Orton <jorton@redhat.com> - 1.6.12-8
- move PIE flag to Makefile

* Tue Sep 07 2010 Joe Orton <jorton@redhat.com> - 1.6.12-7
- add svnserve init script - split out -libs subpackage

* Fri Sep 03 2010 Joe Orton <jorton@redhat.com> - 1.6.12-6
- restore PIE support

* Fri Sep 03 2010 Joe Orton <jorton@redhat.com> - 1.6.12-5
- restore PIE support

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-4
- dist-git conversion

* Sat Jul 24 2010 dmalcolm <dmalcolm@fedoraproject.org> - 1.6.12-3
- for now, disable python cases that fail against python 2.7 (patch 9)

* Thu Jul 22 2010 dmalcolm <dmalcolm@fedoraproject.org> - 1.6.12-2
- Rebuilt for
  https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 07 2010 jorton <jorton@fedoraproject.org> - 1.6.12-1
- update to 1.6.12 (#586629) - fix comments in subversion.conf (#551484)

* Wed Jun 02 2010 Marcela Mašláňová <mmaslano@fedoraproject.org> - 1.6.11-2
- Mass rebuild with perl-5.12.0

* Sat Apr 17 2010 jorton <jorton@fedoraproject.org> - 1.6.11-1
- update to 1.6.11

* Sat Feb 13 2010 jorton <jorton@fedoraproject.org> - 1.6.9-3
- fix URL

* Sat Feb 13 2010 jorton <jorton@fedoraproject.org> - 1.6.9-2
- fix detection of libkdecore

* Mon Feb 08 2010 jorton <jorton@fedoraproject.org> - 1.6.9-1
- update to 1.6.9 (#561810) - fix comments in subversion.conf (#551484) -
  update to psvn.el r40299

* Mon Jan 25 2010 Ville Skyttä <scop@fedoraproject.org> - 1.6.6-8
- Include svn2cl and its man page only in the -svn2cl subpackage (#558598).
  - Do not include bash completion in docs, it's installed.

* Mon Dec 07 2009 Štěpán Kasal <kasal@fedoraproject.org> - 1.6.6-7
- rebuild against perl 5.10.1

* Thu Nov 26 2009 jorton <jorton@fedoraproject.org> - 1.6.6-6
- rebuild for new db4 - trim libsvn_* from dependency_libs in *.la

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 1.6.6-5
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Wed Nov 25 2009 Kevin Kofler <kkofler@fedoraproject.org> - 1.6.6-4
- rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable
  ABI) NOTE: Your package needs to be rebuilt IF AND ONLY IF it was built
  against Qt 4.6.0 Beta 1. This was in the buildroot ONLY for dist-f13
  after F12 branched. Packages built against Qt 4.5.x or older do NOT need
  a rebuild for 4.6.x (backwards binary compatibility). I have a list of
  packages needing a rebuild and am going through it. This package is in my
  list, so I am rebuilding it.

* Sun Nov 08 2009 jorton <jorton@fedoraproject.org> - 1.6.6-3
- remove old tarball.

* Sun Nov 08 2009 jorton <jorton@fedoraproject.org> - 1.6.6-2
- fix kwallet patch for fuzz=0

* Sun Nov 08 2009 jorton <jorton@fedoraproject.org> - 1.6.6-1
- update to 1.6.6

* Mon Nov 02 2009 Ville Skyttä <scop@fedoraproject.org> - 1.6.5-5
- Apply svn2cl upstream patch to fix newline issues with libxml2 2.7.4+,
  see http://bugs.debian.org/546990 for details.

* Sat Sep 19 2009 Ville Skyttä <scop@fedoraproject.org> - 1.6.5-4
- Ship svn2cl (#496456).

* Sat Sep 19 2009 Ville Skyttä <scop@fedoraproject.org> - 1.6.5-3
- Ship bash completion (#496456).

* Sat Sep 19 2009 Ville Skyttä <scop@fedoraproject.org> - 1.6.5-2
- Add %%defattr to -gnome and -kde (#496456).

* Sun Aug 23 2009 jorton <jorton@fedoraproject.org> - 1.6.5-1
- update to 1.6.5

* Tue Aug 18 2009 jorton <jorton@fedoraproject.org> - 1.6.4-3
- rebuild

* Wed Aug 12 2009 Ville Skyttä <scop@fedoraproject.org> - 1.6.4-2
- Use bzipped upstream tarball. https://www.redhat.com/archives/fedora-
  devel-list/2009-August/msg00563.html

* Fri Aug 07 2009 jorton <jorton@fedoraproject.org> - 1.6.4-1
- update to 1.6.4

* Mon Jul 27 2009 Jesse Keating <jkeating@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 jorton <jorton@fedoraproject.org> - 1.6.3-2
- remove -devel dependency on -gnome, -kde (#513313)

* Tue Jun 23 2009 jorton <jorton@fedoraproject.org> - 1.6.3-1
- update to 1.6.3

* Sun Jun 14 2009 jorton <jorton@fedoraproject.org> - 1.6.2-6
- attempt to force load of auth providers

* Sun Jun 14 2009 jorton <jorton@fedoraproject.org> - 1.6.2-5
- add -gnome, -kde subpackages

* Mon Jun 01 2009 jorton <jorton@fedoraproject.org> - 1.6.2-4
- enable KWallet, gnome-keyring support

* Mon Jun 01 2009 jorton <jorton@fedoraproject.org> - 1.6.2-3
- add updated RPATH patch

* Mon Jun 01 2009 jorton <jorton@fedoraproject.org> - 1.6.2-2
- enable KWallet, gnome-keyring support

* Fri May 15 2009 jorton <jorton@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Wed Apr 15 2009 jorton <jorton@fedoraproject.org> - 1.6.1-2
- really disable PIE

* Tue Apr 14 2009 jorton <jorton@fedoraproject.org> - 1.6.1-1
- update to 1.6.1; disable PIE patch for the time being

* Tue Mar 31 2009 jorton <jorton@fedoraproject.org> - 1.6.0-2
- BR sqlite-devel

* Tue Mar 31 2009 jorton <jorton@fedoraproject.org> - 1.6.0-1
- update to 1.6.0

* Sat Mar 14 2009 Dennis Gilmore <ausil@fedoraproject.org> - 1.5.6-5
- use -fPIE on sparc64

* Mon Mar 09 2009 jorton <jorton@fedoraproject.org> - 1.5.6-4
- update to 1.5.6 - autoload psvn (#238491, Tom Tromey) - regenerate swig
  bindings (#480503) - fix build with libtool 2.2 (#469524)

* Mon Mar 09 2009 jorton <jorton@fedoraproject.org> - 1.5.6-3
- update to 1.5.6 - autoload psvn (#238491, Tom Tromey) - regenerate swig
  bindings (#480503) - fix build with libtool 2.2 (#469524)

* Mon Mar 09 2009 jorton <jorton@fedoraproject.org> - 1.5.6-2
- update to 1.5.6 - autoload psvn (#238491, Tom Tromey) - regenerate swig
  bindings (#480503)

* Mon Mar 09 2009 jorton <jorton@fedoraproject.org> - 1.5.6-1
- update to 1.5.6 - autoload psvn (#238491, Tom Tromey)

* Thu Feb 26 2009 Jesse Keating <jkeating@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 jorton <jorton@fedoraproject.org> - 1.5.5-1
- update to 1.5.5

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazquez@fedoraproject.org> - 1.5.4-3
- Rebuild for Python 2.6

* Mon Oct 27 2008 jorton <jorton@fedoraproject.org> - 1.5.4-2
- update to 1.5.4

* Mon Oct 27 2008 jorton <jorton@fedoraproject.org> - 1.5.4-1
- fix build

* Mon Oct 13 2008 jorton <jorton@fedoraproject.org> - 1.5.3-2
- fix build

* Mon Oct 13 2008 jorton <jorton@fedoraproject.org> - 1.5.3-1
- update to 1.5.3 (#466674) - update psvn.el to r33557

* Tue Sep 30 2008 jorton <jorton@fedoraproject.org> - 1.5.2-3
- fix for zero-fuzz

* Tue Sep 30 2008 jorton <jorton@fedoraproject.org> - 1.5.2-2
- enable SASL support (#464267)

* Fri Sep 12 2008 jorton <jorton@fedoraproject.org> - 1.5.2-1
- update to 1.5.2

* Mon Jul 28 2008 jorton <jorton@fedoraproject.org> - 1.5.1-2
- fix %%changelog removed in previous commit - rediff -rpath patch for
  zero-fuzz - remove old patch

* Mon Jul 28 2008 jorton <jorton@fedoraproject.org> - 1.5.1-1
- *** empty log message ***

* Thu Jul 10 2008 Tom Callaway <spot@fedoraproject.org> - 1.5.0-10
- rebuild against db4 4.7

* Thu Jul 03 2008 jorton <jorton@fedoraproject.org> - 1.5.0-9
- add svnmerge and wcgrep to docdir (Edward Rudd, #451932) - drop neon
  version overrides

* Wed Jul 02 2008 jorton <jorton@fedoraproject.org> - 1.5.0-8
- build with OpenJDK

* Wed Jul 02 2008 jorton <jorton@fedoraproject.org> - 1.5.0-7
- fix files list

* Wed Jul 02 2008 jorton <jorton@fedoraproject.org> - 1.5.0-6
- swig-perl test suite fix for Perl 5.10 (upstream r31546)

* Tue Jul 01 2008 jorton <jorton@fedoraproject.org> - 1.5.0-5
- attempt build without java bits

* Thu Jun 26 2008 jorton <jorton@fedoraproject.org> - 1.5.0-4
- less parallel make

* Thu Jun 26 2008 jorton <jorton@fedoraproject.org> - 1.5.0-3
- remove old .tar.gz.

* Thu Jun 26 2008 jorton <jorton@fedoraproject.org> - 1.5.0-2
- update sources.

* Thu Jun 26 2008 jorton <jorton@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Mar 03 2008 Tom Callaway <spot@fedoraproject.org> - 1.4.6-6
- disable broken tests

* Mon Mar 03 2008 Tom Callaway <spot@fedoraproject.org> - 1.4.6-5
- new perl

* Thu Feb 21 2008 Lubomir Rintel <lkundrak@fedoraproject.org> - 1.4.6-4
- Correct jar location (#433295)

* Wed Feb 06 2008 Tom Callaway <spot@fedoraproject.org> - 1.4.6-3
- BR: perl(ExtUtils::Embed)

* Wed Feb 06 2008 Tom Callaway <spot@fedoraproject.org> - 1.4.6-2
- Rebuild for new perl

* Fri Dec 21 2007 jorton <jorton@fedoraproject.org> - 1.4.6-1
- update to 1.4.6

* Tue Dec 11 2007 Warren Togami <wtogami@fedoraproject.org> - 1.4.4-11
- temporarily disable test suite 4 days of broken deps is not acceptable,
  especially when this is blocking other builds. More important to fix
  broken software at the expense of possibly broken software at this point.
  Please fix the actual test failure cause real soon now.

* Thu Dec 06 2007 jorton <jorton@fedoraproject.org> - 1.4.4-10
- fix build with swig 1.3.33 (patch by Torsten Landschoff)

* Wed Dec 05 2007 jorton <jorton@fedoraproject.org> - 1.4.4-9
- rebuild for OpenLDAP soname bump

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 1.4.4-8
- makefile update to properly grab makefile.common

* Sun Sep 02 2007 jorton <jorton@fedoraproject.org> - 1.4.4-7
- rebuild for fixed 32-bit APR

* Thu Aug 30 2007 jorton <jorton@fedoraproject.org> - 1.4.4-6
- clarify License tag; re-enable test suite

* Thu Aug 23 2007 jorton <jorton@fedoraproject.org> - 1.4.4-5
- rebuild for neon 0.27

* Wed Aug 22 2007 jorton <jorton@fedoraproject.org> - 1.4.4-4
- trim dependencies from .la files - detabify spec file - test suite
  disabled to ease stress on builders

* Wed Aug 08 2007 jorton <jorton@fedoraproject.org> - 1.4.4-3
- BuildRequire perl(Test::More)

* Wed Aug 08 2007 jorton <jorton@fedoraproject.org> - 1.4.4-2
- fix build with new glibc open()-as-macro - build all swig code in
  %%build, not %%install

* Tue Jul 03 2007 jorton <jorton@fedoraproject.org> - 1.4.4-1
- update to 1.4.4 - add Provides: svn (#245087) - fix without-java build
  (Lennert Buytenhek, #245467)

* Wed Apr 11 2007 jorton <jorton@fedoraproject.org> - 1.4.3-12
- fix version of apr/apr-util in BR (#216181)

* Fri Mar 30 2007 jorton <jorton@fedoraproject.org> - 1.4.3-11
- revert changes

* Fri Mar 30 2007 jorton <jorton@fedoraproject.org> - 1.4.3-10
- fix BR; thanks to gbenson

* Fri Mar 30 2007 jorton <jorton@fedoraproject.org> - 1.4.3-9
- attempt four at fixing javahl

* Fri Mar 30 2007 jorton <jorton@fedoraproject.org> - 1.4.3-8
- third attempt

* Thu Mar 29 2007 jorton <jorton@fedoraproject.org> - 1.4.3-7
- second attempt

* Thu Mar 29 2007 jorton <jorton@fedoraproject.org> - 1.4.3-6
- fix javahl compile failure

* Thu Mar 15 2007 jorton <jorton@fedoraproject.org> - 1.4.3-5
- bump release

* Thu Mar 15 2007 jorton <jorton@fedoraproject.org> - 1.4.3-4
- update to 1.4.3 (#228691) - remove trailing dot from Summary - use
  current preferred standard BuildRoot - add post/postun ldconfig
  scriptlets for -ruby and -javahl

* Fri Feb 16 2007 jorton <jorton@fedoraproject.org> - 1.4.3-3
- commit updated .asc files

* Fri Feb 16 2007 jorton <jorton@fedoraproject.org> - 1.4.3-2
- remove trailing dot from Summary - use current preferred standard
  BuildRoot
  ----------------------------------------------------------------------

* Fri Feb 16 2007 jorton <jorton@fedoraproject.org> - 1.4.3-1
- update to 1.4.3

* Fri Dec 08 2006 jorton <jorton@fedoraproject.org> - 1.4.2-3
- fix use of python_sitearch

* Thu Dec 07 2006 Jeremy Katz <katzj@fedoraproject.org> - 1.4.2-2
- rebuild against python 2.5 - follow python packaging guidelines

* Wed Nov 08 2006 jorton <jorton@fedoraproject.org> - 1.4.2-1
- update to 1.4.2

* Mon Sep 11 2006 jorton <jorton@fedoraproject.org> - 1.4.0-2
- enable %%check again

* Mon Sep 11 2006 jorton <jorton@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Thu Jul 13 2006 jorton <jorton@fedoraproject.org> - 1.3.2-8
- fix ruby packaging (#191611)

* Wed Jul 12 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.3.2-7
- bumped for rebuild

* Wed Jun 07 2006 jorton <jorton@fedoraproject.org> - 1.3.2-6
- disable test suite

* Wed Jun 07 2006 jorton <jorton@fedoraproject.org> - 1.3.2-5
- disable tests to check that %%files is at least right

* Wed Jun 07 2006 jorton <jorton@fedoraproject.org> - 1.3.2-4
- BR gettext

* Wed Jun 07 2006 jorton <jorton@fedoraproject.org> - 1.3.2-3
- revert Ruby sitelibdir patch to see how the build fails

* Wed Jun 07 2006 jorton <jorton@fedoraproject.org> - 1.3.2-2
- re-enable test suite

* Fri Jun 02 2006 jorton <jorton@fedoraproject.org> - 1.3.2-1
- update to 1.3.2 - fix Ruby sitelibdir (Garrick Staples, #191611) - own
  /etc/subversion (#189071) - update to psvn.el r19857

* Thu Apr 06 2006 jorton <jorton@fedoraproject.org> - 1.3.1-2
- move libsvn_swig_ruby* back to subversion-ruby

* Tue Apr 04 2006 jorton <jorton@fedoraproject.org> - 1.3.1-1
- update to 1.3.1 - update to psvn.el r19138 (Stefan Reichoer) - build
  -java on s390 again

* Thu Feb 16 2006 Florian La Roche <laroche@fedoraproject.org> - 1.3.0-10
- ruby libs are already in the main package

* Sat Feb 11 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.3.0-9
- bump for bug in double-long on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@fedoraproject.org> - 1.3.0-8
- bump for new gcc/glibc

* Tue Jan 31 2006 jorton <jorton@fedoraproject.org> - 1.3.0-7
- run check-swig-py in %%check (#178448) - relax JDK requirement (Kenneth
  Porter, #177367)

* Tue Jan 31 2006 jorton <jorton@fedoraproject.org> - 1.3.0-6
- fix to build with neon 0.25.5

* Tue Jan 31 2006 jorton <jorton@fedoraproject.org> - 1.3.0-5
- rebuild for neon 0.25

* Wed Jan 04 2006 jorton <jorton@fedoraproject.org> - 1.3.0-4
- book no longer bundled

* Wed Jan 04 2006 jorton <jorton@fedoraproject.org> - 1.3.0-3
- turn off java on s390

* Wed Jan 04 2006 jorton <jorton@fedoraproject.org> - 1.3.0-2
- work around 1.3.0 fubar

* Wed Jan 04 2006 jorton <jorton@fedoraproject.org> - 1.3.0-1
- update to 1.3.0 (#176833) - update to psvn.el r17921 Stefan Reichoer

* Mon Dec 12 2005 jorton <jorton@fedoraproject.org> - 1.2.3-7
- unconditionally enable java; fix glob pattern

* Mon Dec 12 2005 jorton <jorton@fedoraproject.org> - 1.2.3-6
- fix ownership of libsvnjavahl.* (#175289) - try building javahl on
  ia64/ppc64 again

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org> - 1.2.3-5
- gcc update bump

* Fri Dec 02 2005 jorton <jorton@fedoraproject.org> - 1.2.3-4
- rebuild for httpd-2.2/apr-1.2/apr-util-1.2

* Thu Nov 10 2005 Tomáš Mráz <tmraz@fedoraproject.org> - 1.2.3-3
- rebuilt against new openssl

* Thu Sep 08 2005 jorton <jorton@fedoraproject.org> - 1.2.3-2
- update to psvn.el r16070 from Stefan Reichoer - synch up gpg sigs

* Thu Sep 08 2005 jorton <jorton@fedoraproject.org> - 1.2.3-1
- update to 1.2.3 - merge subversion.conf changes from RHEL4 - merge
  filter-requires.sh changes from FC4 updates

* Fri Jul 22 2005 jorton <jorton@fedoraproject.org> - 1.2.1-1
- update to 1.2.1 - fix BuildRequires for ruby and apr-util (#163126) -
  drop static library archives

* Wed May 25 2005 jorton <jorton@fedoraproject.org> - 1.2.0-4
- don't run ruby checks.

* Wed May 25 2005 jorton <jorton@fedoraproject.org> - 1.2.0-3
- disable java on all but x86, x86_64, ppc (#158719)

* Wed May 25 2005 jorton <jorton@fedoraproject.org> - 1.2.0-2
- disable java on ppc64 (#158719)

* Tue May 24 2005 jorton <jorton@fedoraproject.org> - 1.2.0-1
- update to 1.2.0; add ruby subpackage

* Wed Apr 13 2005 jorton <jorton@fedoraproject.org> - 1.1.4-5
- disable on ia64,
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=154700

* Wed Apr 13 2005 jorton <jorton@fedoraproject.org> - 1.1.4-4
- fix %%install for java

* Wed Apr 13 2005 jorton <jorton@fedoraproject.org> - 1.1.4-3
- try better at enabling java

* Wed Apr 13 2005 jorton <jorton@fedoraproject.org> - 1.1.4-2
- enable java subpackage again - tweak subversion.conf comments

* Sun Apr 03 2005 jorton <jorton@fedoraproject.org> - 1.1.4-1
- update to 1.1.4

* Tue Mar 22 2005 jorton <jorton@fedoraproject.org> - 1.1.3-15
- further swig bindings fix (upstream via Max Bowsher, #151798) - fix perl
  File::Path dependency in filter-requires.sh

* Tue Mar 22 2005 jorton <jorton@fedoraproject.org> - 1.1.3-14
- really make swig bindings build again

* Tue Mar 22 2005 jorton <jorton@fedoraproject.org> - 1.1.3-13
- restore swig bindings support (from upstream via Max Bowsher, #141343) -
  tweak SELinux commentary in default subversion.conf

* Wed Mar 09 2005 jorton <jorton@fedoraproject.org> - 1.1.3-12
- bump release

* Wed Mar 09 2005 jorton <jorton@fedoraproject.org> - 1.1.3-11
- fix svn_load_dirs File::Path version requirement

* Tue Mar 08 2005 jorton <jorton@fedoraproject.org> - 1.1.3-10
- conditionalize java subpackage

* Tue Mar 08 2005 jorton <jorton@fedoraproject.org> - 1.1.3-9
- try non-parallel build

* Tue Mar 08 2005 jorton <jorton@fedoraproject.org> - 1.1.3-8
- bump release

* Tue Mar 08 2005 jorton <jorton@fedoraproject.org> - 1.1.3-7
- add -java subpackage for javahl libraries (Anthony Green, #116202)

* Fri Mar 04 2005 jorton <jorton@fedoraproject.org> - 1.1.3-6
- rebuild

* Tue Feb 15 2005 jorton <jorton@fedoraproject.org> - 1.1.3-5
- run test suite in C locale

* Mon Feb 07 2005 jorton <jorton@fedoraproject.org> - 1.1.3-4
- adjust -pie patch for build.conf naming upstream

* Wed Jan 19 2005 jorton <jorton@fedoraproject.org> - 1.1.3-3
- rebuild to pick up db-4.3 properly; don't ignore test failures

* Mon Jan 17 2005 jorton <jorton@fedoraproject.org> - 1.1.3-2
- update to 1.1.3 sources.

* Sun Jan 16 2005 jorton <jorton@fedoraproject.org> - 1.1.3-1
- update to 1.1.3 (#145236) - fix python bindings location on x86_64
  (#143522)

* Sun Jan 16 2005 jorton <jorton@fedoraproject.org> - 1.1.2-4
- New upstream keys.

* Mon Jan 10 2005 jorton <jorton@fedoraproject.org> - 1.1.2-3
- More %%files fixes.

* Mon Jan 10 2005 jorton <jorton@fedoraproject.org> - 1.1.2-2
- Update for 1.1.2.

* Mon Jan 10 2005 jorton <jorton@fedoraproject.org> - 1.1.2-1
- update to 1.1.2 - disable swig bindings due to incompatible swig version

* Wed Nov 24 2004 jorton <jorton@fedoraproject.org> - 1.1.1-7
- update subversion.conf examples to be SELinux-friendly

* Sat Nov 13 2004 jbj <jbj@fedoraproject.org> - 1.1.1-6
- Hmmm, ppc64 fails too ...

* Sat Nov 13 2004 jbj <jbj@fedoraproject.org> - 1.1.1-5
- Skip make check on s390x as well.

* Sat Nov 13 2004 jbj <jbj@fedoraproject.org> - 1.1.1-4
- x86_64: don't fail "make check" while diagnosing db-4.3.21 upgrade.

* Sat Nov 13 2004 jbj <jbj@fedoraproject.org> - 1.1.1-3
- rebuild against db-4.3.21.

* Tue Nov 09 2004 Jeremy Katz <katzj@fedoraproject.org> - 1.1.1-2
- rebuild against python 2.4

* Mon Oct 25 2004 jorton <jorton@fedoraproject.org> - 1.1.1-1
- update to 1.1.1 - update -pie patch to address #134786

* Mon Oct 04 2004 jorton <jorton@fedoraproject.org> - 1.1.0-6
- use pure_vendor_install to fix Perl modules - use %%find_lang to package
  translations (Axel Thimm)

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.1.0-5
- don't use parallel make for swig-py

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.1.0-4
- BuildRequire newest swig for "swig -ldflags" fix

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.1.0-3
- fix swig bindings build on x86_64

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.1.0-2
- Fixups for 1.1.0.

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.0.8-4
- Update to 1.1.0 sources.

* Thu Sep 30 2004 jorton <jorton@fedoraproject.org> - 1.0.8-3
- Fix typo.

* Thu Sep 23 2004 jorton <jorton@fedoraproject.org> - 1.0.8-2
- update to 1.0.8 - remove -neonver patch - update psvn.el to 11062

* Thu Sep 23 2004 jorton <jorton@fedoraproject.org> - 1.0.8-1
- update to 1.0.8 - remove -neonver patch

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.6-2
- auto-import changelog data from subversion-1.0.6-3.src.rpm Mon Aug 23
  2004 Joe Orton <jorton@redhat.com> 1.0.6-3 - add svn_load_dirs.pl to
  docdir (#128338) - add psvn.el (#128356)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.6-1
- auto-import changelog data from subversion-1.0.6-2.src.rpm Thu Jul 22
  2004 Joe Orton <jorton@redhat.com> 1.0.6-2 - rebuild Tue Jul 20 2004 Joe
  Orton <jorton@redhat.com> 1.0.6-1 - update to 1.0.6 - allow build against
  neon 0.24.*

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.5-1
- auto-import changelog data from subversion-1.0.5-2.src.rpm Tue Jun 15
  2004 Elliot Lee <sopwith@redhat.com> - rebuilt Thu Jun 10 2004 Joe Orton
  <jorton@redhat.com> 1.0.5-1 - update to 1.0.5

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.4-1
- auto-import subversion-1.0.4-1.1 from subversion-1.0.4-1.1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.2-1
- auto-import subversion-1.0.2-1 from subversion-1.0.2-1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1.0.1-1
- auto-import subversion-1.0.1-1 from subversion-1.0.1-1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.37.0-1
- auto-import subversion-0.37.0-1 from subversion-0.37.0-1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.32.1-7
- auto-import changelog data from subversion-0.32.1-5.src.rpm Wed Jun 09
  2004 Joe Orton <jorton@redhat.com> 0.32.1-5 - add security fix for CVE
  CAN-2004-0413 (Ben Reser)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 0.32.1-6
- auto-import changelog data from subversion-0.32.1-2.src.rpm Wed May 12
  2004 Joe Orton <jorton@redhat.com> 0.32.1-2 - add security fix for CVE
  CAN-2004-0397 (Ben Reser)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import subversion-0.32.1-1 from subversion-0.32.1-1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from subversion-0.27.0-2.src.rpm Tue Apr 06
  2004 Joe Orton <jorton@redhat.com> 0.27.0-2 - fix RPATH and libtool
  issues

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from subversion-0.27.0-1.src.rpm Mon Apr 05
  2004 Joe Orton <jorton@redhat.com> 0.27.0-1 - update to 0.27.0 (last
  version using the format 1 db schema) - add neon fix for CAN-2004-0179

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from subversion-0.17.1-4503.0.src.rpm Wed Jan
  22 2003 Jeff Johnson <jbj@redhat.com> 0.17.1-4503.0 - upgrade to 0.17.1.
  Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.16-3987.1 - upgrade to
  0.16. Wed Nov 13 2002 Jeff Johnson <jbj@redhat.com> 0.15-3687.2 - don't
  mess with the info handbook install yet. Sun Nov 10 2002 Jeff Johnson
  <jbj@redhat.com> 0.15-3687.1 - use libdir, build on x86_64 too. - avoid
  "perl(Config::IniFiles) >= 2.27" dependency. Sat Nov 09 2002 Jeff Johnson
  <jbj@redhat.com> 0.15-3687.0 - first build from adapted spec file, only
  client and libraries for now. - internal apr/apr-utils/neon until
  incompatibilities sort themselves out. - avoid libdir issues on x86_64
  for the moment.

* Wed Feb 09 2011 Dennis Gilmore <dennis@ausil.us> - 1.6.15-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 18 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.17-10
- Use upstream version of patch
  http://svn.apache.org/viewvc?view=revision&revision=1145203

* Fri Jul 01 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.17-9
- change cflags in Makefile.PL to work with Perl 5.14.1

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.17-8
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.6.17-7
- Perl mass rebuild

* Thu Jun 28 2012 Petr Písař <ppisar@redhat.com>
- Perl 5.16 rebuild

* Mon Jun 18 2012 Dan Horák <dan@danny.cz>
- fix build with recent gcc 4.7 (svn rev 1345740)

* Fri Jun 08 2012 Petr Písař <ppisar@redhat.com>
- Perl 5.16 rebuild

* Fri Feb 15 2013 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 17 2013 Petr Písař <ppisar@redhat.com>
- Perl 5.18 rebuild

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.8-1
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Aug 18 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Dennis Gilmore <dennis@ausil.us> - 1.8.9-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jun 19 2015 Dennis Gilmore <dennis@ausil.us> - 1.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.8.13-2
- Own bash-completion dirs not owned by anything in dep chain

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.13-1
- Perl 5.22 rebuild

* Thu Jul 06 2017 Joe Orton <jorton@redhat.com> - 1.9.6-1
- update to 1.9.6 (#1467890) update to latest upstream psvn.el move
  libsvnjavahl to -libs, build -javahl noarch fix javahl Requires

* Thu Feb 01 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 1.9.7-3
- Update Python 2 dependency declarations to new packaging standards

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.9.7-2
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.7-1
- F-28: rebuild for ruby25

* Tue May 19 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.0~rc2-6
- Updated build-requires for java and qt5

* Tue May 19 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-5
- switch subpackages to lock-step requires on -libs rather than subversion

* Thu Apr 30 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-4
- drop Berkeley DB support for Fedora > 32 BR java-11-openjdk-devel

* Tue Apr 28 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-3
- Fix for -rc

* Fri Apr 24 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-2
- BR py3c-devel

* Thu Apr 23 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-1
- update to 1.14.0-rc2

* Wed Feb 12 2020 Joe Orton <jorton@redhat.com> - 1.13.0-6
- fix FTBFS on 32-bit arches

* Wed Feb 12 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.13.0-5
- F-32: fix include path for ruby 2.7

* Fri Jan 17 2020 Joe Orton <jorton@redhat.com> - 1.13.0-4
- conditionally package bdb tools in -tools

* Fri Jan 17 2020 Joe Orton <jorton@redhat.com> - 1.13.0-3
- update for KDE 5 (Phil O, #1768693) Resolves: rhbz#1768693

* Thu Nov 28 2019 Joe Orton <jorton@redhat.com> - 1.13.0-2
- Tweak issue links.

* Fri Nov 01 2019 Joe Orton <jorton@redhat.com> - 1.13.0-1
- update to 1.13.0

* Fri Nov 01 2019 Joe Orton <jorton@redhat.com> - 1.12.2-1
- subversion.spec
- update to 1.13.0

* Fri Feb 14 2025 Joe Orton <jorton@redhat.com> - 1.14.5-12
- try to avoid build failures running svnauthz in ELN

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-11
- fix bcond for non-Java architectures

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-10
- fix java bcond.

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-9
- simplify build conditional definitions.

* Mon Feb 03 2025 Tomas Korbar <tkorbar@redhat.com> - 1.14.5-8
- Fix debuginfo building and stop building ruby and java subpackages

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 1.14.5-7
- enable parallelisation in "make check"

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.14.5-6
- Add explicit BR: libxcrypt-devel

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.5-4
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Wed Dec 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.5-3
- Explicitly add dependency for rubygem(csv) for ruby3.4

* Fri Dec 13 2024 Joe Orton <jorton@redhat.com> - 1.14.5-2
- fix ELN build failure

* Wed Dec 11 2024 Joe Orton <jorton@redhat.com> - 1.14.5-1
- update to 1.14.5 (#2331047) use %%autosetup enable tests by default again

* Fri Nov 01 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.4-1
- Rebase to version 1.14.4

* Mon Oct 07 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-12
- Rebuild for utf8proc SONAME bump

* Tue Aug 06 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-11
- Fix debuginfo generation for bindings

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.3-9
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.14.3-8
- Rebuilt for Python 3.13

* Thu Mar 28 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.3-7
- Do not use %%eln macro

* Mon Mar 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.14.3-6
- Really rebuild for java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.14.3-5
- Rebuilt for java-21-openjdk as system jdk

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-3
- Fix building with gcc 14

* Fri Jan 12 2024 Tomas Korbar <tkorbar@redhat.com> - 1.14.3-2
- Fix testing of binary patch

* Fri Jan 05 2024 Richard Lescak <rlescak@redhat.com> - 1.14.3-1
- rebase to version 1.14.3 (#2256062)

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-26
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Mon Nov 20 2023 Joe Orton <jorton@redhat.com> - 1.14.2-25
- fix mod_authz_svn, mod_dontdothat (#2250182)

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-24
- use %%patch -P throughout

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-23
- restore plaintext password storage by default (per upstream)

* Wed Nov 08 2023 Joe Orton <jorton@redhat.com> - 1.14.2-22
- restrict symbols exposed by DSOs built for httpd

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-20
- Perl 5.38 rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 1.14.2-19
- Rebuilt for Python 3.12

* Mon Jul 03 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-18
- temporary disable tests for eln to prevent FTBFS

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.14.2-17
- Rebuilt for Python 3.12

* Mon May 08 2023 Florian Weimer <fweimer@redhat.com> - 1.14.2-16
- Port to C99

* Thu Feb 16 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-15
- SPDX migration

* Fri Jan 27 2023 Richard Lescak <rlescak@redhat.com> - 1.14.2-14
- add requirement for python3-setuptools with new Python 3.12 (#2155420)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-12
- Remove perl(MODULE_COMPAT), it will be replaced by generators

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-11
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Mon Oct 10 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-10
- Really apply ruby32 patch

* Sun Oct 09 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.2-9
- Backport upstream fix for ruby3.2 support

* Wed Oct 05 2022 Richard Lescak <rlescak@redhat.com> - 1.14.2-8
- fix segfault in Python swig test (#2128024)

* Fri Jul 29 2022 Joe Orton <jorton@redhat.com> - 1.14.2-7
- improve library versioning so filenames are unique across releases

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 05 2022 Joe Orton <jorton@redhat.com> - 1.14.2-5
- disable libmagic during test runs

* Tue Jul 05 2022 Joe Orton <jorton@redhat.com> - 1.14.2-4
- update for new Java arches and bump to JDK 17 (#2103909)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.14.2-3
- Rebuilt for Python 3.11

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.2-2
- Perl 5.36 rebuild

* Wed May 04 2022 Joe Orton <jorton@redhat.com> - 1.14.2-1
- update to 1.14.2 (#2073852, CVE-2021-28544, CVE-2022-24070)

* Sat Feb 05 2022 Jiri <jvanek@redhat.com> - 1.14.1-12
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.1-11
- F-36: rebuild against ruby31

* Mon Jan 24 2022 Timm Bäder <tbaeder@redhat.com> - 1.14.1-10
- Disable automatic .la file removal

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Richard Lescak <rlescak@redhat.com> - 1.14.1-8
- Replaced deprecated method readfp() in gen_base.py to build with Python
  3.11 (#2019019)

* Wed Dec 01 2021 Joe Orton <jorton@redhat.com> - 1.14.1-7
- fix intermittent FTBFS in tests (#1956806)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.14.1-5
- Rebuilt for Python 3.10

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.1-4
- Perl 5.34 rebuild

* Thu May 20 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.1-3
- Temporary disable the tests for Perl mass rebuil

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.14.1-2
- Rebuilt for updated systemd-rpm-macros

* Wed Feb 10 2021 Joe Orton <jorton@redhat.com> - 1.14.1-1
- update to 1.14.1 (#1927265, #1768698) Resolves: rhbz#1768698 Resolves:
  rhbz#1927265

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Tom Stellard <tstellar@redhat.com> - 1.14.0-20
- Add BuildRequires: make

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.14.0-19
- F-34: rebuild against ruby 3.0

* Fri Dec 11 2020 Joe Orton <jorton@redhat.com> - 1.14.0-18
- strip libdir from pkgconfig files add missing -libs dep from
  python3-subversion

* Thu Dec 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-17
- fix KWallet conditional (#1902598) Resolves: rhbz#1902598

* Wed Dec 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-16
- Reorder bconds.

* Mon Nov 30 2020 Jan Grulich <jgrulich@redhat.com> - 1.14.0-15
- Disable KWallet for RHEL and ELN Resolves: bz#1902598

* Tue Sep 29 2020 Joe Orton <jorton@redhat.com> - 1.14.0-14
- bump required apr-devel BR gcc, gcc-c++

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.14.0-11
- Perl 5.32 rebuild

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-10
- Fix chronology, again.

* Wed Jun 03 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.14.0-9
- Minor conditional fixes for ELN

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-8
- Fix chronology more.

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-7
- use minor version as libtool library revision number

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-6
- Amend changelog.

* Wed Jun 03 2020 Joe Orton <jorton@redhat.com> - 1.14.0-5
- Seems the ruby bindings failure was a false -ve, though libsvn_swig_ruby
  only builds with many mismatched callback pointer types, so looks
  dubious.

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-4
- disable Ruby bindings, failing tests with Ruby 2.7

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-3
- remove duplicated %%changelog entries

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-2
- enable Python swig bindings by default for f32+

* Tue Jun 02 2020 Joe Orton <jorton@redhat.com> - 1.14.0-1
- update to 1.14.0 (#1840565, #1812195) Resolves: rhbz#1812195 Resolves:
  rhbz#1840565

* Mon Jun 01 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-8
- revise %%changelog history to restore chronological order

* Mon Jun 01 2020 Joe Orton <jorton@redhat.com> - 1.14.0~rc2-7
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
