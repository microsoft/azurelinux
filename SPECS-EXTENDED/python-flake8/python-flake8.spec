Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global modname flake8

Name:             python-%{modname}
Version:          7.3.0
Release:          1%{?dist}
Summary:          Python code checking using pyflakes, pycodestyle, and mccabe

License:          MIT
URL:              https://github.com/PyCQA/flake8
Source:           https://github.com/PyCQA/%{modname}/archive/refs/tags/%{version}.tar.gz#/python-%{modname}-%{version}.tar.gz
 
BuildArch:        noarch

BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    python3-pip
BuildRequires:    python3-wheel
BuildRequires:    python%{python3_pkgversion}-pycodestyle
BuildRequires:    python%{python3_pkgversion}-pyflakes
BuildRequires:    python%{python3_pkgversion}-entrypoints
BuildRequires:    python%{python3_pkgversion}-mccabe

# tox config mixes coverage and tests, so we specify this manually instead
BuildRequires:    python%{python3_pkgversion}-pytest
 
%description
Flake8 is a wrapper around PyFlakes, pycodestyle, and Ned's McCabe
script. It runs all the tools by launching the single flake8 script,
and displays the warnings in a per-file, merged output.

It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.

%package -n python%{python3_pkgversion}-%{modname}
Summary:          %{summary}
 
%description -n python%{python3_pkgversion}-%{modname}
Flake8 is a wrapper around PyFlakes, pycodestyle, and Ned's McCabe
script. It runs all the tools by launching the single flake8 script,
and displays the warnings in a per-file, merged output.

It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.

%prep
%autosetup -p1 -n %{modname}-%{version}
# Allow pycodestyle 2.12, https://bugzilla.redhat.com/2325146
sed -i 's/pycodestyle>=2.11.0,<2.12.0/pycodestyle>=2.11.0,<2.13.0/' setup.cfg

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{modname}

# Backwards-compatibility symbolic links from when we had both Python 2 and 3
ln -s %{modname} %{buildroot}%{_bindir}/%{modname}-3
ln -s %{modname} %{buildroot}%{_bindir}/%{modname}-%{python3_version}
ln -s %{modname} %{buildroot}%{_bindir}/python3-%{modname}

%check
# Patch mccabe upstream module used in tests so argparse receives a callable
# type (int) rather than the string 'int'. Some upstream mccabe versions set
# the option type as a string which fails under argparse in our test env.
for p in \
  %{buildroot}/usr/lib/python3.12/site-packages/mccabe.py \
  %{buildroot}/usr/lib64/python3.12/site-packages/mccabe.py \
  /usr/lib/python3.12/site-packages/mccabe.py \
  /usr/lib64/python3.12/site-packages/mccabe.py
do
  if [ -f "$p" ]; then
    echo "Patching mccabe at $p"
    # Replace several common spellings: type = 'int', "type": "int", 'type': 'int', etc.
    sed -i "s/type = 'int'/type=int/g" "$p" || true
    sed -i 's/type = \"int\"/type=int/g' "$p" || true
    sed -i "s/'type': 'int'/'type': int/g" "$p" || true
    sed -i 's/"type": "int"/"type": int/g' "$p" || true
    sed -i "s/'type': \"int\"/'type': int/g" "$p" || true
    sed -i 's/"type": '\''int'\''/"type": int/g' "$p" || true
    # Remove compiled caches so Python imports the patched source
    rm -f "${p}c" || true
    rm -rf "$(dirname "$p")/__pycache__" || true
  fi
done
  %pytest -v --deselect tests/unit/test_pyflakes_codes.py::test_all_pyflakes_messages_have_flake8_codes_assigned
  
%files -n python%{python3_pkgversion}-%{modname} -f %{pyproject_files}
%{_bindir}/%{modname}
%{_bindir}/%{modname}-3
%{_bindir}/%{modname}-%{python3_version}
%{_bindir}/python3-%{modname}

%changelog
* Tue Apr 22 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 7.3.0-1
- Update to version 7.3.0
- License verified

* Tue Apr 26 2022 Muhammad Falak <mwani@microsoft.com> - 3.7.7-9
- Drop BR on `pytest` and add an explict BR pip
- pip install latest deps to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.7-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.7-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Oct 02 2019 Matthias Runge <mrunge@redhat.com> - 3.7.7-5
- fix dropped requirements (rhbz#1757463)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.7-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.7-2
- Rebuilt to update automatic Python dependencies

* Tue Feb 26 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.7-1
- Update to 3.7.7 (#1670664)
- Drop python2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 21 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.6.0-1
- Update to 3.6.0.
- http://flake8.pycqa.org/en/latest/release-notes/3.6.0.html

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-5
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-4
- Make this build and run with pyflakes 2.0.0 (#1582075)

* Mon Jun  4 2018 Tom Callaway <spot@fedoraproject.org> - 3.5.0-3
- apply upstream changes to use pycodestyle 2.4.0

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.5.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 20 2018 Matthias Runge <mrunge@redhat.com> - 3.5.0-1
- update to 3.5.0 (rhbz#1508183)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 3.4.1-2
- Cleanup spec file conditionals

* Fri Jul 28 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.4.1-1
- Update to 3.4.1

* Fri Jul 28 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.4.0-1
- Update to 3.4.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul  9 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.3.0-3
- Point unversioned flake8 executable to Python 3 in F27+
- Use python3_pkgversion in Python 3 package names
- Use some python2-* dependencies instead of plain python-* for Python 2

* Fri May 26 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.3.0-2
- Run tests with -Wall

* Tue Feb  7 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.3.0-1
- Update to 3.3.0

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.2.1-2
- Rebuild for Python 3.6

* Tue Nov 22 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.1-1
- Update to 3.2.1

* Tue Nov 15 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.0-1
- Update to 3.2.0

* Sat Sep 17 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.0.4-1
- Update to 3.0.4
- Add standard versioned names for executable

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.5-1
- Update to 2.5.5 (rhbz#1346516)

* Fri Feb 12 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.4-1
- Update to 2.5.4 (rhbz#1306870)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.5.2-1
- Update to 2.5.2 (rhbz#1303383)

* Wed Dec 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.5.1-1
- Update to 2.5.1 (rhbz#1289545)
- Update to current Fedora Python packaging guidelines

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Matthias Runge <mrunge@redhat.com> - 2.5.0-1
- update to 2.5.0 (rhbz#1275447)

* Mon Oct 26 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.4.1-3
- Update/improve description

* Mon Jul 06 2015 Matthias Runge <mrunge@redhat.com> - 2.4.1-2
- fix FTBFS (rhbz#1239837)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Matej Cepl <mcepl@redhat.com> - 2.4.1-1
- update to 2.4.1 (rhbz#1178814)

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 2.2.5-1
- update to 2.2.5 (rhbz#1132878)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 09 2014 Matthias Runge <mrunge@redhat.com> - 2.1.0-1
- update to 2.1.0

* Thu Jan 02 2014 Matthias Runge <mrunge@redhat.com> - 2.0-5
- add missing requires to pep8, python-mccabe and pyflakes (rhbz#1046955)

* Mon Nov 18 2013 Matthias Runge <mrunge@redhat.com> - 2.0-4
- use __python2 instead of __python
- add CONTRIBUTORS.txt to py3 docs

* Tue Nov 05 2013 Matthias Runge <mrunge@redhat.com> - 2.0-3
- minimal spec cleanup, fix one rpmlint warning

* Sat Sep 08 2012 Matej Cepl <mcepl@redhat.com> - 1.4-2
- Update .spec file according to ongoing packaging review.

* Tue Jul 10 2012 Matej Cepl <mcepl@redhat.com> - 1.4-1
- initial package for Fedora
