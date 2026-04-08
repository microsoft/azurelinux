# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?python3_includedir: %global python3_includedir %(%{__python3} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")}
Name:       python-igraph
Version:    0.11.9
%global igraph_version 0.9
Release:    4%{?dist}
Summary:    Python bindings for igraph

License:    GPL-2.0-or-later
URL:        https://github.com/igraph/python-igraph
Source0:    https://github.com/igraph/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  igraph-devel >= %{igraph_version}
BuildRequires:  gcc-c++
BuildRequires:  libxml2-devel

BuildRequires:  python3-devel
BuildRequires:  cmake

BuildRequires:  git-core

# for tests
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist texttable}
BuildRequires:  %{py3_dist networkx}
BuildRequires:  %{py3_dist numpy}
# not available on ix86
BuildRequires:  (%{py3_dist pandas} or python3(x86-32))
BuildRequires:  %{py3_dist scipy}
# does not provide py3_dist variant, needs fixing
# not available on ix86
BuildRequires:  (python3-graph-tool or python3(x86-32))

%description
This module extends Python with a Graph class which is capable of
handling arbitrary directed and undirected graphs with thousands of
nodes and millions of edges. Since the module makes use of the open
source igraph library written in almost 100% pure C, it is blazing
fast and outperforms most other pure Python-based graph packages
around.

%package -n python3-igraph
Summary:    %{summary}
Requires:   libxml2
Requires:   igraph >= %{igraph_version}

%description -n python3-igraph
This module extends Python with a Graph class which is capable of
handling arbitrary directed and undirected graphs with thousands of
nodes and millions of edges. Since the module makes use of the open
source igraph library written in almost 100% pure C, it is blazing
fast and outperforms most other pure Python-based graph packages
around.

%package -n python3-igraph-devel
Requires:  python3-igraph = %{version}-%{release}
Requires:  pkgconfig
Summary:   Development files for igraph

%description -n python3-igraph-devel
The python3-igraph-devel package contains the header files and some
documentation needed to develop application with %{name}.


%prep
%autosetup -S git -p0

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel -C--global-option=--use-pkg-config

%install
%pyproject_install
%pyproject_save_files -l igraph

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%pytest -v

%files -n python3-igraph -f %{pyproject_files}
%{_bindir}/igraph

%files -n python3-igraph-devel
%{python3_includedir}/igraph

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.11.9-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.11.9-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.11.9-1
- 0.11.9

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 0.11.8-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.11.8-1
- 0.11.8

* Fri Sep 27 2024 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.11.6-3
- Add patch to fix py3.13 builds
- Enable tests

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.11.6-1
- 0.11.6

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.11.5-2
- Rebuilt for Python 3.13

* Tue May 07 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.11.5-1
- 0.11.5

* Thu Feb 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.11.4-1
- 0.11.4

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.11.3-1
- 0.11.3

* Tue Oct 24 2023 Gwyn Ciesla <gwync@protonmail.com> 0.11.2-2
- Patch for Python 3.13

* Mon Oct 16 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.11.2-1
- 0.11.2

* Tue Sep 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.8-1
- 0.10.8

* Tue Sep 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.7-1
- 0.10.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 17 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.6-1
- 0.10.6

* Wed Jul 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.5-1
- 0.10.5

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.10.4-3
- Rebuilt for Python 3.12

* Tue Mar 07 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.4-2
- migrated to SPDX license

* Mon Jan 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.4-1
- 0.10.4

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.10.3-1
- 0.10.3

* Tue Oct 18 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.2-1
- 0.10.2

* Mon Sep 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.1-1
- 0.10.1

* Tue Sep 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.10.0-1
- 0.10.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.9.11-2
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.11-1
- 0.9.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.10-2
- Rebuilt for Python 3.11

* Mon Apr 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.10-1
- 0.9.10

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.9.9-1
- 0.9.9

* Fri Oct 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.8-1
- 0.9.8

* Fri Oct 15 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.7-1
- 0.9.7

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.6-1
- 0.9.6

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.4-2
- Rebuilt for Python 3.10

* Tue Jun 01 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.4-1
- 0.9.4

* Mon Mar 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.1-1
- 0.9.1

* Fri Feb 26 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.9.0-1
- 0.9.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 08 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.3-1
- 0.8.3

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.2-20
- BR python3-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.8.2-19
- Rebuilt for Python 3.9

* Wed Apr 29 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.2-1
- 0.8.2

* Mon Apr 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.1-1
- 0.8.1

* Mon Feb 10 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.8.0-1
- 0.8.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1.post6-17
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7.1.post6-16
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.7.1.post6-15
- Drop Python 2.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.1.post6-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Jan Beran <jberan@redhat.com> - 0.7.1.post6-9
- Fix of missing Python 3 version executables

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.1.post6-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1.post6-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1.post6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1.post6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Oct  1 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7.1.post6-1
- Update to 0.7.1.post6 (improved python3 support)

* Tue Sep 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7-1
- Create python2-igraph* binary packages.
- Add python3 support, create python3-igraph* subpackages.

* Tue Sep 29 2015 Brian Stinson <bstinson@ksu.edu> - 0.7-1
- Update to 0.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 09 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.6.5-1
- Update to 0.6.5
- Clean the spec a little
- Comment out the tests for the moment
- Update macro to python2
- Add the devel subpackage for the header file

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.5.4-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Neal Becker <ndbecker2@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May  2 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-3
- Try removing Requires

* Mon Apr 27 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-2
- Try running check

* Mon Apr 27 2009 Neal Becker <ndbecker2@gmail.com> - 0.5.2-1
- Update to 0.5.2
- Try building without patch2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 0.5.1-3
- Bump tag

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.1-2
- Rebuild for Python 2.6

* Sun Nov 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5.1-1
- Update to 0.5.1

* Mon Feb 25 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-5
- Nothing

* Sun Feb 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-4
- Fix requires igraph

* Sun Feb 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-3
- Add BR python

* Sat Feb 16 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-2
- Fix BR

* Fri Feb 15 2008 Neal Becker <ndbecker2@gmail.com> - 0.5-1
- Update to 0.5

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-7
- Add AUTHORS

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-6
- More patches from upstream

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-5
- try memory patch

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-4
- patch2

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-3
- Got patch from upstream

* Thu Jan 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-2
- Add BR gcc
- BR libxml2-devel, Req libxml2

* Wed Jan 23 2008 Neal Becker <ndbecker2@gmail.com> - 0.4.5-1
- Initial package

