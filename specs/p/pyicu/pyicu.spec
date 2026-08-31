# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define		realname PyICU
Name:		pyicu
Version:	2.14
Release:	8%{?dist}
Summary:	Python extension wrapping the ICU C++ libraries

License:	MIT
URL:		https://pypi.org/project/PyICU/
Source0:	https://files.pythonhosted.org/packages/source/P/%{realname}/%{realname}-%{version}.tar.gz

BuildRequires:	gcc-c++
BuildRequires:	libicu-devel
BuildRequires:	python3-devel
%if 0%{?fedora}
BuildRequires:	python3-pytest
%endif
BuildRequires:	python3-setuptools
BuildRequires:	python3-six

%global _description\
PyICU is a python extension implemented in C++ that wraps the C/C++ ICU\
library.

%description %_description

%package -n python3-pyicu
Summary: Python 3 extension wrapping the ICU C++ libraries

%description -n python3-pyicu %_description

%prep
%setup -q

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files icu

%if 0%{?fedora}
%check
%pytest
%endif

%files -n python3-pyicu -f %{pyproject_files}
%doc LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.14-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.14-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 František Zatloukal <fzatlouk@redhat.com> - 2.14-6
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.14-4
- Rebuilt for Python 3.14

* Fri Mar 14 2025 Lumír Balhar <lbalhar@redhat.com> - 2.14-3
- Fix compatibility with the newest setuptools

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Pete Walter <pwalter@fedoraproject.org> - 2.14-1
- Update to 2.14

* Wed Aug 14 2024 Gwyn Ciesla <gwync@protonmail.com> - 2.13.1-4
- 2.13.1
- Modernize packaging.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.12-2
- Rebuilt for Python 3.13

* Tue Jan 30 2024 Pete Walter <pwalter@fedoraproject.org> - 2.12-1
- Update to 2.12

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.11-1
- 2.11

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2.10.2-6
- Rebuilt for ICU 73.2

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.10.2-5
- Rebuilt for Python 3.12

* Thu Mar 09 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.10.2-4
- Patch for Python 3.12.

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.10.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2.10.2-1
- Update to 2.10.2

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.9-4
- Rebuilt for ICU 71.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 2.9-2
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 2.9-1
- 2.9

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.7.3-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.7.3-3
- Rebuilt for Python 3.10

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 2.7.3-2
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2.7.3-1
- Update to 2.7.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Pete Walter <pwalter@fedoraproject.org> - 2.5-1
- Update to 2.5
- Update URL

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.4.3-3
- Rebuilt for Python 3.9

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2.4.3-2
- Rebuild for ICU 67

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Pete Walter <pwalter@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2-2
- Subpackage python2-pyicu has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 2.2-1
- Update to 2.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.2-5
- Rebuild for ICU 62

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-4
- Rebuilt for Python 3.7

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.2-3
- Rebuild for ICU 61.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Tue Jan 09 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0-1
- Update to 2.0

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.9.8-1
- Update to 1.9.8

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.5-25
- Rebuild for ICU 60.1

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5-24
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5-23
- Python 2 binary package renamed to python2-pyicu
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.5-20
- Rebuild due to bug in RPM (RHBZ #1468476)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5-18
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-17
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.5-16
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Oct 29 2015 Eike Rathke <erack@redhat.com> - 1.5-13
- fix build with ICU 56.1

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.5-12
- rebuild for ICU 56.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5-10
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 1.5-9
- rebuild for ICU 54.1

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 1.5-8
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Bastien Nocera <bnocera@redhat.com> 1.5-6
- Build Python3 version as well (#917449)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Parag Nemade <paragn AT fedoraproject DOT org> - 1.5-4
- Rebuild for icu 52

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 David Tardon <dtardon@redhat.com> - 1.5-2
- rebuild for ICU ABI break

* Fri Feb 08 2013 Jon Ciesla <limburgher@gmail.com> - 1.5-1
- libicu rebuild.
- Update to 1.5, 1.4 doesn't build on new libicu.

* Wed Aug 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-1
- update to 1.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2-1
- New upstream 1.2 release

* Sun May 08 2011 Prabin Kumar Datta <prabindatta@fedoraproject.org> - 1.1-2
- added CHANGES CREDITS under doc section
- updated URL
- added check section

* Thu Mar 17 2011 Prabin Kumar Datta <prabindatta@fedoraproject.org> - 1.1-1
- Initial build
