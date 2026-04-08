# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_python3 %{?_without_python3: 0} %{?!_without_python3: 1}
%global with_php %{?_without_php: 0} %{?!_without_php: 0}
%global with_tcl %{?_without_tcl: 0} %{?!_without_tcl: 1}
%global with_ruby %{?_without_ruby: 0} %{?!_without_ruby: 1}
%global with_lua %{?_without_lua: 0} %{?!_without_lua: 1}
%global with_dbi %{?rhel: 0} %{?!rhel: 1}
%global php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global svnrev r1190
#global pretag 1.2.99908020600

%if "%{php_version}" < "5.6"
%global ini_name     %{name}.ini
%else
%global ini_name     40-%{name}.ini
%endif


Summary: Round Robin Database Tool to store and display time-series data
Name: rrdtool
Version: 1.9.0
Release: 7%{?dist}
# gd license in php bindings isn't by default built-in
License: gpl-1.0-or-later AND gpl-2.0-or-later AND gpl-2.0-or-later WITH rrdtool-floss-exception-2.0 AND mit AND lgpl-2.0-or-later AND lgpl-2.1-or-later AND bsd-source-code AND snprintf AND bsd-3-clause AND gpl-2.0-only AND licenseref-fedora-public-domain AND gtkbook
URL: https://oss.oetiker.ch/rrdtool/
Source0: https://github.com/oetiker/rrdtool-1.x/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1: php4-%{svnrev}.tar.gz
Patch1: rrdtool-1.4.4-php54.patch
# disable logo for php 5.5.
Patch2: rrdtool-1.4.7-php55.patch
Patch3: rrdtool-1.6.0-ruby-2-fix.patch
# enable php bindings on ppc
Patch4: rrdtool-1.4.8-php-ppc-fix.patch
# fix compatibility with tcl 9.0
Patch5: rrdtool-1.9.0-tcl90.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: freetype-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: intltool >= 0.35.0
BuildRequires: cairo-devel >= 1.4.6
BuildRequires: pango-devel >= 1.17
BuildRequires: libtool
BuildRequires: groff
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: systemd
BuildRequires: sed
%if %{with_dbi}
BuildRequires: libdbi-devel
%endif
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-generators
BuildRequires: perl-Pod-Html
BuildRequires: perl-devel
BuildRequires: automake
BuildRequires: autoconf
Requires: dejavu-sans-mono-fonts
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). It stores the data in a very compact way that will not
expand over time, and it presents useful graphs by processing the data to
enforce a certain data density. It can be used either via simple wrapper
scripts (from shell or Perl) or via frontends that poll network devices and
put a friendly user interface on it.

%package devel
Summary: RRDtool libraries and header files
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package allow you to use directly this library.

%package doc
Summary: RRDtool documentation

%description doc
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package contains documentation on using RRD.

%package perl
Summary: Perl RRDtool bindings
Requires: %{name} = %{version}-%{release}
Obsoletes: perl-%{name} < %{version}-%{release}
Provides: perl-%{name} = %{version}-%{release}

%description perl
The Perl RRDtool bindings


%package -n python3-rrdtool
%{?python_provide:%python_provide python3-rrdtool}
Summary: Python RRDtool bindings
BuildRequires: python3-devel, python3-setuptools
%{?__python3:Requires: %{__python3}}
Requires: %{name} = %{version}-%{release}

%description -n python3-rrdtool
Python RRDtool bindings.

%if %{with_php}
%package php
Summary: PHP RRDtool bindings
BuildRequires: php-devel >= 4.0
Requires: php >= 4.0
Requires: %{name} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
Obsoletes: php-%{name} < %{version}-%{release}
Provides: php-%{name} = %{version}-%{release}
Provides: php-pecl(rrdtool)

%description php
The %{name}-php package includes a dynamic shared object (DSO) that adds
RRDtool bindings to the PHP HTML-embedded scripting language.
%endif

%if %{with_tcl}
%package tcl
Summary: Tcl RRDtool bindings
BuildRequires: tcl-devel >= 8.0
Requires: tcl >= 8.0
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}

%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.
%endif

%if %{with_ruby}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}

%package ruby
Summary: Ruby RRDtool bindings
BuildRequires: ruby, ruby-devel
Requires: %{name} = %{version}-%{release}

%description ruby
The %{name}-ruby package includes RRDtool bindings for Ruby.
%endif

%if %{with_lua}
%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%package lua
Summary: Lua RRDtool bindings
BuildRequires: lua, lua-devel
%if "%{luaver}" != ""
Requires: lua(abi) = %{luaver}
%endif
Requires: %{name} = %{version}-%{release}

%description lua
The %{name}-lua package includes RRDtool bindings for Lua.
%endif

%prep
%setup -q -n %{name}-%{version} %{?with_php: -a 1}
%if %{with_php}
%patch -P1 -p1 -b .php54
%patch -P2 -p1 -b .php55
%endif
# Workaround for rhbz#92165
# Do not apply on RHEL-6 or lower
%if %{?rhel} %{?!rhel:7} > 6
%patch -P3 -p1 -b .ruby-2-fix
%endif
%patch -P4 -p1 -b .php-ppc-fix
%patch -P5 -p1 -b .tcl90

# Fix to find correct python dir on lib64
perl -pi -e 's|get_python_lib\(0,0,prefix|get_python_lib\(1,0,prefix|g' \
    configure

# Most edits shouldn't be necessary when using --libdir, but
# w/o, some introduce hardcoded rpaths where they shouldn't
perl -pi.orig -e 's|/lib\b|/%{_lib}|g' \
    configure Makefile.in php4/configure php4/ltconfig*

# Perl 5.10 seems to not like long version strings, hack around it
perl -pi.orig -e 's|1.299907080300|1.29990708|' \
    bindings/perl-shared/RRDs.pm bindings/perl-piped/RRDp.pm

#
# fix config files for php4 bindings
# workaround needed due to https://bugzilla.redhat.com/show_bug.cgi?id=211069
cp -p /usr/lib/rpm/redhat/config.{guess,sub} php4/

%build
./bootstrap
%configure \
    --with-perl-options='INSTALLDIRS="vendor"' \
    --disable-rpath \
%if %{with_tcl}
    --enable-tcl-site \
    --with-tcllib=%{_libdir} \
%else
    --disable-tcl \
%endif
%if %{with_python3}
    --enable-python \
%else
    --disable-python \
%endif
%if %{with_ruby}
    --enable-ruby \
%else
    --disable-ruby \
%endif
%if %{with_dbi}
    --enable-libdbi \
%else
    --disable-libdbi \
%endif
    --disable-static \
    --with-pic

# Fix another rpath issue
perl -pi.orig -e 's|-Wl,--rpath -Wl,\$rp||g' \
    bindings/perl-shared/Makefile.PL

%if %{with_ruby}
# Remove Rpath from Ruby
perl -pi.orig -e 's|-Wl,--rpath -Wl,\$\(EPREFIX\)/lib||g' \
    bindings/ruby/extconf.rb
sed -i 's|extconf.rb \\|extconf.rb --vendor \\|' bindings/Makefile
%endif

# Force RRDp bits where we want 'em, not sure yet why the
# --with-perl-options and --libdir don't take
pushd bindings/perl-piped/
perl Makefile.PL INSTALLDIRS=vendor
perl -pi.orig -e 's|/lib/perl|/%{_lib}/perl|g' Makefile
popd

%{make_build}

# Build the php module, the tmp install is required
%if %{with_php}
%global rrdtmp %{_tmppath}/%{name}-%{version}-tmpinstall
%{__make} install DESTDIR="%{rrdtmp}"
pushd php4/

export PYTHON=%{__python3}

%configure \
    --with-rrdtool="%{rrdtmp}%{_prefix}" \
    --disable-static
%{make_build} PYTHON="$PYTHON"
popd
rm -rf %{rrdtmp}
%endif

# Fix @perl@ and @PERL@
find examples/ -type f \
    -exec perl -pi -e 's|^#! \@perl\@|#!%{__perl}|gi' {} \;
find examples/ -name "*.pl" \
    -exec perl -pi -e 's|\015||gi' {} \;

# Rebuild python
pushd bindings/python
%py3_build
popd

%install
export PYTHON=%{__python3}
%{make_install} PYTHON="$PYTHON"

# Install the php module
%if %{with_php}
install -D -m0755 php4/modules/rrdtool.so \
    %{buildroot}%{php_extdir}/rrdtool.so
# Clean up the examples for inclusion as docs
rm -rf php4/examples/.svn
# Put the php config bit into place
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/%{ini_name}
; Enable rrdtool extension module
extension=rrdtool.so
__EOF__
%endif

# Pesky RRDp.pm...
mv $RPM_BUILD_ROOT%{perl_vendorlib}/RRDp.pm $RPM_BUILD_ROOT%{perl_vendorarch}/

# Dunno why this is getting installed here...
rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/leaktest.pl

# We only want .txt and .html files for the main documentation
mkdir -p doc2/html doc2/txt
cp -a doc/*.txt doc2/txt/
cp -a doc/*.html doc2/html/

# Put perl docs in perl package
mkdir -p doc3/html
mv doc2/html/RRD*.html doc3/html/

# Clean up the examples
rm -f examples/Makefile* examples/*.in examples/rrdcached/Makefile*

# This is so rpm doesn't pick up perl module dependencies automatically
find examples/ -type f -exec chmod 0644 {} \;

# Reinstall python
pushd bindings/python
%py3_install
popd

# Clean up the buildroot
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-* \
        $RPM_BUILD_ROOT%{perl_vendorarch}/ntmake.pl \
        $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod \
        $RPM_BUILD_ROOT%{_datadir}/%{name}/examples \
        $RPM_BUILD_ROOT%{perl_vendorarch}/auto/*/{.packlist,*.bs}

%find_lang %{name}

%check
# minimal load test for the PHP extension
%if %{with_php}
LD_LIBRARY_PATH=%{buildroot}%{_libdir} php -n \
    -d extension_dir=%{buildroot}%{php_extdir} \
    -d extension=rrdtool.so -m \
    | grep rrdtool
%endif


%post
/sbin/ldconfig
%systemd_post rrdcached.service rrdcached.socket

%preun
%systemd_post rrdcached.service rrdcached.socket

%postun
/sbin/ldconfig
%systemd_post rrdcached.service rrdcached.socket

%files -f %{name}.lang
%license LICENSE
%doc CONTRIBUTORS COPYRIGHT TODO NEWS CHANGES THREADS
%{_bindir}/*
%{_libdir}/*.so.*
%{_unitdir}/rrdcached.service
%{_unitdir}/rrdcached.socket
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man3/lib*.3*

%files devel
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

# License file is missing, upstream was notified
%files doc
%doc examples doc2/html doc2/txt

%files perl
%doc doc3/html
%{_mandir}/man3/*.3pm*
%{perl_vendorarch}/*.pm
%attr(0755,root,root) %{perl_vendorarch}/auto/RRDs/


%files -n python3-rrdtool
%doc bindings/python/COPYING bindings/python/README.md
%{python3_sitearch}/rrdtool*.so
%{python3_sitearch}/rrdtool-*.egg-info

%if %{with_php}
%files php
%doc php4/examples php4/README
%config(noreplace) %{_sysconfdir}/php.d/%{ini_name}
%{php_extdir}/rrdtool.so
%endif

%if %{with_tcl}
%files tcl
%doc bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir}/rrdtool/*.tcl
%endif

%if %{with_ruby}
%files ruby
%doc bindings/ruby/README
%{ruby_vendorarchdir}/RRD.so
%endif

%if %{with_lua}
%files lua
%doc bindings/lua/README
%{lualibdir}/*
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.0-6
- Perl 5.42 rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.9.0-5
- Rebuilt for Python 3.14

* Fri Mar 21 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/TclTk9.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.0-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Tue Jul 30 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1.9.0-1
- New version
  Resolves: rhbz#2301450

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.0-19
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.0-18
- Rebuilt for Python 3.13

* Mon May 27 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1.8.0-17
- Added recently approved SPDX exception rrdtool-floss-exception-2.0

* Wed Jan 24 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1.8.0-16
- Converted license to SPDX

* Mon Jan 22 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1.8.0-15
- Fixed FTBFS with GCC 14

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-13
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.0-11
- Perl 5.38 rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.8.0-10
- Rebuilt for Python 3.12

* Mon Apr 17 2023 Florian Weimer <fweimer@redhat.com> - 1.8.0-9
- Backport upstream patch to fix C99 issue in configure script

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-7
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Fri Dec 02 2022 Wolfgang Stöggl <c72578@yahoo.de> - 1.8.0-6
- Fix BUILD_DATE
  Add patch: rrdtool-1.8.0-BUILD_DATE-fix.patch

* Thu Nov 24 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> - 1.8.0-5
- Remove excludes for nonexistent .la files
- Fix Ruby directory lookup
- Move librrd(3) man page from -perl subpackage to main package

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-3
- Rebuilt for Python 3.11

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.0-2
- Perl 5.36 rebuild

* Tue Mar 22 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.8.0-1
- New version
  Resolves: rhbz#2065186

* Thu Jan 27 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.2-23
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.2-20
- Rebuilt for Python 3.10

* Wed May 26 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.2-19
- Removed rpath from python bindings better way

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.2-18
- Perl 5.34 rebuild

* Thu May 13 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.2-17
- Removed rpath from python bindings

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.2-15
- F-34: rebuild against ruby 3.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-14
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.2-12
- Used macros for make

* Tue Jun 30 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-11
- Rebuilt for Lua 5.4

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.2-10
- Perl 5.32 rebuild

* Mon Jun  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.2-9
- Fixed FTBFS
  Resolves: rhbz#1845126

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.2-6
- F-32: rebuild against ruby27

* Fri Aug 30 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-5
- Subpackage python2-rrdtool has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.2-2
- Perl 5.30 rebuild

* Mon May 27 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.2-1
- New version
  Resolves: rhbz#1714347
- Dropped compile-fix patch (upstreamed)

* Tue Feb  5 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.1-1
- New version
  Resolves: rhbz#1672309
- Dropped fix-configure-parameters patch (upstreamed)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-20
- F-30: rebuild against ruby26

* Wed Dec  5 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.0-19
- Dropped useless Makefile in examples/rrdcached

* Thu Sep 27 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.0-18
- Introduced python3 change requested by python team

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Petr Pisar <ppisar@redhat.com> - 1.7.0-16
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-15
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-14
- Perl 5.28 rebuild

* Tue Jun 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.0-13
- Added support for python3

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.7.0-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.7.0-10
- Rebuilt for switch to libxcrypt

* Mon Jan 08 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-9
- Again rebuild for ruby25

* Fri Jan  5 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.0-8
- Dropped libdbi on RHEL
  Resolves: rhbz#1531474

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-7
- F-28: rebuild for ruby25

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.0-6
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.0-5
- Python 2 binary package renamed to python2-rrdtool
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.7.0-2
- Perl 5.26 rebuild

* Wed May 17 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1.7.0-1
- New version
  Resolves: rhbz#1451534
- Spec cleanup
- Added support for locales

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-7
- F-26: rebuild for ruby24

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 1.6.0-6
- Adjust lua version computaion to SRPM build root without lua

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.6.0-4
- Disabled php bindings due to rhbz#1353500 and:
  https://github.com/oetiker/rrdtool-1.x/issues/724

* Fri Jul 15 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.6.0-3
- Rebuilt for php

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.6.0-2
- Perl 5.24 rebuild

* Wed Apr 20 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.6.0-1
- New version
  Resolves: rhbz#1328651
- Dropped lua-5.2 and arm-crash-fix patches (upstreamed)
- Updated ruby-2-fix patch

* Tue Apr 19 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.6-1
- New version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Wed Nov 11 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.5-1
- New version
  Resolves: rhbz#1280118

* Mon Aug 10 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.4-1
- New version
  Resolves: rhbz#1251737
- Defuzzified ruby-2-fix and lua-5.2 patches
- Used global instead of define
- Dropped macros for commands (e.g. rm)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.5.3-3
- Perl 5.22 rebuild

* Mon May 25 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.3-2
- Fixed crash on ARM
  Resolves: rhbz#1224530

* Mon May  4 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.3-1
- New version
  Resolves: rhbz#1217759

* Sat Apr 25 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.2-1
- New version
  Resolves: rhbz#1215162

* Thu Apr 23 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.1-1
- New version
  Resolves: rhbz#1214750
- Dropped python-fix (upstreamed)

* Mon Apr 20 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1.5.0-1
- New version
  Resolves: rhbz#1213035
- Dropped autoconf and doc-fix patches (all upstreamed)
- Included systemd rrdcached service and socket from upstream
- General documentation (like NEWS) moved to basic package

* Mon Jan 19 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.9-4
- Again rebuild for ruby 2.2

* Sun Jan 18 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.4.9-3
- Rebuilt for Lua 5.3

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.9-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Sep 30 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.9-1
- New version
  Resolves: rhbz#1147901
- Dropped imginfo-check patch (upstreamed)
- De-fuzzified patches

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.4.8-18
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-16
- Enabled php bindings on ppc

* Fri Aug  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-15
- Fixed conditionalized patch to be according to Packaging guidelines

* Tue Jun 24 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-14
- Improved backward compatibility
  Resolves: rhbz#111633

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.4.8-13
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- cleanup filter (no more needed in F20+)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Vít Ondruch <vondruch@redhat.com> - 1.4.8-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Mon Feb 17 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-10
- Used macro to detect all ppc64 host variants
  Resolves: rhbz#1054300

* Tue Jan 21 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.8-9
- rebuild for new libdbi

* Mon Dec  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-8
- Enabled libdbi support
  Resolves: rhbz#1039326

* Mon Nov  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-7
- Fixed multilib problems

* Fri Oct 11 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-6
- Fixed twice packaging of tclrrd1.4.8.so

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.4.8-4
- Perl 5.18 rebuild

* Mon Jul  1 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-3
- Minor doc / man fixes

* Fri Jun  7 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-2
- Added imginfo format check
  Resolves: CVE-2013-2131

* Thu May 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.8-1
- New version
  Resolves: rhbz#966639
- Updated and defuzzified patches

* Mon May 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-17
- Require lua abi instead of package version

* Wed May 15 2013 Tom Callaway <spot@fedoraproject.org> - 1.4.7-16
- lua 5.2

* Tue May  7 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-15
- Removed unneccassary dejavu-lgc-sans-mono-fonts requirement
  Resolves: rhbz#922467

* Tue Mar 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-14
- Fixed autoconf (by autoconf-fix patch)
- Added support for aarch64
  Resolves: rhbz#926455

* Mon Mar 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-13
- Fixed build failure
  Resolves: rhbz#926037

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.4.7-12
- rebuild for http://fedoraproject.org/wiki/Features/Php55
- remove rrdtool_logo_guid function

* Tue Mar 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-11
- Dropped ruby(abi) explicit requirement

* Mon Mar 18 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-10
- Fixed build failure with ruby-2.0 (by ruby-2-fix patch)
- Fixed bogus date in changelog

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-8
- Removed libtool archive from the lua subpackage

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.4.7-6
- Perl 5.16 rebuild

* Thu Feb  9 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-5
- Changed ruby(abi) to 1.9.1

* Wed Feb  8 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-4
- Used ruby_vendorarchdir instead of ruby_sitearch

* Wed Feb  8 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-3
- Fixed ruby(abi) requires

* Tue Feb  7 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-2
- Rebuilt for new ruby

* Thu Jan 26 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.7-1
- New version
  Resolves: rhbz#783553
- Dropped fix-tcl-site-option patch (upstreamed)

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.4.4-9
- build with php 5.4

* Thu Dec 29 2011 Remi Collet <remi@fedoraproject.org> - 1.4.4-8
- add patch for php 5.4
- add minimal load test for PHP extension
- add provides filters

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.4.4-7
- Rebuild for new libpng

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.4-6
- Perl mass rebuild

* Sat Jun 11 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.4-5
- Fixed build failure due to change in php_zend_api macro type

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.4-4
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.4-2
- Fixed mixed tabs and spaces rpmlint warning
- Fixed tcl-site configure option (upstream ticket #281)
- Removed Rpath from Ruby
- Enabled Lua bindings (#656080), thanks to Tim Niemueller

* Tue Nov 16 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4.4-1
- Update to rrdtool 1.4.4

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.8-7
- Mass rebuild with perl-5.12.0

* Wed Jan 13 2010 Stepan Kasal <skasal@redhat.com> - 1.3.8-6
- remove python_* macros clashing with the built-in ones
- fix for new vendorlib directory

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.3.8-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 1.3.8-3
- rebuild for new PHP 5.3.0 ABI (20090626)

* Tue May 26 2009 Jarod Wilson <jarod@redhat.com> 1.3.8-2
- Update dejavu font deps yet again, hopefully for the last time... (#473551)

* Tue May 19 2009 Jarod Wilson <jarod@redhat.com> 1.3.8-1
- Update to rrdtool 1.3.8

* Thu Apr 09 2009 Jarod Wilson <jarod@redhat.com> 1.3.7-1
- Update to rrdtool 1.3.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Jarod Wilson <jarod@redhat.com> 1.3.6-1
- Update to rrdtool 1.3.6

* Fri Jan 16 2009 Jarod Wilson <jarod@redhat.com> 1.3.5-2
- dejavu font package names changed again...

* Tue Dec 16 2008 Jarod Wilson <jarod@redhat.com> 1.3.5-1
- Update to rrdtool 1.3.5

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.4-5
- Rebuild for Python 2.6

* Mon Dec 01 2008 Jarod Wilson <jarod@redhat.com> 1.3.4-4
- Update dejavu font dependencies (#473551)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.4-3
- Rebuild for Python 2.6

* Mon Oct 20 2008 Jarod Wilson <jarod@redhat.com> 1.3.4-2
- Drop php bindings patch, rrd_update changed back to its
  prior prototype post-beta (#467593)

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> 1.3.4-1
- Update to rrdtool 1.3.4

* Mon Sep 15 2008 Jarod Wilson <jarod@redhat.com> 1.3.3-1
- Update to rrdtool 1.3.3
  * fixes segfault on graph creation regression in 1.3.2 (#462301)

* Sat Sep 06 2008 Jarod Wilson <jwilson@redhat.com> 1.3.2-1
- Update to rrdtool 1.3.2
  * fixes a data corruption bug when rrd wraps around
  * make imginfo behave the same as docs say it does
  * fixes for numerous memory leaks

* Tue Aug 12 2008 Jarod Wilson <jwilson@redhat.com> 1.3.1-1
- Update to rrdtool 1.3.1

* Mon Jun 16 2008 Chris Ricker <kaboom@oobleck.net> 1.3.0-1
- Update to rrdtool 1.3.0

* Sun Jun 08 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.20.rc9
- Update to rrdtool 1.3 rc9
- Minor spec tweaks to permit building on older EL

* Wed Jun 04 2008 Chris Ricker <kaboom@oobleck.net> 1.3-0.19.rc7
- Update to rrdtool 1.3 rc7

* Tue May 27 2008 Chris Ricker <kaboom@oobleck.net> 1.3-0.18.rc6
- Update to rrdtool 1.3 rc6

* Wed May 21 2008 Chris Ricker <kaboom@oobleck.net> 1.3-0.17.rc4
- Bump version and rebuild

* Wed May 21 2008 Chris Ricker <kaboom@oobleck.net> 1.3-0.16.rc4
- Fix php bindings compile on x86_64

* Mon May 19 2008 Chris Ricker <kaboom@oobleck.net> 1.3-0.15.rc4
- Update to rrdtool 1.3 rc4

* Tue May 13 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.15.rc1
- Update to rrdtool 1.3 rc1
- Fix versioning in changelog entries, had an extra 0 in there...
- Drop cairo and python patches, they're in 1.3 rc1
- Add Requires: gettext and libxml2-devel for new translations

* Wed Apr 30 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.14.beta4
- Drop some conditional flags, they're not working at the moment...

* Wed Apr 30 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.13.beta4
- Fix problem with cairo_save/cairo_restore (#444827)

* Wed Apr 23 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.12.beta4
- Fix python bindings rrdtool info implementation (#435468)

* Tue Apr 08 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.11.beta4
- Work around apparent version string length issue w/perl 5.10 (#441359)

* Sat Apr 05 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.10.beta4
- Fix use of rrd_update in php bindings (#437558)

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-0.9.beta4
- rebuild for new perl (again)

* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.8.beta4
- Update to rrdtool 1.3 beta4

* Tue Feb 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3-0.7.beta3
- rebuild for new perl (and fix license tag)

* Mon Feb 04 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.6.beta3
- Plug memory leak (#430879)

* Mon Jan 07 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.5.beta3
- Fix right-aligned text alignment and scaling (Resolves: #427609)

* Wed Jan 02 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.4.beta3
- Add newly built python egg to %%files

* Wed Jan 02 2008 Jarod Wilson <jwilson@redhat.com> 1.3-0.3.beta3
- Update to rrdtool 1.3 beta3
- Return properly from errors in RRDp.pm (Resolves: #427040)
- Requires: dejavu-lgc-fonts (Resolves: #426935)

* Thu Dec 06 2007 Jarod Wilson <jwilson@redhat.com> 1.3-0.2.beta2
- Update to rrdtool 1.3 beta2

* Wed Aug 08 2007 Jarod Wilson <jwilson@redhat.com> 1.3-0.1.beta1
- Update to rrdtool 1.3 beta1

* Tue Jul 10 2007 Jarod Wilson <jwilson@redhat.com> 1.2.999-0.3.r1144
- Update to latest rrdtool pre-1.3 svn snapshot (svn r1144)
- Add php abi check (Resolves: #247339)

* Fri Jun 15 2007 Jarod Wilson <jwilson@redhat.com> 1.2.999-0.2.r1127
- Fix up BuildRequires

* Fri Jun 15 2007 Jarod Wilson <jwilson@redhat.com> 1.2.999-0.1.r1127
- Update to rrdtool pre-1.3 svn snapshot (svn r1127)

* Mon May 21 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-5
- BR: ruby so %%ruby_sitearch gets set

* Mon May 21 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-4
- Build ruby bindings

* Thu May 03 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-3
- Disable php bits on ppc64 for now, they fail to build

* Thu May 03 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-2
- Add BR: perl-devel for Fedora 7 and later

* Tue May 01 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-1
- New upstream release

* Tue May 01 2007 Jarod Wilson <jwilson@redhat.com> 1.2.21-1
- New upstream release

* Wed Apr 25 2007 Jarod Wilson <jwilson@redhat.com> 1.2.19-2
- Define %%python_version *before* its needed (#237826)

* Mon Apr 09 2007 Jarod Wilson <jwilson@redhat.com> 1.2.19-1
- New upstream release

* Tue Jan 23 2007 Jarod Wilson <jwilson@redhat.com> 1.2.18-1
- New upstream release

* Mon Jan 22 2007 Jarod Wilson <jwilson@redhat.com> 1.2.17-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 1.2.15-9
- Fix crash with long error strings (upstream
  changesets 929 and 935)

* Thu Dec 14 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-8
- Fix for log grid memory leak (#201241)

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-7
- Rebuild for python 2.5

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-6
- Conditionalize python, php and tcl bits (Resolves #203275)

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-5
- Add tcl sub-package (#203275)

* Tue Sep 05 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-4
- Rebuild for new glibc

* Wed Aug 02 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-3
- One more addition to initrrdtool patch, to fully revert
  and correct upstream changeset 839
- Fix for no python in minimal fc4 buildroots

* Tue Aug  1 2006 Mihai Ibanescu <misa@redhat.com> 1.2.15-2
- Fixed rrdtool-python to import the module properly (patch
  rrdtool-1.2.15-initrrdtool.patch)

* Mon Jul 17 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-1
- Update to 1.2.15
- Minor spec cleanups

* Sat Jun 24 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-7
- Fix up Obsoletes

* Mon Jun 19 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-6
- Flip perl, php and python sub-package names around to 
  conform with general practices

* Sat Jun 10 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-5
- Minor fixes to make package own created directories

* Wed Jun 07 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-4
- Add php bits back into the mix

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-3
- Merge spec fixes from bz 185909

* Sun Jun 04 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-2
- Remove explicit perl dep, version grabbing using rpm during
  rpmbuild not guaranteed to work (fails on ppc in plague),
  and auto-gen perl deps are sufficient

* Sat Jun 03 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-1
- Update to release 1.2.13
- Merge spec changes from dag, atrpms and mdk builds
- Additional hacktastic contortions for lib64 & rpath messiness
- Add missing post/postun ldconfig
- Fix a bunch of rpmlint errors
- Disable static libs, per FE guidelines
- Split off docs

* Wed Apr 19 2006 Chris Ricker <kaboom@oobleck.net> 1.2.12-1
- Rev to 1.2

* Fri May 20 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-5
- Include patch from Michael to fix perl module compilation on FC4 (#156242).

* Fri May 20 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-4
- Fix for the php module patch (Joe Pruett, Dag Wieers), #156716.
- Update source URL to new location since 1.2 is now the default stable.
- Don't (yet) update to 1.0.50, as it introduces some changes in the perl
  modules install.

* Mon Jan 31 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-3
- Put perl modules in vendor_perl and not site_perl. #146513

* Thu Jan 13 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-2
- Minor cleanups.

* Wed Aug 25 2004 Dag Wieers <dag@wieers.com> - 1.0.49-1
- Updated to release 1.0.49.

* Wed Aug 25 2004 Dag Wieers <dag@wieers.com> - 1.0.48-3
- Fixes for x86_64. (Garrick Staples)

* Fri Jul  2 2004 Matthias Saou <http://freshrpms.net/> 1.0.48-3
- Actually apply the patch for fixing the php module, doh!

* Thu May 27 2004 Matthias Saou <http://freshrpms.net/> 1.0.48-2
- Added php.d config entry to load the module once installed.

* Thu May 13 2004 Dag Wieers <dag@wieers.com> - 1.0.48-1
- Updated to release 1.0.48.

* Tue Apr 06 2004 Dag Wieers <dag@wieers.com> - 1.0.47-1
- Updated to release 1.0.47.

* Thu Mar  4 2004 Matthias Saou <http://freshrpms.net/> 1.0.46-2
- Change the strict dependency on perl to fix problem with the recent
  update.

* Mon Jan  5 2004 Matthias Saou <http://freshrpms.net/> 1.0.46-1
- Update to 1.0.46.
- Use system libpng and zlib instead of bundled ones.
- Added php-rrdtool sub-package for the php4 module.

* Fri Dec  5 2003 Matthias Saou <http://freshrpms.net/> 1.0.45-4
- Added epoch to the perl dependency to work with rpm > 4.2.
- Fixed the %% escaping in the perl dep.

* Mon Nov 17 2003 Matthias Saou <http://freshrpms.net/> 1.0.45-2
- Rebuild for Fedora Core 1.

* Sun Aug  3 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.45.

* Wed Apr 16 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.42.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Wed Mar  5 2003 Matthias Saou <http://freshrpms.net/>
- Added explicit perl version dependency.

* Sun Feb 23 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.41.

* Fri Jan 31 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.40.
- Spec file cleanup.

* Fri Jul 05 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.39

* Mon Jun 03 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.38

* Fri Apr 19 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.37

* Tue Mar 12 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.34
- rrdtools include zlib 1.1.4 which fix vulnerabilities in 1.1.3

