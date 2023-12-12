Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Linux scheduler python bindings
Name: python-schedutils
Version: 0.6
Release: 13%{?dist}
License: GPLv2
URL: https://rt.wiki.kernel.org/index.php/Tuna
Source: https://cdn.kernel.org/pub/software/libs/python/%{name}/%{name}-%{version}.tar.xz

BuildRequires: python3-devel
BuildRequires: gcc


%global _description\
Python interface for the Linux scheduler sched_{get,set}{affinity,scheduler}\
functions and friends.

%description %_description

%package -n python3-schedutils
Summary: %summary
%{?python_provide:%python_provide python3-schedutils}

%description -n python3-schedutils %_description

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

%files -n python3-schedutils
%license COPYING
%{_bindir}/pchrt
%{_bindir}/ptaskset
%{_mandir}/man1/pchrt.1*
%{_mandir}/man1/ptaskset.1*
%{python3_sitearch}/schedutils*.so
%{python3_sitearch}/*.egg-info

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.6-13
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jan 31 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.6-12
- Move to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6-7
- Subpackage python2-schedutils has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Jiri Kastner <jkastner@redhat.com> - 0.6-2
- duplicated license line in file list

* Mon Nov 20 2017 Jiri Kastner <jkastner@redhat.com> - 0.6-1
- added python 3 support

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5-5
- Python 2 binary package renamed to python2-schedutils
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Jiri Kastner <jkastner@redhat.com - 0.5-1
- new upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 10 2014 Jiri Kastner <jkastner@redhat.com> - 0.4-4
- fix source and url

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec  4 2013 Jiri Kastner <jkastner@redhat.com> - 0.4-1
- new upstream release
- resolves bz #879973

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2-3
- Rebuild for Python 2.6

* Thu Aug 28 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-2
- Fix build and install sections as suggested by the fedora rewiewer
  (BZ #460387)

* Wed Aug 27 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-1
- Add get_priority_{min,max} methods
- Add constants for SCHED_{BATCH,FIFO,OTHER,RR}
- Implement get_priority method
- Add pchrt utility for testing the bindings, chrt clone
- Add ptaskset utility for testing the bindings, taskset clone

* Tue Jun 10 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-3
- add dist to the release tag

* Wed Dec 19 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-2
- First build into rhel5-rt

* Wed Dec 19 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-1
- Initial package
