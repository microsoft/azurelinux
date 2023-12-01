%global debug_package %{nil}

Name:           catch
Version:        2.13.8
Release:        1%{?dist}
Summary:        Modern, C++-native, header-only, framework for unit-tests, TDD and BDD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
License:        Boost
URL:            https://github.com/catchorg/Catch2
Source0:        https://github.com/catchorg/Catch2/archive/refs/tags/v%{version}.tar.gz#/Catch2-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  python3

%description
Catch stands for C++ Automated Test Cases in Headers and is a
multi-paradigm automated test framework for C++ and Objective-C (and,
maybe, C). It is implemented entirely in a set of header files, but
is packaged up as a single header for extra convenience.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
Catch stands for C++ Automated Test Cases in Headers and is a
multi-paradigm automated test framework for C++ and Objective-C (and,
maybe, C). It is implemented entirely in a set of header files, but
is packaged up as a single header for extra convenience.

%prep
%autosetup -n Catch2-%{version}

%build
%cmake . -Bbuild -DCATCH_ENABLE_WERROR=OFF
%make_build -Cbuild

%install
%make_install -Cbuild
rm -rf %{buildroot}/%{_docdir}

%check
cd build
ctest -V %{?_smp_mflags}

%files devel
%license LICENSE.txt
%doc README.md CODE_OF_CONDUCT.md docs
%{_includedir}/catch2/
%{_datadir}/Catch2/
%{_datadir}/pkgconfig/catch2.pc
%{_libdir}/cmake/Catch2/

%changelog
* Tue Jan 11 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.13.8-1
- Upgrade to 2.13.8

* Thu Nov 11 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.13.7-1
- Upgrade to latest upstream version for glibc > 2.33 compatibility

* Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.10.2-1
- Update to 2.10.2 upstream release. License verified.

* Thu Dec 5 2019 Emre Girgin <mrgirgin@microsoft.com> - 2.9.2-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Fri Aug 16 2019 Tom Hughes <tom@compton.nu> - 2.9.2-1
- Update to 2.9.2 upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Tom Hughes <tom@compton.nu> - 2.9.1-1
- Update to 2.9.1 upstream release

* Sun Jun 16 2019 Tom Hughes <tom@compton.nu> - 2.9.0-1
- Update to 2.9.0 upstream release

* Mon May 27 2019 Tom Hughes <tom@compton.nu> - 2.8.0-1
- Update to 2.8.0 upstream release

* Mon Apr 22 2019 Tom Hughes <tom@compton.nu> - 2.7.2-1
- Update to 2.7.2 upstream release

* Mon Apr  8 2019 Tom Hughes <tom@compton.nu> - 2.7.1-1
- Update to 2.7.1 upstream release

* Fri Mar  8 2019 Tom Hughes <tom@compton.nu> - 2.7.0-1
- Update to 2.7.0 upstream release

* Tue Feb 12 2019 Tom Hughes <tom@compton.nu> - 2.6.1-1
- Update to 2.6.1 upstream release

* Thu Jan 31 2019 Tom Hughes <tom@compton.nu> - 2.6.0-1
- Update to 2.6.0 upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec  3 2018 Tom Hughes <tom@compton.nu> - 2.5.0-1
- Update to 2.5.0 upstream release

* Sun Oct 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Mon Jul 23 2018 Tom Hughes <tom@compton.nu> - 2.3.0-1
- Update to 2.3.0 upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun  8 2018 Tom Hughes <tom@compton.nu> - 2.2.3-1
- Update to 2.2.3 upstream release

* Fri Apr  6 2018 Tom Hughes <tom@compton.nu> - 2.2.2-1
- Update to 2.2.2 upstream release

* Sun Mar 11 2018 Tom Hughes <tom@compton.nu> - 2.2.1-1
- Update to 2.2.1 upstream release

* Wed Mar  7 2018 Tom Hughes <tom@compton.nu> - 2.2.0-1
- Update to 2.2.0 upstream release

* Sat Feb 10 2018 Tom Hughes <tom@compton.nu> - 2.1.2-1
- Update to 2.1.2 upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Tom Hughes <tom@compton.nu> - 2.1.1-1
- Update to 2.1.1 upstream release

* Sun Jan 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Sun Jan 14 2018 Tom Hughes <tom@compton.nu> - 1.12.0-1
- Update to 1.12.0 upstream release

* Wed Nov  1 2017 Tom Hughes <tom@compton.nu> - 1.11.0-1
- Update to 1.11.0 upstream release

* Sun Aug 27 2017 Tom Hughes <tom@compton.nu> - 1.10.0-1
- Update to 1.10.0 upstream release

* Fri Aug 11 2017 Tom Hughes <tom@compton.nu> - 1.9.7-1
- Update to 1.9.7 upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Tom Hughes <tom@compton.nu> - 1.9.6-1
- Update to 1.9.6 upstream release

* Fri Jun 16 2017 Tom Hughes <tom@compton.nu> - 1.9.5-1
- Update to 1.9.5 upstream release

* Tue May 16 2017 Tom Hughes <tom@compton.nu> - 1.9.4-1
- Update to 1.9.4 upstream release

* Wed Apr 26 2017 Tom Hughes <tom@compton.nu> - 1.9.3-1
- Update to 1.9.3 upstream release

* Tue Apr 25 2017 Tom Hughes <tom@compton.nu> - 1.9.2-1
- Update to 1.9.2 upstream release

* Mon Apr 10 2017 Tom Hughes <tom@compton.nu> - 1.9.1-1
- Update to 1.9.1 upstream release

* Sat Apr  8 2017 Tom Hughes <tom@compton.nu> - 1.9.0-1
- Update to 1.9.0 upstream release

* Wed Mar 15 2017 Tom Hughes <tom@compton.nu> - 1.8.2-1
- Update to 1.8.2 upstream release

* Sat Mar  4 2017 Tom Hughes <tom@compton.nu> - 1.8.1-1
- Update to 1.8.1 upstream release

* Wed Mar  1 2017 Tom Hughes <tom@compton.nu> - 1.8.0-1
- Update to 1.8.0 upstream release

* Fri Feb 10 2017 Tom Hughes <tom@compton.nu> - 1.7.1-1
- Update to 1.7.1 upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb  3 2017 Tom Hughes <tom@compton.nu> - 1.7.0-1
- Update to 1.7.0 upstream release

* Sun Jan 29 2017 Tom Hughes <tom@compton.nu> - 1.6.1-1
- Update to 1.6.1 upstream release

* Sun Jan 15 2017 Tom Hughes <tom@compton.nu> - 1.6.0-1
- Update to 1.6.0 upstream release

* Tue Dec 13 2016 Tom Hughes <tom@compton.nu> - 1.5.9-1
- Update to 1.5.9 upstream release

* Thu Nov 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.5.8-1
- Update to 1.5.8

* Sat May 14 2016 Tom Hughes <tom@compton.nu> - 1.5.4-1
- Update to 1.5.4 upstream release

* Thu Apr 28 2016 Tom Hughes <tom@compton.nu> - 1.5.1-1
- Update to 1.5.1 upstream release

* Sun Apr 24 2016 Tom Hughes <tom@compton.nu> - 1.5.0-1
- Update to 1.5.0 upstream release

* Wed Mar 30 2016 Tom Hughes <tom@compton.nu> - 1.4.0-1
- Update to 1.4.0 upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Tom Hughes <tom@compton.nu> - 1.2.1-1
- Initial build
