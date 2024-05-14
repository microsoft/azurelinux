Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:           sblim-cmpi-devel
Version:        2.0.3
Release:        21%{?dist}
Summary:        SBLIM CMPI Provider Development Support

License:        EPL
URL:            https://sblim.wiki.sourceforge.net/
Source0:        https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
# Source1: macro definitions
Source1: macros.sblim-cmpi-devel

# Patch0:       remove version from docdir
Patch0:         sblim-cmpi-devel-2.0.3-docdir.patch
BuildRequires:  gcc


%description
This packages provides the C and C++ CMPI header files needed by
provider developers and can be used standalone. If used for
C++ provider development it is also necessary to have
tog-pegasus-devel installed.

%package -n libcmpiCppImpl0
License:        EPL
Summary:        CMPI C++ wrapper library
Conflicts:      tog-pegasus-libs
BuildRequires:  gcc-c++

%description -n libcmpiCppImpl0
This packages provides the C++ wrapper library for CMPI development

%prep
%setup -q
%patch 0 -p1 -b .docdir

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
# install macro definitions
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cp %{SOURCE1} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d

%ldconfig_scriptlets -n libcmpiCppImpl0

%files
%doc AUTHORS COPYING README
%{_includedir}/cmpi
%{_rpmconfigdir}/macros.d/macros.sblim-cmpi-devel

%files -n libcmpiCppImpl0
%{_libdir}/libcmpiCppImpl.so*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.3-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-16
- Add BuildRequires gcc and gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-14
- Remove Group tag from spec file

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.3-8
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 25 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-7
- Add macros.sblim-cmpi-devel
- Remove %%clean section

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-4
- Fix for unversioned docdir change
  Resolves: #994075

* Thu Jul 25 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-3
- Fix libcmpiCppImpl0 Conflicts

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 13 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.3-1
- Update to sblim-cmpi-devel-2.0.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 28 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-3
- Enable -debuginfo package

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 20 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.1-1
- Update to sblim-cmpi-devel-2.0.1
- Ship libcmpiCppImpl library in libcmpiCppImpl0 package

* Wed Nov  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-2
- Fix conversion between CMPIData and String

* Thu Aug 27 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.0.5-2
- Fix License
- Spec file cleanup, rpmlint check

* Fri Oct 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.0.5-1
- Update to 1.0.5
  Resolves: #468326

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-6
- Autorebuild for GCC 4.3

* Mon Dec 18 2006 Mark Hamzy <hamzy@us.ibm.com> - 1.0.4-5
- Removed -debuginfo package.
- Removed ldconfig from post/postun

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.0.4-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Feb 09 2006 Viktor Mihajlovski <mihajlov@de.ibm.com> - 1.0.4-1
- Initial RH/Fedora version
