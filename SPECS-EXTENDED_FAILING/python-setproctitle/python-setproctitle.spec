Vendor:         Microsoft Corporation
Distribution:   Mariner
%global tarname setproctitle

Name:           python-setproctitle
Version:        1.1.10
Release:        18%{?dist}
Summary:        Python module to customize a process title

License:        BSD
URL:            http://pypi.python.org/pypi/%{tarname}
Source0:        https://pypi.io/packages/source/s/%{tarname}/%{tarname}-%{version}.tar.gz#/python-%{tarname}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  /usr/bin/2to3

%global _description\
Python module allowing a process to change its title as displayed by\
system tool such as ps and top.\
\
It's useful in multiprocess systems, allowing to identify tasks each forked\
process is busy with. This technique has been used by PostgreSQL and OpenSSH.\
\
It's based on PostgreSQL implementation which has proven to be portable.\
\


%description %_description

%package -n python3-%{tarname}
Summary:        Python module to customize a process title
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose

%description -n python3-%{tarname}
Python module allowing a process to change its title as displayed by
system tool such as ps and top.

It's useful in multi-process systems, allowing to identify tasks each forked
process is busy with. This technique has been used by PostgreSQL and OpenSSH.

It's based on PostgreSQL implementation which has proven to be portable.

%prep
%setup -q -n %{tarname}-%{version}


%build
%py3_build

%install
%py3_install
chmod 0755 %{buildroot}%{python3_sitearch}/setproctitle*.so

%check
# python3-config is broken for F31+:
# https://bugzilla.redhat.com/show_bug.cgi?id=1724190
#PYTHON=python3 PYCONFIG=python3-config make tests/pyrun3


%files -n python3-%{tarname}
%doc README.rst COPYRIGHT
# For arch-specific packages: sitearch
%{python3_sitearch}/%{tarname}*.so
%{python3_sitearch}/%{tarname}*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.10-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.10-16
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 26 2019 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.10-14
- Fix RPM FTBFS with python 3.8 (RHBZ#1718363)

* Thu Jul 11 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.10-13
- Subpackage python2-setproctitle has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.10-11
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.10-9
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.10-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.1.10-6
- Cleanup spec file conditionals

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.1.10-5
- Revert changes for EPEL7

* Thu Nov 16 2017 Björn Esser <besser82@fedoraproject.org> - 1.1.10-5
- Changes for EPEL7

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.10-4
- Python 2 binary package renamed to python2-setproctitle
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.10-1
- Upstream 1.1.10 (RHBZ#1448910)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.9-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Aug 15 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.9-1
- Upstream 1.1.9

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug  4 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.6-1
- upstream 1.1.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.3-2
- enable tests execution
- spec cleaning

* Sun Jan 29 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1.1.3-1
- initial packaging

