%define version_with_hyphens %(version="%{version}" && echo "${version//./-}")

Summary:        NTLMv1 authentication library
Name:           libntlm
Version:        1.6
Release:        1%{?dist}
License:        LGPL-2.1-only
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/gsasl/libntlm/
Source0:        https://gitlab.com/gsasl/libntlm/-/archive/%{name}-%{version_with_hyphens}/%{name}-%{name}-%{version_with_hyphens}.tar.gz

BuildRequires:  gcc
BuildRequires:  pkg-config

Provides:       bundled(gnulib)

%description
A library for authenticating with Microsoft NTLMV1 challenge-response,
derived from Samba sources.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
sed -i 's|$(install_sh) -c|$(install_sh) -pc|g' Makefile

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -delete -print

%files
%license COPYING
%doc AUTHORS ChangeLog README THANKS
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/ntlm.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Nov 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-1
- Updated to version 1.6 to fix CVE-2019-17455.
- License verified.
- Updated URLs.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Kevin Fenzi <kevin@scrye.com> - 1.5-1
- Update to 1.5.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Kevin Fenzi <kevin@scrye.com> - 1.4-11
- Fix FTBFS bug #1604621.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Christopher Meng <rpm@cicku.me> - 1.4-1
- New release(BZ#1000496).
- Add gnulib virtual provides(BZ#821770).
- Add AArch64 support(BZ#925829).
- Devel package explicit arch requires.
- Correct summary as it only supports V1 protocol.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 5 2011 Nikolay Vladimirov <nikolay@vladimiroff.com> - 1.3-1
- new upstream release
- change sources

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 12 2010 Nikolay Vladimirov <nikolay@vladimiroff.com> - 1.2-1
- new upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Apr 19 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> - 1.0-1
- new upstream release

* Thu Mar 6 2008 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.4.2-1
- new upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.1-2
- Autorebuild for GCC 4.3

* Wed Jan 23 2008  Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.4.1-1
- new upstrem release

* Wed Aug 29 2007  Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.3.13-5
- rebuild for ppc32 selinux fix

* Thu Aug 2 2007 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.3.13-4
- License tag changed

* Thu Jun 21 2007 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.3.13-3
- minor mixed-use-of-spaces-and-tabs fix

* Thu Jun 21 2007 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.3.13-2
- fixed summary
- fixed requires and buildrequires for pkgconfig
- fixed the timestamp of ntlm.h

* Wed Jun 20 2007 Nikolay Vladimirov <nikolay@vladimiroff.com> - 0.3.13-1
- initial release
