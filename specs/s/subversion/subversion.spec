## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.14.5-21
- Latest state for subversion

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
