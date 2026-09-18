# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-jsonpickle
# version is inserted into setup.cfg manually (see %%prep). Please be careful
# to use a Python-compatible version number if you need to set an "uncommon"
# version for this RPM.
Version:        4.0.2
Release:        6%{?dist}
Summary:        A module that allows any object to be serialized into JSON

License:        BSD-3-Clause
URL:            https://github.com/jsonpickle/jsonpickle
Source0:        %{pypi_source jsonpickle}

%global _docdir_fmt %{name}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
jsonpickle is a library for the two-way conversion of complex Python objects
and JSON. jsonpickle builds upon the existing JSON encoders, such as
simplejson, json, and ujson.}

%description %{_description}


%package -n python3-jsonpickle
Summary:        A module that allows any object to be serialized into JSON

%description -n python3-jsonpickle %{_description}


%prep
%autosetup -n jsonpickle-%{version} -p1

sed -r -i 's/[[:blank:]]--cov[^[:blank:]]*//g' pytest.ini

sed -i /bson/d pyproject.toml
sed -i /pymongo/d pyproject.toml
sed -i /histogram/d pyproject.toml
sed -i /black\ /d pyproject.toml
sed -i /pytest-checkdocs\ /d pyproject.toml
sed -i /pytest-cov\ /d pyproject.toml
sed -i /pytest-flake8\ /d pyproject.toml
sed -i /pytest-enabler\ /d pyproject.toml
sed -i /pytest-ruff\ /d pyproject.toml
sed -i /atheris\ /d pyproject.toml

%if 0%{?el9}
# Not yet packaged:
# [RFE:EPEL9] EPEL9 branch for python-pandas
# https://bugzilla.redhat.com/show_bug.cgi?id=2032550
# (python-scikit-learn: no EPEL9 request yet)
sed -r -i -e 's/^([[:blank:]]*)(pandas|scikit-learn)/\1# \2/' setup.cfg
%endif


%generate_buildrequires
%pyproject_buildrequires -x testing,testing.libs


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files jsonpickle


%check
%pytest %{?el9:--ignore=jsonpickle/ext/pandas.py} --ignore=fuzzing/


%files -n python3-jsonpickle -f %{pyproject_files}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.2-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.2-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Python Maint <python-maint@redhat.com> - 4.0.2-3
- Rebuilt for Python 3.14

* Tue Jun 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.0.2-2
- Patch out pymongo test dependency (to match bson)

* Mon Feb 17 2025 Gwyn Ciesla <gwync@protonmail.com> - 4.0.2-1
- 4.0.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Gwyn Ciesla <gwync@protonmail.com> - 4.0.1-1
- 4.0.1

* Tue Nov 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 4.0.0-1
- 4.0.0

* Wed Nov 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.4.2-1
- 3.4.2

* Tue Sep 03 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.3.0-1
- 3.3.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.2.2-1
- 3.2.2

* Wed Jun 12 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.2.1-1
- 3.2.1

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 3.0.4-3
- Rebuilt for Python 3.13

* Sat Jun 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.4-2
- Patch for Python 3.13 (fix RHBZ#2284005)

* Thu Apr 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.0.4-1
- 3.0.4

* Tue Feb 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 3.0.3-1
- 3.0.3

* Mon Feb 19 2024 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.0.2-4
- Fix tests with Pandas 2.2 and Cython 3 

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.0.2-1
- 3.0.2
- Drop signature verification due to PyPi change.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 3.0.1-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.0.1-1
- 3.0.1

* Tue Dec 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.0-4
- EPEL9 compatibility

* Tue Dec 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.0-3
- Switch URL to the GitHub project page
- Stop using deprecated zero-argument form of pypi_source
- Remove workarounds for EL7/8 and end-of-lifed Fedoras
- Update description and stop implying there is a Python 2 version
- Drop obsolete python_provide macro
- Port to pyproject-rpm-macros
- Re-enable GPG verification
- Update License to SPDX

* Mon Dec 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.0.0-2
- Unpin setuptools requirement.

* Fri Dec 02 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.0.0-1
- 3.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Adam Williamson <awilliam@redhat.com> - 2.2.0-3
- Backport PR #396 to make it work with Python 3.11 (#2098982)

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.2.0-2
- Rebuilt for Python 3.11

* Thu May 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.2.0-1
- 2.2.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.1.0-1
- 2.1.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.10

* Mon Feb 08 2021 Gwyn Ciesla <gwync@protonmail.com> - 2.0.0-1
- 2.0.0

* Mon Feb 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.5.1-1
- 1.5.1 + patch for test failure.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-1
- 1.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-5
- Rebuilt for Python 3.9

* Mon May 18 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 1.4.1-4
- add EPEL 8 version

* Wed May 13 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 1.4.1-3
- add source file verification

* Mon Apr 27 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 1.4.1-2
- Add patch to fix build until 1.5.1 is released

* Tue Apr 21 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.1-1
- 1.4.1

* Mon Apr 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4-1
- 1.4

* Fri Feb 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.3-1
- 1.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.2-1
- 1.2, drop Python 2.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Gwyn Ciesla <limburgher@gmail.com> - 1.1-1
- 1.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.4-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 30 2017 Ralph Bean <rbean@redhat.com> - 0.9.4-2
- Conditionalize python3 package for EPEL7 compat.

* Thu Mar 30 2017 Ralph Bean <rbean@redhat.com> - 0.9.4-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-2
- Rebuild for Python 3.6

* Fri Dec 09 2016 Jon Ciesla <limburgher@gmail.com> - 0.9.3-1
- 0.9.3

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Jon Ciesla <limburgher@gmail.com> - 0.9.2-3
- Disable tests to fix build.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jul  2 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.2-1
- Update to latest version
- Clean up spec file a bit
- Add python3 subpackage (#1233915)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Jon Ciesla <limburgher@gmail.com> - 0.4.0-1
- Latest upstream release, 0.4.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jan 23 2010 Ben Boeckel <MathStuf@gmail.com> - 0.3.1-1
- Update to 0.3.1

* Mon Nov 02 2009 Ben Boeckel <MathStuf@gmail.com> - 0.2.0-1
- Initial package
