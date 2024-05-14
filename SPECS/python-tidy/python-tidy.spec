%global         oname uTidylib
%global         _description\
Python wrapper (bindings) for tidylib, this allows you to tidy HTML\
files through a Pythonic interface.
Summary:        Python wrapper for tidy, from the HTML tidy project
Name:           python-tidy
Version:        0.6
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://cihar.com/software/utidylib/
Source0:        https://dl.cihar.com/utidylib/uTidylib-%{version}.tar.bz2
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildArch:      noarch

%description    %{_description}

%package     -n python3-tidy
%{?python_provide:%python_provide python3-tidy}
Summary:        %{summary}
Requires:       libtidy
Requires:       python3-six

%description -n python3-tidy %{_description}

%prep
%setup -q -n %{oname}-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test || :


%files -n python3-tidy
%license LICENSE
%doc README.rst
%{python3_sitelib}/tidy
%{python3_sitelib}/uTidylib-*-py3*.egg-info

%changelog
* Wed Nov 30 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.6-5
- Move to Core.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Sep 30 2019 Terje Rosten <terjeros@phys.ntnu.no> - 0.6-1
- 0.6

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-14
- Rebuilt for Python 3.8

* Sun Aug 18 2019 Terje Rosten <terje.rosten@ntnu.no> - 0.3-13
- No Python 2 in newer Fedoras

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3-8
- Rebuilt for Python 3.7

* Mon Feb 19 2018 Terje Rosten <terje.rosten@ntnu.no> - 0.3-7
- Clean up, minor issue with tidy 5.6

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3-3
- rebuild (tidy)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3-2
- Rebuild for Python 3.6

* Sun Sep 18 2016 Terje Rosten <terjeros@phys.ntnu.no> - 0.3-1
- 0.3
- New upstream
- Add Python 3 support

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-17
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2-5
- Rebuild for Python 2.6

* Sat Oct 18 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.2-4
- Not 64 bits clean, #467246, thanks to Jose Pedro Oliveira
  for report and patch.

* Sun Feb 17 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.2-3
- Fix license (again)

* Sun Feb 17 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.2-2
- Simplify %%files
- Fix license, req and group

* Sat Feb 16 2008 Terje Rosten <terjeros@phys.ntnu.no> - 0.2-1
- Initial build.
