%global major_version 5.4
# Normally, this is the same as version, but... not always.
%global test_version 5.4.3
# If you are incrementing major_version, enable bootstrapping and adjust accordingly.
# Version should be the latest prior build. If you don't do this, RPM will break and
# everything will grind to a halt.
%global bootstrap 1
%global bootstrap_major_version 5.3
%global bootstrap_version %{bootstrap_major_version}.5

# Place rpm-macros into proper location.
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           lua
Version:        %{major_version}.3
Release:        2%{?dist}
Summary:        Powerful light-weight programming language
License:        MIT
URL:            https://www.lua.org/
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://www.lua.org/ftp/%{name}-%{version}.tar.gz
# copied from doc/readme.html on 2014-07-18
Source1:        mit.txt
%if 0%{?bootstrap}
Source2:        http://www.lua.org/ftp/lua-%{bootstrap_version}.tar.gz
%endif
Source3:        http://www.lua.org/tests/lua-%{test_version}-tests.tar.gz
# multilib
Source4:        luaconf.h
Patch0:         %{name}-5.4.0-beta-autotoolize.patch
Patch1:         %{name}-5.3.0-idsize.patch
#Patch2:        %%{name}-5.3.0-luac-shared-link-fix.patch
Patch3:         %{name}-5.2.2-configure-linux.patch
Patch4:         %{name}-5.3.0-configure-compat-module.patch
%if 0%{?bootstrap}
Patch5:         %{name}-5.3.0-autotoolize.patch
Patch6:		    %{name}-5.3.5-luac-shared-link-fix.patch
%endif
# https://www.lua.org/bugs.html
Patch18:	    %{name}-5.3.5-CVE-2020-24370.patch
Patch19:	    %{name}-5.4.3-bug3.patch
Patch20:	    CVE-2021-43519.patch
Patch21:        CVE-2022-28805.patch

BuildRequires:  automake autoconf libtool readline-devel ncurses-devel
BuildRequires:  make
Requires:       lua-libs = %{version}-%{release}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Requires:       lua-rpm-macros

%description devel
This package contains development files for %{name}.

%package libs
Summary:        Libraries for %{name}
Provides:       lua(abi) = %{major_version}

%description libs
This package contains the shared libraries for %{name}.

%package static
Summary:        Static library for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.


%prep
%if 0%{?bootstrap}
%setup -q -a 2 -a 3 -n %{name}-%{version}
%else
%setup -q -a 3
%endif
cp %{SOURCE1} .
mv src/luaconf.h src/luaconf.h.template.in
%patch0 -p1 -E -z .autoxxx
%patch1 -p1 -z .idsize
#%% patch2 -p1 -z .luac-shared
%patch3 -p1 -z .configure-linux
%patch4 -p1 -z .configure-compat-all
# Put proper version in configure.ac, patch0 hardcodes 5.3.0
sed -i 's|5.3.0|%{version}|g' configure.ac
%patch19 -p1 -b .bug3
%patch20 -p1
%patch21 -p1
autoreconf -ifv

%if 0%{?bootstrap}
cd lua-%{bootstrap_version}/
mv src/luaconf.h src/luaconf.h.template.in
%patch5 -p1 -b .autoxxx
%patch1 -p1 -b .idsize
%patch3 -p1 -z .configure-linux
%patch4 -p1 -z .configure-compat-all
%patch6 -p1 -b .luac-shared-link-fix
%patch18 -p1 -b .CVE-2020-24370
autoreconf -i
cd ..
%endif

%build
%configure --with-readline --with-compat-module
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Autotools give me a headache sometimes.
sed -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
%make_build LIBS="-lm -ldl"
# only /usr/bin/lua links with readline now #luac_LDADD="liblua.la -lm -ldl"

%if 0%{?bootstrap}
pushd lua-%{bootstrap_version}
%configure --with-readline --with-compat-module
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Autotools give me a headache sometimes.
sed -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
%make_build LIBS="-lm -ldl" luac_LDADD="liblua.la -lm -ldl"
popd
%endif

%check
cd ./lua-%{test_version}-tests/

# Dont skip the fully portable or ram-hungry tests:
# sed -i.orig -e '
#     /attrib.lua/d;
#     /files.lua/d;
#     /db.lua/d;
#     /errors.lua/d;
#     ' all.lua
# LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir} $RPM_BUILD_ROOT/%{_bindir}/lua all.lua

# Removing tests that fail under mock/koji
sed -i.orig -e '
    /db.lua/d;
    /errors.lua/d;
    ' all.lua
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir} $RPM_BUILD_ROOT/%{_bindir}/lua -e"_U=true" all.lua

%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{major_version}

# Rename luaconf.h to luaconf-<arch>.h to avoid file conflicts on
# multilib systems and install luaconf.h wrapper
mv %{buildroot}%{_includedir}/luaconf.h %{buildroot}%{_includedir}/luaconf-%{_arch}.h
install -p -m 644 %{SOURCE4} %{buildroot}%{_includedir}/luaconf.h

%if 0%{?bootstrap}
pushd lua-%{bootstrap_version}
mkdir $RPM_BUILD_ROOT/installdir
make install DESTDIR=$RPM_BUILD_ROOT/installdir
cp -a $RPM_BUILD_ROOT/installdir/%{_libdir}/liblua-%{bootstrap_major_version}.so $RPM_BUILD_ROOT%{_libdir}/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/lua/%{bootstrap_major_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lua/%{bootstrap_major_version}
rm -rf $RPM_BUILD_ROOT/installdir
popd
%endif

%files
%{!?_licensedir:%global license %%doc}
%license mit.txt

%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%{_bindir}/lua
%{_bindir}/luac
%{_mandir}/man1/lua*.1*

%files libs
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%{_libdir}/liblua-%{major_version}.so
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}

%if 0%{?bootstrap}
%dir %{_libdir}/lua/%{bootstrap_major_version}
%{_libdir}/liblua-%{bootstrap_major_version}.so
%dir %{_datadir}/lua/%{bootstrap_major_version}
%endif

%files devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a


%changelog
* Fri May 20 2022 Olivia Crain <oliviacrain@microsoft.com> - 5.4.3-2
- Add upstream patch for CVE-2022-28805

* Wed Jan 19 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> 5.4.3-1
- Update lua version to 5.4.3
- Apply patch for CVE-2021-43519.

* Thu Oct 01 2020 Daniel McIlvaney <damcilva@microsoft.com> 5.3.5-11
- Nopatch CVE-2020-24342
- Apply patch for CVE-2019-6706 from Lua mailing list
- Apply patch for CVE-2020-15888 from Open Embedded

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 5.3.5-10
- Nopatch CVE-2020-15889 since it only affects 5.4.0

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 5.3.5-9
- Update URL to https.
- License verified.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 5.3.5-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT)
- Remove bootstrap option

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.3.5-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Tom Callaway <spot@fedoraproject.org> - 5.3.5-3
- apply fix for CVE-2019-6706 (bz1670020)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Tom Callaway <spot@fedoraproject.org> - 5.3.5-1
- update to 5.3.5

* Tue Feb 13 2018 Tom Callaway <spot@fedoraproject.org> - 5.3.4-10
- move lua(abi) provide to -libs
- add fix for bug 6

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan  2 2018 Richard W.M. Jones <rjones@redhat.com> - 5.3.4-8
- Unnecessary change to RISC-V macros in GCC requires change in luaconf.h.

* Mon Dec  4 2017 Tom Callaway <spot@fedoraproject.org> - 5.3.4-7
- fix pkgconfig provides (bz1519921)

* Sun Oct 29 2017 Tom Callaway <spot@fedoraproject.org> - 5.3.4-6
- apply known upstream bugfixes

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 28 2017 Björn Esser <besser82@fedoraproject.org> - 5.3.4-3
- Refactor macros to a more common syntax
- Use rpm's build-in lua for macros

* Wed May 24 2017 Björn Esser <besser82@fedoraproject.org> - 5.3.4-2
- Add rpm-macros file, providing packaging macros for lua add-ons (#1447324)

* Thu Feb  9 2017 Tom Callaway <spot@fedoraproject.org> 5.3.4-1
- update to 5.3.4

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 5.3.3-4
- Rebuild for readline 7.x

* Tue Jul 26 2016 Tom Callaway <spot@fedoraproject.org> - 5.3.3-3
- create lua-libs subpackage
- disable bootstrap

* Mon Jul 25 2016 Tom Callaway <spot@fedoraproject.org> - 5.3.3-2
- apply fixes for upstream bug 1 & 2

* Tue Jun  7 2016 Tom Callaway <spot@fedoraproject.org> - 5.3.3-1
- update to 5.3.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Tom Callaway <spot@fedoraproject.org> - 5.3.2-2
- fix multilib support (#1229992)

* Fri Dec 11 2015 "D. Johnson" <fenris02@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2 (#1039249,1173984)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Kalev Lember <kalevlember@gmail.com> - 5.3.0-3
- Define LUA_COMPAT_5_2 in addition to LUA_COMPAT_5_1 (#1204129)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 5.3.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 15 2015 Tom Callaway <spot@fedoraproject.org> - 5.3.0-1
- update to 5.3.0
- add bootstrapping glue

* Wed Dec 10 2014 Tom Callaway <spot@fedoraproject.org> - 5.2.3-1
- update to 5.2.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 5.2.2-7
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 Tom Callaway <spot@fedoraproject.org> - 5.2.2-5
- readd and fix configure-compat-module.patch to use LUA_CONFIG_ALL instead

* Wed Oct 23 2013 Tom Callaway <spot@fedoraproject.org> - 5.2.2-4
- drop configure-compat-module.patch, if you really need old lua behavior, use compat-lua

* Mon Aug 05 2013 Hans de Goede <hdegoede@redhat.com> - 5.2.2-3
- Drop compat-lua-libs package, as there now is a separate compat-lua
  package (including a -devel)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Tom Callaway <spot@fedoraproject.org> - 5.2.2-1
- update to 5.2.2
- incorporate Aaron Faanes's changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 06 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-9
- Provide lua(abi) = 5.1 for better distro updates later

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-7
- Add patch to from lua.org with smaller bugfixes
- sed -i -e 's/5\.1\.3/5.1.4/g' on autotoolize patch, bug #641144

* Fri Jan 28 2011 Tim Niemueller <tim@niemueller.de> - 5.1.4-6
- Add patch to increase IDSIZE for more useful error messages

* Sun May 09 2010 Tim Niemueller <tim@niemueller.de> - 5.1.4-5
- Add patch regarding dlopen flags to support Lunatic (Lua-Python bridge)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Tim Niemueller <tim@niemueller.de> - 5.1.4-2
- Link liblua.so with -lm (math lib), fixes rhbz #499238

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 03 2008 Tim Niemueller <tim@niemueller.de> - 5.1.4-1
- New upstream release 5.1.4

* Mon May 12 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-6
- Add -static subpackage with static liblua, fixes rh bug #445939

* Sun Apr 13 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-5
- Provide lua = 5.1, this way add-on packages can easily depend on the Lua
  base version and expect certain paths for packages

* Sat Apr  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.3-4
- Not only own $libdir/lua/5.1 and $datadir/lua/5.1 but also $libdir/lua
  and $datadir/lua for proper removal of these dirs upon lua removal

* Fri Mar 14 2008 Tim Niemueller <tim@niemueller.de> - 5.1.3-3
- own $libdir/lua/5.1 and $datadir/lua/5.1. These are the standard package
  search path for Lua. Packaging them properly allows for easy creation of
  Lua addon packages.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.1.3-2
- Autorebuild for GCC 4.3

* Sat Jan 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.3-1
- New upstream release 5.1.3

* Mon Nov 26 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-4
- Fix libdir in lua.pc being /usr/lib on x86_64 (bz 399101)

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-3
- Also use lib64 instead of lib on ia64 and sparc64 

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-2
- Fix multilib condlict in luaconf.h (bz 342561)

* Mon Apr  2 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.2-1
- New upstream release 5.1.2
- Fix use of rpath on x86_64

* Fri Jan 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-3
- Remove "-lreadline -lncurses" from lua.pc (bz 213895)

* Sun Oct 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-2
- Only link /usr/bin/lua with readline / do not link %%{_libdir}/liblua-5.1.so
  with readline so that we don't cause any License troubles for packages
  linking against liblua-5.1.so, otherwise lua could drag the GPL only readline
  lib into the linking of non GPL apps.

* Sat Oct 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 5.1.1-1
- New upstream release 5.1.1
- Fix detection of readline during compile (iow add readline support back)

* Sun Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-7
- Rebuild for FC6

* Thu Jun 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-6
- fixed broken provides

* Tue Jun 06 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-5
- split out devel subpackage

* Thu Jun 01 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-4
- added Requires for pkgconfig BZ#193674

* Mon May 29 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-3
- added autotools patch from Petri Lehtinen, http://lua-users.org

* Mon May 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-2
- fixed x86_64 builds

* Mon May 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 5.1-1
- version bump

* Sun Oct 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 5.0.2-5
- Fix -debuginfo (#165304).
- Cosmetic specfile improvements.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 5.0.2-4
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 5.0.2-3
- rebuilt

* Sat Feb 12 2005 David Woodhouse <dwmw2@infradead.org> - 5.0.2-2
- Don't use fastround on ppc

* Tue Feb 01 2005 Panu Matilainen <pmatilai@welho.com> - 5.0.2-1
- update to 5.0.2
- remove epoch 0, drop fedora.us release tag

* Mon Nov 17 2003 Oren Tirosh <oren at hishome.net> - 0:5.0-0.fdr.2
- Enable readline support.

* Sat Jun 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:5.0-0.fdr.1
- First build.
