# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-ujson
Version:        5.11.0
Release:        2%{?dist}
Summary:        Ultra fast JSON encoder and decoder written in pure C

# The entire source is BSD-3-Clause, except:
#
# ----
#
#   Portions of code from MODP_ASCII - Ascii transformations (upper/lower, etc)
#   https://github.com/client9/stringencoders
#
# BSD-3-Clause but with its own copyright statement
#
# ----
#
#   Numeric decoder derived from from TCL library
#   https://opensource.apple.com/source/tcl/tcl-14/tcl/license.terms
#
# TCL: possibly present in python/objToJSON.c, python/ujson.c, and/or
# python/JSONtoObj.c.
#
# ----
#
# Filed upstream:
#   Please consider including other licenses mentioned in LICENSE.txt
#   https://github.com/ultrajson/ultrajson/issues/565
License:        BSD-3-Clause AND TCL
URL:            https://github.com/ultrajson/ultrajson
Source0:        %{pypi_source ujson}

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  double-conversion-devel

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
UltraJSON is an ultra fast JSON encoder and decoder written in pure C with
bindings for Python.}

%description %{_description}

%package -n python3-ujson
Summary:        %{summary}

%description -n python3-ujson %{_description}

%prep
%autosetup -n ujson-%{version} -p1
# Remove bundled double-conversion
rm -rv src/ujson/deps

%generate_buildrequires
%pyproject_buildrequires

%build
export UJSON_BUILD_NO_STRIP=1
export UJSON_BUILD_DC_INCLUDES='%{_includedir}/double-conversion'
export UJSON_BUILD_DC_LIBS='-ldouble-conversion'
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l ujson

%check
%pytest -v

%files -n python3-ujson -f %{pyproject_files}
%doc README.md

%dir %{python3_sitearch}/ujson-stubs
%{python3_sitearch}/ujson-stubs/__init__.pyi

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Aug 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 5.11.0-1
- Update to 5.11.0 (close RHBZ#2389730)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.10.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 5.10.0-1
- Update to 5.10.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.9.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 5.9.0-1
- Update to 5.9.0 (close RHBZ#2253921)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 5.8.0-1
- Update to 5.8.0 (close RHBZ#2214034)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 5.7.0-4
- Rebuilt for Python 3.12

* Fri Mar 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 5.7.0-3
- Apply upstream PR#565 to add license texts to LICENSE.txt

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 5.7.0-1
- Update to 5.7.0 (close RHBZ#2158945)

* Thu Dec 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.6.0-1
- Update to 5.6.0 (close RHBZ#2149975)

* Sat Sep 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.5.0-1
- Update to 5.5.0 (closes RHBZ#2127227)
- Update License to SPDX and include additional license texts

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Alfredo Moralejo <amoralej@redhat.com> - 5.4.0-1
- Update to 5.4.0 (closes rhbz#2103379)
- Includes fixes for CVE-2022-31117 and CVE-2022-31116

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.3.0-2
- Rebuilt for Python 3.11

* Fri May 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.3.0-1
- Update to 5.3.0 (close RHBZ#2088232)

* Fri Apr 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.2.0-1
- Update to 5.2.0 (close RHBZ#2072241)
- Migrate to pyproject-rpm-macros (“new Python guidelines”)

* Sun Mar 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.1.0-1
- Update to 5.1.0 (close RHBZ#1862763)
- Unbundle double-conversion and prevent debug symbol stripping with separate
  patches, both offered upstream
- Drop obsolete %%python_provide macro

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jul 31 2021 Kushal Das <kushal@fedoraproject.org> 4.0.2-1
- Update to 4.0.2

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.0.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Kushal Das <kushal@fedoraproject.org> 3.0.0-1
- Update to 3.0.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.3.20170206git2f1d487
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0-0.2.20170206git2f1d487
- Subpackage python2-ujson has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0-0.1.20170206git2f1d487.9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0-0.1.20170206git2f1d487.5
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0-0.1.20170206git2f1d487.4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-0.1.20170206git2f1d487.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Adam Williamson <awilliam@redhat.com> - 2.0-0.1.20170206git2f1d487
- Update to pre-2.0 git snapshot, removes non-standard serialization behaviour

* Sun Jan 01 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.35-1
- Update to 1.35
- Run test suite
- Spec cleanups

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.33-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 1.33-2
- Rebuilt for Python3.5 rebuild

* Sat Aug 1 2015 Julien Enselme <jujens@jujens.eu> - 1.33-1
- Update to 1.33
- Enable python3 subpackage
- Update SPEC to match packaging guidelines

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Dec 19 2012 Kushal Das <kushal@fedoraproject.org> 1.23-1
- Intial package
