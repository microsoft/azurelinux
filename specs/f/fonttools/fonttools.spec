# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1

# Some extras are disabled in RHEL to avoid bringing in additional
# dependencies.
#
# Requires python-lz4:
%bcond graphite_extra %[ %{undefined rhel} || %{defined epel} ]
# Requires python-skia-pathops, not packaged:
%bcond pathops_extra 0
# Requires python-matplotlib:
%bcond plot_extra %[ %{undefined rhel} || %{defined epel} ]
# Requires python-uharfbuzz, currently only in F42+
%bcond repacker_extra %[ 0%{?fedora} > 41 ]
# Requires python-sympy (not yet in any EPEL):
%bcond symfont_extra %{undefined rhel}
# Requires python-fs:
%bcond ufo_extra %[ %{undefined rhel} || %{defined epel} ]
# Requires python-brotli, python-zopfli:
%bcond woff_extra %[ %{undefined rhel} || %{defined epel} ]
# Requires scipy, munkres, pycairo
%bcond interpolatable_extra 1


%global desc %{expand:
fontTools is a library for manipulating fonts, written in Python. The project
includes the TTX tool, that can convert TrueType and OpenType fonts to and from
an XML text format, which is also called TTX. It supports TrueType, OpenType,
AFM and to an extent Type 1 and some Mac-specific formats.}

Name:           fonttools
Version:        4.61.0
Release: 2%{?dist}
Summary:        Tools to manipulate font files

# https://spdx.org/licenses/MIT.html
License:        MIT
URL:            https://github.com/fonttools/fonttools/
Source:         %{url}/archive/%{version}/fonttools-%{version}.tar.gz

Requires:       python3-fonttools = %{version}-%{release}
Provides:       ttx = %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  gcc

%if %{with tests}
# A few additional requirements for specific tests, noted in requirements.txt:
BuildRequires:  %{py3_dist pytest}
# Not included in RHEL, but available in EPEL:
%if %{undefined rhel} || %{defined epel}
BuildRequires:  %{py3_dist pytest-randomly}
%endif
# For Tests/cu2qu/{ufo,cli}_test.py
# Not yet in EPEL10:
%if %{undefined rhel} || (%{defined epel} && !%{defined el10})
BuildRequires:  %{py3_dist ufoLib2}
%endif
# Not yet in any EPEL:
%if %{undefined rhel}
BuildRequires:  %{py3_dist ufo2ft}
%endif

# For Tests/pens/freetypePen_test.py
%if %{undefined rhel} || (%{defined epel} && !%{defined el10})
BuildRequires:  %{py3_dist freetype-py}
%global have_freetype_py 1
%endif

# For Tests/varLib/interpolatable_test.py
# Not yet in any EPEL:
%if %{undefined rhel}
BuildRequires:  %{py3_dist glyphsLib}
%endif
%endif

%description %{desc}

%package -n python3-fonttools
Summary:        Python 3 fonttools library

# From 3.31.0 and on, python3-fonttools incorporated the ufolib project under fontTools.ufoLib
# python-ufolib has been retired and fontTools.ufoLib should be used instead.
# See https://github.com/fonttools/fonttools/releases/tag/3.31.0 for further reference
Obsoletes: python3-ufolib <= 2.1.1-11

%description -n python3-fonttools %{desc}

# Cannot package “all” extra unless dependencies for all individual extras
# become satisfiable.
%if %{with graphite_extra}
%pyproject_extras_subpkg -n python3-fonttools graphite
%endif
%if %{with interpolatable_extra}
%pyproject_extras_subpkg -n python3-fonttools interpolatable
%endif
%pyproject_extras_subpkg -n python3-fonttools lxml
%if %{with pathops_extra}
%pyproject_extras_subpkg -n python3-fonttools pathops
%endif
%if %{with plot_extra}
%pyproject_extras_subpkg -n python3-fonttools plot
%endif
%if %{with repacker_extra}
%pyproject_extras_subpkg -n python3-fonttools repacker
%endif
%if %{with symfont_extra}
%pyproject_extras_subpkg -n python3-fonttools symfont
%endif
%pyproject_extras_subpkg -n python3-fonttools type1
%if %{with ufo_extra}
%pyproject_extras_subpkg -n python3-fonttools ufo
%endif
%pyproject_extras_subpkg -n python3-fonttools unicode
%if %{with woff_extra}
%pyproject_extras_subpkg -n python3-fonttools woff
%endif

%prep
%autosetup -p1

# Remove shebang
sed -r -i '1{/^#!/d}' Lib/fontTools/mtiLib/__init__.py

%generate_buildrequires
export FONTTOOLS_WITH_CYTHON=1
# We use tox to get things like pytest, but we add extras manually since not
# all dependencies from requirements.txt might be satisfiable and not all
# extras might be packaged; plus, requirements.txt pins exact versions.
%{pyproject_buildrequires \
    %{?with_graphite_extra:-x graphite} \
    %{?with_interpolatable_extra:-x interpolatable} \
    -x lxml \
    %{?with_pathops_extra:-x pathops} \
    %{?with_plot_extra:-x plot} \
    %{?with_repacker_extra:-x repacker} \
    %{?with_symfont_extra:-x symfont} \
    -x type1 \
    %{?with_ufo_extra:-x ufo} \
    -x unicode \
    %{?with_woff_extra:-x woff} \
    }

%build
export FONTTOOLS_WITH_CYTHON=1
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l fontTools

%check
# - fontTools.misc.symfont requires python3dist(sympy), i.e., the symfont extra
# - fontTools.pens.freetypePen requires python3dist(freetype-py)
# - fontTools.pens.quartzPen only works on Darwin
# - fontTools.pens.reportLabPen requires python3dist(reportlab), and it is not
#   worth adding the BuildRequires just for the import check
# - fontTools.ttLib.removeOverlaps requires python3dist(skia-pathops), i.e., the
#   pathops extra
# - fontTools.ufoLib(.*) requires python3dist(fs), i.e., the ufo extra
# - fontTools.varLib.plot requires python3dist(matplotlib), i.e., the plot
#   extra
%{pyproject_check_import \
    %{?!with_symfont_extra:-e fontTools.misc.symfont} \
    %{?!have_freetype_pen:-e fontTools.pens.freetypePen} \
    -e fontTools.pens.quartzPen \
    -e fontTools.pens.reportLabPen \
    %{?!with_pathops_extra:-e fontTools.ttLib.removeOverlaps} \
    %{?!with_ufo_extra:-e fontTools.ufoLib*} \
    %{?!with_plot_extra:-e fontTools.varLib.plot} \
    %{?!with_interpolatable_extra:-e fontTools.varLib.interpolatable*} \
    %{nil}}

%if %{with tests}
%if %{without ufo_extra}
# These tests pertain to the interpolatable extra, but also require the ufo
# extra (even though the interpolatable extra as a whole does not):
k="${k-}${k+ and }not (InterpolatableTest and test_designspace)"
k="${k-}${k+ and }not (InterpolatableTest and test_interpolatable_ufo)"
k="${k-}${k+ and }not (InterpolatableTest and test_sparse_designspace)"
k="${k-}${k+ and }not (InterpolatableTest and test_sparse_interpolatable_ufos)"
%endif

# Below test is randomly failing on any arch, mostly the arch on which build runs
k="${k-}${k+ and }not (test_ttcompile_timestamp_calcs)"

%pytest ${ignore-} -k "${k-}" -rs -v
%endif

%files
%{_bindir}/pyftmerge
%{_bindir}/pyftsubset
%{_bindir}/ttx
%{_bindir}/fonttools
%{_mandir}/man1/ttx.1*

%files -n python3-fonttools -f %{pyproject_files}
%doc NEWS.rst README.rst

%changelog
* Tue Dec 09 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.61.0-1
- Update to 4.61.0 version (#2419183)

* Thu Oct 02 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.60.1-1
- Update to 4.60.1 version (#2400374)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.60.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 17 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.60.0-1
- Update to 4.60.0 version (#2396057)

* Thu Aug 28 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.59.2-1
- Update to 4.59.2 version (#2391330)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.59.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Aug 15 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.59.1-1
- Update to 4.59.1 version (#2388618)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.59.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.59.0-2
- Skip failing test test_ttcompile_timestamp_calcs

* Wed Jul 16 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.59.0-1
- Update to 4.59.0 version (#2381317)

* Fri Jul 04 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.58.5-1
- Update to 4.58.5 version (#2376209)

* Mon Jun 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.58.4-1
- Update to 4.58.4 version (#2370864)
- No longer bootstrapping (build with tests enabled)

* Sun Jun 15 2025 Python Maint <python-maint@redhat.com> - 4.58.1-3
- Bootstrap for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.58.1-2
- Bootstrap for Python 3.14

* Thu May 29 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.58.1-1
- Update to 4.58.1 version (#2368984)

* Mon May 12 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.58.0-1
- Update to 4.58.0 version (#2365442)

* Fri Apr 04 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.57.0-1
- Update to 4.57.0 version (#2357231)

* Sun Mar 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.56.0-2
- Enable the repacker extra in F42+

* Sat Feb 08 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.56.0-1
- Update to 4.56.0 version (#2342588)

* Sat Jan 25 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.55.6-1
- Update to 4.55.6 version (#2341748)

* Thu Jan 23 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.55.5-1
- Update to 4.55.5 version (#2341748)

* Wed Jan 22 2025 Parag Nemade <pnemade AT redhat DOT com> - 4.55.4-1
- Update to 4.55.4 version (#2339159)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.55.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Romain Geissler <romain.geissler@amadeus.com> - 4.55.3-3
- Build the graphite subpackage on EPEL 10 now that python-lz4 is available.

* Wed Dec 18 2024 Romain Geissler <romain.geissler@amadeus.com> - 4.55.3-2
- Update extra dependencies for EPEL.

* Sun Dec 15 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.55.3-1
- Update to 4.55.3 version (#2331592)

* Sat Dec 07 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.55.2-1
- Update to 4.55.2 version (#2330109)

* Fri Nov 15 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.55.0-1
- Update to 4.55.0 version (#2326307)

* Tue Nov 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.54.1-3
- Avoid tox dependency

* Fri Oct 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 4.54.1-2
- Port to pyproject-rpm-macros (modern Python guidelines)

* Wed Sep 25 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.54.1-1
- Update to 4.54.1 version (#2314462)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.53.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.53.1-1
- Update to 4.53.1 version (#2296086)

* Thu Jun 27 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.53.0-1
- Update to 4.53.0 version (#2284160)

* Mon Jun 17 2024 Python Maint <python-maint@redhat.com> - 4.52.4-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.52.4-2
- Bootstrap for Python 3.13

* Tue May 28 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.52.4-1
- Update to 4.52.4 version (#2283255)

* Tue May 28 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.51.0-2
- Generate extra subpackages only for Fedora release

* Wed Apr 10 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.51.0-1
- Update to 4.51.0 version (#2273774)

* Sat Mar 16 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.50.0-1
- Update to 4.50.0 version (#2269759)

* Sat Feb 17 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.49.0-1
- Update to 4.49.0 version (#2264616)

* Wed Feb 07 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.48.1-1
- Update to 4.48.1 version (#2263197)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.47.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.47.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Lumír Balhar <lbalhar@redhat.com> - 4.47.2-2
- Remove version limit from lxml

* Fri Jan 12 2024 Parag Nemade <pnemade AT redhat DOT com> - 4.47.2-1
- Update to 4.47.2 version (#2257911)

* Wed Dec 20 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.47.0-1
- Update to 4.47.0 version (#2255170)

* Tue Dec 05 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.46.0-1
- Update to 4.46.0 version (#2252586)

* Fri Dec 01 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.45.1-1
- Update to 4.45.1 version (#2250746)

* Thu Nov 16 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.44.3-1
- Update to 4.44.3 version (#2249771)

* Sun Nov 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.44.0-1
- Update to 4.44.0 version (#2247927)

* Sun Oct 08 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.43.1-1
- Update to 4.43.1 version (#2241574)

* Tue Aug 22 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.42.1-1
- Update to 4.42.1 version (#2232931)

* Wed Aug 09 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 4.42.0-2
- Skip unwanted test dependencies in RHEL builds

* Thu Aug 03 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.42.0-1
- Update to 4.42.0 version (#2228656)

* Mon Jul 24 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.41.1-1
- Update to 4.41.1 version (#2224718)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.41.0-1
- Update to 4.41.0 version (#2222762)

* Fri Jul 07 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.40.0-3
- Help msuchy to count this package as already using SPDX license expression

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.40.0-2
- Rebuilt for Python 3.12

* Sun Jun 18 2023 Benson Muite <benson_muite@emailplus.org> - 4.40.0-1
- Update to 4.40.0 version

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.39.4-2
- Bootstrap for Python 3.12

* Thu May 11 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.39.4-1
- Update to 4.39.4 version (#2198487)

* Wed Mar 29 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.39.3-1
- Update to 4.39.3 version (#2182480)

* Mon Mar 20 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.39.2-1
- Update to 4.39.2 version (#2179416)

* Tue Mar 07 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.39.0-1
- Update to 4.39.0 version (#2176001)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 24 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.38.0-1
- Update to 4.38.0 version (#2137001)

* Mon Oct 03 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.37.4-1
- Update to 4.37.4 version (#2131432)

* Sun Sep 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.37.3-1
- Update to 4.37.3 version (#2128605)

* Fri Sep 16 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.37.2-1
- Update to 4.37.2 version (#2127330)

* Thu Aug 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.37.1-1
- Update to 4.37.1 version (#2120891)

* Thu Aug 18 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.36.0-1
- Update to 4.36.0 version (#2119236)

* Wed Aug 17 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.35.0-1
- Update to 4.35.0 version (#2118800)

* Fri Jul 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 4.34.4-3
- Enable Cython acceleration; the package is no longer noarch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.34.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Parag Nemade <pnemade@fedoraproject.org> - 4.34.4-1
- Update to 4.34.4 version (#2104988)

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.33.3-2
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.33.3-1
- Update to 4.33.3 version (#2079108)

* Mon Apr 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.33.2-1
- Update to 4.33.2 version (#2077754)

* Tue Apr 12 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.32.0-1
- Update to 4.32.0 version (#2073543)

* Wed Mar 23 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.31.2-1
- Update to 4.31.2 version (#2065959)

* Mon Mar 14 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.30.0-1
- Update to 4.30.0 version (#2063182)

* Thu Feb 03 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.29.1-1
- Update to 4.29.1 version (#2049408)

* Tue Jan 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.29.0-1
- Update to 4.29.0 version (#2044666)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.28.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.28.5-1
- Update to 4.28.5 version (#2033126)

* Mon Dec 13 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 4.28.3-2
- Add missing extras metapackages: graphite, interpolatable, lxml, plot,
  symfont, type1

* Mon Dec 06 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.28.3-1
- Update to 4.28.3 version (#2029061)

* Tue Nov 30 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.28.2-1
- Update to 4.28.2 version (#2025382)

* Mon Nov 08 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.28.1-1
- Update to 4.28.1 version (#2021206)

* Sat Nov 06 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.28.0-1
- Update to 4.28.0 version (#2020845)

* Tue Sep 28 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.27.1-1
- Update to 4.27.1 version (#2007503)

* Sat Sep 18 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.27.0-1
- Update to 4.27.0 version (#2004586)

* Mon Aug 16 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.26.2-1
- Update to 4.26.2 version (#1991789)

* Sat Aug 07 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.26.1-2
- Add woff functionality subpackage
- Rewrite separate BR's required to run test files

* Wed Aug 04 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.26.1-1
- Update to 4.26.1 version (#1989769)

* Tue Jul 27 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.25.2-1
- Update to 4.25.2 version (#1986153)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.25.1-1
- Update to 4.25.1 version (#1983287)

* Mon Jul 12 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.25.0-1
- Update to 4.25.0 version (#1979468)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.24.4-2
- Rebuilt for Python 3.10

* Fri May 28 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.24.4-1
- Update to 4.24.4 version (#1964877)

* Fri May 21 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.24.3-1
- Update to 4.24.3 version (#1963105)

* Fri May 21 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.24.2-1
- Update to 4.24.2 version (#1962823)

* Tue May 18 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.24.0-1
- Update to 4.24.0 version (#1961440)

* Sat May 15 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.23.1-1
- Update to 4.23.1 version (#1960473)

* Wed Apr 28 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.22.1-1
- Update to 4.22.1 version (#1953840)

* Fri Apr 02 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.22.0-1
- Update to 4.22.0 version (#1945743)

* Sun Feb 28 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.21.1-1
- Update to 4.21.1 version (#1933357)

* Tue Feb 16 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.20.0-1
- Update to 4.20.0 version (#1929113)

* Tue Feb  2 14:32:49 IST 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.19.1-1
- Update to 4.19.1 version (#1921968)

* Wed Jan 27 10:02:16 IST 2021 Parag Nemade <pnemade AT redhat DOT com> - 4.19.0-1
- Update to 4.19.0 version (#1920265)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 13:37:03 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.18.2-1
- Update to 4.18.2 version (#1908485)

* Fri Dec 11 18:47:51 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.18.1-1
- Update to 4.18.1 version (#1906095)

* Sat Dec  5 09:13:23 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.18.0-1
- Update to 4.18.0 version (#1904631)

* Sat Nov 21 08:48:57 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.17.1-1
- Update to 4.17.1 version (#1898343)

* Fri Nov 13 12:13:39 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.17.0-1
- Update to 4.17.0 version (#1897467)

* Sun Oct 18 16:32:27 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.16.1-1
- Update to 4.16.1 version (#1885448)

* Thu Oct  1 08:45:20 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.16.0-1
- Update to 4.16.0 version (#1884087)

* Tue Sep 22 10:40:10 IST 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.15.0-1
- Update to 4.15.0 version (#1881283)

* Thu Aug 20 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.14.0-1
- Update to 4.14.0 version (#1870253)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Miro Hrončok <mhroncok@redhat.com> - 4.13.0-2
- Add fonttools[ufo] and fonttools[unicode] subpackages

* Sat Jul 11 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.13.0-1
- Update to 4.13.0 version (#1855929)

* Wed Jun 24 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.12.1-3
- Add missing BR: python3-setuptools

* Sun Jun 21 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 4.12.1-2
- Obsolete retired python3-ufolib package

* Tue Jun 16 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.12.1-1
- Update to 4.12.1 version (#1847541)

* Mon Jun 01 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.11.0-1
- Update to 4.11.0 version (#1841433)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.10.2-2
- Rebuilt for Python 3.9

* Wed May 20 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.10.2-1
- Update to 4.10.2 version (#1837964)

* Wed May 20 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.10.1-1
- Update to 4.10.1 version (#1837643)

* Sun May 17 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.10.0-1
- Update to 4.10.0 version (#1836575)

* Fri May 08 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.9.0-3
- enable tests

* Thu May 07 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.9.0-2
- Fix source tarball

* Thu May 07 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.9.0-1
- Update to 4.9.0 version (#1829451)

* Sat Apr 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.8.1-1
- Update to 4.8.1 version (#1824982)

* Wed Apr 15 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.7.0-1
- Update to 4.7.0 version (#1820763)

* Tue Mar 31 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.6.0-3
- Fix the changelog entry in previous build

* Tue Mar 31 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.6.0-2
- Resolves: rh#1809062 - Add missing Requires: on few packages

* Wed Mar 25 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.6.0-1
- Update to 4.6.0 version (#1816808)

* Sat Mar 21 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.5.0-1
- Update to 4.5.0 version (#1815641)

* Mon Mar 16 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.4.3-1
- Update to 4.4.3 version (#1813103)

* Thu Feb 27 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.4.1-1
- Update to 4.4.1 version (#1804509)

* Tue Feb 04 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.3.0-1
- Update to 4.3.0 version (#1796166)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 4.2.4-1
- Update to 4.2.4 version (#1788778)

* Fri Dec 13 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.2.2-1
- Update to 4.2.2 version (#1782256)

* Sat Nov 30 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.2.0-1
- Update to 4.2.0 version (#1777967)

* Tue Nov 19 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.1.0-1
- Update to 4.1.0 version (#1773756)

* Mon Sep 30 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.0.2-1
- Update to 4.0.2 version (#1755890)

* Wed Sep 11 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.0.1-1
- Update to 4.0.1 version (#1751254)

* Fri Aug 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 4.0.0-1
- Update to 4.0.0 version (#1744582)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.44.0-2
- Rebuilt for Python 3.8

* Sat Aug 17 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.44.0-1
- Update to 3.44.0 version (#1742448)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.43.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.43.1-1
- Update to 3.43.1 version (#1721658)

* Sat Jun 01 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.42.0-1
- Update to 3.42.0 version (#1714617)

* Tue May 14 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.41.2-1
- Update to 3.41.2 version (#1709287)

* Wed May 01 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.41.0-1
- Update to 3.41.0 version (#1704383)

* Fri Apr 12 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.40.0-1
- Update to 3.40.0 version (#1697579)

* Sat Mar 23 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.39.0-1
- Update to 3.39.0 version (#1690561)
- Removed python2 package

* Mon Feb 18 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.38.0-1
- Update to 3.38.0 version (#1678366)

* Tue Feb 12 2019 Kalev Lember <klember@redhat.com> - 3.37.3-2
- Add missing requires on python3-setuptools (#1676290)

* Wed Feb 06 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.37.3-1
- Update to 3.37.3 version (#1672607)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Parag Nemade <pnemade AT redhat DOT com> - 3.37.0-1
- Update to 3.37.0 version (#1670213)

* Fri Dec 21 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.34.2-1
- Update to 3.34.2 version

* Fri Nov 23 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.32.0-1
- Update to 3.32.0 version

* Thu Oct 25 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.31.0-1
- Update to 3.31.0 version (#1642082)

* Sat Jul 28 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.29.0-1
- Update to 3.29.0 version (#1609078)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.28.0-2
- Rebuilt for Python 3.7

* Sat Jun 23 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.28.0-1
- Update to 3.28.0 version
- License corrected to MIT as upstream changed it since 3.21.0 release

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.27.1-2
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.27.1-1
- Update to 3.27.1 version (#1591522)

* Mon May 07 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.26.0-1
- Update to 3.26.0 version (#1575168)

* Wed Apr 04 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.25.0-1
- Update to 3.25.0 version (#1563434)

* Tue Mar 27 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.24.2-1
- Update to 3.24.2 version (#1560987)

* Wed Mar 07 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.24.1-1
- Update to 3.24.1 version (#1552589)

* Fri Mar 02 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.24.0-1
- Update to 3.24.0 version (#1550749)

* Tue Feb 27 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.23.0-1
- Update to 3.23.0 version (#1549339)

* Thu Feb 08 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.22.0-1
- Update to 3.22.0 version (#1542272)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.21.2-1
- Update to 3.21.2 version (#1532417)

* Sun Jan 07 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.21.1-1
- Update to 3.21.1 version (#1530999)

* Thu Dec 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.21.0-1
- Update to 3.21.0 version (#1528078)

* Wed Nov 22 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.20.0-1
- Update to 3.20.0 version (#1515794)

* Wed Nov 08 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.19.0-1
- Update to 3.19.0 version (#1510218)

* Wed Nov 01 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.18.0-1
- Update to 3.18.0 version (#1508232)

* Tue Oct 03 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.16.0-1
- Update to 3.16.0 version (#1498063)

* Sun Aug 20 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.15.1-1
- Update to 3.15.1 version

* Tue Aug 01 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.14.0-1
- Update to 3.14.0 version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.13.1-1
- Update to 3.13.1 version

* Thu May 25 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.13.0-1
- Update to 3.13.0 version

* Wed May 03 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.11.0-1
- Update to 3.11.0 version

* Sun Apr 16 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.10.0-1
- Update to 3.10.0 version

* Sun Apr 09 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.9.2-1
- Update to 3.9.2 version

* Tue Mar 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.9.1-1
- Update to 3.9.1 version

* Tue Mar 14 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.9.0-1
- Update to 3.9.0 version

* Mon Mar 06 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.8.0-1
- Update to 3.8.0 version

* Sat Feb 18 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.7.2-1
- Update to 3.7.2 version

* Fri Feb 17 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.7.1-1
- Update to 3.7.1 version

* Sun Feb 12 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.7.0-1
- Update to 3.7.0 version

* Mon Feb 06 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.6.2-1
- Update to 3.6.2 version

* Sun Jan 29 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.6.1-1
- Update to 3.6.1 version

* Fri Jan 27 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.6.0-1
- Update docs file names
- Update to 3.6.0 version

* Mon Jan 16 2017 Parag Nemade <pnemade AT redhat DOT com> - 3.5.0-1
- Update to 3.5.0 version

* Thu Dec 22 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.4.0-1
- Update to 3.4.0 version

* Tue Dec 20 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.3.1-1
- Update to version 3.3.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.3.0-2
- Rebuild for Python 3.6

* Wed Dec 07 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.3.0-1
- Update to version 3.3.0
- This release removed top level sstruct and xmlWriter

* Mon Dec 05 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.2.3-1
- Update to version 3.2.3

* Tue Nov 29 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.2.2-2
- Resolves: rh#1278201 - ImportError: No module named 'pygtk' 

* Fri Nov 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.2.2-1
- Update to version 3.2.2

* Tue Nov 08 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.2.1-1
- Update to version 3.2.1

* Thu Nov 03 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.2.0-1
- Update to version 3.2.0

* Mon Oct 10 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.1.2-1
- Update to version 3.1.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Mar 06 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.0-4
- Resolves:rh#1240265- fonttools 2.5 takes too much memory

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 02 2015 Parag Nemade <pnemade AT redhat DOT com> - 3.0-1
- Updated to version 3.0

* Mon Jul 13 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.5-4
- Fix ttx execution backtrace (rh#1242549)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Nov 16 2014 Parag <pnemade AT redhat DOT com> - 2.5-2
- Upstream dropped file eexecOp.so so make this package noarch
- Change %%{python2_sitearch} to %%{python2_sitelib} python2 macros
- Fix URL tag (rh#1164448)

* Sat Nov 15 2014 Peter Oliver <rpm@mavit.org.uk> - 2.5-1
- Changed upstream to https://github.com/behdad/fonttools.
- Updated to version 2.5.
- Use python2 macros (Parag Nemade)
- Use released tarball (Parag Nemade)
- Remove optional group tag (Parag Nemade)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Parag <pnemade AT redhat DOT com> - 2.4-1
- New upstream release 2.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Parag <pnemade AT redhat DOT com> - 2.3-6
- Resolves:rh#880063 - BR: python2-devel required

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Akira TAGOH <tagoh@redhat.com> - 2.3-2
- Rebuild.

* Fri Jul 23 2010 Akira TAGOH <tagoh@redhat.com> - 2.3-1
- New upstream release. (Paul Williams, #599281)
  - drop upstreamed patch.
  - correct man page location.
- Update the spec file to keep consistensy of usage in the macro as far as possible.

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Oct 02 2009 Caolán McNamara <caolanm@redhat.com> - 2.2-7
* Resolves: rhbz#525444 as is a reserved keyword in python

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Roozbeh Pournader <roozbeh@gmail.com> - 2.2-5
* Change dependency on python-numeric to numpy

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2-3
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2-2
- Rebuild for Python 2.6

* Tue Sep 16 2008 Matt Domsch <mdomsch@fedoraproject.org> - 2.2-1
- update to 2.2, drop upstreamed patch, fix FTBFS BZ#434409

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0-0.12.20060223cvs
- Autorebuild for GCC 4.3

* Sat Dec 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.11.20060223cvs
- Rebuild for Python 2.5

* Fri Dec 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.10.20060223cvs
- Update the Unicode names file to Unicode 5.0.0

* Thu Nov 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.9.20060223cvs
- Update to newer CVS snapshot dated 2006-02-23
- Cleanup based on latest Python packaging guidelines

* Wed Nov 08 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.8.20050624cvs
- De-ghost .pyo files

* Wed Nov 08 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.7.20050624cvs
- Rebuild to get into Rawhide

* Mon May 08 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.6.20050624cvs
- Change specification of ulUnicodeRange1-4 to unsigned long

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.5.20050624cvs
- Rebuild for Fedora Extras 5

* Thu Feb 02 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.4.20050624cvs
- Provide ttx

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.3.20050624cvs
- Use upstream snapshots, moving the difference into a patch
- Change alphatag time to the latest change in CVS
- Use %%{python_sitearch} instead of %%{python_sitelib} (for x86_86)
- Use sed instead of a patch to remove shebang

* Sun Jan 08 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.2.20060103cvs
- Add %%{?dist} tag

* Fri Jan 06 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 2.0-0.1.20060103cvs
- Initial packaging
