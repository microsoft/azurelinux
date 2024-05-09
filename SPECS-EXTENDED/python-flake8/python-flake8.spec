Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global modname flake8

%global entrypoints_dep >= 0.3
%global pyflakes_dep    >= 2.1.0
%global pycodestyle_dep >= 2.5.0
%global mccabe_dep      >= 0.6.0

Name:             python-%{modname}
Version:          3.7.7
Release:          9%{?dist}
Summary:          Python code checking using pyflakes, pycodestyle, and mccabe

License:          MIT
URL:              https://gitlab.com/pycqa/flake8
Source0:          https://files.pythonhosted.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz#/python-%{modname}-%{version}.tar.gz
BuildArch:        noarch
%if 0%{?with_check}
BuildRequires:    python3-pip
%endif

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
Summary:        Python code checking using pyflakes, pycodestyle, and mccabe

%{?python_provide:%python_provide python%{python3_pkgversion}-%{modname}}

Requires:         python%{python3_pkgversion}-setuptools
Requires:         python%{python3_pkgversion}-mccabe %{mccabe_dep}
Requires:         python%{python3_pkgversion}-pycodestyle %{pycodestyle_dep}
Requires:         python%{python3_pkgversion}-pyflakes %{pyflakes_dep}

BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    python%{python3_pkgversion}-setuptools
BuildRequires:    python%{python3_pkgversion}-entrypoints %{entrypoints_dep}
BuildRequires:    python%{python3_pkgversion}-mccabe %{mccabe_dep}
BuildRequires:    python%{python3_pkgversion}-pycodestyle %{pycodestyle_dep}
BuildRequires:    python%{python3_pkgversion}-pyflakes %{pyflakes_dep}
BuildRequires:    python%{python3_pkgversion}-mock

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

# we have 0.3, that is not deemed >= 0.3.0 by RPM
sed -i 's/entrypoints >= 0.3.0/entrypoints >= 0.3/' setup.py


%build
%py3_build


%install
%py3_install
ln -s flake8 %{buildroot}%{_bindir}/flake8-3
ln -s flake8 %{buildroot}%{_bindir}/flake8-%{python3_version}
ln -s flake8 %{buildroot}%{_bindir}/python3-flake8


%check
pip3 install pytest
pip3 install .
%{__python3} -m pytest tests -v


%files -n python%{python3_pkgversion}-%{modname}
%license LICENSE
%doc README.rst CONTRIBUTORS.txt
%{_bindir}/flake8
%{_bindir}/flake8-3
%{_bindir}/flake8-%{python3_version}
%{_bindir}/python3-flake8
%{python3_sitelib}/%{modname}*


%changelog
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
- https://flake8.pycqa.org/en/latest/release-notes/3.6.0.html

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

