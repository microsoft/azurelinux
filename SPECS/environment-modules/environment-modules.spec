%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
Summary:        Provides dynamic modification of a user's environment
Name:           environment-modules
Version:        5.3.1
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://modules.sourceforge.net/
Source0:        https://downloads.sourceforge.net/modules/modules-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  dejagnu
BuildRequires:  gcc
BuildRequires:  hostname
BuildRequires:  less
BuildRequires:  make
BuildRequires:  man
BuildRequires:  procps
BuildRequires:  sed
BuildRequires:  tcl-devel
Requires:       less
Requires:       man
Requires:       procps
Requires:       sed
Requires:       tcl
Requires(post): %{_sbindir}/update-alternatives
Requires(post): coreutils
Requires(postun): %{_sbindir}/update-alternatives
Provides:       environment(modules)
Obsoletes:      environment-modules-compat <= 4.8.99

%description
The Environment Modules package provides for the dynamic modification of
a user's environment via modulefiles.

Each modulefile contains the information needed to configure the shell
for an application. Once the Modules package is initialized, the
environment can be modified on a per-module basis using the module
command which interprets modulefiles. Typically modulefiles instruct
the module command to alter or set shell environment variables such as
PATH, MANPATH, etc. modulefiles may be shared by many users on a system
and users may have their own collection to supplement or replace the
shared modulefiles.

Modules can be loaded and unloaded dynamically and atomically, in an
clean fashion. All popular shells are supported, including bash, ksh,
zsh, sh, csh, tcsh, as well as some scripting languages such as perl.

Modules are useful in managing different versions of applications.
Modules can also be bundled into metamodules that will load an entire
suite of different applications.

NOTE: You will need to get a new shell after installing this package to
have access to the module alias.

%prep
%setup -q -n modules-%{version}


%build
%configure --prefix=%{_datadir}/Modules \
           --libdir=%{_libdir}/%{name} \
           --etcdir=%{_sysconfdir}/%{name} \
           --bindir=%{_datadir}/Modules/bin \
           --libexecdir=%{_datadir}/Modules/libexec \
           --mandir=%{_mandir} \
           --nagelfardatadir=%{_datadir}/Modules/nagelfar \
           --with-bashcompletiondir=%{_datadir}/bash-completion/completions \
           --with-fishcompletiondir=%{_datadir}/fish/vendor_completions.d \
           --with-zshcompletiondir=%{_datadir}/zsh/site-functions \
           --enable-multilib-support \
           --disable-doc-install \
           --enable-modulespath \
           --with-python=%{_bindir}/python3 \
           --with-modulepath=%{_datadir}/Modules/modulefiles:%{_sysconfdir}/modulefiles:%{_datadir}/modulefiles \
           --with-quarantine-vars='LD_LIBRARY_PATH LD_PRELOAD'

%make_build


%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/modulefiles
mkdir -p %{buildroot}%{_datadir}/modulefiles
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{_bindir}

# Set up for alternatives.
touch %{buildroot}%{_sysconfdir}/profile.d/modules.{csh,sh}
touch %{buildroot}%{_bindir}/modulecmd
# remove modulecmd wrapper as it will be handled by alternatives
rm -f %{buildroot}%{_datadir}/Modules/bin/modulecmd

# Major utilities go to regular bin dir.
mv %{buildroot}%{_datadir}/Modules/bin/envml %{buildroot}%{_bindir}/


mv {doc/build/,}NEWS.txt
mv {doc/build/,}MIGRATING.txt
mv {doc/build/,}CONTRIBUTING.txt
mv {doc/build/,}INSTALL.txt
mv {doc/build/,}changes.txt

rm -f %{buildroot}%{_docdir}/%{name}/{COPYING.GPLv2,ChangeLog-compat,INSTALL.txt,NEWS-compat}

# install the rpm config file
install -Dpm 644 contrib/rpm/macros.%{name} %{buildroot}/%{macrosdir}/macros.%{name}

rm -rf %{buildroot}%{_datadir}/Modules/share/vim

%check
make test QUICKTEST=1

%post
# Cleanup from pre-alternatives
[ ! -L %{_sysconfdir}/profile.d/modules.sh ] &&  rm -f %{_sysconfdir}/profile.d/modules.sh
[ ! -L %{_sysconfdir}/profile.d/modules.csh ] &&  rm -f %{_sysconfdir}/profile.d/modules.csh
[ ! -L %{buildroot}%{_bindir}/modulecmd ] &&  rm -f %{_bindir}/modulecmd

# Migration from version 3.x to 4
if [ "$(readlink %{_sysconfdir}/alternatives/modules.sh)" = '%{_datadir}/Modules/init/modules.sh' ]; then
  %{_sbindir}/update-alternatives --remove modules.sh %{_datadir}/Modules/init/modules.sh
fi

%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/profile.d/modules.sh modules.sh %{_datadir}/Modules/init/profile.sh 40 \
  --slave %{_sysconfdir}/profile.d/modules.csh modules.csh %{_datadir}/Modules/init/profile.csh \
  --slave %{_bindir}/modulecmd modulecmd %{_datadir}/Modules/libexec/modulecmd.tcl \
%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove modules.sh %{_datadir}/Modules/init/profile.sh
fi

%files
%license COPYING.GPLv2
%doc ChangeLog.gz README NEWS.txt MIGRATING.txt CONTRIBUTING.txt INSTALL.txt changes.txt
%{_sysconfdir}/modulefiles
%ghost %{_sysconfdir}/profile.d/modules.csh
%ghost %{_sysconfdir}/profile.d/modules.sh
%ghost %{_bindir}/modulecmd
%{_bindir}/envml
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libtclenvmodules.so
%dir %{_datadir}/Modules
%{_datadir}/Modules/bin
%dir %{_datadir}/Modules/libexec
%{_datadir}/Modules/libexec/modulecmd.tcl
%dir %{_datadir}/Modules/init
%{_datadir}/Modules/init/*
# do not need to require shell package as we "own" completion dir
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/module
%{_datadir}/bash-completion/completions/ml
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_module
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/module.fish
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/initrc
%config(noreplace) %{_sysconfdir}/%{name}/modulespath
%config(noreplace) %{_sysconfdir}/%{name}/siteconfig.tcl
%{_datadir}/Modules/modulefiles
%{_datadir}/modulefiles
%{_mandir}/man1/ml.1.gz
%{_mandir}/man1/module.1.gz
%{_mandir}/man4/modulefile.4.gz
%{macrosdir}/macros.%{name}
%dir %{_datadir}/Modules/nagelfar
%{_datadir}/Modules/nagelfar/*

%changelog
* Mon Jan 22 2024 Andrew Phelps <anphel@microsoft.com> - 5.3.1-1
- Upgrade to 5.3.1

* Fri Feb 03 2023 Riken Maharjan <rmaharjan@microsoft.com> - 5.2.0-1
- Move from extended to Core.
- Update to 5.2.0 (from Fedora 38 (license: MIT)).
- License verified.
- Remove compat.

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 4.4.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove X11 dependencies.
- Build without vim modules.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan  6 2020 Jan Synáček <jsynacek@redhat.com> - 4.4.1-1
- Update to 4.4.1 (#1787690)

* Wed Nov 27 2019 Jan Synáček <jsynacek@redhat.com> - 4.4.0-1
- Update to 4.4.0 (#1773590)

* Wed Oct  2 2019 Jan Synáček <jsynacek@redhat.com> - 4.3.1-1
- Update to 4.3.1 (#1754182)

* Mon Jul 29 2019 Jan Synáček <jsynacek@redhat.com> - 4.3.0-1
- Update to 4.3.0 (#1733752)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul  9 2019 Jan Synáček <jsynacek@redhat.com> - 4.2.5-1
- Update to 4.2.5 (#1727988)

* Mon Apr 29 2019 Jan Synáček <jsynacek@redhat.com> - 4.2.4-1
- Update to 4.2.4 (#1703415, #1687033)

* Mon Mar 25 2019 Jan Synáček <jsynacek@redhat.com> - 4.2.3-1
- Update to 4.2.3 (#1692024, #1687033)

* Mon Feb 18 2019 Jan Synáček <jsynacek@redhat.com> - 4.2.2-1
- Update to 4.2.2 (#1678041)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Jan Synáček <jsynacek@redhat.com> - 4.2.1-1
- Update to 4.2.1 (#1648738)

* Thu Oct 18 2018 Jan Synáček <jsynacek@redhat.com> - 4.2.0-1
- Update to 4.2.0 (#1640450)

* Tue Aug 21 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.4-2
- Don't install any files under /usr as config files (#1506663)

* Tue Aug 21 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.4-1
- Update to 4.1.4 (#1619415)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.3-1
- Update to 4.1.3 (#1592179, #1575479, #1585305)

* Fri May  4 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.2-2
- Fix postun script (#1565699)

* Tue Apr  3 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.2-1
- Update to 4.1.2 (#1562535)

* Tue Mar  6 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.1-2
- Fix error messages caused by unquoted parameters (#1549664)

* Tue Feb 20 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.1-1
- Update to 4.1.1 (#1546450, #1139165, #1545369)
  + Big thanks to Xavier Delaruelle for a spec patch!

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Jan Synáček <jsynacek@redhat.com> - 4.1.0-1
- Update to 4.1.0 (#1534746)
  + Big thanks to Xavier Delaruelle for a spec patch!

* Tue Nov 21 2017 Jan Synáček <jsynacek@redhat.com> - 4.0.0-2
- Fix 4.0.0 BuildRequires and Requires (#1503408)
  + Big thanks to Xavier Delaruelle for a spec patch!
- Fix installing manpages as alternatives

* Mon Nov 20 2017 Jan Synáček <jsynacek@redhat.com> - 4.0.0-1
- Update to 4.0.0 (#1503408)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.10-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 16 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-21
- Use alternatives for man pages as well

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.10-19
- Rebuild for Python 3.6

* Sun Dec 4 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-18
- Fix compilation with -Werror=implicit-function-declaration
- Use %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Orion Poplwski <orion@cora.nwra.com> - 3.2.10-16
- Add patch to fix unload from loaded modulefile (bug #1117334)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 2 2015 Orion Poplwski <orion@cora.nwra.com> - 3.2.10-14
- Fix createmodule.sh to handle exported functions (bug #1197321)
- Handle more prefix/suffix cases in createmodule.{sh,py} (bug #1079341)

* Wed Jan 28 2015 Orion Poplwski <orion@cora.nwra.com> - 3.2.10-13
- Add patch for python 3 support, use python3 for createmodule.py on F22

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Orion Poplwski <orion@cora.nwra.com> - 3.2.10-10
- Add patch to support Tcl 8.6

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Mon Apr 14 2014 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-9
- Use alternatives for /etc/profile.d/modules.{csh,sh}
- Add /usr/share/modulefiles to MODULEPATH
- Add rpm macro to define %%_modulesdir

* Mon Dec 23 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-8
- Fix -Werror=format-security (bug #1037053)

* Wed Sep 4 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-7
- Update createmodule scripts to handle more path like variables (bug #976647)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-5
- Really do not replace modified profile.d scripts (bug #962762)
- Specfile cleanup

* Wed Apr 17 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-4
- Do not replace modified profile.d scripts (bug #953199)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-2
- Add patch to comment out stray module use in modules file when not using
  versioning (bug #895555)
- Add patch to fix module clear command (bug #895551)
- Add patch from modules list to add completion to avail command

* Fri Dec 21 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.10-1
- Update to 3.2.10
- Drop regex patch

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-5
- Updated createmodule.sh, added createmodule.py, can handle path prefixes

* Fri Aug 24 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-4
- Add patch to fix segfault from Tcl RexExp handling (bug 834580)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-1
- Update to 3.2.9c (fixes bug 753760)

* Tue Nov 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-2
- Make .modulespath a config file

* Tue Nov 15 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-1
- Update to 3.2.9b

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-2
- Add %%check section

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-1
- Update to 3.2.9a
- Drop strcpy patch

* Thu Sep 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-3
- Add patch to fix overlapping strcpy() in Remove_Path, hopefully fixes
  bug 737043

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-1
- Update to 3.2.8a, changes --with-def-man-path to --with-man-path

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8-1
- Update to 3.2.8
- Drop mandir patch, use --with-def-man-path

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-7
- Add patch to set a sane default MANPATH
- Add createmodule.sh utility script for creating modulefiles

* Mon Nov 30 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-6
- Add Requires: propcs (bug #54272)

* Mon Oct 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-5
- Don't assume different shell init scripts exist (bug #530770)

* Fri Oct 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-4
- Don't load bash init script when bash is running as "sh" (bug #529745)

* Mon Oct 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-3
- Support different flavors of "sh" (bug #529493)

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-2
- Add patch to fix modulecmd path in init files

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-1
- Update to 3.2.7b

* Mon Sep 21 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7-1
- Update to 3.2.7, fixes bug #524475
- Drop versioning patch fixed upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 3 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-6
- Change %%patch -> %%patch0

* Fri Mar 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-5
- Add BR libX11-devel so modulecmd can handle X resources

* Wed Mar  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-4
- Add patch to fix extraneous version path entry properly
- Use --with-module-path to point to /etc/modulefiles for local modules,
  this also fixes bug #436041

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-3
- Rebuild for gcc 3.4

* Thu Jan 03 2008 - Alex Lancaster <alexlan at fedoraproject.org> - 3.2.6-2
- Rebuild for new Tcl (8.5).

* Fri Nov  2 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-1
- Update to 3.2.6

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-2
- Update license tag to GPLv2

* Fri Feb 16 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-2
- Rebuild for Tcl downgrade

* Fri Feb 09 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-1
- Update to 3.2.4

* Wed Dec 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-3
- Add --with-version-path to set VERSIONPATH (bug 220260)

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-2
- Rebuild for FC6

* Fri Jun  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-1
- Update to 3.2.3

* Fri May  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.2-1
- Update to 3.2.2

* Fri Mar 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1

* Thu Feb  9 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0p1-1
- Update to 3.2.0p1

* Fri Jan 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Add profile.d links

* Tue Jan 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Fedora Extras packaging
