Vendor:         Microsoft Corporation
Distribution:   Mariner
%global modname mutagen
# Share doc between python2- and python3-
%global _docdir_fmt %{name}

Name:           python-%{modname}
Version:        1.43.0
Release:        4%{?dist}
Summary:        Mutagen is a Python module to handle audio meta-data

License:        GPLv2+
URL:            https://github.com/quodlibet/mutagen
Source0:        %{url}/releases/download/release-%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

%if %{with_check}
BuildRequires:  python3-pip
%endif

%global _description \
Mutagen is a Python module to handle audio meta-data. It supports\
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.\
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora\
comments. It can also read MPEG audio and Xing headers, FLAC stream\
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it\
includes a module to handle generic Ogg bit-streams.

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx_rtd_theme
Obsoletes:      python2-mutagen < 1.42.0-10

%description -n python3-%{modname} %{_description}

Python 3 version.

%package doc
Summary:        Documentation for python-mutagen
BuildRequires:  %{_bindir}/sphinx-build

%description doc
Contains the html documentation for python mutagen.

%prep
%autosetup -n %{modname}-%{version} -p1

%build
%py3_build

sphinx-build -b html -n docs docs/_build

%install
%py3_install

%{__install} -D -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1

# Remove hidden files
rm -rf docs/_build/{.buildinfo,.doctrees}

%check
# Testing code quality is helpful upstream, to keep maintainability.
# But lint and code style issues don't mean there's antyhing wrong
# with the code.
rm -rv tests/quality/
pip3 install pytest==7.1.2 hypothesis==6.45.1

%{__python3} setup.py test


%files -n python3-%{modname}
%license COPYING
%doc NEWS README.rst
%{python3_sitelib}/%{modname}-*.egg-info
%{python3_sitelib}/%{modname}/

%{_bindir}/*
%{_mandir}/man1/*.1*

%files doc
%doc docs/_build/*

%changelog
* Wed May 04 2022 Muhammad Falak <mwani@microsoft.com> - 1.43.0-4
- Drop BR on pytest & pip install latests deps to enable ptest
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.43.0-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Michele Baldessari <michele@acksyn.org> - 1.43.0-2
- Obsolete python2-mutagen

* Mon Jan 20 2020 Michele Baldessari <michele@acksyn.org> - 1.43.0-1
- New upstream

* Thu Nov 28 2019 Miro Hrončok <mhroncok@redhat.com> - 1.42.0-9
- Subpackage python2-mutagen has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Oct 29 2019 Petr Viktorin <pviktori@redhat.com> - 1.42.0-8
- Remove build dependency on python2-hypothesis, skip related tests

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.42.0-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.42.0-6
- Rebuilt for Python 3.8

* Mon Jul 29 2019 Petr Viktorin <pviktori@redhat.com> - 1.42.0-5
- Do not run style checks and linters in %%check

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.42.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 23 2019 Michele Baldessari <michele@acksyn.org> - 1.42.0-3
- Explicitely add python3-sphinx_rtd_theme as build deps (should fix rhbz#1716509)
- Add a patch to fix tests due to over-indenting

* Sun Feb 10 2019 Michele Baldessari <michele@acksyn.org> - 1.42.0-2
- Move from pytest-pep8 to pycodestyle

* Sun Feb 10 2019 Michele Baldessari <michele@acksyn.org> - 1.42.0-1
- New upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.41.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Michele Baldessari <michele@acksyn.org> - 1.41.1-1
- New upstream

* Tue Jul 17 2018 Michele Baldessari <michele@acksyn.org> - 1.41.0-1
- New upstream

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.40.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Michele Baldessari <michele@acksyn.org> - 1.40.0-1
- New upstream

* Mon Nov 06 2017 Michele Baldessari <michele@acksyn.org> - 1.39-1
- New upstream
- Requires python*-hypothesis

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.38-1
- Update to 1.38

* Mon Mar 13 2017 Michele Baldessari <michele@acksyn.org> - 1.37-1
- New upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.36.2-1
- Update to 1.36.2 (RHBZ #1415532)

* Mon Jan 23 2017 Michele Baldessari <michele@acksyn.org> - 1.36.1-1
- New upstream release

* Sat Dec 31 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.36-2
- Modernize spec

* Fri Dec 23 2016 Michele Baldessari <michele@acksyn.org> - 1.36-1
- New upstream release

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.35.1-2
- Rebuild for Python 3.6

* Thu Nov 10 2016 Michele Baldessari <michele@acksyn.org> - 1.35.1
- New upstream release

* Thu Nov 03 2016 Michele Baldessari <michele@acksyn.org> - 1.35
- New upstream release

* Sun Sep 04 2016 Michele Baldessari <michele@acksyn.org> - 1.34.1-1
- New upstream release

* Mon Jul 25 2016 Michele Baldessari <michele@acksyn.org> - 1.34-1
- New upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Michele Baldessari <michele@acksyn.org> - 1.33.2-1
- New upstream release
- Split docs to -doc subpackage

* Tue May 03 2016 Michele Baldessari <michele@acksyn.org> - 1.32-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 Michele Baldessari <michele@acksyn.org> - 1.31-4
- Fixes tests on big endian architectures (BZ 1270298)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov  9 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.31-2
- Move the scripts to the python3 package.  This fixes two issues:
  * The scripts couldn't work without manual intervention because they required
    the python3 versions the library but no dep existed to bring them in.
  * The python2 version of the package required /usr/bin/python3

* Thu Sep 10 2015 Michele Baldessari <michele@acksyn.org> - 1.31-1
- New upstream release

* Mon Aug 24 2015 Michele Baldessari <michele@acksyn.org> - 1.30-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Michele Baldessari <michele@acksyn.org> - 1.29-1
- New upstream release

* Sat Mar 07 2015 Michele Baldessari <michele@acksyn.org> - 1.28-1
- New upstream release (BZ#1199683)

* Sun Mar 01 2015 Michele Baldessari <michele@acksyn.org> - 1.27-2
- Add initial Python 3 support on Fedora

* Mon Dec 15 2014 Michele Baldessari <michele@acksyn.org> - 1.27-1
- New upstream release
- Only use macro style for buildroot

* Sun Nov 23 2014 Michele Baldessari <michele@acksyn.org> - 1.26-1
- Fixed homepage and source URL
- Set python2-devel as BR
- Fix documentation building and shipping
- Fix spelling errors in description

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Silas Sewell <silas@sewell.ch> - 1.20-1
- Update to 1.20

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.19-1
- Update to 1.19
- Add tests

* Thu Feb 18 2010 Silas Sewell <silas@sewell.ch> - 1.18-1
- Update to 1.18

* Thu Oct 22 2009 Silas Sewell <silas@sewell.ch> - 1.17-1
- Update to 1.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Silas Sewell <silas@sewell.ch> - 1.16-1
- Update to 1.16
- New project URLs

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.15-3
- Normalize spec

* Fri Apr 10 2009 Silas Sewell <silas@sewell.ch> - 1.15-2
- Make sed safer
- Add back in removed changelogs

* Sun Mar 29 2009 Silas Sewell <silas@sewell.ch> - 1.15-1
- Update to 1.15

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.13-3
- Rebuild for Python 2.6

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-2
- Add egg-info to package

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-1
- 1.13

* Sat Aug 25 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.12-1
- Update to 1.12
- License tag fix

* Sat Apr 28 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.11-1
- Update to 1.11

* Wed Jan 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.10.1-1
- Update to 1.10.1

* Wed Dec 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.9-1
- Bump to 1.9

* Tue Dec 12 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-2
- Python 2.5 rebuild

* Sun Oct 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-1
- Bump to 1.8

* Fri Sep 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-2
- .pyo files no longer ghosted

* Fri Aug 11 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-1
- Update upstream to 1.6

* Fri Jul 21 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-5
- Some fixes in preamble.
- Change name from mutagen to python-mutagen.
- Delete CFLAGS declaration.

* Thu Jul 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-4
- Add BuildArch: noarch to preamble.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-3
- Remove python-abi dependency.
- Prep section deletes first two lines in __init__.py file due to rpmlint error.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-2
- Clean at files section.
- Fix charset in TUTORIAL file.

* Fri Jul 14 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-1
- First build.
