Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		pps-tools
Version:	1.0.2
Release:	6%{?dist}
Summary:	LinuxPPS user-space tools

License:	GPLv2+
URL:		https://github.com/redlab-i/pps-tools
Source0:	https://github.com/redlab-i/pps-tools/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	gcc

%description
This package includes the LinuxPPS user-space tools.

%package devel
Summary: LinuxPPS PPSAPI header file

%description devel
This package includes the header needed to compile PPSAPI (RFC-2783)
applications.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_includedir}/sys}
install -m755 -t $RPM_BUILD_ROOT%{_bindir} \
	ppsctl ppsfind ppsldisc ppstest ppswatch
install -p -m644 -t $RPM_BUILD_ROOT%{_includedir}/sys timepps.h

%files
%license COPYING
%{_bindir}/pps*

%files devel
%license COPYING
%{_includedir}/sys/timepps.h

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Miroslav Lichvar <mlichvar@redhat.com> 1.0.2-1
- update to 1.0.2
- add gcc to build requirements
- build with hardening LDFLAGS

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.16.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.15.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.14.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.13.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.12.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.11.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.10.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.8.20120407git0deb9c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Miroslav Lichvar <mlichvar@redhat.com> 0-0.7.20120407git0deb9c
- update to 20120407git0deb9c
- move timepps.h to sys (#852950)
- include license files in devel subpackage
- remove obsolete macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.20120215gitac0aa6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.20120215gitac0aa6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Miroslav Lichvar <mlichvar@redhat.com> 0-0.4.20120215gitac0aa6
- update to 20120215gitac0aa6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20100413git74c32c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.2.20100413git74c32c
- include README and copyright (#692069) 
- provide also <sys/timepps.h>

* Wed Mar 30 2011 Miroslav Lichvar <mlichvar@redhat.com> 0-0.1.20100413git74c32c
- initial release
