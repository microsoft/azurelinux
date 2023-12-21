Vendor:         Microsoft Corporation
Distribution:   Mariner
%global debug_package %{nil}

Name:           catch1
Version:        1.12.2
Release:        7%{?dist}
Summary:        A modern, C++-native, header-only, framework for unit-tests, TDD and BDD

License:        Boost
URL:            https://github.com/philsquared/Catch
Source0:        https://github.com/philsquared/Catch/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         catch1-sigstksz.patch

BuildRequires:  cmake make gcc-c++

%description
Catch stands for C++ Automated Test Cases in Headers and is a
multi-paradigm automated test framework for C++ and Objective-C (and,
maybe, C). It is implemented entirely in a set of header files, but
is packaged up as a single header for extra convenience.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Conflicts:      catch-devel

%description    devel
Catch stands for C++ Automated Test Cases in Headers and is a
multi-paradigm automated test framework for C++ and Objective-C (and,
maybe, C). It is implemented entirely in a set of header files, but
is packaged up as a single header for extra convenience.


%prep
%autosetup -p 1 -n Catch2-%{version}


%build
%cmake . -Bbuild -DCATCH_ENABLE_WERROR=OFF
%make_build -Cbuild


%install
mkdir -p %{buildroot}%{_includedir}
cp -pr include  %{buildroot}%{_includedir}/catch


%check
cd build
ctest -V %{?_smp_mflags}


%files devel
%doc README.md catch-logo-small.png docs
%license LICENSE.txt
%{_includedir}/catch


%changelog
* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.12.2-7
- Add catch1-sigstksz patch.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.12.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 15 2018 Tom Hughes <tom@compton.nu> - 1.12.2-1
- Update to 1.12.2 upstream release

* Sat Mar  3 2018 Tom Hughes <tom@compton.nu> - 1.12.1-1
- Update to 1.12.1 upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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
