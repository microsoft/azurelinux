# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       python-multilib
Version:    1.3
Release: 6%{?dist}
Summary:    A module for determining if a package is multilib or not
License:    GPL-2.0-only
URL:        https://pagure.io/releng/python-multilib
Source0:    https://releases.pagure.org/releng/python-multilib/%{name}-%{version}.tar.bz2

BuildArch:  noarch


%global _description \
A Python module that supports several multilib "methods" useful for \
determining if a 32-bit package should be included with its 64-bit analogue \
in a compose.

%description %{_description}

%package conf
Summary:        Configuration files for %{name}

%description conf
This package provides the configuration files for %{name}.


%package -n python%{python3_pkgversion}-multilib
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}
Requires:       %{name}-conf = %{version}-%{release}

%description -n python%{python3_pkgversion}-multilib %{_description}


%prep
%setup -q

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l '*'
%{__install} -D -m 0644 etc/multilib.conf %{buildroot}%{_sysconfdir}/multilib.conf

%check
%pyproject_check_import

# testing requires complete composes available locally, which no buildsystem
# would ever want included in a build root
#{__python2} setup.py test
#{__python3} setup.py test

%files conf
%config(noreplace) %{_sysconfdir}/multilib.conf


%files -n python%{python3_pkgversion}-multilib -f %{pyproject_files}
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.3-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Python Maint <python-maint@redhat.com> - 1.3-2
- Rebuilt for Python 3.14

* Tue Jun 10 2025 Lubomír Sedlář <lsedlar@redhat.com> - 1.3-1
- Bump to latest version. No functional changed, only packaging updates.

* Mon Jun 09 2025 Lubomír Sedlář <lsedlar@redhat.com> - 1.2-32
- Drop python2 compatibility
- Switch to pyproject_ macros

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.2-31
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2-28
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.2-24
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2-21
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2-18
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.2-15
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2-10
- Disable python2 package again (rhbz#1687417)

* Wed Mar 27 2019 Lubomír Sedlář <lsedlar@redhat.com> - 1.2-9
- Enable python2- subpackage again (rhbz#1692588)

* Mon Mar 11 2019 Lubomír Sedlář <lsedlar@redhat.com> - 1.2-8
- Disable python2 package on F >= 31

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Lubomír Sedlář <lsedlar@redhat.com> - 1.2-2
- Update requires for epel builds

* Thu Mar 02 2017 Lubomír Sedlář <lsedlar@redhat.com> - 1.2-1
- New upstream version with support for DNF package objects
- Updated URL to point to new upstream on Pagure.io

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Jay Greguske <jgregusk@redhat.com> - 1.1-5
- Package up for Fedora rawhide

* Sun May 01 2016 Neal Gompa <ngompa13@gmail.com> - 1.1-3
- Port to Python 3 and enable its subpackage
- Split config file to its own subpackage

* Thu Apr 07 2016 Dennis Gilmore <dennis@ausil.us> - 1.1-2
- setup to make python3 down the road.
- spec and srpm named python-multilib
- fix license

* Tue Jul 21 2009 Jay Greguske <jgregusk@redhat.com> - 1.1-1
- consider dependencies in multilib testing
- fix a couple import errors

* Tue Jul 21 2009 Jay Greguske <jgregusk@redhat.com> - 1.0-1
- Initial RPM release
