Vendor:         Microsoft Corporation
Distribution:   Mariner
%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global macros_dir %{_rpmconfigdir}/macros.d
%else
%global macros_dir %{_sysconfdir}/rpm
%endif

Name:           ghc-rpm-macros
Version:        2.4.4
Release:        2%{?dist}
Summary:        RPM macros for building Haskell packages for GHC

License:        GPLv3+
# Currently source is only in pkg git but tarballs could be made if it helps
URL:            https://src.fedoraproject.org/rpms/ghc-rpm-macros/
Source0:        macros.ghc
Source1:        COPYING
Source2:        AUTHORS
Source3:        ghc-deps.sh
Source4:        cabal-tweak-dep-ver
Source5:        cabal-tweak-flag
Source6:        macros.ghc-extra
Source7:        ghc.attr
Source8:        ghc-pkg-wrapper
Source9:        macros.ghc-os
Source10:       Setup.hs
Source11:       cabal-tweak-drop-dep
Source12:       cabal-tweak-remove-upperbound
Requires:       redhat-rpm-config
# ghc_version needs ghc-compiler or ghcX.Y-compiler-default
Requires:       chrpath
BuildArch:      noarch

%description
A set of macros for building GHC packages following the Haskell Guidelines
of the Fedora Haskell SIG.


%package extra
Summary:        Extra RPM macros for building Haskell library subpackages
Requires:       %{name} = %{version}-%{release}

%description extra
Extra macros used for subpackaging of Haskell libraries,
for example in ghc and haskell-platform.


%if 0%{?fedora} < 37
%package -n ghc-filesystem
Summary:        Shared directories for Haskell documentation

%description -n ghc-filesystem
This package provides some common directories used for
Haskell libraries documentation.
%endif


# ideally packages should be obsoleted by some relevant package
# this is a last resort when there is no such appropriate package
%package -n ghc-obsoletes
Summary:        Dummy package to obsolete deprecated Haskell packages
%if 0%{?fedora} >= 29
Obsoletes:      ghc-content-store < 0.2.1-3, ghc-content-store-devel < 0.2.1-3
Obsoletes:      ghc-bdcs < 0.6.1-3, ghc-bdcs-devel < 0.6.1-3
Obsoletes:      ghc-bdcs-api < 0.1.3-3, ghc-bdcs-api-devel < 0.1.3-3
%endif
%if 0%{?fedora} >= 30
# ghc
Obsoletes:      ghc-hoopl < 3.10.2.2-74, ghc-hoopl-devel < 3.10.2.2-74
# language-ecmascript
Obsoletes:      ghc-tagshare < 0.0-10, ghc-tagshare-devel < 0.0-10
Obsoletes:      ghc-testing-feat < 0.4.0.3-10, ghc-testing-feat-devel < 0.4.0.3-10
# enumerator
Obsoletes:      ghc-enumerator < 0.4.20-12, ghc-enumerator-devel < 0.4.20-12
Obsoletes:      ghc-attoparsec-enumerator < 0.3.4-10, ghc-attoparsec-enumerator-devel < 0.3.4-10
Obsoletes:      ghc-blaze-builder-enumerator < 0.2.1.0-8, ghc-blaze-builder-enumerator-devel < 0.2.1.0-8
Obsoletes:      ghc-zlib-enum < 0.2.3.1-12, ghc-zlib-enum-devel < 0.2.3.1-12
# Agda
Obsoletes:      ghc-monadplus < 1.4.2-17, ghc-monadplus-devel < 1.4.2-17
# conduit-combinators
Obsoletes:      ghc-conduit-combinators < 1.3.1
%endif
%if 0%{?fedora} >= 31
# base package obsoleted above in f30
Obsoletes:      ghc-conduit-combinators-devel < 1.3.1
%endif
%if 0%{?fedora} >= 32
Obsoletes:      ghc-derive < 2.6.5-5, ghc-derive-devel < 2.6.5-5, ghc-derive-prof < 2.6.5-5
Obsoletes:      ghc-here < 1.2.13-17, ghc-here-devel < 1.2.13-17, ghc-here-prof < 1.2.13-17
%endif
%if 0%{?fedora} >= 33
Obsoletes:      ghc-easytest < 0.2.1-4, ghc-easytest-devel < 0.2.1-4, ghc-easytest-prof < 0.2.1-4,
Obsoletes:      ghc-EdisonAPI < 1.3.1-23, ghc-EdisonAPI-devel < 1.3.1-23, ghc-EdisonAPI-prof < 1.3.1-23
Obsoletes:      ghc-EdisonCore < 1.3.2.1-23, ghc-EdisonCore-devel < 1.3.2.1-23, ghc-EdisonCore-prof < 1.3.2.1-23
Obsoletes:      ghc-gtksourceview2 < 0.13.3.1-14, ghc-gtksourceview2-devel < 0.13.3.1-14, ghc-gtksourceview2-prof < 0.13.3.1-14
%endif
Obsoletes:      ghc-iwlib < 0.1.0-16, ghc-iwlib-devel < 0.1.0-16, ghc-iwlib-prof < 0.1.0-16
%if 0%{?fedora} >= 35
Obsoletes:      pandoc-citeproc < 0.18, ghc-pandoc-citeproc < 0.18, ghc-pandoc-citeproc-devel < 0.18, ghc-pandoc-citeproc-doc < 0.18, ghc-pandoc-citeproc-prof < 0.18, pandoc-citeproc-common < 0.18
Obsoletes:      ghc-base-noprelude < 4.13.0.1, ghc-base-noprelude-devel < 4.13.0.1, ghc-base-noprelude-doc < 4.13.0.1, ghc-base-noprelude-prof < 4.13.0.1
Obsoletes:      ghc-HsYAML-aeson < 0.2.0.1, ghc-HsYAML-aeson-devel < 0.2.0.1, ghc-HsYAML-aeson-doc < 0.2.0.1, ghc-HsYAML-aeson-prof < 0.2.0.1
Obsoletes:      ghc-chalmers-lava2000 < 1.6.2, ghc-chalmers-lava2000-devel < 1.6.2, ghc-chalmers-lava2000-doc < 1.6.2, ghc-chalmers-lava2000-prof < 1.6.2
Obsoletes:      ghc-codec-rpm < 0.2.3, ghc-codec-rpm-devel < 0.2.3, ghc-codec-rpm-doc < 0.2.3, ghc-codec-rpm-prof < 0.2.3
Obsoletes:      ghc-cpio-conduit < 0.7.1, ghc-cpio-conduit-devel < 0.7.1, ghc-cpio-conduit-doc < 0.7.1, ghc-cpio-conduit-prof < 0.7.1
Obsoletes:      ghc-failure < 0.2.0.4, ghc-failure-devel < 0.2.0.4, ghc-failure-doc < 0.2.0.4, ghc-failure-prof < 0.2.0.4
Obsoletes:      ghc-attempt < 0.4.0.2, ghc-attempt-devel < 0.4.0.2, ghc-attempt-doc < 0.4.0.2, ghc-attempt-prof < 0.4.0.2
%endif
%if 0%{?fedora} >= 36
Obsoletes:      ghc-regex-applicative-text < 0.1.0.1-16, ghc-regex-applicative-text-devel < 0.1.0.1-16, ghc-regex-applicative-text-doc < 0.1.0.1-16, ghc-regex-applicative-text-prof < 0.1.0.1-16
%endif

%description -n ghc-obsoletes
Meta package for obsoleting deprecated Haskell packages.

This package can safely be removed.


%prep
%setup -c -T
cp %{SOURCE1} %{SOURCE2} .


%build
echo no build stage


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}%{macros_dir}/macros.ghc
install -p -D -m 0644 %{SOURCE6} %{buildroot}%{macros_dir}/macros.ghc-extra
install -p -D -m 0644 %{SOURCE9} %{buildroot}%{macros_dir}/macros.ghc-os

install -p -D -m 0755 %{SOURCE3} %{buildroot}%{_prefix}/lib/rpm/ghc-deps.sh

%if 0%{?fedora} || 0%{?rhel} >= 7
install -p -D -m 0644 %{SOURCE7} %{buildroot}%{_prefix}/lib/rpm/fileattrs/ghc.attr
%endif

install -p -D -m 0644 %{SOURCE10} %{buildroot}%{_datadir}/%{name}/Setup.hs

install -p -D -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/cabal-tweak-dep-ver
install -p -D -m 0755 %{SOURCE5} %{buildroot}%{_bindir}/cabal-tweak-flag
install -p -D -m 0755 %{SOURCE11} %{buildroot}%{_bindir}/cabal-tweak-drop-dep
install -p -D -m 0755 %{SOURCE12} %{buildroot}%{_bindir}/cabal-tweak-remove-upperbound
install -p -D -m 0755 %{SOURCE8} %{buildroot}%{_prefix}/lib/rpm/ghc-pkg-wrapper

%if 0%{?fedora} < 37
mkdir -p %{buildroot}%{_docdir}/ghc/html/libraries
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
cat >> %{buildroot}%{_prefix}/lib/rpm/ghc-deps.sh <<EOF

echo \$files | tr [:blank:] '\n' | %{_rpmconfigdir}/rpmdeps --requires
EOF
%endif


%files
%license COPYING
%doc AUTHORS
%{macros_dir}/macros.ghc
%{macros_dir}/macros.ghc-os
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_prefix}/lib/rpm/fileattrs/ghc.attr
%endif
%{_prefix}/lib/rpm/ghc-deps.sh
%{_prefix}/lib/rpm/ghc-pkg-wrapper
%{_bindir}/cabal-tweak-dep-ver
%{_bindir}/cabal-tweak-drop-dep
%{_bindir}/cabal-tweak-flag
%{_bindir}/cabal-tweak-remove-upperbound
%{_datadir}/%{name}/Setup.hs


%files extra
%{macros_dir}/macros.ghc-extra


%if 0%{?fedora} < 37
%files -n ghc-filesystem
%dir %{_docdir}/ghc
# %%{ghc_html_dir}
%dir %{_docdir}/ghc/html
# %%{ghc_html_libraries_dir}
%dir %{_docdir}/ghc/html/libraries
%endif


%if 0%{?fedora} >= 29
%files -n ghc-obsoletes
%endif


%changelog
* Sat Aug  6 2022 Jens Petersen <petersen@redhat.com> - 2.4.4-2
- F36 obsoletes regex-applicative-text

* Tue Jul 26 2022 Jens Petersen <petersen@redhat.com> - 2.4.4-1
- ghc_gen_filelists: check pkg licensedir exists
- in 9.4.1 Hadrian html docdirs are versioned again (breaks older Hadrian)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Jens Petersen <petersen@redhat.com> - 2.4.3-1
- in F37 ghc-filesystem is now a subpackage of ghc

* Tue Jul 19 2022 Jens Petersen <petersen@redhat.com> - 2.4.2-1
- ghc_bin_build,ghc_lib_build: define ghc_debuginfo to really enable debuginfo

* Sun Jul 17 2022 Jens Petersen <petersen@redhat.com> - 2.4.1-1
- ghc_bin_build,ghc_lib_build: use ghc_debuginfo to enable debuginfo

* Fri Jun 10 2022 Jens Petersen <petersen@redhat.com> - 2.4.0-1
- change ghc-deps.sh, splitting buildroot path from ghclibdir
  so that the ghc version can be used more precisely

* Wed Jun  8 2022 Jens Petersen <petersen@redhat.com> - 2.3.16-1
- define ghc_prefix (used for ghcX.Y packaging)
- add _ghc_doc_dir

* Wed Apr 27 2022 Jens Petersen <petersen@redhat.com> - 2.3.15-2
- drop ghc-compiler requires to allow using ghcX.Y-compiler-default

* Wed Apr 27 2022 Tim Landscheidt <tim@tim-landscheidt.de>
- Update license from https://www.gnu.org/licenses/
- Use https for subpackage URLs

* Thu Mar 10 2022 Jens Petersen <petersen@redhat.com> - 2.3.15-1
- ghc_set_gcc_flags: disable brp-strip-lto to avoid strip timestamp warnings

* Sat Feb 12 2022 Jens Petersen <petersen@redhat.com> - 2.3.14-1
- ghc_set_gcc_flags: also sed CFLAGS when preset in F36
  because of https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck

* Tue Feb  8 2022 Jens Petersen <petersen@redhat.com> - 2.3.13-1
- ghc_set_gcc_flags: disable _lto_cflags for all archs
  to address missing symbol linking errors across packages
  (particularly those using FFI)

* Fri Jan 21 2022 Jens Petersen <petersen@redhat.com> - 2.3.12-1
- disable package notes which broke all Haskell package builds (#2043092)
  https://fedoraproject.org/wiki/Changes/Package_information_on_ELF_objects

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan  5 2022 Jens Petersen <petersen@redhat.com> - 2.3.11-1
- ghc-deps.sh: fix the rts deps erasure cleanly

* Wed Dec 29 2021 Jens Petersen <petersen@redhat.com> - 2.3.10-1
- ghc_html_dir: use ghc_name for ghcX.Y docs

* Mon Dec 20 2021 Jens Petersen <petersen@redhat.com> - 2.3.9-1
- ghc-deps.sh: only exclude unversioned rts.conf

* Mon Dec 20 2021 Jens Petersen <petersen@redhat.com> - 2.3.8-1
- _arch fits Cabal better for ghclibplatform

* Mon Dec 20 2021 Jens Petersen <petersen@redhat.com> - 2.3.7-1
- ghclibplatform: Cabal uses i386 for i686

* Mon Dec 20 2021 Jens Petersen <petersen@redhat.com> - 2.3.6-1
- fix missing Hadrian ghc dependency generation

* Sun Dec 19 2021 Jens Petersen <petersen@redhat.com> - 2.3.5-1
- Hadrian haddock dirs are not versioned

* Sun Dec 19 2021 Jens Petersen <petersen@redhat.com> - 2.3.4-1
- move Cabal_arch into ghclibplatform macro

* Sun Dec 19 2021 Jens Petersen <petersen@redhat.com> - 2.3.3-1
- fixup ghc_arch renaming it to Cabal_arch

* Sat Dec 18 2021 Jens Petersen <petersen@redhat.com> - 2.3.2-1
- define ghcliblib and ghclibplatform globally
- fix ghc-deps.sh dependency generation for Hadrian
- Cabal uses ppc64 in paths for ppc64le

* Fri Dec 17 2021 Jens Petersen <petersen@redhat.com> - 2.3.1-1
- ghc_gen_filelists: support ghc Hadrian install

* Wed Dec  8 2021 Jens Petersen <petersen@redhat.com> - 2.3.0-1
- support fileattrs dependency generation for ghc9.2
- drop dependency generation for rhel6

* Thu Sep  9 2021 Jens Petersen <petersen@redhat.com> - 2.2.4-1
- cabal_configure: add -fhide-source-paths to ghc-options
  (works for ghc-8.2 and above)

* Mon Aug 23 2021 Jens Petersen <petersen@redhat.com> - 2.2.3-6
- F35 obsoletes for attempt

* Mon Aug 23 2021 Jens Petersen <petersen@redhat.com> - 2.2.3-5
- add F35 obsoletes for base-noprelude and failure

* Tue Aug 17 2021 Jens Petersen <petersen@redhat.com> - 2.2.3-4
- F35 obsoletes for pandoc-citeproc, HsYAML-aeson, chalmers-lava2000,
  cpio-conduit, and codec-rpm

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Jens Petersen <petersen@redhat.com> - 2.2.3-2
- drop obsoletes for haskell-platform GL graphics libraries
  which have been packaged and cabal-plan

* Sat Jul 10 2021 Jens Petersen <petersen@redhat.com> - 2.2.3-1
- fix ghc_fix_doc_perms only to touch files not dirs

* Thu Jun 17 2021 Jens Petersen <petersen@redhat.com> - 2.2.2-2
- haddock has not used hscolour for a long time

* Tue Jun  8 2021 Jens Petersen <petersen@redhat.com> - 2.2.2-1
- restore ghc_fix_rpath for now for backward compatibility
  and drop it from ghc_libs_install

* Tue Jun  8 2021 Jens Petersen <petersen@redhat.com> - 2.2.1-1
- ghc-rpm-macros needs to require chrpath now instead of ghc-rpm-macros-extra

* Mon Jun  7 2021 Jens Petersen <petersen@redhat.com> - 2.2.0-1
- ghc_delete_rpaths macro replaces ghc_fix_rpath(), needed for
  https://fedoraproject.org/wiki/Changes/Broken_RPATH_will_fail_rpmbuild

* Wed Mar 24 2021 Jens Petersen <petersen@redhat.com> - 2.1.0-1
- add ghc-filesystem subpackage to own /usr/share/doc/ghc/{,html/{,libraries/}}
  (#1926757)
- drop obsoletes from before f29
- update url
- fix ghc_fix_doc_perms grep regexp quoting

* Sat Jan 30 2021 Jens Petersen <petersen@redhat.com> - 2.0.15-1
- add ghc_fix_doc_perms and use it in ghc_bin_build and ghc_lib_build
- ghc_lib_subpackage: define ghc_subpackages_list

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 29 2020 Jens Petersen <petersen@redhat.com> - 2.0.14-1
- ghc-deps.sh: be careful when filtering out rts (#1873687)

* Wed Aug 26 2020 Jens Petersen <petersen@redhat.com> - 2.0.13-2
- obsolete ghc-iwlib (xmobar)

* Tue Aug  4 2020 Jens Petersen <petersen@redhat.com> - 2.0.13-1
- disable LTO on (unregisterised) s390x (#1863601)
  to prevent linker warning flood for prof libraries

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Jens Petersen <petersen@redhat.com> - 2.0.12-2
- obsoletes for ghc-EdisonAPI, ghc-EdisonCore, ghc-easytest

* Tue Jul 21 2020 Jens Petersen <petersen@redhat.com> - 2.0.12-1
- make doc packages noarch for subpackaging
- obsoletes for ghc-gtksourceview2

* Wed Jun 24 2020 Jens Petersen <petersen@redhat.com> - 2.0.11-1
- handle meta subpackages:
  - ghc_lib_subpackage -m
  - only add dynlib to file-list if it exists

* Thu Jun 18 2020 Jens Petersen <petersen@redhat.com> - 2.0.10-1
- cabal-tweak script now output errors to stderr

* Thu Jun  4 2020 Jens Petersen <petersen@redhat.com> - 2.0.9-1
- doc subpackages should own /usr/share/doc/ghc/, /usr/share/doc/ghc/html/,
  and /usr/share/doc/ghc/html/libraries/ (#1795526)

* Sun May 10 2020 Jens Petersen <petersen@redhat.com> - 2.0.8-1
- ghc-deps.sh: ignore internal libraries (#1822444)

* Fri May  8 2020 Jens Petersen <petersen@redhat.com> - 2.0.7-2
- obsolete ghc-here (dropped from hledger)

* Mon Apr 27 2020 Jens Petersen <petersen@redhat.com> - 2.0.7-1
- use -package Cabal to build Setup

* Tue Mar  3 2020 Jens Petersen <petersen@redhat.com> - 2.0.6-2
- obsolete ghc-cabal-helper, ghc-cabal-plan, ghc-derive
- unobsolete ghc-hgettext

* Mon Feb 10 2020 Jens Petersen <petersen@redhat.com> - 2.0.6-1
- ghc-deps.sh: fix prof deps for subpackages

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Jens Petersen <petersen@redhat.com> - 2.0.5-4
- obsolete ghc-hgettext

* Fri Sep 27 2019 Jens Petersen <petersen@redhat.com> - 2.0.5-3
- ghc_devel_prof macro not available early enough in koji

* Fri Sep 27 2019 Jens Petersen <petersen@redhat.com> - 2.0.5-2
- define ghc_devel_prof

* Tue Aug 27 2019 Jens Petersen <petersen@redhat.com> - 2.0.5-1
- ghc-deps.sh: fix generation of prof deps

* Tue Aug 13 2019 Jens Petersen <petersen@redhat.com> - 2.0.4-1
- add cabal-tweak-remove-upperbound script

* Sat Aug 10 2019 Jens Petersen <petersen@redhat.com> - 2.0.3-1
- only depend on ghc-prof(pkgid) if libHSpkgid_p.a exists

* Tue Aug  6 2019 Jens Petersen <petersen@redhat.com> - 2.0.2-1
- check if doc haddock dir exists

* Mon Aug  5 2019 Jens Petersen <petersen@redhat.com> - 2.0.1-1
- ghc_lib_subpackage: provide static with isa suffix

* Wed Jul 31 2019 Jens Petersen <petersen@redhat.com> - 2.0-1
- bring back doc and prof subpackages
- ghc_lib_subpackage: provide static

* Fri Jul 26 2019 Jens Petersen <petersen@redhat.com> - 1.10.0-1
- drop devel subpackage scriplets (replaced by ghc-compiler triggers)
- remove deprecated ghc_fix_dynamic_rpath

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 18 2019 Jens Petersen <petersen@redhat.com> - 1.9.9-3
- ghc-conduit-combinators base package obsoleted in f30

* Fri May 10 2019 Jens Petersen <petersen@redhat.com> - 1.9.9-2
- obsoletes for f30 deprecated packages
  (including haskell-platform subpackaged libraries and enumerator)

* Mon Apr 15 2019 Jens Petersen <petersen@redhat.com> - 1.9.9-1
- cabal_configure: re-enable stripping by Cabal
  (remove --disable-executable-stripping --disable-library-stripping)
- obsolete hoopl

* Tue Apr  9 2019 Jens Petersen <petersen@redhat.com> - 1.9.8-1
- re-instate ghc_without_shared since useful for standalone builds

* Sun Feb 24 2019 Jens Petersen <petersen@redhat.com> - 1.9.7-1
- ghc_fix_rpath was a noop when ghc_without_dynamic

* Fri Feb  1 2019 Jens Petersen <petersen@redhat.com> - 1.9.6-1
- disable debuginfo by undefining _enable_debug_packages
- leave stripping to generic rpm macros
- use C.utf8 locale for building instead of en_US.utf8

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 25 2018 Jens Petersen <petersen@redhat.com> - 1.9.5-5
- need to disable -Werror=format-security too on s390x

* Wed Oct 24 2018 Jens Petersen <petersen@redhat.com> - 1.9.5-4
- silence C compiler Wunused-label warnings flood on s390x again

* Tue Oct 23 2018 Jens Petersen <petersen@redhat.com> - 1.9.5-3
- f29: obsolete content-store, bdcs, and bdcs-api

* Sat Oct  6 2018 Jens Petersen <petersen@redhat.com> - 1.9.5-2
- fix ghc_set_gcc_flags name

* Sat Oct  6 2018 Jens Petersen <petersen@redhat.com> - 1.9.5-1
- disable hardened ldflags again

* Fri Oct  5 2018 Jens Petersen <petersen@redhat.com> - 1.9.4-1
- cabal_configure now uses ghc_set_gcc_flags

* Fri Oct  5 2018 Jens Petersen <petersen@redhat.com> - 1.9.3-1
- disable dynamic linking of executables for better portability
- replace ghc_set_cflags with simplified ghc_set_gcc_flags

* Tue Jul 31 2018 Jens Petersen <petersen@redhat.com> - 1.9.2-1
- inject a Setup.hs if none shipped

* Tue Jul 24 2018 Jens Petersen <petersen@redhat.com> - 1.9.1-1
- remove -Wall and -Werror=format-security separately (on aarch64 and s390x)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 24 2018 Jens Petersen <petersen@redhat.com> - 1.9.0-1
- support Cabal bundled internal libraries (yuck)
- ghc_check_bootstrap should be redundant now according to upstream
- rename ghc_bootstrap to ghc_quick_build (disables prof and haddock)

* Mon Apr 30 2018 Jens Petersen <petersen@redhat.com> - 1.8.7-6
- obsolete ghc-fail

* Sat Apr  7 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.8.7-5
- drop hash from pkgdir in ghc_gen_filelists too

* Thu Apr  5 2018 Jens Petersen <petersen@redhat.com> - 1.8.7-4
- configure libexecsubdir (Cabal-2 only) (#1563863)
- drop hash from libsubdir

* Tue Mar  6 2018 Jens Petersen <petersen@redhat.com> - 1.8.7-3
- obsolete ghc-ltk

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb  3 2018 Jens Petersen <petersen@redhat.com> - 1.8.7-1
- no longer need to prune -z defs from LDFLAGS
- drop the ldconfig scripts since they are not needed for F28

* Mon Jan 29 2018 Jens Petersen <petersen@redhat.com> - 1.8.6-1
- cabal-tweak-drop-dep: quote grep pattern to allow whitespace

* Sun Jan 28 2018 Jens Petersen <petersen@redhat.com> - 1.8.5-1
- re-enable _ghcdynlibdir (for ghc-8.2)

* Sun Jan 28 2018 Jens Petersen <petersen@redhat.com> - 1.8.4-1
- make the recent dynlib packaging changes conditional on _ghcdynlibdir
- temporarily disable _ghcdynlibdir for Rawhide

* Thu Jan 25 2018 Jens Petersen <petersen@redhat.com> - 1.8.3-1
- remove "-z defs" from LDFLAGS since it breaks linking with ghc (see #1535422)

* Tue Jan 23 2018 Jens Petersen <petersen@redhat.com> - 1.8.1-1
- ghc_fix_rpath: remove leading or trailing ':'

* Mon Jan 22 2018 Jens Petersen <petersen@redhat.com> - 1.8.0-1
- add _ghcdynlibdir for Cabal --dynlibdir
- dynlibs in _libdir
- drop ghc_without_shared
- ghc_fix_rpath removes RPATHs for 8.2+
- add ldconfig install scripts to ghc_lib_subpackage

* Mon Dec  4 2017 Jens Petersen <petersen@fedoraproject.org> - 1.6.51-1
- add ghc_set_cflags macro

* Wed Nov 15 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-9
- obsolete ghc-webkit (#1375825)

* Wed Nov 15 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-8
- rename macros.ghc-fedora to macros.ghc-os

* Wed Nov 15 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-7
- use shell variable instead of macro to carry licensedir version

* Tue Nov 14 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-6
- make package noarch RHEL > 7
- only version license dir for RHEL <= 7

* Fri Nov 10 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-5
- -Werror=format-security fails without -Wall

* Fri Nov 10 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-4
- do not set -Wall on aarch64 and s390x since -Wunused-label is extremely noisy

* Fri Nov 10 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-3
- temporarily set Wall for all archs to see which are noisy

* Tue Oct 10 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-2
- drop the git-annex obsoletes

* Wed Sep 13 2017 Jens Petersen <petersen@redhat.com> - 1.6.50-1
- make some macro call args explicit for rpm-4.14 scope change
  (this breaks builds with earlier versions of rpm)
- fix the package.conf existence check

* Wed Aug  2 2017 Jens Petersen <petersen@redhat.com>
- ghc_gen_filelists: check package.conf exists

* Sun Jul 30 2017 Jens Petersen <petersen@redhat.com> - 1.6.20-2
- make package noarch again for f27

* Sun Jul 30 2017 Jens Petersen <petersen@redhat.com> - 1.6.20-1
- add _ghclicensedir macro
- add ghc_smp_mflags macro, since -j4 breaks reproducible-builds.org completely
  (report by Bernhard Wiedemann)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Jens Petersen <petersen@redhat.com> - 1.6.19-2
- obsolete git-annex

* Fri Mar 24 2017 Jens Petersen <petersen@redhat.com> - 1.6.19-1
- fix haddock generation
- cabal_configure now outputs Cabal version
- fix ghc-deps.sh for ghc-pkg < 8 which does not accept pkg id
- fix ghc_fix_rpath for ghc-7.10
- Group and defattr are only needed for rhel5

* Thu Mar 16 2017 Jens Petersen <petersen@redhat.com> - 1.6.18-3
- condition obsoletes on fedora version
- add f26 obsoletes for cgi and multipart

* Sun Mar 12 2017 Jens Petersen <petersen@redhat.com> - 1.6.18-2
- obsolete geniplate and sized-types for F26

* Thu Mar  2 2017 Jens Petersen <petersen@redhat.com> - 1.6.18-1
- fix ghc_fix_rpath, ghc_gen_filelists, and ghc-deps.sh when pkg-ver already
  installed
- ghc_bin_install and ghc_lib_install now run ghc_fix_rpath on subpkgs

* Wed Feb 22 2017 Jens Petersen <petersen@redhat.com> - 1.6.17-1
- setup --global/--user in cabal_configure
- allow subpackage names to contain digits

* Wed Feb 22 2017 Jens Petersen <petersen@redhat.com> - 1.6.16-1
- fix generation of haddock's
- fix fixing of rpaths for subpackages

* Tue Feb 14 2017 Jens Petersen <petersen@redhat.com> - 1.6.15-2
- do not set CFLAGS on ppc64 or ppc64le due to -Wunused-label noise

* Mon Feb 13 2017 Jens Petersen <petersen@redhat.com> - 1.6.15-1
- fix handling of ghc's .files with new ghc_lib_subpackage -d option

* Fri Feb 10 2017 Jens Petersen <petersen@redhat.com> - 1.6.14-1
- if ghc_subpackaging set configure with --user otherwise --global

* Thu Feb  9 2017 Jens Petersen <petersen@redhat.com> - 1.6.13-1
- build subpackages inside main package directory

* Wed Feb  8 2017 Jens Petersen <petersen@redhat.com> - 1.6.12-1
- no longer use a topdir for subpackage building
- only autopackage license if subpackaging
- add new cabal-tweak-drop-dep script for excluding trivial deps
- move uniq to ghc-pkg-wrapper
- add macros.ghc-fedora for Fedora specific config
- replace cabal_verbose with cabal_configure_verbose, cabal_build_verbose,
  cabal_install_verbose, cabal_haddock_verbose, and cabal_test_verbose
- new _ghcdocdir

* Fri Dec  2 2016 Jens Petersen <petersen@redhat.com> - 1.6.11-2
- add more F25 obsoletes for: editline, hashed-storage, nats, primes

* Fri Nov 25 2016 Jens Petersen <petersen@redhat.com> - 1.6.11-1
- re-enable dynlink on armv7hl and aarch64 since binutils was fixed (#1386126)
- condition use of _defaultlicensedir
- quote some echo'd macros

* Mon Oct 31 2016 Jens Petersen <petersen@redhat.com> - 1.6.10-2
- only disable arm dynlinking for f26 (#1386126)

* Wed Oct 26 2016 Jens Petersen <petersen@redhat.com> - 1.6.10-1
- make ghc_lib_subpackage backward compatible with older 2 args form

* Mon Oct 17 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-8
- disable dynlinking on armv7hl too (#1386126)

* Mon Oct 17 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-7
- set LDFLAGS for aarch64 again
- disable dynamic linking for aarch64 since it fails (#1386126)

* Mon Oct 17 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-6
- only pass CFLAGS and LDFLAGS to ghc if set

* Mon Oct 17 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-5
- for aarch64 do not set CFLAGS and LDFLAGS

* Wed Oct 12 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-4
- remove Agda obsoletes

* Tue Oct  4 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-3
- obsolete idris

* Tue Sep 27 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-2
- macros.ghc-extra requires chrpath

* Tue Sep 27 2016 Jens Petersen <petersen@redhat.com> - 1.6.9-1
- new ghc_fix_rpath macro deprecates ghc_fix_dynamic_rpath
- ghc-pkg-wrapper: quieter and simple output
- ghc_libs_install now runs ghc_fix_rpath to fix subpackage rpaths

* Tue Sep  6 2016 Jens Petersen <petersen@redhat.com> - 1.6.8-1
- set Cabal docdir to licensedir so licenses end up in right place

* Thu Sep  1 2016 Jens Petersen <petersen@redhat.com> - 1.6.7-1
- ghc_lib_subpackage now takes name-version processed with lua

* Fri Aug 26 2016 Jens Petersen <petersen@redhat.com> - 1.6.6-1
- ghc_gen_filelists: support packages with more than one license file
- move licenses from docdir to licensedir instead of removing,
  also for ghc_bin_install

* Thu Aug 25 2016 Jens Petersen <petersen@redhat.com> - 1.6.5-1
- ghc_gen_filelists now handles license files automatically

* Wed Aug 17 2016 Jens Petersen <petersen@redhat.com> - 1.6.4-1
- add ghc_libs_build and ghc_libs_install to ease bundling libraries
- drop _smp_mflags for now since it can overwhelm armv7hl

* Sat Aug  6 2016 Jens Petersen <petersen@redhat.com> - 1.6.3-1
- cabal_verbose from github fedora-haskell/ghc-rpm-macros

* Fri Jul 22 2016 Jens Petersen <petersen@redhat.com> - 1.6.2-4
- try obsoleting Agda

* Wed Jul 20 2016 Jens Petersen <petersen@redhat.com> - 1.6.2-3
- obsolete cmdtheline, concrete-typerep, glade, bluetile, lambdabot-utils,
  haddock, monad-unify

* Wed Jun 22 2016 Jens Petersen <petersen@redhat.com> - 1.6.2-2
- obsoletes for hakyll and leksah-server

* Mon Jun 13 2016 Jens Petersen <petersen@redhat.com> - 1.6.2-1
- ghc_gen_filelists: uniq keyname to prevent build failure for installed version

* Mon Jun  6 2016 Jens Petersen <petersen@redhat.com> - 1.6.1-1
- disable debuginfo again until working

* Fri Jun  3 2016 Jens Petersen <petersen@redhat.com> - 1.6.0-1
- enable debuginfo package
- ghc-7.10 support from copr http://github.com/fedora-haskell/ghc-rpm-macros:
- ghc_gen_filelists: determine keyname with pkgnamever not just pkgname
  (fixes building newer version of installed package)
- use _rpmconfigdir macro
- support el6 (no fileattrs or /usr/lib/rpm/macros.d)
- change url to github
- add and use ghc-pkg-wrapper script
- use ghc-pkg key field (for ghc-7.10)
- configure libsubdir using pkgkey like ghc-cabal
- handle no ghc-srpm-macros for fedora < 21
- fix ghc-pkg path in ghc-deps.sh for ghc-7.10
- update ghc_gen_filelists to use new keyed library filepaths
  and specify libHS*.so more loosely
- ghc-dep.sh now just makes versioned devel reqs
- rename ghc_lib.attr to ghc.attr and drop ghc_bin.attr

* Tue Mar  8 2016 Jens Petersen <petersen@redhat.com> - 1.4.15-5
- add ghc-citeproc-hs to obsoletes

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-3
- reenable dynamic linking for aarch64 (#1195231)

* Mon May 25 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-2
- add leksah to ghc-obsoletes

* Thu May  7 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-1
- cabal macro now sets utf8 locale
- disable dynamic linking on aarch64 as a workaround (#1195231)

* Thu Apr  2 2015 Jens Petersen <petersen@redhat.com> - 1.4.14-1
- add explicit --enable-shared again for arm64

* Mon Mar 23 2015 Jens Petersen <petersen@redhat.com> - 1.4.13-1
- fix ghc-deps.sh for ghc builds:
- use .a files again instead of .conf for devel deps
- extract pkg-ver from library filename rather than directory
  (should also work for 7.10)
- introduce ghc_pkgdocdir since no _pkgdocdir in RHEL 7 and earlier

* Sat Mar  7 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.12-1
- version ghc-pkg in ghc_pkg_recache
- allow overriding ghc- prefix with ghc_name (for ghc784 etc)

* Fri Mar  6 2015 Jens Petersen <petersen@redhat.com> - 1.4.11-2
- add ghc-obsoletes dummy subpackage for obsoleting deprecated packages
- initially: ForSyDe, parameterized-data, type-level, and cgi for F22

* Mon Mar  2 2015 Jens Petersen <petersen@redhat.com> - 1.4.11-1
- fix ghc-deps.sh to handle meta-packages
- configure --disable-shared if ghc_without_shared

* Fri Feb 27 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.10-1
- have to turn off hardening in cabal_configure: set _hardened_ldflags to nil

* Fri Feb 27 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.9-1
- turn off _hardened_build for libraries since it breaks linking
  <https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code>

* Sun Feb  1 2015 Jens Petersen <petersen@redhat.com> - 1.4.8-1
- drop cabal_tests_not_working since not all tests failing on ARMv7

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.7-1
- fix arch for cabal_tests_not_working
- add cabal_test macro which uses it

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.6-1
- disable Cabal tests on armv7 since they give an internal error
  https://ghc.haskell.org/trac/ghc/ticket/10029
- fix building of meta packages:
- only run cabal haddock for real libraries with modules
- make sure basepkg.files is also created for meta packages

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.5-1
- fix the R*PATH regexp

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.4-1
- ghc_fix_dynamic_rpath: on ARMv7 RPATH is RUNPATH

* Thu Jan 22 2015 Jens Petersen <petersen@redhat.com> - 1.4.3-1
- version ghcpkgdocdir
- add new names ghc_html_dir, ghc_html_libraries_dir, and ghc_html_pkg_dir

* Thu Jan 22 2015 Jens Petersen <petersen@redhat.com> - 1.4.2-1
- correct cabal-tweak-flag error message for missing flag (#1184508)

* Sat Jan 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.1-1
- revert to versioned doc htmldirs

* Sat Jan 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.0-1
- enable shared libraries and dynamic linking on all arch's
  since ghc-7.8 now supports that
- disable debuginfo until ghc-7.10 which will support dwarf debugging output
  (#1138982)

* Fri Nov 14 2014 Jens Petersen <petersen@redhat.com> - 1.3.10-1
- split ghc.attr into ghc_lib.attr and ghc_bin.attr for finer grained handling
- require ghc-compiler for ghc_version

* Mon Oct 27 2014 Jens Petersen <petersen@redhat.com> - 1.3.9-1
- macros.ghc: cabal_configure now passes CFLAGS and LDFLAGS to ghc (#1138982)
  (thanks to Sergei Trofimovich and Ville Skyttä)

* Thu Oct 23 2014 Jens Petersen <petersen@redhat.com> - 1.3.8-1
- ghc-deps.sh: support ghc-pkg for ghc builds <= 7.4.2 as well

* Thu Oct 16 2014 Jens Petersen <petersen@redhat.com> - 1.3.7-1
- ghc.attr needs to handle requires for /usr/bin files too

* Wed Sep 10 2014 Jens Petersen <petersen@redhat.com> - 1.3.6-1
- improve ghc_fix_dynamic_rpath not to assume cwd = pkg_name

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 1.3.5-1
- no longer disable debuginfo by default:
  packages now need to explicitly opt out of debuginfo if appropriate

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 1.3.4-1
- drop -O2 for ghc-7.8: it uses too much build mem

* Fri Aug 22 2014 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- temporarily revert to ghc-7.6 config for shared libs
  until we move to ghc-7.8

* Thu Aug 21 2014 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- add an rpm .attr file for ghc-deps.sh rather than running it
  as an external dep generator (#1132275)
  (see http://rpm.org/wiki/PackagerDocs/DependencyGenerator)

* Wed Aug 20 2014 Jens Petersen <petersen@redhat.com> - 1.3.1-1
- fix warning in macros.ghc-extra about unused pkgnamever

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug  2 2014 Jens Petersen <petersen@redhat.com> - 1.3.0-1
- shared libs available for all archs in ghc-7.8
- cabal_configure --disable-shared with ghc_without_shared
- ghc_clear_execstack no longer needed

* Fri Jun 27 2014 Jens Petersen <petersen@redhat.com> - 1.2.13-2
- ghc-srpm-macros is now a separate source package

* Fri Jun  6 2014 Jens Petersen <petersen@redhat.com> - 1.2.13-1
- add aarch64

* Sun Jun  1 2014 Jens Petersen <petersen@redhat.com> - 1.2.12-1
- add missing ppc64, s390, and s390x to ghc_arches
- add new ppc64le to ghc_arches

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 1.2.11-1
- condition use of execstack since no prelink on ppc64le or arm64

* Wed May 21 2014 Dennis Gilmore <dennis@ausil.us> - 1.2.10-2
- add %%ghc_arches back to macros.ghc-srpm to maintain compatability with
- existing specs

* Fri May 16 2014 Jens Petersen <petersen@redhat.com> - 1.2.10-1
- do bcond cabal configure --enable-tests also for Bin packages

* Fri May 16 2014 Jens Petersen <petersen@redhat.com> - 1.2.9-1
- enable configure bcond check for tests

* Tue May 13 2014 Jens Petersen <petersen@redhat.com> - 1.2.8-1
- use -O2 also for executable (Bin) packages and allow it to be overrided

* Wed Apr 30 2014 Jens Petersen <petersen@redhat.com> - 1.2.7-1
- ghc-rpm-macros requires ghc-srpm-macros
- ghc-srpm-macros does not require ghc-rpm-macros
- drop ExclusiveArch and make hscolour requires arch conditional
- make ghc-srpm-macros subpackage noarch
- set Url field when generating subpackages

* Mon Apr 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.6-1
- move macros.ghc-srpm from redhat-rpm-config to new ghc-srpm-macros subpackage:
  defines ghc_arches_with_ghci and drops no longer used ghc_arches (#1089102)
- update license tag to GPLv3+

* Fri Mar 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.5-1
- handle no _pkgdocdir in RHEL7 and docdir path different to F20+

* Mon Mar 17 2014 Jens Petersen <petersen@redhat.com> - 1.2.4-1
- abort ghc_fix_dynamic_rpath if no chrpath

* Thu Feb 13 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.3-2
- Install macros to %%{_rpmconfigdir}/macros.d.

* Mon Feb 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.3-1
- set datasubdir in cabal_configure for ghc-7.8

* Fri Jan 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.2-1
- quote the ghc_fix_dynamic_rpath error message

* Fri Jan 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.1-1
- ghc_fix_dynamic_rpath: abort for non-existent executable name
- cabal-tweak-flag: add manual field to enforce flag changes

* Tue Oct 15 2013 Jens Petersen <petersen@redhat.com> - 1.2-1
- add ghcpkgdocdir, which like _pkgdocdir allows for unversioned haddock dirs

* Tue Sep 10 2013 Jens Petersen <petersen@redhat.com> - 1.1.3-1
- ghc-deps.sh: fix ghc-pkg path when bootstrapping new ghc version

* Mon Sep  9 2013 Jens Petersen <petersen@redhat.com> - 1.1.2-1
- fix ghc-deps.sh when bootstrapping a new ghc version

* Mon Sep  9 2013 Jens Petersen <petersen@redhat.com> - 1.1.1-1
- use objdump -p instead of ldd to read executable dependencies

* Sat Sep  7 2013 Jens Petersen <petersen@redhat.com> - 1.1-1
- update ghc-deps.sh to handling ghc-7.8 rts

* Tue Aug 27 2013 Jens Petersen <petersen@redhat.com> - 1.0.8-1
- drop ghc_docdir in favor of _pkgdocdir
- no longer version package htmldirs

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.7-1
- add ghc_docdir for package's docdir since not provided by standard macros

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.6-1
- also make %%ghc_lib_build docdir unversioned
- require redhat-rpm-config >= 9.1.0-50.fc20 for unversioned docdir

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.5-1
- F20 Change: docdir's are now unversioned

* Thu Jul 11 2013 Jens Petersen <petersen@redhat.com> - 1.0.4-1
- check for bindir before looking for executables in ghc_clear_execstack

* Wed Jul 10 2013 Jens Petersen <petersen@redhat.com> - 1.0.3-1
- add ghc_clear_execstack and use it also in ghc_lib_install (#973512)
  and require prelink for execstack

* Tue Jul  9 2013 Jens Petersen <petersen@redhat.com> - 1.0.2-1
- drop doc and prof obsoletes and provides from ghc_lib_subpackage
- clear executable stack flag when installing package executables (#973512)

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0.1-1
- only configure with --global if not subpackaging libs

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0-3
- reenable hscolour

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0-2
- turn off hscolour for bootstrap

* Wed Jun 19 2013 Jens Petersen <petersen@redhat.com> - 1.0-1
- add --global to cabal_configure

* Mon Jun 17 2013 Jens Petersen <petersen@redhat.com> - 0.99.4-1
- merge remaining extra macros into ghc_lib_subpackage

* Thu Jun  6 2013 Jens Petersen <petersen@redhat.com> - 0.99.3-1
- configure builds with ghc -O2 (#880135)

* Wed Jun  5 2013 Jens Petersen <petersen@redhat.com> - 0.99.2-1
- drop -h option from extra macros and make -m work again

* Fri May 17 2013 Jens Petersen <petersen@redhat.com> - 0.99.1-1
- drop new ghc_compiler macro since it is not good for koji
- ghc_fix_dynamic_rpath: do not assume first RPATH

* Tue Apr 23 2013 Jens Petersen <petersen@redhat.com> - 0.99-1
- update for simplified revised Haskell Packaging Guidelines
  (https://fedorahosted.org/fpc/ticket/194)
- packaging for without_shared is now done the same way as shared
  to make non-shared arch packages same as shared ones:
  so all archs will now have base library binary packages
- move spec section metamacros and multiple library packaging macros still
  needed for ghc and haskell-platform to new extra subpackage
- drop ghc_add_basepkg_file macro and ghc_exclude_docdir
- for ghc-7.6 --global-package-db replaces --global-conf and
  --no-user-package-db deprecates --no-user-package-conf

* Wed Mar 20 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.98.1-4
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Tue Feb 26 2013 Jens Petersen <petersen@redhat.com> - 0.98.1-3
- only add lib pkgdir to filelist if it exists
  to fix haskell-platform build on secondary archs (no shared libs)
- add ghc_with_lib_for_ghci which re-enables ghci library .o files
  (should not normally be necessary since ghci can load .a files)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jens Petersen <petersen@redhat.com> - 0.98.1-1
- simplify cabal-tweak-flag script to take one flag value

* Mon Jan 21 2013 Jens Petersen <petersen@redhat.com> - 0.98-1
- new ghc_fix_dynamic_rpath macro for cleaning up package executables
  linked against their own libraries

* Fri Jan 18 2013 Jens Petersen <petersen@redhat.com> - 0.97.6-1
- be more careful about library pkgdir ownership (#893777)

* Mon Dec  3 2012 Jens Petersen <petersen@redhat.com> - 0.97.5-1
- add cabal-tweak-flag script for toggling flag default

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.97.4-1
- enable hscolour again

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.97.3.1-1
- bootstrap hscolour

* Thu Oct 25 2012 Jens Petersen <petersen@redhat.com> - 0.97.3-1
- BR redhat-rpm-config instead of ghc-rpm-macros
- no longer set without_hscolour in macros.ghc for bootstrapping

* Tue Oct  9 2012 Jens Petersen <petersen@redhat.com> - 0.97.2-1
- "cabal haddock" needs --html option with --hoogle to output html

* Thu Sep 20 2012 Jens Petersen <petersen@redhat.com> - 0.97.1-2
- no need to BR hscolour

* Wed Sep 19 2012 Jens Petersen <petersen@redhat.com> - 0.97.1-1
- fix broken duplicate hash output for haskell-platform binaries buildhack
  when haskell-platform locally installed

* Sat Sep  8 2012 Jens Petersen <petersen@redhat.com> - 0.97-1
- ghc-rpm-macros now requires hscolour so packages no longer need to BR it
- this can be disabled for bootstrapping by setting without_hscolour

* Fri Aug 24 2012 Jens Petersen <petersen@redhat.com> - 0.96-1
- make haddock build hoogle files
- Fedora ghc-7.4.2 Cabal will not build ghci lib files by default

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Jens Petersen <petersen@redhat.com> - 0.95.6-1
- provide doc from devel a little longer to silence rpmlint

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.5.1-1
- cabal-tweak-dep-ver: be careful only to match complete dep name and
  do not match beyond ","

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.5-1
- some cabal-tweak-dep-ver improvements:
- show file name when no match
- backslash quote . and * in the match string
- create a backup file if none exists

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.4-1
- new cabal-tweak-dep-ver script to tweak depends version bounds in .cabal

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 0.95.3-1
- ghc-dep.sh: only use buildroot package.conf.d if it exists

* Fri Jun  8 2012 Jens Petersen <petersen@redhat.com> - 0.95.2-1
- ghc-deps.sh: look in buildroot package.conf.d for program deps

* Fri Jun  8 2012 Jens Petersen <petersen@redhat.com> - 0.95.1-1
- add a meta-package option to ghc_devel_package and use in ghc_devel_requires

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.95-1
- let ghc_bin_install take an arg to disable implicit stripping for subpackages

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.94-1
- allow ghc_description, ghc_devel_description, ghc_devel_post_postun
  to take args

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.93-1
- fix doc handling of subpackages for ghc_without_shared

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.92-1
- move --disable-library-for-ghci to ghc_lib_build
- revert back to fallback behaviour for common_summary and common_description
  since it is needed for ghc and haskell-platform subpackaging
- without ghc_exclude_docdir include doc dir also for subpackages

* Tue Jun  5 2012 Jens Petersen <petersen@redhat.com> - 0.91-1
- no longer build redundant ghci .o library files
- support meta packages like haskell-platform without base lib files
- make it possible not to have to use common_summary and common_description
- rename ghc_binlib_package to ghc_lib_subpackage
- add ghc_lib_build_without_haddock
- no longer drop into package dirs when subpackaging with ghc_lib_build and
  ghc_lib_install
- add shell variable cabal_configure_extra_options to cabal_configure for
  local configuration

* Mon Mar 19 2012 Jens Petersen <petersen@redhat.com> - 0.90-1
- use new rpm metadata hash format for ghc-7.4
- drop prof meta hash data
- no longer include doc files automatically by default
- no longer provide doc subpackage
- do not provide prof when without_prof set

* Thu Feb 23 2012 Jens Petersen <petersen@redhat.com> - 0.15.5-1
- fix handling of devel docdir for non-shared builds
- simplify ghc_bootstrap

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 0.15.4-1
- allow dynamic linking of Setup with ghc_without_shared set

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.15.3-1
- new ghc_add_basepkg_file to add a path to base lib package filelist

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 0.15.2-1
- add ghc_devel_post_postun to help koji/mock with new macros

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 0.15.1-1
- add ghc_package, ghc_description, ghc_devel_package, ghc_devel_description

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 0.15-1
- new ghc_files wrapper macro for files which takes base doc files as args
  and uses new ghc_shared_files and ghc_devel_files macros
- when building for non-shared archs move installed docfiles to devel docdir

* Fri Dec  2 2011 Jens Petersen <petersen@redhat.com> - 0.14.3-1
- do not use ghc user config by default when compiling Setup
- do not setup hscolour if without_hscolour defined

* Thu Nov 17 2011 Jens Petersen <petersen@redhat.com> - 0.14.2-1
- test for HsColour directly when running "cabal haddock" instead of
  check hscolour is available (reported by Giam Teck Choon, #753833)

* Sat Nov 12 2011 Jens Petersen <petersen@redhat.com> - 0.14.1-1
- fix double listing of docdir in base lib package

* Tue Nov  1 2011 Jens Petersen <petersen@redhat.com> - 0.14-1
- replace devel ghc requires with ghc-compiler
- disable testsuite in ghc_bootstrap

* Mon Oct 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.13-1
- add ghc_bootstrapping to ghc_bootstrap for packages other than ghc
- make ghc-deps.sh also work when bootstrapping a new ghc version

* Sat Oct 15 2011 Jens Petersen <petersen@redhat.com> - 0.13.12-1
- add ghc_exclude_docdir to exclude docdir from filelists

* Fri Sep 30 2011 Jens Petersen <petersen@redhat.com> - 0.13.11-1
- fix devel subpackage's prof and doc obsoletes and provides versions
  for multiple lib packages like ghc (reported by Henrik Nordström)

* Tue Sep 13 2011 Jens Petersen <petersen@redhat.com> - 0.13.10-1
- do not setup ghc-deps.sh when ghc_bootstrapping
- add ghc_test build config

* Wed Aug  3 2011 Jens Petersen <petersen@redhat.com> - 0.13.9-1
- drop without_testsuite from ghc_bootstrap since it breaks koji

* Fri Jul  1 2011 Jens Petersen <petersen@redhat.com> - 0.13.8-1
- drop redundant defattr from filelists
- move dependency generator setup from ghc_package_devel to ghc_lib_install
  in line with ghc_bin_install

* Mon Jun 27 2011 Jens Petersen <petersen@redhat.com> - 0.13.7-1
- add requires for redhat-rpm-config for ghc_arches
- drop ghc_bootstrapping from ghc_bootstrap: doesn't work for koji

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.6-1
- also set ghc_without_dynamic for ghc_bootstrap
- drop without_hscolour from ghc_bootstrap: doesn't work for koji

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.5-1
- ghc_bootstrap is now a macro which sets ghc_bootstrapping,
  ghc_without_shared, without_prof, without_haddock, without_hscolour,
  without_manual, without_testsuite
- tweaks to ghc_check_bootstrap

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.4-1
- add ghc_check_bootstrap

* Thu Jun  2 2011 Jens Petersen <petersen@redhat.com> - 0.13.3-1
- rename macros.ghc-pkg back to macros.ghc
- move the devel summary prefix back to a suffix

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.2-1
- macros need to live in /etc/rpm
- use macro_file for macros.ghc filepath

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.1-1
- move macros.ghc to /usr/lib/rpm to avoid conflict with redhat-rpm-config

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 0.13-1
- merge prof subpackages into devel to simplify packaging

* Mon May  9 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- include ghc_pkg_c_deps even when -c option used

* Sat May  7 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- drop ghc_pkg_deps from ghc_package_devel and ghc_package_prof since
  ghc-deps.sh generates better inter-package dependencies already
- condition --htmldir on pkg_name

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 0.11.14-1
- provides ghc-*-doc still needed for current lib templates

* Mon Mar 28 2011 Jens Petersen <petersen@redhat.com> - 0.11.13-1
- ghc-deps.sh: check PKGBASEDIR exists to avoid warning for bin package
- abort cabal_configure if ghc is not self-bootstrapped
- make ghc_reindex_haddock a safe no-op
- no longer provide ghc-*-doc
- no longer run ghc_reindex_haddock in ghc-*-devel scripts

* Thu Mar 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.12-1
- add ghc_pkg_obsoletes to binlib base lib package too

* Wed Mar  9 2011 Jens Petersen <petersen@redhat.com> - 0.11.11-1
- add docdir when subpackaging packages too

* Sun Feb 13 2011 Jens Petersen <petersen@redhat.com> - 0.11.10-1
- this package is now arch-dependent
- rename without_shared to ghc_without_shared and without_dynamic
  to ghc_without_dynamic so that they can be globally defined for
  secondary archs without shared libs
- use %%undefined macro
- disable debug_package in ghc_bin_build and ghc_lib_build
- set ghc_without_shared and ghc_without_dynamic on secondary
  (ie non main intel) archs
- disable debuginfo for self

* Fri Feb 11 2011 Jens Petersen <petersen@redhat.com> - 0.11.9-1
- revert "set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build" change, since happening for all archs

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.8-1
- only link Setup dynamically if without_shared and without_dynamic not set
- set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build
- add cabal_configure_options to pass extra options to cabal_configure

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.7-1
- fix ghc-deps.sh for without_shared libraries

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Jens Petersen <petersen@redhat.com> - 0.11.6-1
- simplify adding shared subpackage license file
- own ghc-deps.sh not /usr/lib/rpm

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 0.11.5-1
- add rpm hash requires for dynamic executables in ghc-deps.sh
- compile Setup in cabal macro
- use _rpmconfigdir

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 0.11.4-1
- drop deprecated ghcdocdir and ghcpkgdir
- new ghclibdocdir
- replace some missed RPM_BUILD_ROOT's
- bring back ghc requires in ghc_devel_requires
- improve prof summary and description
- add without_prof and without_haddock option macros

* Fri Jan 21 2011 Jens Petersen <petersen@redhat.com> - 0.11.3-1
- compile Setup to help speed up builds

* Thu Jan 20 2011 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- put docdir (license) also into shared lib subpackage
- add ghc_binlib_package option to exclude package from ghc_packages_list
- condition lib base package additional description for srpm

* Mon Jan  3 2011 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- use buildroot instead of RPM_BUILD_ROOT
- rename ghcpkgbasedir to ghclibdir
- split "[name-version]" args into "[name] [version]" args
- move remaining name and version macro options (-n and -v) to args
- drop deprecated -o options

* Thu Dec 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- add support for subpackaging ghc's libraries:
- deprecate ghcpkgdir and ghcdocdir from now on
- ghc_gen_filelists optional arg is now name-version
- ghc_lib_build, ghc_lib_install, cabal_pkg_conf now take optional
  name-version arg

* Mon Dec 20 2010 Jens Petersen <petersen@redhat.com> - 0.10.3-1
- revert disabling debug_package, since with redhat-rpm-config installed
  the behaviour depended on the position of ghc_lib_package in the spec file
  (reported by narasim)

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com>
- drop with_devhelp since --html-help option gone from haddock-2.8.0

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- ignore ghc's builtin pseudo-libs

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.1-1
- bring back the explicit n-v-r internal package requires for devel and prof packages

* Mon Nov 22 2010 Jens Petersen <petersen@redhat.com> - 0.10.0-1
- turn on pkg hash metadata (for ghc-7 builds)
- ghc-deps.sh now requires an extra buildroot/ghcpkgbasedir arg
- automatic internal package deps from prof to devel to base
- rename ghc_requires to ghc_devel_requires
- drop ghc_doc_requires
- ghc_reindex_haddock is deprecated and now a no-op

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- fix without_shared build so it actually works

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.0-1
- add rpm provides and requires script ghc-deps.sh for package hash metadata
- turn on hash provides and disable debuginfo by default
- make shared and hscolour default
- use without_shared and without_hscolour to disable them
- add ghc_pkg_obsoletes for obsoleting old packages
- use ghcpkgbasedir
- always obsolete -doc packages, but keep -o for now for backward compatibility

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.1-1
- fix ghc_strip_dynlinked when no dynlinked files
- devel should provide doc also when not obsoleting

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-1
- merge -doc into -devel and provide -o obsoletes doc subpackage option

* Mon Jun 28 2010 Jens Petersen <petersen@redhat.com> - 0.7.1-1
- support hscolour'ing of src from haddock
- really remove redundant summary and description option flags

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.7.0-1
- new ghc_bin_build, ghc_bin_install, ghc_lib_build, ghc_lib_install

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.2-1
- a couple more fallback summary tweaks

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.1-1
- drop the summary -s and description -d package options since rpm does not
  seem to allow white\ space in macro option args anyway

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.6.0-1
- make ghc_strip_dynlinked conditional on no debug_package

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- replace ghc_strip_shared with ghc_strip_dynlinked

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.8-1
- add ghc_strip_shared to strip shared libraries

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- add comments over macros
- drop unused cabal_makefile

* Mon Apr 12 2010 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- drop unused ghc_pkg_ver macro
- add ghc_pkg_recache macro

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.5.5-1
- drop optional 2nd version arg from ghcdocdir, ghcpkgdir, and
  ghc_gen_filelists: multiversion subpackages are not supported
- add ghcpkgbasedir
- bring back some shared conditions which were dropped temporarily
- test for ghcpkgdir and ghcdocdir in ghc_gen_filelists
- allow optional pkgname arg for cabal_pkg_conf
- can now package gtk2hs

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- use -v in ghc_requires and ghc_prof_requires for version

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- drop "Library for" from base lib summary

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.2-1
- use -n in ghc_requires and ghc_prof_requires for when no pkg_name

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.1-1
- add ghcdocbasedir
- revert ghcdocdir to match upstream ghc
- ghcdocdir and ghcpkgdir now take optional name version args
- update ghc_gen_filelists to new optional name version args
- handle docdir in ghc_gen_filelists
- ghc_reindex_haddock uses ghcdocbasedir
- summary and description options to ghc_binlib_package, ghc_package_devel,
  ghc_package_doc, and ghc_package_prof

* Sun Jan 10 2010 Jens Petersen <petersen@redhat.com> - 0.5.0-1
- pkg_name must be set now for binlib packages too
- new ghc_lib_package and ghc_binlib_package macros make packaging too easy
- ghc_package_devel, ghc_package_doc, and ghc_package_prof helper macros
- ghc_gen_filelists now defaults to ghc-%%{pkg_name}
- add dynamic bcond to cabal_configure instead of cabal_configure_dynamic

* Thu Dec 24 2009 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- add cabal_configure_dynamic
- add ghc_requires, ghc_doc_requires, ghc_prof_requires

* Tue Dec 15 2009 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- use ghc_version_override to override ghc_version
- fix pkg .conf filelist match

* Sat Dec 12 2009 Jens Petersen <petersen@redhat.com> - 0.3.0-1
- major updates for ghc-6.12, package.conf.d, and shared libraries
- add shared support to cabal_configure, ghc_gen_filelists
- version ghcdocdir
- replace ghc_gen_scripts, ghc_install_scripts, ghc_register_pkg, ghc_unregister_pkg
  with cabal_pkg_conf
- allow (ghc to) override ghc_version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.5-1
- make ghc_pkg_ver only return pkg version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.4-1
- change GHCRequires to ghc_pkg_ver

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.3-1
- use the latest installed pkg version for %%GHCRequires

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.2-1
- add %%GHCRequires for automatically versioned library deps

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-2
- no, revert versioned ghcdocdir again!

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-1
- version ghcdocdir to allow multiple doc versions like ghcpkgdir

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Jens Petersen <petersen@redhat.com> - 0.2-1
- drop version from ghcdocdir since it breaks haddock indexing

* Wed May 13 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-7
- specifies the macros file as a %%conf

* Sat May  9 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-6
- removes archs and replaces with noarch
- bumps to avoid conflicts with jens

* Fri May  8 2009 Jens Petersen <petersen@redhat.com> - 0.1-5
- make it arch specific to fedora ghc archs
- setup a build dir so it can build from the current working dir

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-4
- renamed license file
- removed some extraneous comments needed only at review time

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-3
- updated license to GPLv3
- added AUTHORS file

* Tue May  5 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-2
- moved copying license from %%build to %%prep

* Mon May  4 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-1
- creation of package
