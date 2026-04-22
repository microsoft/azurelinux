# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
%global xapian_core_support ON
%global build_wizard ON
%global system_spdlog ON
%global system_fmt ON
%else
%global xapian_core_support OFF
%global build_wizard OFF
%global system_spdlog OFF
%global system_fmt OFF
%endif
%global build_search %{xapian_core_support}
%global clang_support ON
%global system_sqlite3 ON

Summary: A documentation system for C/C++
Name:    doxygen
Epoch:   2
Version: 1.14.0
Release: 6%{?dist}
# No version is specified.
License: GPL-2.0-or-later
Url: https://github.com/doxygen
Source0: https://www.doxygen.nl/files/%{name}-%{version}.src.tar.gz
# this icon is part of kdesdk
Source1: doxywizard.desktop
# these icons are part of doxygen and converted from doxywizard.ico
Source2: doxywizard-icons.tar.xz
Source3: README.rpm-packaging
Source4: doxygen-unbundler

# upstream fixes
# fix input buffer overflow
Patch1: doxygen-input-buffer-overflow.patch

BuildRequires: %{_bindir}/python3
BuildRequires: perl-interpreter, perl-open
BuildRequires: texlive-bibtex
BuildRequires: web-assets-devel
# Building an RPM package typically needs unbundling of Javascript assets.
Requires: (js-doxygen if redhat-rpm-config)

%if ! 0%{?_module_build}
BuildRequires: tex(dvips)
BuildRequires: tex(latex)
# From doc/manual.sty
BuildRequires: tex(helvet.sty)
BuildRequires: tex(sectsty.sty)
BuildRequires: tex(tocloft.sty)
BuildRequires: tex(fontenc.sty)
BuildRequires: tex(fancyhdr.sty)
# From templates/latex/doxygen.sty
BuildRequires: tex(alltt.sty)
BuildRequires: tex(calc.sty)
BuildRequires: tex(float.sty)
BuildRequires: tex(verbatim.sty)
BuildRequires: tex(xcolor.sty)
BuildRequires: tex(fancyvrb.sty)
BuildRequires: tex(tabularx.sty)
BuildRequires: tex(multirow.sty)
BuildRequires: tex(hanging.sty)
BuildRequires: tex(ifpdf.sty)
BuildRequires: tex(adjustbox.sty)
BuildRequires: tex(amssymb.sty)
BuildRequires: tex(stackengine.sty)
BuildRequires: tex(ulem.sty)
# From doc/doxygen_manual.tex
BuildRequires: tex(ifthen.sty)
BuildRequires: tex(array.sty)
BuildRequires: tex(geometry.sty)
BuildRequires: tex(makeidx.sty)
BuildRequires: tex(natbib.sty)
BuildRequires: tex(graphicx.sty)
BuildRequires: tex(multicol.sty)
BuildRequires: tex(float.sty)
BuildRequires: tex(geometry.sty)
BuildRequires: tex(listings.sty)
BuildRequires: tex(color.sty)
BuildRequires: tex(xcolor.sty)
BuildRequires: tex(textcomp.sty)
BuildRequires: tex(wasysym.sty)
BuildRequires: tex(import.sty)
BuildRequires: tex(appendix.sty)
BuildRequires: tex(hyperref.sty)
BuildRequires: tex(pspicture.sty)
BuildRequires: tex(inputenc.sty)
BuildRequires: tex(mathptmx.sty)
BuildRequires: tex(courier.sty)
# From src/latexgen.cpp
BuildRequires: tex(fixltx2e.sty)
BuildRequires: tex(ifxetex.sty)
BuildRequires: tex(caption.sty)
BuildRequires: tex(etoc.sty)
# From src/util.cpp
BuildRequires: tex(newunicodechar.sty)
# From templates/latex/tabu_doxygen.sty
BuildRequires: tex(varwidth.sty)
BuildRequires: tex(xtab.sty)
BuildRequires: tex(tabu.sty)
BuildRequires: /usr/bin/epstopdf
BuildRequires: texlive-epstopdf
BuildRequires: ghostscript
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: graphviz
%endif
BuildRequires: zlib-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: cmake
BuildRequires: git
%if "x%{?xapian_core_support}" == "xON"
BuildRequires: xapian-core-devel
%endif
%if "x%{?clang_support}" == "xON"
BuildRequires: llvm-devel
BuildRequires: clang-devel
%else
BuildRequires: gcc-c++ gcc
%endif
%if "%{system_spdlog}" == "ON"
BuildRequires: spdlog-devel
%else
# SPDLOG_VER* defined in deps/spdlog/include/spdlog/version.h
Provides: bundled(spdlog) = 1.14.1
%endif
%if "%{system_sqlite3}" == "ON"
BuildRequires: sqlite-devel
%else
# SQLITE_VERSION defined in deps/sqlite3/sqlite3.h
Provides: bundled(sqlite) = 3.42.0
%endif
%if "%{system_fmt}" == "ON"
BuildRequires: fmt-devel
%else
# deps/fmt/README.md
Provides: bundled(fmt) = 10.2.1
%endif

Requires: perl-interpreter
Requires: graphviz

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%package -n js-doxygen
Summary: Javascript files used by Doxygen
Requires: web-assets-filesystem
BuildArch: noarch
%description -n js-doxygen
Javascript files for use by locally installed Doxygen documentation.

%if  "x%{build_wizard}" == "xON"
%package doxywizard
Summary: A GUI for creating and editing configuration files
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildRequires: qt5-qtbase-devel

%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.
%endif

%if ! 0%{?_module_build}
%package latex
Summary: Support for producing latex/pdf output from doxygen
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tex(latex)
Requires: tex(dvips)
Requires: texlive-wasy
%if 0%{?fedora} > 17 || 0%{?rhel} > 6
# From doc/manual.sty
Requires: tex(helvet.sty)
Requires: tex(sectsty.sty)
Requires: tex(tocloft.sty)
Requires: tex(fontenc.sty)
Requires: tex(fancyhdr.sty)
# From templates/latex/doxygen.sty
Requires: tex(alltt.sty)
Requires: tex(calc.sty)
Requires: tex(float.sty)
Requires: tex(verbatim.sty)
Requires: tex(xcolor.sty)
Requires: tex(fancyvrb.sty)
Requires: tex(tabularx.sty)
Requires: tex(multirow.sty)
Requires: tex(hanging.sty)
Requires: tex(ifpdf.sty)
Requires: tex(adjustbox.sty)
Requires: tex(amssymb.sty)
Requires: tex(stackengine.sty)
Requires: tex(ulem.sty)
# From doc/doxygen_manual.tex
Requires: tex(ifthen.sty)
Requires: tex(array.sty)
Requires: tex(geometry.sty)
Requires: tex(makeidx.sty)
Requires: tex(natbib.sty)
Requires: tex(graphicx.sty)
Requires: tex(multicol.sty)
Requires: tex(float.sty)
Requires: tex(geometry.sty)
Requires: tex(listings.sty)
Requires: tex(color.sty)
Requires: tex(xcolor.sty)
Requires: tex(textcomp.sty)
Requires: tex(wasysym.sty)
Requires: tex(import.sty)
Requires: tex(appendix.sty)
Requires: tex(hyperref.sty)
Requires: tex(pspicture.sty)
Requires: tex(inputenc.sty)
Requires: tex(mathptmx.sty)
Requires: tex(courier.sty)
# From src/latexgen.cpp
Requires: tex(fixltx2e.sty)
Requires: tex(ifxetex.sty)
Requires: tex(caption.sty)
Requires: tex(etoc.sty)
# From src/util.cpp
Requires: tex(newunicodechar.sty)
# From templates/latex/tabu_doxygen.sty
Requires: tex(varwidth.sty)
# I'm 99% sure this isn't needed anymore since
# doxygen has a local fork of tabu... but it doesn't seem to be hurting anything.
Requires: tex(tabu.sty)
# There also does not seem to be any references to xtab in the code... but eh.
Requires: tex(xtab.sty)
# Explicitly called binaries
Requires: texlive-bibtex
Requires: texlive-makeindex
Requires: texlive-epstopdf
%endif

%description latex
%{summary}.
%endif


%prep
%autosetup -p1 -a2

# convert into utf-8
iconv --from=ISO-8859-1 --to=UTF-8 LANGUAGE.HOWTO > LANGUAGE.HOWTO.new
touch -r LANGUAGE.HOWTO LANGUAGE.HOWTO.new
mv LANGUAGE.HOWTO.new LANGUAGE.HOWTO

cp %{SOURCE3} .

%build
%cmake \
	-Dbuild_wizard=%{build_wizard} \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-Dbuild_search=%{build_search} \
	-Duse_libclang=%{clang_support} \
	-DMAN_INSTALL_DIR=%{_mandir}/man1 \
	-Dbuild_doc=OFF \
	-DPYTHON_EXECUTABLE=%{_bindir}/python3 \
	-Dbuild_xmlparser=ON \
	-Duse_sys_sqlite3=%{system_sqlite3} \
	-Duse_sys_spdlog=%{system_spdlog} \
	-Duse_sys_fmt=%{system_fmt}

%cmake_build %{?_smp_mflags}

%install
%cmake_install

# install man pages
mkdir -p %{buildroot}/%{_mandir}/man1
cp doc/*.1 %{buildroot}/%{_mandir}/man1/

%if  "x%{build_wizard}" == "xOFF"
rm -f %{buildroot}/%{_mandir}/man1/doxywizard.1*
%else
# install icons
icondir=%{buildroot}%{_datadir}/icons/hicolor
mkdir -m755 -p $icondir/{16x16,32x32,48x48,128x128}/apps
install -m644 -p -D doxywizard-6.png $icondir/16x16/apps/doxywizard.png
install -m644 -p -D doxywizard-5.png $icondir/32x32/apps/doxywizard.png
install -m644 -p -D doxywizard-4.png $icondir/48x48/apps/doxywizard.png
install -m644 -p -D doxywizard-3.png $icondir/128x128/apps/doxywizard.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
%endif

%if "x%{?xapian_core_support}" == "xOFF"
rm -f %{buildroot}/%{_mandir}/man1/doxyindexer.1* %{buildroot}/%{_mandir}/man1/doxysearch.1*
%endif

# remove duplicate
rm -rf %{buildroot}/%{_docdir}/packages

# Install the asset files.
install -m644 -D --target-directory=%{buildroot}%{_jsdir}/doxygen \
  templates/html/*.js
# Generate the macros file.  Expand version/release/%%_jsdir.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.doxygen <<'EOF'
%%doxygen_js_requires() Requires: js-doxygen >= %{version}-%{release}
%%doxygen_unbundle_buildroot() %%{_rpmconfigdir}/redhat/doxygen-unbundler "%{_jsdir}" "%%{buildroot}" %%[ %%# == 0 ? "%%{_docdir}" : "%%1"]
%%doxygen_unbundle() %{_rpmconfigdir}/redhat/doxygen-unbundler "%{_jsdir}" "" %%*
EOF
# Install the unbundler script.
install -m755 -D --target-directory=%{buildroot}%{_rpmconfigdir}/redhat %{SOURCE4}

%check
%ctest

%files
%doc LANGUAGE.HOWTO README.md README.rpm-packaging
%license LICENSE
%if ! 0%{?_module_build}
%if "x%{?xapian_core_support}" == "xON"
%{_bindir}/doxyindexer
%{_bindir}/doxysearch*
%endif
%endif
%{_bindir}/doxygen
%{_mandir}/man1/doxygen.1*
%if "x%{?xapian_core_support}" == "xON"
%{_mandir}/man1/doxyindexer.1*
%{_mandir}/man1/doxysearch.1*
%endif
%{_rpmconfigdir}/macros.d/macros.doxygen
%{_rpmconfigdir}/redhat/doxygen-unbundler
%if "x%{build_wizard}" == "xON" 
%files doxywizard
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*
%{_datadir}/applications/doxywizard.desktop
%{_datadir}/icons/hicolor/*/apps/doxywizard.png
%endif

%files -n js-doxygen
%{_jsdir}/doxygen/*

%if ! 0%{?_module_build}
%files latex
# intentionally left blank
%endif

%changelog
* Fri Nov 28 2025 Than Ngo <than@redhat.com> - 2:1.14.0-5
- Fix rhbz#2416173, Rebuilt against llvm-21

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 25 2025 Than Ngo <than@redhat.com> - 2:1.14.0-3
- Upstream fix for input buffer overflow

* Wed May 28 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2:1.14.0-2
- Use bundled spdlog on RHEL, redux

* Sun May 25 2025 Than Ngo <than@redhat.com> - 2:1.14.0-1
- Fix rhbz#2368381, update to 1.14.0

* Tue Feb 11 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2:1.13.2-5
- Use bundled spdlog on RHEL

* Mon Feb 10 2025 Than Ngo <than@redhat.com> - 2:1.13.2-4
- built with system sqlite3 and spdlog 

* Sat Feb 08 2025 Than Ngo <than@redhat.com> - 2:1.13.2-3
- Introduce js-doxygen subpackage and unbundle Javascript during RPM builds
- Use system spdlog and sqlite3

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Than Ngo <than@redhat.com> - 2:1.13.2-1
- Fix rhbz#2336720, Update to 1.13.2
- Fix rhbz#2336536, FTBFS in ignition-transport

* Fri Jan 03 2025 Than Ngo <than@redhat.com> - 2:1.13.1-1
- Fix rhbz#2335266, Update to 1.13.1

* Thu Jan 02 2025 Than Ngo <than@redhat.com> - 2:1.13.0-1
- Fix rhbz#2334703, Update to 1.13.0

* Mon Oct 28 2024 Than Ngo <than@redhat.com> - 2:1.12.0-3
- Fix rhbz#2295788, Non-reproducible file names in doxygen output

* Mon Oct 28 2024 Than Ngo <than@redhat.com> - 2:1.12.0-2
- Fix rhbz#x2322116, broken markdown links to anchors

* Wed Aug 07 2024 Than Ngo <than@redhat.com> - 2:1.12.0-1
- update to 1.12.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Than Ngo <than@redhat.com> - 2:1.11.0-4
- fixed rhbz#2292250, update license

* Fri May 31 2024 Than Ngo <than@redhat.com> - 2:1.11.0-3
- removed workaround for debuginfo

* Wed May 29 2024 Than Ngo <than@redhat.com> - 2:1.11.0-2
- fixed rhbz#2283362, fix buffer overflow

* Tue May 21 2024 Than Ngo <than@redhat.com> - 2:1.11.0-1
- update to 1.11.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Than Ngo <than@redhat.com> - 2:1.10.0-2
- don't use clang to build doxygen as workaround for a bug in gcc-14

* Tue Dec 26 2023 Than Ngo <than@redhat.com> - 1.10.0-1
- bz#2255826, update to 1.10

* Mon Sep 11 2023 Than Ngo <than@redhat.com> - 1.9.8-1
- fix bz#2235035, update to 1.9.8

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Than Ngo <than@redhat.com> - 2:1.9.7-2
- disable build_wizard for eln
- fixed broken unicode test

* Fri May 19 2023 Than Ngo <than@redhat.com> - 2:1.9.7-1
- fix #2208417, rebase to 1.9.7

* Fri Mar 10 2023 Than Ngo <than@redhat.com> - 2:1.9.6-7
- replace obsolescent egrep with grep -E 

* Fri Feb 17 2023 Than Ngo <than@redhat.com> - 2:1.9.6-6
- migrated to SPDX license

* Wed Jan 25 2023 Than Ngo <than@redhat.com> - 2:1.9.6-5
- rebuilt against new ghostscript-10 

* Fri Jan 20 2023 Than Ngo <than@redhat.com> - 2:1.9.6-4
- fixed bz#2162170, add Require on texlive-wasy

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Than Ngo <than@redhat.com> - 2:1.9.6-2
- fixed bz#2161515 - doxygen FTBFS if _module_build is 1

* Tue Jan 03 2023 Than Ngo <than@redhat.com> - 2:1.9.6-1
- fixed bz#2156564, update to 1.9.6

* Sun Sep 18 2022 Pete Walter <pwalter@fedoraproject.org> - 2:1.9.5-2
- Rebuild for llvm 15

* Fri Sep 09 2022 Than Ngo <than@redhat.com> - 2:1.9.5-1
- 1.9.5

* Thu Aug 04 2022 Than Ngo <than@redhat.com> - 2:1.9.4-2
- Fixed #2113876, Failed to build LaTex output 

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.9.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 06 2022 Than Ngo <than@redhat.com> - 2:1.9.4-1
- 1.9.4

* Thu Feb 17 2022 Than Ngo <than@redhat.com> - 2:1.9.4-0.20220217gite18f715e
- update to 1.9.4 snapshot

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Than Ngo <than@redhat.com> - 2:1.9.1-12
- revert 1.9.1, noarch package built differently on different architectures 

* Wed Oct 27 2021 Than Ngo <than@redhat.com> - 1:1.9.2-4
- update

* Thu Oct 07 2021 Tom Stellard <tstellar@redhat.com> - 1:1.9.2-3
- Rebuild for llvm-13.0.0

* Sun Sep 12 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 1:1.9.2-2
- Use predictable and reproducible filenames (rhbz#2000138)

* Thu Aug 19 2021 Than Ngo <than@redhat.com> - 1:1.9.2-1
- rebase to 1.9.2

* Tue Aug 17 2021 Björn Esser <besser82@fedoraproject.org> - 1:1.9.1-11
- Rebuild for clang-13.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1:1.9.1-9
- Rebuilt for removed libstdc++ symbol (#1937698)

* Sun Mar 21 2021 Than Ngo <than@redhat.com> - 1:1.9.1-8
- update source

* Mon Feb 22 2021 Than Ngo <than@redhat.com> - 1:1.9.1-7
- drop test-suite

* Wed Feb 10 2021 Than Ngo <than@redhat.com> - 1:1.9.1-6
- fixed Coverity issues
- fixed crash in docparser

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Tom Stellard <tstellar@redhat.com> - 1:1.9.1-4
- Rebuild for clang-11.1.0

* Tue Jan 19 2021 Than Ngo <than@redhat.com> - 1.9.1-3
- fixed doxygen crashes when parsing config file part2


* Tue Jan 19 2021 Than Ngo <than@redhat.com> - 1.9.1-2
- fixed bz#1916161, crashes when parsing config file

* Mon Jan 11 2021 Than Ngo <than@redhat.com> - 1.9.1-1
- update to 1.9.1

* Mon Jan 11 2021 Than Ngo <than@redhat.com> - 1.8.20-6
- drop BR on ImageMagick in RHEL

* Tue Sep 29 2020 Than Ngo <than@redhat.com> - 1.8.20-5
- backport upstream patches

* Thu Sep 17 2020 Than Ngo <than@redhat.com> - 1.8.20-4
- Fix doxygen crash

* Tue Sep 15 2020 Mattias Ellert <mattias.ellert@physics.uu.se> - 1:1.8.20-3
- Fix doxygen producing different results on 32 and 64 bit architectures

* Fri Aug 28 2020 Scott Talbert <swt@techie.net> - 1:1.8.20-2
- Fix issue with enums being defined in multiple files

* Tue Aug 25 2020 Than Ngo <than@redhat.com> - 1.8.20-1
- update to 1.8.20

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.18-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Than Ngo <than@redhat.com> - 1.8.18-4
- fixed link issue against new clang

* Thu Jun 18 2020 Than Ngo <than@redhat.com> - 1.8.18-3
- fixed bz#1834591, enable clang support in fedora

* Wed May 27 2020 Tom Callaway <spot@fedoraproject.org> - 1.8.18-2
- update tex dependencies

* Mon May 25 2020 Than Ngo <than@redhat.com> - 1.8.18-1
- update to 1.8.18
- backport fixes: buffer-overflow, memory leeks and md5 hash does not match for
  2 diffferent runs

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 1:1.8.17-3
- Fix string quoting for rpm >= 4.16

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Than Ngo <than@redhat.com> - 1:1.8.17-1
- resolves #1786799, update to 1.8.17

* Tue Dec 10 2019 Than Ngo <than@redhat.com> - 1:1.8.16-3
- fixed covscan issues

* Mon Sep 16 2019 Than Ngo <than@redhat.com> - 1:1.8.16-2
- backpored upstream patch to fix #7248

* Wed Sep 11 2019 Than Ngo <than@redhat.com> - 1:1.8.16-1
- resolves #1742614, update to 1.8.16

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Christoph Junghans <junghans@votca.org> - 1:1.8.15-9
- Incl. xml fix for c++11

* Sat Mar 16 2019 Than Ngo <than@redhat.com> - 1:1.8.15-8
- added license file

* Wed Mar 13 2019 Than Ngo <than@redhat.com> - 1:1.8.15-7
- added Requirement on dot

* Thu Feb 14 2019 Than Ngo <than@redhat.com> - 1:1.8.15-6
- fixed bz#1677000, fixed multilib issue

* Tue Feb 12 2019 Than Ngo <than@redhat.com> - 1:1.8.15-5
- fixed bz#1675288, doxygen 1.8.15 segfault

* Fri Feb 08 2019 Than Ngo <than@redhat.com> - 1:1.8.15-4
- fixed bz#673228 - operator whitespace changes cause wxpython FTBFS
- fixed bz#1673230 - BR on tex(newunicodechar.sty) in doxygen-latex 

* Tue Feb 05 2019 Than Ngo <than@redhat.com> - 1:1.8.15-3
- fixed bz#1671999, backported from upstream
- added test for XML output with an empty TOC

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Than Ngo <than@redhat.com> - 1:1.8.15-1
- update to 1.8.15

* Thu Dec 06 2018 Than Ngo <than@redhat.com> - 1:1.8.14-8
- enable testing 

* Mon Jul 23 2018 Than Ngo <than@redhat.com> - 1:1.8.14-7
- add BR: gcc-c++ gcc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Than Ngo <than@redhat.com> - 1:1.8.14-5
- support Qt5

* Wed Jun 20 2018 Than Ngo <than@redhat.com> - 1.8.14-4
- enble search addon on fedora

* Mon Apr 30 2018 Than Ngo <than@redhat.com> - 1.8.14-3
- added missing BR on adjustbox.sty for refman

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 29 2017 Than Ngo <than@redhat.com> - 1:1.8.14-1
- update to 1.8.14

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 1:1.8.13-10
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Tue Jul 04 2017 Than Ngo <than@redhat.com> - 1:1.8.13-9
- backport to fix C# property initializer parsing 
- backport to fix non reachable links and redirected links in documentation

* Tue May 30 2017 Than Ngo <than@redhat.com> - 1:1.8.13-8
- backport to fix problem where automatic line breaking caused
  missing vertical bars in the parameter table for Latex output

* Sat Apr 22 2017 Karsten Hopp <karsten@redhat.com> - 1.8.13-7
- fix _module_build macro

* Fri Apr 21 2017 Karsten Hopp <karsten@redhat.com> - 1.8.13-6
- use new _module_build macro to limit dependencies for Modularity

* Mon Mar 13 2017 Than Ngo <than@redhat.com> - 1:1.8.13-5
- backport to fix behavior of @ref const matching (#776988)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Than Ngo <than@redhat.com> - 1:1.8.13-3
- Bug 775493 - Usage of underscore's in parameter names

* Tue Jan 17 2017 Björn Esser <besser82@fedoraproject.org> - 1:1.8.13-2
- Add upstream patch to fix regression (rhbz#1413296)

* Thu Dec 29 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.8.13-1
- Update to 1.8.13
- Drop upstream patches

* Thu Dec 22 2016 Orion Poplawski <orion@cora.nwra.com> - 1:1.8.12-7
- Rebuild for xapian soname bump
- Add patch to build with python rc

* Mon Dec 12 2016 Than Ngo <than@redhat.com> - 1:1.8.12-6
- backport upstream patch to fix
    Bug 707266 - C++/CLI indexed property not documented
    Bug 774949 - Unknown reference in manual
    Bug 775245 - referencing Python files via tagfile broken

* Thu Dec 08 2016 Than Ngo <than@redhat.com> - 1:1.8.12-5
- fixed bz#1402043 - runtime dependency on perl
- backport upstream patch to fix Bug 774138 . add HTML classes to "Definition at..." & "Referenced by..." for CSS

* Fri Nov 25 2016 Than Ngo <than@redhat.com> - - 1:1.8.12-4
- Bug 774273 - INLINE_SIMPLE_STRUCTS with enums in classes does not work

* Tue Nov 15 2016 Than Ngo <than@redhat.com> - 1:1.8.12-3
- bz#1394456, add missing docs
- fix build issue when build_doc=ON

* Thu Oct 20 2016 Than Ngo <than@redhat.com> - 1:1.8.12-2
- backport upstream fixes
  Bug 771310 - French description for "Namespace Members" is wrong and causes fatal javascript error
  Bug 771344 - Class name 'internal' breaks class hierarchy in C++

* Tue Sep 06 2016 Than Ngo <than@redhat.com> - 1:1.8.12-1
- 1.8.12
- fixed bz#1373167 - doxygen ships bogus man pages 

* Sun Mar 06 2016 Than Ngo <than@redhat.com> - 1:1.8.11-4
- bz#1305739, Unescaped percent sign in doxygen

* Mon Feb 22 2016 Than Ngo <than@redhat.com> - 1:1.8.11-3
- fix bz#1305739, Unescaped percent sign in doxygen

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Than Ngo <than@redhat.com> - 1:1.8.11-1
- 1.8.11

* Fri Dec 04 2015 Than Ngo <than@redhat.com> - 1:1.8.10-7
- backport to fix a couple of small memory leaks

* Tue Nov 10 2015 Than Ngo <than@redhat.com> - 1:1.8.10-6
- backport patches to fix follow issues:
   angle brackets (< and >) not escaped in HTML formula alt text
   don't support longer key in bibtex
   math does not work in LaTeX with custom header and footer
   writeMemberNavIndex template calls static fixSpaces
   XML empty <argsstring/> in python
   XML not documenting a class in python
   add option to build latex without timestamps

* Mon Nov 09 2015 Than Ngo <than@redhat.com> - 1:1.8.10-5
- fix install issue

* Thu Oct 08 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1:1.8.10-4
- Fix patch to apply

* Thu Oct 08 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1:1.8.10-3
- drop QT_ARCH_X86_64 hardcoded definition to get doxygen built on aarch64
  (it built by pure luck on other architectures)

* Wed Sep 23 2015 Than Ngo <than@redhat.com> - 1.8.10-2
- fix broken deps

* Fri Aug 28 2015 Than Ngo <than@redhat.com> - 1.8.10-1
- update to 1.8.10

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Than Ngo <than@redhat.com> - 1:1.8.9.1-3
- rebuild

* Wed Apr 29 2015 Than Ngo <than@redhat.com> - 1:1.8.9.1-2
- Resolves: bz#1198355, doxygen generates \backmatter in article class

* Wed Jan 21 2015 Than Ngo <than@redhat.com> 1:1.8.9.1-1
- update to 1.8.9.1

* Mon Aug 25 2014 Than Ngo <than@redhat.com> - 1:1.8.8-1
- 1.8.8

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Than Ngo <than@redhat.com> - 1:1.8.7-1
- 1.8.7

* Thu Dec 26 2013 Orion Poplawski <orion@cora.nwra.com> - 1:1.8.6-1
- 1.8.6

* Tue Oct 08 2013 Than Ngo <than@redhat.com> - 1:1.8.5-2
- add exlive-epstopdf-bin in requirement

* Mon Aug 26 2013 Than Ngo <than@redhat.com> - 1:1.8.5-1
- 1.8.5

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> - 1:1.8.4-4
- Work around strange dependencies in epstopdf packages (#991699)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Than Ngo <than@redhat.com> - 1:1.8.4-2
- backport upstream patch to fix endless loop

* Tue May 21 2013 Than Ngo <than@redhat.com> - 1:1.8.4-1
- 1.8.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Than Ngo <than@redhat.com> - 1.8.3.1-1
- 1.8.3.1
- fedora/rhel condition

* Tue Jan 08 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:1.8.3-3
- -latex subpkg (#892288)
- .spec cleanup

* Thu Jan 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 1:1.8.3-2
- doxygen is missing dependencies for texlive update (#891452)
- doxywizard: tighten dep on main pkg

* Wed Jan 02 2013 Than Ngo <than@redhat.com> - 1:1.8.3-1
- 1.8.3

* Mon Aug 13 2012 Than Ngo <than@redhat.com> - 1:1.8.2-1
- 1.8.2

* Mon Jul 30 2012 Than Ngo <than@redhat.com> - 1:1.8.1.2-1
- 1.8.1.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Than Ngo <than@redhat.com> - 1:1.8.1.1-3
- bz#832525, fix multilib issue

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1:1.8.1.1-2
- make HTML_TIMESTAMP default FALSE

* Mon Jun 11 2012 Than Ngo <than@redhat.com> - 1:1.8.1.1-1
- 1.8.1.1

* Wed Jun 06 2012 Than Ngo <than@redhat.com> - 1:1.8.1-1
- 1.8.1

* Mon Feb 27 2012 Than Ngo <than@redhat.com> - 1:1.8.0-1
- 1.8.0

* Wed Jan 18 2012 Than Ngo <than@redhat.com> - 1:1.7.6.1-2
- bz#772523, add desktop file

* Fri Dec 16 2011 Than Ngo <than@redhat.com> - 1:1.7.6.1-1
- 1.7.6.1

* Tue Dec 06 2011 Than Ngo <than@redhat.com> - 1:1.7.6-1
- 1.7.6

* Tue Nov 08 2011 Than Ngo <than@redhat.com> - 1:1.7.5.1-1
- 1.7.5.1

* Tue Aug 23 2011 Than Ngo <than@redhat.com> - 1:1.7.5-1
- 1.7.5

* Mon Jun 27 2011 Than Ngo <than@redhat.com> - 1:1.7.4-2
- bz#688684, apply patch to fix crash when not generating man format

* Tue Mar 29 2011 Than Ngo <than@redhat.com> - 1.7.4-1
- 1.7.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Than Ngo <than@redhat.com> - 1.7.3-1
- 1.7.3
- bz#661107

* Fri Nov 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.7.2-2
- Wrong Buildrequire to qt-devel (#651064)

* Mon Oct 11 2010 Than Ngo <than@redhat.com> - 1.7.2-1
- 1.7.2

* Wed Sep 08 2010 Than Ngo <than@redhat.com> - 1:1.7.1-2
- bz#629286, apply patch to fix broken thread handling
- bz#627553, #define in included file in different directory not handled properly
- Inherited documentation doesn't work in case of multiple inheritance

* Mon Jul 19 2010 Than Ngo <than@redhat.com> - 1.7.1-1
- 1.7.1

* Fri Feb 12 2010 Than Ngo <than@redhat.com> - 1.6.2-1.svn20100208
- fix #555526, snapshot 1.6.2-20100208

* Mon Jan 04 2010 Than Ngo <than@redhat.com> - 1:1.6.2-1
- 1.6.2

* Fri Dec 18 2009 Than Ngo <than@redhat.com> - 1:1.6.1-4
- drop _default_patch_fuzz

* Fri Dec 18 2009 Than Ngo <than@redhat.com> - 1:1.6.1-3
- bz#225709, merged review

* Fri Dec 11 2009 Than Ngo <than@redhat.com> - 1:1.6.1-2
- bz#225709, merged review 

* Tue Aug 25 2009 Than Ngo <than@redhat.com> - 1.6.1-1
- 1.6.1

* Mon Aug 24 2009 Than Ngo <than@redhat.com> - 1.6.0-2
- fix #516339, allow to enable/disable timstamp to avoid the multilib issue
  HTMP_TIMESTAMP is disable by default

* Fri Aug 21 2009 Than Ngo <than@redhat.com> - 1.6.0-1
- 1.6.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.9-3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Than Ngo <than@redhat.com> - 1.5.9-1
- 1.5.9

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Than Ngo <than@redhat.com> 1.5.8-1
- 1.5.8

* Mon Oct 06 2008 Than Ngo <than@redhat.com> 1.5.7.1-1
- 1.5.7.1

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.6-3
- fix license tag

* Wed May 21 2008 Than Ngo <than@redhat.com> 1.5.6-2
- rebuild

* Mon May 19 2008 Than Ngo <than@redhat.com> 1.5.6-1
- 1.5.6

* Fri Mar 14 2008 Than Ngo <than@redhat.com> 1.5.5-3
- apply patch to not break partial include paths, thanks to Tim Niemueller

* Wed Feb 20 2008 Than Ngo <than@redhat.com> 1.5.5-2
- apply patch to make doxygen using system libpng/zlib

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 1.5.5-1
- 1.5.5

* Wed Nov 28 2007 Than Ngo <than@redhat.com> 1.5.4-1
- 1.5.4

* Fri Aug 10 2007 Than Ngo <than@redhat.com> - 1:1.5.3-1
- 1.5.3

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 1:1.5.2-1
- 1.5.2

* Fri Nov 03 2006 Than Ngo <than@redhat.com> 1:1.5.1-2
- 1.5.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.7-1.1
- rebuild

* Mon Jun 12 2006 Than Ngo <than@redhat.com> 1:1.4.7-1
- update to 1.4.7

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-5
- fix build problem in mock #193358 

* Fri May 12 2006 Than Ngo <than@redhat.com> 1:1.4.6-4
- apply patch to fix Doxygen crash on empty file #191392 
- html docs #187177 

* Wed Mar 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-3
- fix typo bug #184400

* Mon Mar 06 2006 Than Ngo <than@redhat.com> 1:1.4.6-2
- fix build problem #184042

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Than Ngo <than@redhat.com> 1.4.6-1
- 1.4.6

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 1.4.5-3
- apply patch to fix build problem with gcc-4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com>
- fix references to /usr/X11R6

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.4.5

* Mon Sep 19 2005 Than Ngo <than@redhat.com> 1:1.4.4-2
- move doxywizard man page to subpackge doxywizard

* Thu Jul 21 2005 Than Ngo <than@redhat.com> 1:1.4.4-1
- update to 1.4.4

* Tue Jun 14 2005 Than Ngo <than@redhat.com> 1.4.3-1
- 1.4.3

* Thu Mar 31 2005 Than Ngo <than@redhat.com> 1:1.4.2-1
- 1.4.2

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:1.4.1-2
- rebuilt against gcc-4

* Wed Jan 19 2005 Than Ngo <than@redhat.com> 1:1.4.1-1
- update to 1.4.1

* Sun Oct 10 2004 Than Ngo <than@redhat.com> 1:1.3.9.1-1
- update to 1.3.9.1

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 1:1.3.9-1
- update to 1.3.9

* Sun Jul 25 2004 Than Ngo <than@redhat.com> 1:1.3.8-1
- update to 1.3.8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Than Ngo <than@redhat.com> 1.3.7-1
- update to 1.3.7, bug #119340

* Sun Apr 04 2004 Than Ngo <than@redhat.com> 1:1.3.6-2
- fix qt-mt linking problem

* Thu Feb 26 2004 Than Ngo <than@redhat.com> 1:1.3.6-1
- update to 1.3.6
- added more buildrequires, #110752

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 17 2003 Than Ngo <than@redhat.com> 1:1.3.5-1
- 1.3.5 release

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1:1.3.4-1
- update to 1.3.4
- doxsearch was removed

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without qt/doxywizard

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Than Ngo <than@redhat.com> 1.3-1
- 1.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 27 2002 Than Ngo <than@redhat.com> 1.2.18-2
- use gnu install

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 1.2.18-1.2
- fix some build problem

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 1.2.18-1
- 1.2.18

* Wed Aug 28 2002 Than Ngo <than@redhat.com> 1.2.17-1
- 1.2.17 fixes many major bugs

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-5
- rebuild against qt 3.0.3-10

* Fri Mar  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-4
- rebuild against qt 3.0.2

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.2.14-2
- rebuild against qt 2.3.2

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.14-1
- 1.2.14

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jan 06 2002 Than Ngo <than@redhat.com> 1.2.13.1-1
- update to 1.2.13.1
- fixed build doxywizard with qt3

* Sun Dec 30 2001 Jeff Johnson <jbj@redhat.com> 1.2.13-1
- update to 1.2.13

* Sun Nov 18 2001 Than Ngo <than@redhat.com> 1.2.12-1
- update to 1.2.12
- s/Copyright/License

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Wed Jun 13 2001 Than Ngo <than@redhat.com>
- update tp 1.2.8.1
- make doxywizard as separat package
- fix to use install as default

* Tue Jun 05 2001 Than Ngo <than@redhat.com>
- update to 1.2.8

* Tue May 01 2001 Than Ngo <than@redhat.com>
- update to 1.2.7
- clean up specfile
- patch to use RPM_OPT_FLAG

* Wed Mar 14 2001 Jeff Johnson <jbj@redhat.com>
- update to 1.2.6

* Wed Feb 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Dec 26 2000 Than Ngo <than@redhat.com>
- update to 1.2.4
- remove excludearch ia64
- bzip2 sources

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- rebuild with the fixed fileutils

* Mon Oct 30 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.3.

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.2.
- enable doxywizard.

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- 1.2.1 is latest stable, so we upgrade before Winston is released.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Florian La Roche <laroche@redhat.de>
- fix QTDIR detection

* Fri Jun 09 2000 Preston Brown <pbrown@redhat.com>
- compile on x86 w/o optimization, revert when compiler fixed!!

* Wed Jun 07 2000 Preston Brown <pbrown@redhat.com>
- use newer RPM macros

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- add to distro.

* Tue May  9 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- recompile with current Qt (2.1.0/1.45)

* Wed Jan  5 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.0.0.
- recompile with qt-2.0.1 if available.
- relocatable package.

* Mon Nov  8 1999 Tim Powers <timp@redhat.com>
-updated to 0.49-991106

* Tue Jul 13 1999 Tim Powers <timp@redhat.com>
- updated source
- cleaned up some stuff in the spec file

* Thu Apr 22 1999 Jeff Johnson <jbj@redhat.com>
- Create Power Tools 6.0 package.
