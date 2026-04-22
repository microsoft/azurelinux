# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# build nano-default-editor by default only on fedora
%if 0%{?fedora}
%bcond_without default_editor
%else
%bcond_with default_editor
%endif

Summary:         A small text editor
Name:            nano
Version:         8.5
Release: 3%{?dist}
License:         GPL-3.0-or-later
URL:             https://www.nano-editor.org

Source0:         https://www.nano-editor.org/dist/latest/%{name}-%{version}.tar.xz
Source1:         https://www.nano-editor.org/dist/latest/%{name}-%{version}.tar.xz.asc
# gpg --keyserver keyserver.ubuntu.com --recv-key 168E6F4297BFD7A79AFD4496514BBE2EB8E1961F
# gpg --output bensberg.pgp --armor --export bensberg@telfort.nl
Source2:         bensberg.pgp

# Additional sources
Source3:         nanorc

# Shell snippets for default-editor setup
Source11:        nano-default-editor.sh
Source12:        nano-default-editor.csh
Source13:        nano-default-editor.fish

BuildRequires:   file-devel
BuildRequires:   gettext-devel
BuildRequires:   gcc
BuildRequires:   git
BuildRequires:   gnupg2
BuildRequires:   groff
BuildRequires:   make
BuildRequires:   ncurses-devel
BuildRequires:   sed
BuildRequires:   texinfo
Conflicts:       filesystem < 3

%description
GNU nano is a small and friendly text editor.

%if %{with default_editor}
%package default-editor
Summary:         Sets GNU nano as the default editor
Requires:        nano = %{version}-%{release}
# Ensure that only one package with this capability is installed
Provides:        system-default-editor
Conflicts:       system-default-editor
BuildArch:       noarch

%description default-editor
This package ensures the EDITOR shell variable
is set in common shells to GNU nano.

%package -n default-editor
Summary:         Metapackage for DNF group
Recommends:      nano-default-editor
Requires:        system-default-editor
BuildArch:       noarch

%description -n default-editor
The package acts as a placeholder in DNF group 'Standard', which will
install nano-default-editor on fresh installs and it will not block users
who don't have nano as a default editor during upgrade.
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git

%build
mkdir build
cd build
%global _configure ../configure
%configure
%make_build

# generate default /etc/nanorc
# - set hunspell as the default spell-checker
# - enable syntax highlighting by default (#1270712)
sed -E -e 's/^#.*set speller.*$/set speller "hunspell"/' \
       -e 's|^# (include "?/usr/share/nano/\*.nanorc"?)|\1|' \
    %{SOURCE3} doc/sample.nanorc > ./nanorc

%install
cd build
%make_install
rm -f %{buildroot}%{_infodir}/dir

# remove installed HTML documentation
rm -f %{buildroot}%{_docdir}/nano/{nano,nano.1,nanorc.5,rnano.1}.html

# install default /etc/nanorc
mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 ./nanorc %{buildroot}%{_sysconfdir}/nanorc

# enable all extra syntax highlighting files by default
mv %{buildroot}%{_datadir}/nano/extra/* %{buildroot}%{_datadir}/nano
rm -rf %{buildroot}%{_datadir}/nano/extra

%find_lang %{name}

%if %{with default_editor}
# install nano-default-editor snippets
install -Dpm 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/profile.d/%{basename:%{S:11}}
install -Dpm 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/profile.d/%{basename:%{S:12}}
install -Dpm 0644 %{SOURCE13} %{buildroot}%{_datadir}/fish/vendor_conf.d/%{basename:%{S:13}}
%endif

%files -f build/%{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%doc build/doc/sample.nanorc
%doc doc/{faq,nano}.html
%{_bindir}/{,r}nano
%config(noreplace) %{_sysconfdir}/nanorc
%{_mandir}/man1/{,r}nano.1*
%{_mandir}/man5/nanorc.5*
%{_infodir}/nano.info*
%{_datadir}/nano

%if %{with default_editor}
%files default-editor
%dir %{_sysconfdir}/profile.d
%config(noreplace) %{_sysconfdir}/profile.d/nano-default-editor.*
%dir %{_datadir}/fish/vendor_conf.d
%{_datadir}/fish/vendor_conf.d/nano-default-editor.fish

%files -n default-editor
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Lukáš Zaoral <lzaoral@redhat.com> - 8.5-1
- rebase to latest upstream release (rhbz#2372436)

* Mon Apr 07 2025 Lukáš Zaoral <lzaoral@redhat.com> - 8.4-1
- rebase to latest upstream release (rhbz#2357699)

* Thu Mar 20 2025 Lukáš Zaoral <lzaoral@redhat.com> - 8.3-3
- fix nano syntax highlighting in default nanorc (rhbz#2353508)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Lukáš Zaoral <lzaoral@redhat.com> - 8.3-1
- rebase to latest upstream version (rhbz#2333643)

* Thu Sep 05 2024 Lukáš Zaoral <lzaoral@redhat.com> - 8.2-1
- rebase to latest upstream release (rhbz#2310179)

* Thu Jul 18 2024 Lukáš Zaoral <lzaoral@redhat.com> - 8.1-1
- rebase to latest upstream release (rhbz#2297610)

* Thu May 02 2024 Lukáš Zaoral <lzaoral@redhat.com> - 8.0-1
- rebase to latest upstream version (rhbz#2278126)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Lukáš Zaoral <lzaoral@redhat.com> - 7.2-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Lukáš Zaoral <lzaoral@redhat.com> - 7.2-1
- Update to 7.2 (rhbz#2161916)
- Do not use %%{_bindir}/* and %%{_mandir}/* as suggested by the packaging
  guidelines.

* Wed Dec 14 2022 Lukáš Zaoral <lzaoral@redhat.com> - 7.1-1
- new upstream release (#2153268)

* Tue Nov 15 2022 Lukáš Zaoral <lzaoral@redhat.com> - 7.0-1
- new upstream release (#2142885)
- update GPG signature key

* Tue Aug 02 2022 Lukáš Zaoral <lzaoral@redhat.com> - 6.4-1
- new upstream release (#2113894)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 28 2022 Kamil Dudka <kdudka@redhat.com> - 6.3-1
- new upstream release

* Sat Feb 19 2022 Kamil Dudka <kdudka@redhat.com> - 6.2-1
- new upstream release

* Wed Feb 09 2022 Kamil Dudka <kdudka@redhat.com> - 6.1-1
- new upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Kamil Dudka <kdudka@redhat.com> - 6.0-1
- new upstream release

* Wed Oct 06 2021 Kamil Dudka <kdudka@redhat.com> - 5.9-1
- new upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Kamil Dudka <kdudka@redhat.com> - 5.8-3
- fix infinite recursion when handling an error (#1976410)

* Wed Jun 16 2021 Zdenek Dohnal <zdohnal@redhat.com> - 5.8-2
- introduce 'default-editor' subpackage to support smooth non-nano upgrades (#1955884)

* Tue Jun 15 2021 Kamil Dudka <kdudka@redhat.com> - 5.8-1
- new upstream release

* Tue May 25 2021 Florian Weimer <fweimer@redhat.com> - 5.7-3
- Rebuild with new binutils to fix ppc64le corruption (#1960730)

* Wed May 05 2021 Kamil Dudka <kdudka@redhat.com> - 5.7-2
- build nano-default-editor by default only on fedora

* Thu Apr 29 2021 Kamil Dudka <kdudka@redhat.com> - 5.7-1
- new upstream release

* Wed Mar 03 2021 Kamil Dudka <kdudka@redhat.com> - 5.6.1-1
- new upstream release

* Wed Feb 24 2021 Kamil Dudka <kdudka@redhat.com> - 5.6-1
- new upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Kamil Dudka <kdudka@redhat.com> - 5.5-1
- new upstream release

* Wed Dec 02 2020 Kamil Dudka <kdudka@redhat.com> - 5.4-1
- new upstream release

* Thu Oct 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 5.3-4
- fix nano-default-editor.fish - don't give EDITOR an universal scope

* Mon Oct 12 2020 Neal Gompa <ngompa13@gmail.com> - 5.3-3
- Ensure default-editor subpackage is easily swappable

* Thu Oct 08 2020 Neal Gompa <ngompa13@gmail.com> - 5.3-2
- Enable all extra definitions for syntax highlighting (#1886561)

* Wed Oct 07 2020 Kamil Dudka <kdudka@redhat.com> - 5.3-1
- new upstream release

* Mon Aug 24 2020 Kamil Dudka <kdudka@redhat.com> - 5.2-1
- new upstream release

* Sat Aug 15 2020 Kamil Dudka <kdudka@redhat.com> - 5.1-1
- new upstream release

* Thu Jul 30 2020 Kamil Dudka <kdudka@redhat.com> - 5.0-1
- new upstream release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Tom Stellard <tstellar@redhat.com> - 4.9.3-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Jul 16 2020 Neal Gompa <ngompa13@gmail.com> - 4.9.3-2
- Add default-editor subpackage (#1854444)

* Mon May 25 2020 Kamil Dudka <kdudka@redhat.com> - 4.9.3-1
- new upstream release

* Tue Apr 07 2020 Kamil Dudka <kdudka@redhat.com> - 4.9.2-1
- new upstream release

* Tue Mar 31 2020 Kamil Dudka <kdudka@redhat.com> - 4.9.1-1
- new upstream release

* Tue Mar 24 2020 Kamil Dudka <kdudka@redhat.com> - 4.9-1
- new upstream release

* Fri Feb 07 2020 Kamil Dudka <kdudka@redhat.com> - 4.8-1
- new upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 2019 Kamil Dudka <kdudka@redhat.com> - 4.7-1
- new upstream release

* Fri Nov 29 2019 Kamil Dudka <kdudka@redhat.com> - 4.6-1
- new upstream release

* Fri Oct 04 2019 Kamil Dudka <kdudka@redhat.com> - 4.5-1
- new upstream release

* Mon Aug 26 2019 Kamil Dudka <kdudka@redhat.com> - 4.4-1
- new upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Kamil Dudka <kdudka@redhat.com> - 4.3-1
- new upstream release

* Tue May 28 2019 Kamil Dudka <kdudka@redhat.com> - 4.2-2
- fix possible crash while opening help

* Wed Apr 24 2019 Kamil Dudka <kdudka@redhat.com> - 4.2-1
- new upstream release

* Mon Apr 15 2019 Kamil Dudka <kdudka@redhat.com> - 4.1-1
- new upstream release

* Tue Apr 02 2019 Kamil Dudka <kdudka@redhat.com> - 4.0-2
- make sure that variables on stack are initialized

* Mon Mar 25 2019 Kamil Dudka <kdudka@redhat.com> - 4.0-1
- new upstream release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 12 2018 Kamil Dudka <kdudka@redhat.com> - 3.2-1
- new upstream release

* Wed Sep 19 2018 Kamil Dudka <kdudka@redhat.com> - 3.1-1
- new upstream release

* Fri Sep 14 2018 Kamil Dudka <kdudka@redhat.com> - 3.0-2
- when Ctrl+Shift+Delete has no key code, do not fall back to KEY_BACKSPACE

* Mon Sep 10 2018 Kamil Dudka <kdudka@redhat.com> - 3.0-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.8-1
- new upstream release

* Tue May 15 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.7-1
- new upstream release

* Fri Apr 27 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.6-1
- new upstream release

* Wed Apr 25 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.5-2
- fix crash when using word completion

* Thu Mar 29 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.5-1
- new upstream release

* Wed Mar 21 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.4-2
- fix crash of 'nano --restrict' when <Insert> is pressed (#1558532)

* Thu Mar 08 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.4-1
- new upstream release

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.3-3
- add explicit BR for the gcc compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.3-1
- new upstream release

* Tue Jan 02 2018 Kamil Dudka <kdudka@redhat.com> - 2.9.2-1
- new upstream release

* Tue Nov 28 2017 Kamil Dudka <kdudka@redhat.com> - 2.9.1-1
- new upstream release

* Mon Nov 20 2017 Kamil Dudka <kdudka@redhat.com> - 2.9.0-1
- new upstream release

* Mon Aug 28 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.7-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.6-1
- new upstream release

* Sun Jun 25 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.5-1
- new upstream release

* Mon May 22 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.4-1
- new upstream release

* Thu May 18 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.3-1
- new upstream release

* Thu May 04 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.2-1
- new upstream release

* Wed Apr 12 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.1-1
- new upstream release

* Tue Apr 04 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.0-2
- use upstream patch to prevent symlink attack while creating a backup

* Fri Mar 31 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.0-1
- new upstream release

* Thu Feb 23 2017 Kamil Dudka <kdudka@redhat.com> - 2.7.5-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Kamil Dudka <kdudka@redhat.com> - 2.7.4-1
- new upstream release (removes French man pages)

* Fri Dec 30 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.3-1
- new upstream release

* Mon Dec 12 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.2-1
- new upstream release

* Mon Oct 31 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.1-1
- new upstream release

* Thu Sep 01 2016 Kamil Dudka <kdudka@redhat.com> - 2.7.0-1
- new upstream release

* Thu Aug 11 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.3-1
- use %%autosetup in %%prep
- build out of source tree
- do not recode man pages, they are UTF-8 encoded since v2.3.6
- new upstream release

* Thu Jul 28 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.2-1
- drop BuildRoot and Group tags, which are no longer necessary
- new upstream release

* Mon Jun 27 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.1-1
- new upstream release

* Mon Jun 20 2016 Kamil Dudka <kdudka@redhat.com> - 2.6.0-1
- new upstream release

* Fri Feb 26 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.3-1
- new upstream release

* Fri Feb 12 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.2-2
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Kamil Dudka <kdudka@redhat.com> - 2.5.1-1
- new upstream release

* Sun Dec 06 2015 Kamil Dudka <kdudka@redhat.com> - 2.5.0-1
- new upstream release

* Wed Nov 18 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.3-1
- new upstream release

* Mon Oct 12 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.2-2
- enable syntax highlighting by default (#1270712)
- remove installed HTML documentation (to prevent a build failure in rawhide)

* Tue Jul 07 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.2-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.1-1
- new upstream release

* Mon Mar 23 2015 Kamil Dudka <kdudka@redhat.com> - 2.4.0-1
- new upstream release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.3.6-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 27 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-6
- additional fixes to the file locking feature of nano (#1186384)

* Mon Jan 26 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-5
- fix the file locking feature of nano (#1183320)

* Mon Jan 05 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-4
- drop BR for autoconf, which is no longer needed

* Mon Jan 05 2015 Kamil Dudka <kdudka@redhat.com> - 2.3.6-3
- do not use closed file descriptor when setting backup's timestamp (#1177155)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.6-1
- new upstream release

* Wed Jul 16 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.5-1
- new upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.4-1
- new upstream release

* Thu May 29 2014 Kamil Dudka <kdudka@redhat.com> - 2.3.3-1
- new upstream release

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-4
- document the --poslog (-P) option in nano.1 man page

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-2
- add "BuildRequires: file-devel" to build libmagic support (#927994)

* Tue Mar 26 2013 Kamil Dudka <kdudka@redhat.com> - 2.3.2-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 2.3.1-5
- fix specfile issues reported by the fedora-review script

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.3.1-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.1-1
- new upstream release

* Thu Mar 03 2011 Kamil Dudka <kdudka@redhat.com> - 2.3.0-1
- new upstream release (#680736)
- use hunspell as default spell-checker (#681000)
- fix for http://thread.gmane.org/gmane.editors.nano.devel/2911

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 28 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-2
- fix bugs introduced by patches added in 2.2.6-1 (#657875)

* Mon Nov 22 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.6-1
- new upstream release (#655978)
- increase code robustness (patches related to CVE-2010-1160, CVE-2010-1161)

* Sat Aug 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.5-1
- new upstream release (#621857)

* Thu Apr 15 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.4-1
- new upstream release
- CVE-2010-1160, CVE-2010-1161 (#582739)

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.3-1
- new upstream release

* Fri Jan 29 2010 Kamil Dudka <kdudka@redhat.com> - 2.2.2-1
- new upstream release

* Sun Dec 27 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.1-1
- new upstream release

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> - 2.2.0-1
- new upstream release

* Wed Nov 25 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-7
- sanitize specfile according to Fedora Packaging Guidelines 

* Thu Oct 15 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-6
- use nanorc.sample as base of /etc/nanorc

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-5
- fix build failure of the last build

* Tue Oct 13 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-4
- ship a system-wide configuration file along with the nano package
- disable line wrapping by default (#528359)

* Mon Sep 21 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-3
- suppress warnings for __attribute__((warn_unused_result)) (#523951)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-2
- install binaries to /bin (#168340)

* Fri Sep 18 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.9-1
- new upstream release
- dropped patch no longer needed (possible change in behavior though negligible)
- fixed broken HTML doc in FR locales (#523951)

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> - 2.0.6-8
- do process install-info only without --excludedocs(#515943)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.0.6-5
- Mark localized man pages with %%lang, fix French nanorc(5) (#322271).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.6-4
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.0.6-3
- Pass rnano.1 through iconv to silence the final rpmlint complaint
  and finish up the merge review.

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 2.0.6-2
- Update licence
- Fix open(O_CREAT) calls without mode

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 2.0.6-1
- update to 2.0.6

* Mon Feb 05 2007 Florian La Roche <laroche@redhat.com> - 2.0.3-1
- update to 2.0.3
- update spec file syntax, fix scripts rh#220527

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.12-1.1
- rebuild

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.12-1
- Update to 1.3.12

* Tue May 16 2006 David Woodhouse <dwmw2@redhat.com> - 1.3.11-1
- Update to 1.3.11
- BuildRequires: groff (#191946)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.8-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 5 2005 David Woodhouse <dwmw2@redhat.com> 1.3.8-1
- 1.3.8

* Wed Mar 2 2005 David Woodhouse <dwmw2@redhat.com> 1.3.5-0.20050302
- Update to post-1.3.5 CVS tree to get UTF-8 support.

* Wed Aug 04 2004 David Woodhouse <dwmw2@redhat.com> 1.2.4-1
- 1.2.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.2.3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 11 2003 Bill Nottingham <notting@redhat.com> 1.2.1-4
- build in different environment

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Bill Nottingham <notting@redhat.com> 1.2.1-2
- description tweaks

* Mon May  5 2003 Bill Nottingham <notting@redhat.com> 1.2.1-1
- initial build, tweak upstream spec file
