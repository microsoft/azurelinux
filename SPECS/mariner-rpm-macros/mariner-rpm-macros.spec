%global rcdir %{_libdir}/rpm/mariner
%global rcluadir %{_libdir}/rpm/lua/mariner
# Turn off auto byte compilation since when building this spec in the toolchain the needed scripts are not installed yet.
# __brp_python_bytecompile
%global __brp_python_bytecompile %{nil}
Summary:        Mariner specific rpm macro files
Name:           mariner-rpm-macros
Version:        2.0
Release:        25%{?dist}
License:        GPL+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/System
Source0:        macros
Source1:        rpmrc
Source2:        default-hardened-cc1
Source3:        default-hardened-ld
Source4:        default-annobin-cc1
Source5:        macros.check
Source6:        macros.python
Source7:        macros.python3
Source8:        macros.python-srpm
Source9:        macros.openblas-srpm
Source10:       macros.nodejs-srpm
Source11:       macros.mono-srpm
Source12:       macros.ocaml-srpm
Source13:       macros.perl-srpm
Source14:       gpgverify
Source15:       pythondist.attr
Source16:       brp-python-bytecompile
Source17:       macros.pybytecompile
# Use an enhanced copy of Python's compileall module for Python >= 3.4
Source18:       https://github.com/fedora-python/compileall2/raw/v0.7.1/compileall2.py
Source19:       macros.forge
Source20:       common.lua
Source21:       forge.lua
# macros.rust-srpm is taken from https://pagure.io/fedora-rust/rust2rpm
Source22:       macros.rust-srpm
# macros.fonts is taken from the "fontpackages-devel" package.
Source23:       macros.fonts
Source24:       macros.suse
Source25:       gen-ld-script.sh
Source26:       generate-package-note.py
Source27:       verify-package-notes.sh
Source28:       macros.dist
Provides:       redhat-rpm-config
Provides:       openblas-srpm-macros
Provides:       ocaml-srpm-macros
Provides:       perl-srpm-macros
Provides:       python-srpm-macros
Provides:       python-rpm-macros
Provides:       python3-rpm-macros
Provides:       rust-srpm-macros
BuildArch:      noarch

%description
Mariner specific rpm macro files.

%package -n mariner-check-macros
Summary:        Mariner specific rpm macros to override default %%check behavior
Group:          Development/System

%description -n mariner-check-macros
Mariner specific rpm macros to override default %%check behavior

%prep
%setup -q -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}%{rcdir}
install -p -m 644 -t %{buildroot}%{rcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rcdir} default-hardened-*
install -p -m 444 -t %{buildroot}%{rcdir} default-annobin-*
install -p -m 755 -t %{buildroot}%{rcdir} gpgverify
install -p -m 755 -t %{buildroot}%{rcdir} compileall2.py
install -p -m 755 -t %{buildroot}%{rcdir} brp-*
install -p -m 755 -t %{buildroot}%{rcdir} gen-ld-script.sh
install -p -m 755 -t %{buildroot}%{rcdir} generate-package-note.py
install -p -m 755 -t %{buildroot}%{rcdir} verify-package-notes.sh

sed -e 's|@DIST@|%{dist}|g' %{SOURCE28} > macros.dist
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*
mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 644 -t %{buildroot}%{_fileattrsdir} pythondist.attr

mkdir -p %{buildroot}%{rcluadir}/{rpm,srpm}
install -p -m 644 -t %{buildroot}%{rcluadir} common.lua
install -p -m 644 -t %{buildroot}%{rcluadir}/srpm forge.lua

%files
%defattr(-,root,root)
%{rcdir}/macros
%{rcdir}/rpmrc
%{rcdir}/default-hardened-*
%{rcdir}/default-annobin-*
%{rcdir}/gpgverify
%{rcdir}/brp-*
%{rcdir}/compileall2.py
%{rcdir}/gen-ld-script.sh
%{rcdir}/generate-package-note.py
%{rcdir}/verify-package-notes.sh
%{_rpmconfigdir}/macros.d/macros.openblas-srpm
%{_rpmconfigdir}/macros.d/macros.nodejs-srpm
%{_rpmconfigdir}/macros.d/macros.mono-srpm
%{_rpmconfigdir}/macros.d/macros.ocaml-srpm
%{_rpmconfigdir}/macros.d/macros.perl-srpm
%{_rpmconfigdir}/macros.d/macros.rust-srpm
%{_rpmconfigdir}/macros.d/macros.fonts
%{_rpmconfigdir}/macros.d/macros.forge
%{_rpmconfigdir}/macros.d/macros.suse
%{_rpmconfigdir}/macros.d/macros.dist

%dir %{rcluadir}
%dir %{rcluadir}/srpm
%dir %{rcluadir}/rpm
%{rcluadir}/*.lua
%{rcluadir}/srpm/*.lua
%{_rpmconfigdir}/macros.d/macros.pybytecompile
%{_rpmconfigdir}/macros.d/macros.python*
%{_fileattrsdir}/pythondist.attr

%files -n mariner-check-macros
%{_rpmconfigdir}/macros.d/macros.check

%changelog
* Thu Nov 16 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-25
- Added cross-compilation macros.

* Thu Nov 09 2023 George Mileka <gmileka@microsoft.com> - 2.0-24
- Update ccache to use the compiler content for comparison.

* Thu Jul 06 2023 Andrew Phelps <anphel@microsoft.com> - 2.0-23
- Compress rpm binaries with zstd

* Thu Jun 15 2023 Andrew Phelps <anphel@microsoft.com> - 2.0-22
- Optimize __os_install_post

* Tue May 09 2023 Andy Zaugg <azaugg@linkedin.com> - 2.0-21
- Set __python macro to python3 interpreter

* Mon Dec 05 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-20
- Add support to build with ccache when 'mariner_ccache_enabled' is set.

* Wed Nov 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.0-19
- Add dist macro

* Tue Nov 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-18
- Updated Python macros to move away from deprecated APIs. Using Fedora 37 implementation (license: MIT).

* Fri Oct 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-17
- Adding macro to skip stripping of signatures.

* Fri Jun 10 2022 Rachel Menge <rachelmenge@microsoft.com> - 2.0-16
- Modify macros to depend on other macros

* Fri May 20 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-15
- Remove module_info.ld from default LDFLAGS; require setting through "mariner_module_ldflags"
- Modify gen-ld-script.sh to pass OS Version and predefine OS ID instead of parsing from /etc/os-release (no longer in toolchain env)

* Tue Apr 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-14
- Adding the "_mariner_sources_url" macro.

* Mon Mar 28 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0-13
- Remove python2 RPM macros entirely
- Remove python2-related SRPM macros

* Wed Feb 16 2022 Andrew Phelps <anphel@microsoft.com> - 2.0-12
- Use _topdir variable with gen-ld-script.sh

* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.0-11
- add sed step to os_install_post to remove references to module_info.ld in pkgconfigs

* Wed Dec 23 2021 Thomas Crain <thcrain@microsoft.com> - 2.0-10
- Add Fedora's macros for passing flags to extension builders (license: MIT)

* Wed Dec 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.0-9
- Update unversioned python and python3 macros to reflect removal of easy_install binary

* Tue Nov 02 2021 Mateusz Malisz <mamalisz@microsoft.com> - 2.0-8
- Remove too verbose logs from the linker script
- Update default mariner macros with invalid_encoding_terminates_build
- Update linker script to use sed instead of "grep -P" and "tr"

* Tue Nov 02 2021 Andrew Phelps <anphel@microsoft.com> - 2.0-7
- Update linker script to use sed instead of "grep -P" and "tr"
- Create linker script output directory as needed

* Thu Oct 21 2021 Ismail Kose <iskose@microsoft.com> - 2.0-6
- Update generate-package-note.py tool to 2.1.2
- Add verify-package-notes.sh tool
- Verified license

* Tue Sep 21 2021 Andrew Phelps <anphel@microsoft.com> - 2.0-5
- Modify gen-ld-script.sh to ensure moduleVersion contains 4 part version

* Mon Sep 13 2021 Andrew Phelps <anphel@microsoft.com> - 2.0-4
- Add gen-ld-script.sh and generate-package-note.py to generate ELF note metadata

* Thu Aug 19 2021 Henry Li <lihl@microsoft.com> - 2.0-3
- Add fillup-related macros

* Sat Jul 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0-2
- Adding the '_metainfodir' macro.

* Thu Jul 08 2021 Jon Slobodzian <joslobo@microsoft.com> - 2.0-1
- Version update for 2.0.

* Tue Jun 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-17
- Adding font macros from the "fontpackages-devel" package.

* Mon May 17 2021 Thomas Crain <thcrain@microsoft.com> - 1.0-16
- Add Rust SRPM macros from rust2rpm (license: MIT)
- Add rust-srpm-macros Provides

* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> - 1.0-15
- Add _smp_build_cpus and relevant macros.

* Thu Feb 25 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-14
- Add forge macros and scripts.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-13
- Import brp-python-bytecompile, compileall2.py, macros.pybytecompile, and python byte compilation in macros from Fedora 32 (license: MIT).
- Fix %%{_lib} and %%{_lib64} macros to reference the folder names instead of paths.
- Combine mariner-python-macros into the main package for byte compilation support.
- Make python3 the default python interpreter for byte compilation.

* Tue Jan 19 2021 Joe Schmitt <joschmit@microsoft.com> - 1.0-12
- Disable python requirement generator.

* Thu Jan 14 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0-11
- Remove pythondistdeps.py.

* Mon Jan 04 2021 Ruying Chen <v-ruyche@microsoft.com> - 1.0-10
- Enable python dependency generator for dist provides.

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-9
- Define meson macros.

* Mon Nov 02 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-8
- Define gpgverify macro.

* Thu Oct 22 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-7
- Define __make macro.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-6
- Add backwards compatibility macros for compiling and linking.
- Define _fmoddir macro.
- Turn on perl_bootstrap by default.
- Add perl-srpm macros.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-5
- Add srpm macros.
- Add python related macros derived from Fedora 32 python-rpm-macros.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> - 1.0-4
- Add ldconfig_scriptlets related macros derived from Fedora 32 redhat-rpm-config.

* Tue Jun 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-3
- Add macros.check to support non-fatal check section runs for log collection.

* Mon Jun 08 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0-2
- Add vendor folder. Add optflags related macros and rpmrc derived from Fedora 32.

* Fri May 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0-1
- Original version for CBL-Mariner
