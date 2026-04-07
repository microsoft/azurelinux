# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           environment-modules
Version:        5.6.1
Release:        1%{?dist}
Summary:        Provides dynamic modification of a user's environment

License:        GPL-2.0-or-later
URL:            https://envmodules.io
Source0:        http://downloads.sourceforge.net/modules/modules-%{version}.tar.bz2

BuildRequires:  tcl
BuildRequires:  dejagnu
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  less
BuildRequires:  util-linux-core
BuildRequires:  hostname
BuildRequires:  procps-ng
# specific requirements to build extension library
BuildRequires:  gcc
BuildRequires:  tcl-devel
Requires:       tcl
Requires:       sed
Requires:       less
Requires:       util-linux-core
BuildRequires:  vim-filesystem
Requires:       vim-filesystem
BuildRequires:  emacs-nw
Requires:       emacs-filesystem%{?_emacs_version: >= %{_emacs_version}}
Requires:       procps-ng
Requires:       man-db
Requires(post): coreutils
Requires(post): %{_bindir}/update-alternatives
Requires(postun): %{_bindir}/update-alternatives
Provides:       environment(modules)
Obsoletes:      environment-modules-compat <= 4.8.99

# Tcl linter is useful for module lint command
Recommends:     nagelfar

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
Modules can also be bundled into meta-modules that will load an entire
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
           --vimdatadir=%{vimfiles_root} \
           --emacsdatadir=%{_emacs_sitelispdir}/%{name} \
           --nagelfardatadir=%{_datadir}/Modules/nagelfar \
           --with-bashcompletiondir=%{bash_completions_dir} \
           --with-fishcompletiondir=%{fish_completions_dir} \
           --with-zshcompletiondir=%{zsh_completions_dir} \
           --enable-multilib-support \
           --disable-doc-install \
           --enable-modulespath \
           --with-python=/usr/bin/python3 \
           --with-modulepath=%{_datadir}/Modules/modulefiles:%{_sysconfdir}/modulefiles:%{_datadir}/modulefiles \
           --with-quarantine-vars='LD_LIBRARY_PATH LD_PRELOAD'

%make_build

# compile Elisp file
%{_emacs_bytecompile} share/emacs/lisp/modulefile-mode.el


%install
%make_install

mkdir -p %{buildroot}%{_sysconfdir}/modulefiles
mkdir -p %{buildroot}%{_datadir}/modulefiles
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
mkdir -p %{buildroot}%{_datadir}/fish/vendor_conf.d
mkdir -p %{buildroot}%{_bindir}

# setup for alternatives
touch %{buildroot}%{_sysconfdir}/profile.d/modules.{csh,sh}
touch %{buildroot}%{_datadir}/fish/vendor_conf.d/modules.fish
touch %{buildroot}%{_bindir}/modulecmd
# remove modulecmd wrapper as it will be handled by alternatives
rm -f %{buildroot}%{_datadir}/Modules/bin/modulecmd

# major utilities go to regular bin dir
mv %{buildroot}%{_datadir}/Modules/bin/envml %{buildroot}%{_bindir}/

mv {doc/build/,}NEWS.txt
mv {doc/build/,}MIGRATING.txt
mv {doc/build/,}CONTRIBUTING.txt
mv {doc/build/,}INSTALL.txt
mv {doc/build/,}changes.txt

# install the rpm config file
install -Dpm 644 share/rpm/macros.%{name} %{buildroot}/%{macrosdir}/macros.%{name}

# install Emacs init file
install -Dpm 644 share/emacs/lisp/%{name}-init.el %{buildroot}/%{_emacs_sitestartdir}/%{name}-init.el


%check
make test QUICKTEST=1


%post
# Cleanup from pre-alternatives
[ ! -L %{_sysconfdir}/profile.d/modules.sh ] &&  rm -f %{_sysconfdir}/profile.d/modules.sh
[ ! -L %{_sysconfdir}/profile.d/modules.csh ] &&  rm -f %{_sysconfdir}/profile.d/modules.csh
[ ! -L %{_datadir}/fish/vendor_conf.d/modules.fish ] &&  rm -f %{_datadir}/fish/vendor_conf.d/modules.fish
[ ! -L %{_bindir}/modulecmd ] &&  rm -f %{_bindir}/modulecmd

# Migration from version 3.x to 4
if [ "$(readlink /etc/alternatives/modules.sh)" = '%{_datadir}/Modules/init/modules.sh' ]; then
  update-alternatives --remove modules.sh %{_datadir}/Modules/init/modules.sh
fi

update-alternatives \
  --install %{_sysconfdir}/profile.d/modules.sh modules.sh %{_datadir}/Modules/init/profile.sh 40 \
  --follower %{_sysconfdir}/profile.d/modules.csh modules.csh %{_datadir}/Modules/init/profile.csh \
  --follower %{_datadir}/fish/vendor_conf.d/modules.fish modules.fish %{_datadir}/Modules/init/fish \
  --follower %{_bindir}/modulecmd modulecmd %{_datadir}/Modules/libexec/modulecmd.tcl

%postun
if [ $1 -eq 0 ] ; then
  update-alternatives --remove modules.sh %{_datadir}/Modules/init/profile.sh
fi


%files
%license COPYING.GPLv2
%doc ChangeLog.gz README NEWS.txt MIGRATING.txt INSTALL.txt CONTRIBUTING.txt changes.txt
%{_sysconfdir}/modulefiles
%dir %{_datadir}/fish/vendor_conf.d
%ghost %{_sysconfdir}/profile.d/modules.csh
%ghost %{_sysconfdir}/profile.d/modules.sh
%ghost %{_datadir}/fish/vendor_conf.d/modules.fish
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
%dir %{bash_completions_dir}
%{bash_completions_dir}/module
%{bash_completions_dir}/ml
%dir %{zsh_completions_dir}
%{zsh_completions_dir}/_module
%dir %{fish_completions_dir}
%{fish_completions_dir}/module.fish
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/initrc
%config(noreplace) %{_sysconfdir}/%{name}/modulespath
%config(noreplace) %{_sysconfdir}/%{name}/siteconfig.tcl
%{_datadir}/Modules/modulefiles
%{_datadir}/modulefiles
%{_mandir}/man1/envml.1.gz
%{_mandir}/man1/ml.1.gz
%{_mandir}/man1/module.1.gz
%{_mandir}/man5/modulefile.5.gz
%{macrosdir}/macros.%{name}
%{vimfiles_root}/ftdetect/modulefile.vim
%{vimfiles_root}/ftplugin/modulefile.vim
%{vimfiles_root}/syntax/modulefile.vim
%dir %{_emacs_sitelispdir}/%{name}
%{_emacs_sitelispdir}/%{name}/*
%{_emacs_sitestartdir}/%{name}-init.el
%dir %{_datadir}/Modules/nagelfar
%{_datadir}/Modules/nagelfar/*


%changelog
* Thu Nov 27 2025 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.6.1-1
- Update to 5.6.1 (#2417160)
- Update-alternatives is now available from _bindir
- Update URL to https://envmodules.io
- Add missing command to byte compile Elisp file

* Thu Jul 31 2025 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.6.0-1
- Update to 5.6.0 (#2385838)
- Add envml(1) man page
- Use shell completion path macros
- Install Emacs addon files
- Use 'vimfiles_root' macro provided by vim-filesystem

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.5.0-3
- Rebuilt for Tcl 9.0 (#2337702)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.5.0-1
- Update to 5.5.0 (#2325175)
- Require util-linux-core to get logger command for logging capabilities

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.4.0-1
- Update to 5.4.0 (#2265106)
- Move modulefile man page to section 5

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.3.1-1
- Update to 5.3.1 (#2217986)
- Distribute ChangeLog as a zipped file to reduce installation size

* Sat May 27 2023 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.3.0-2
- Install module initialization script for fish as configuration snippet for
  this shell via alternatives (#2196379)

* Mon May 15 2023 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.3.0-1
- Update to 5.3.0 (#2203629)

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 5.2.0-3
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.2.0-1
- Update to 5.2.0 (#2140892)
- Recommends Nagelfar Tcl syntax linter
- Add Nagelfar linter addons

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.1.1-1
- Update to 5.1.1 (#2092100)
- Move libtclenvmodules in an environment-modules directory under libdir

* Sat Apr 30 2022 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.1.0-1
- Update to 5.1.0 (#2080577)
- Install shell completion scripts in system-wide shell-specific locations

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 16 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.0.1-1
- Update to 5.0.1 (#2014796)

* Sun Sep 12 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.0.0-1
- Update to 5.0.0
- Configuration guide example.txt is replaced by more up to date INSTALL.txt
  document

* Sun Jul 25 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 5.0.0-0.1.alpha
- Update to 5.0.0-alpha
- Remove createmodule.sh and createmodule.py utilities ('module sh-to-mod'
  should be used instead)
- Remove configure options that have been made default starting version 5.0
- Remove compat subpackage
- Run non-regression tests in quick mode

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 4.8.0-1
- Update to 4.8.0 (#1982175)

* Tue Apr  6 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 4.7.1-1
- Update to 4.7.1 (#1946442)

* Fri Feb 19 2021 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 4.7.0-1
- Update to 4.7.0 (#1930632)
- Align spec syntax with upstream spec file
- Add 'tcl' to the BuildRequires and remove 'man' from this list
- Fix names of 'procps-ng' and 'man-db' packages on Fedora
- Only install manpages through make install, other docs are handled by %%doc
- Remove alternatives mechanism for manpages

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 15 2020 Xavier Delaruelle <xavier.delaruelle@cea.fr> - 4.6.1-1
- Update to 4.6.1 (#1897820)

* Thu Sep 17 2020 Jan Synáček <jsynacek@redhat.com> - 4.6.0-1
- Update to 4.6.0 (#1879374)

* Wed Sep  2 2020 Jan Synáček <jsynacek@redhat.com> - 4.5.3-1
- Update to 4.5.3 (#1874145)
  + Big thanks to Xavier Delaruelle for a spec patch!

* Mon Aug  3 2020 Jan Synáček <jsynacek@redhat.com> - 4.5.2-1
- Update to 4.5.2 (#1842562)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr  8 2020 Jan Synáček <jsynacek@redhat.com> - 4.5.0-1
- Update to 4.5.0 (#1821883)
  + Big thanks to Xavier Delaruelle for a spec patch!

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
