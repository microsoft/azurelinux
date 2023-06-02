Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           python-pefile
Version:        2023.2.7
Release:        3%{?dist}
Summary:        Python module for working with Portable Executable files
License:        MIT
URL:            https://github.com/erocarrera/pefile


%global srcname pefile

%global common_desc pefile is a multi-platform Python module to read and work with Portable\
Executable (aka PE) files. Most of the information in the PE Header is \
accessible, as well as all the sections, section's information and data.\
pefile requires some basic understanding of the layout of a PE file. Armed \
with it it's possible to explore nearly every single feature of the file.\
Some of the tasks that pefile makes possible are:\
* Modifying and writing back to the PE image\
* Header Inspection\
* Sections analysis\
* Retrieving data\
* Warnings for suspicious and malformed values\
* Packer detection with PEiD’s signatures\
* PEiD signature generation\


#Source0:       https://github.com/erocarrera/%%{srcname}/archive/v%%{version}/%%{srcname}-%%{version}.tar.gz
Source0:        https://github.com/erocarrera/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

# For the patch
# BuildRequires: git-core 

%description
%{common_desc}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
Provides:       python3dist(%{srcname}) = %{version}-%{release}
Requires:       python%{python3_pkgversion}-future

%description -n python%{python3_pkgversion}-%{srcname}
%{common_desc}


%prep
%autosetup -n %{srcname}-%{version}
sed -i -e '/^#!\//, 1d' pefile.py

%build
%py3_build

%install
%py3_install

# check
# regression tests in this package are based on binary blob of exe files - commercial and malware
# at this point (2019-09-20) not suitable to be in Fedora.
# More info on:
# https://github.com/erocarrera/pefile/issues/171
# https://github.com/erocarrera/pefile/issues/82#issuecomment-192018385
# %%{__python3} setup.py test

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README*
%{python3_sitelib}/*

%changelog
* Tue May 30 2023 Vince Perri <viperri@gmail.com> - 2023.2.7-3
- License verified.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).

* Sat Mar 11 2023 Fabio Valentini <decathorpe@gmail.com> - 2023.2.7-2
- Rebuild for https://pagure.io/releng/issue/11327

* Wed Feb 08 2023 Michal Ambroz <rebus _AT seznam.cz> - 2023.2.7-1
- bump to version 2023.2.7

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.5.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.5.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 23 2022 Michal Ambroz <rebus _AT seznam.cz> - 2022.5.30-1
- bump to version 2022.5.30

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2021.9.3-2
- Rebuilt for Python 3.11

* Thu Feb 17 2022 Michal Ambroz <rebus _AT seznam.cz> - 2021.9.3-1
- bump to version 2021.9.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.5.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2021.5.13-2
- Rebuilt for Python 3.10

* Thu May 13 2021 Michal Ambroz <rebus _AT seznam.cz> - 2021.5.13-1
- bump to version 2021.5.13

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2019.4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.4.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2019.4.18-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2019.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 20 2019 Michal Ambroz <rebus _AT seznam.cz> - 2019.4.18-1
- bump to version 2019.4.18

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2017.11.5-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2017.11.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2017.11.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2017.11.5-5
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.11.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2017.11.5-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2017.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.11.5-1
- Update to 2017.11.5 (rhbz #1509751)

* Sat Aug 05 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.8.1-1
- Update to 2017.8.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.5.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.5.26-2
- Fix requirement (rhbz #1474447)

* Sat May 27 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.5.26-1
- Update to 2017.5.26
- Remove upstreamed patch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.3.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2016.3.28-2
- Rebuild for Python 3.6

* Tue Nov 01 2016 Athmane Madjoudj <athmane@fedoraproject.org> - 2016.3.28-1
- Update to 2016.3.28
- Revamp the specfile
- Add patch to fix the build

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10_139-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 07 2014 Christopher Meng <rpm@cicku.me> - 1.2.10_139-1
- Update to 1.2.10_139

* Thu Aug 08 2013 Christopher Meng <rpm@cicku.me> - 1.2.10_123-1
- Update to 1.2.10_123

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.10_63-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May  8 2009 David Malcolm <dmalcolm@redhat.com> - 1.2.10_63-1
- initial packaging

