%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global maj 0
%bcond_with docs
Summary:        An LV2 Resource Description Framework Library
Name:           lilv
Version:        0.24.14
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://drobilla.net/software/lilv
Source0:        https://download.drobilla.net/%{name}-%{version}.tar.bz2
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  sord-devel >= 0.14.0
BuildRequires:  sratom-devel >= 0.4.4
BuildRequires:  lv2-devel >= 1.18.0
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  serd-devel >= 0.30.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libsndfile-devel >= 1.0.0
%if %{with docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_lv2_theme
%endif
Requires:       lv2 >= 1.18.0
%if 0%{?with_check}
BuildRequires:  lcov
%endif

# To try and deal with multilib issues from the -libs split:
# https://bugzilla.redhat.com/show_bug.cgi?id=2052588
Obsoletes:      lilv < 0.24.12-2

%description
%{name} is a library to make the use of LV2 plugins as simple as possible
for applications. Lilv is the successor to SLV2, rewritten to be significantly
faster and have minimal dependencies.

%package        libs
Summary:        Libraries for %{name}

%description libs
%{name} is a lightweight C library for Resource Description Syntax which
supports reading and writing Turtle and NTriples.

This package contains the libraries for %{name}.

%package devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for Resource Description Syntax which
supports reading and writing Turtle and NTriples.

This package contains the headers and development libraries for %{name}.

%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary:        Python bindings for %{name}
Requires:       %{name}-libs%{_isa} = %{version}-%{release}

%description -n python3-%{name}
%{name} is a lightweight C library for Resource Description Syntax which
supports reading and writing Turtle and NTriples.

This package contains the python libraries for %{name}.

%prep
%autosetup -p1
# Do not run ld config
sed -i -e 's|bld.add_post_fun(autowaf.run_ldconfig)||' wscript
# for packagers sake, build the tests with debug symbols
sed -i -e "s|'-ftest-coverage'\]|\
 '-ftest-coverage' \] + '%{optflags}'.split(' ')|" wscript

%build
%{set_build_flags}
export LINKFLAGS="%{__global_ldflags}"
%{python3} waf configure -v --prefix=%{_prefix} \
 --libdir=%{_libdir} --configdir=%{_sysconfdir} --mandir=%{_mandir} \
 --docdir=%{_pkgdocdir} \
%if %{with docs}
 --docs \
%endif
 --test --dyn-manifest

%{python3} waf -v build %{?_smp_mflags}

%install
%{python3} waf -v install --destdir=%{buildroot}
chmod +x %{buildroot}%{_libdir}/lib%{name}-0.so.*

%check
%{python3} waf test

%files
%if %{with docs}
%exclude %{_pkgdocdir}/%{name}-%{maj}/
%endif
%{_bindir}/lilv-bench
%{_bindir}/lv2info
%{_bindir}/lv2ls
%{_bindir}/lv2bench
%{_bindir}/lv2apply
%{_sysconfdir}/bash_completion.d/lilv
%{_mandir}/man1/*

%files libs
%doc AUTHORS NEWS README.md
%license COPYING
%{_libdir}/lib%{name}-%{maj}.so.*

%files devel
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%if %{with docs}
%{_pkgdocdir}/%{name}-%{maj}/
%endif

%files -n python3-%{name}
%{python3_sitelib}/%{name}.*
%{python3_sitelib}/__pycache__/*

%changelog
* Thu Nov 24 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.24.14-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Disable subpackage doc
- Enable check section
- License verified

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.24.14-2
- Rebuilt for Python 3.11

* Sat May 28 2022 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.14-1
- Update to 0.24.14

* Mon Apr 18 2022 Igor Raits <igor.raits@gmail.com> - 0.24.12-5
- Fix upgradepath for multilib

* Thu Feb 24 2022 Adam Williamson <awilliam@redhat.com> - 0.24.12-4
- Try and fix multilib upgrade issues from the package split (#2052588)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Adam Williamson <awilliam@redhat.com> - 0.24.12-2
- Split library into a separate package (#2032115)

* Fri Nov 26 2021 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.12-1
- Update to 0.24.12

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.24.10-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Oct 04 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.10-1
- Update to 0.24.10
- Run new test suite

* Wed Aug 19 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.8-1
- Update to 0.24.8

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.6-4
- Use upstream default lv2 path (#1856001)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.24.6-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 07 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.6-1
- Update to 0.24.6
- Add python3 bindings

* Wed Oct 30 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.4-7
- BR python3-numpy

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.4-4
- Use Python 3

* Wed Oct 03 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.4-3
- Remove Python 2 subpackage
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
  and https://bugzilla.redhat.com/show_bug.cgi?id=1634929

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.24.4-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.4-1
- Update to 0.24.4
- Remove ldconfig scriptlets
- Minor spec cleanup

* Sun Jul 15 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.2-9
- Fix FTBFS due to the move of /usr/bin/python into a separate package
- Add BR for gcc and gcc-c++

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 03 2018 Germano Massullo <germano.massullo@gmail.com> - 0.24.2-7
- removed %%dir %%{_sysconfdir}/bash_completion.d/ to fix bugreport #1303438

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.2-5
- Use versioned python macro python2_sitelib

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.24.2-4
- Python 2 binary package renamed to python2-lilv
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.24.2-1
- Update to 0.24.2
- Use hardened LDFLAGS
- Remove deprecated Group tags
- Use license macro
- Drop gcc patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.20.0-3
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 23 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-2
- Build against new version of sratom / sord

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-1
- Update to 0.20.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 11 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-2
- Add numpy BR

* Fri Jan 10 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-1
- New upstream release

* Thu Nov 28 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.16.0-3
- Install docs to (main, not devel) %%{_pkgdocdir} where available (#993969).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.16.0-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.14.4-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Karsten Hopp <karsten@redhat.com> 0.14.2-3
- bump release and rebuild, lilv was missing some deps on PPC*

* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.2-2
- Corrected waf configure

* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.2-1
- New upstream 0.14.2

* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-2
- Add python binding BR

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-1
- New upstream release 0.14.0

* Wed Feb 29 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Remove redundant build requires, merge python bindings
- Move man3 pages to devel package
- Apply patch to correct scale points iteration in test suite

* Sun Feb 26 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- Add python bindings, and missing build requires
- Move man pages to main package

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
