# NOTE: tests are disabled since should_be has not yet been packaged.

Name:           python-gssapi
Version:        1.7.3
Release:        10%{?dist}
Summary:        Python Bindings for GSSAPI (RFC 2743/2744 and extensions)

License:        ISC
URL:            https://github.com/pythongssapi/python-gssapi
Source0:        https://github.com/pythongssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
# https://github.com/pythongssapi/python-gssapi/pull/321
Patch0:         cython3.patch

BuildRequires:  krb5-devel >= 1.19
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3-Cython

# For autosetup
BuildRequires: git-core

%global _description\
A set of Python bindings to the GSSAPI C library providing both\
a high-level pythonic interfaces and a low-level interfaces\
which more closely matches RFC 2743.  Includes support for\
RFC 2743, as well as multiple extensions.

%description %_description

%package -n python3-gssapi
Summary:        Python 3 Bindings for GSSAPI (RFC 2743/2744 and extensions)
Requires:       krb5-libs >= 1.19

%description -n python3-gssapi %_description

%prep
%autosetup -S git -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files gssapi

%check
# Check import everything except the tests, as we don't have the tests deps
%pyproject_check_import -e 'gssapi.tests*'

%files -n python3-gssapi -f %{pyproject_files}
%doc README.txt

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7.3-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.7.3-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.7.3-2
- Rebuilt for Python 3.11

* Wed Feb 16 2022 Simo Sorce <simo@redhat.com> - 1.7.3-1
- Update to 1.7.3 release

* Thu Feb 03 2022 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-2
- Enable package notes
- Reduce BuildRequires set by using git-core
- Remove redundant runtime requires of python3-six
- Run import check during the build

* Wed Feb  2 2022 Simo Sorce <simo@redhat.com> - 1.7.2-1
- Update to latest release and modernize spec file

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Robbie Harwood <rharwood@redhat.com> - 1.6.14-1
- New upstream release (1.6.14)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.9-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Robbie Harwood <rharwood@redhat.com> - 1.6.9-1
- New upstream release (1.6.9)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.5-2
- Rebuilt for Python 3.9

* Wed Apr 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.6.5-1
- New upstream release (1.6.5)

* Tue Apr 07 2020 Robbie Harwood <rharwood@redhat.com> - 1.6.4-1
- New upstream release (1.6.4)
- Resolves: #1821889

* Tue Feb 25 2020 Robbie Harwood <rharwood@redhat.com> - 1.6.2-1
- New upstream release (1.6.2)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.1-3
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Robbie Harwood <rharwood@redhat.com> - 1.6.1-2
- Drop python2 subpackage for fc32+

* Fri Aug 09 2019 Robbie Harwood <rharwood@redhat.com> - 1.6.1-1
- New upstream version: 1.6.1

* Thu Jul 25 2019 Robbie Harwood <rharwood@redhat.com> - 1.5.1-4
- Restore python2 subpackage for fc31 by request of offlineimap

* Thu May 30 2019 Robbie Harwood <rharwood@redhat.com> - 1.5.1-3
- Drop python2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 18 2018 Robbie Harwood <rharwood@redhat.com> - 1.5.1-1
- Remove warning about collections ABCs on python3.7
- Resolves: #1594834

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.7

* Tue May 08 2018 Robbie Harwood <rharwood@redhat.com> - 1.5.0-2
- Fix tox dependency

* Fri Apr 06 2018 Robbie Harwood <rharwood@redhat.com> - 1.5.0-1
- Prepare for release 1.5.0

* Wed Mar 07 2018 Robbie Harwood <rharwood@redhat.com> - 1.4.1-2
- Add gcc to build-deps

* Fri Feb 16 2018 Robbie Harwood <rharwood@redhat.com> - 1.4.1-1
- Prepare for release 1.4.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Dec 01 2017 Robbie Harwood <rharwood@redhat.com> - 1.3.0-1
- New upstream release v1.3.0

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.0-8
- Python 2 binary package renamed to python2-gssapi
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 04 2017 Robbie Harwood <rharwood@redhat.com> 1.2.0-5
- Fix problem where gss_display_status can infinite loop
- Move to autosetup and rpm-git-tree

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 03 2016 Robbie Harwood <rharwood@redhat.com> - 1.2.0-1
- New upstream version 1.2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.4-1
- New upstream version 1.1.4
- Resolves #1286458

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.1.3-2
- Rebuilt for Python3.5 rebuild

* Fri Sep 04 2015 Robbie Harwood <rharwood@redhat.com> - 1.1.3-1
- New upstream minor release

* Thu Aug 20 2015 Simo Sorce <simo@redhat.com> - 1.1.2-1
- New minor release.
- Resolves #1254458
- Fixes a crash bug when inquiring incomplete security contexts

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Simo Sorce <simo@redhat.com> - 1.1.1-1
- New minor release.

* Thu Feb 19 2015 Solly Ross <sross@redhat.com> - 1.1.0-1
- Initial Packaging
