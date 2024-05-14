Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           cpuid
Version:        20200427
Release:        2%{?dist}
Summary:        Dumps information about the CPU(s)

License:        GPLv2+
URL:            https://www.etallen.com/cpuid.html
Source0:        https://www.etallen.com/%{name}/%{name}-%{version}.src.tar.gz

BuildRequires:  gcc
BuildRequires:  perl-podlators

ExclusiveArch:  %{ix86} x86_64

%description
cpuid dumps detailed information about x86 CPU(s) gathered from the CPUID
instruction, and also determines the exact model of CPU(s). It supports Intel,
AMD, and VIA CPUs, as well as older Transmeta, Cyrix, UMC, NexGen, and Rise
CPUs. 

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64 -DVERSION=%{version}" LDFLAGS="$RPM_LD_FLAGS"

%install
install -Dp -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dp -m 0755 cpuinfo2cpuid %{buildroot}%{_bindir}/cpuinfo2cpuid
install -Dp -m 0644 %{name}.man.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%files
%doc ChangeLog FUTURE
%license LICENSE
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_bindir}/cpuinfo2cpuid

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200427-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 27 2020 Fabian Affolter <mail@fabian-affolter.ch> - 20200427-1
- Update to new upstream version 20200427 (rhbz#1828251)

* Thu Feb 27 2020 Fabian Affolter <mail@fabian-affolter.ch> - 20200211-1
- Update to new upstream version 20200211 (rhbz#1792969)

* Thu Jan 30 2020 Fabian Affolter <mail@fabian-affolter.ch> - 20200127-1
- Update to new upstream version 20200127

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Fabian Affolter <mail@fabian-affolter.ch> - 20200116-1
- Update to new upstream version 20200116 (rhbz#1792118)

* Sun Jan 12 2020 Fabian Affolter <mail@fabian-affolter.ch> - 20200112-1
- Update to new upstream version 20200112 (rhbz#1790230)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180519-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180519-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180519-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Fabian Affolter <mail@fabian-affolter.ch> - 20180519-1
- Update to new upstream version 20180519 (rhbz#1580087)

* Sat May 05 2018 Fabian Affolter <mail@fabian-affolter.ch> - 20180419-1
- Update to new upstream version 20180419 (rhbz#1569758)

* Thu Feb 22 2018 Florian Weimer <fweimer@redhat.com> - 20170122-7
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170122-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 22 2017 Fabian Affolter <mail@fabian-affolter.ch> - 20170122-5
- Add cpuinfo2cpuid

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170122-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Fabian Affolter <mail@fabian-affolter.ch> - 20170122-1
- Update to new upstream version 20170122 (rhbz#1415518)

* Sun Dec 04 2016 Fabian Affolter <mail@fabian-affolter.ch> - 20161201-1
- Update to new upstream version 20161201 (rhbz#1400731)

* Fri Nov 18 2016 Fabian Affolter <mail@fabian-affolter.ch> - 20161114-2
- Update license is now GPLv2+ and no longer MIT

* Tue Nov 15 2016 Fabian Affolter <mail@fabian-affolter.ch> - 20161114-1
- Update to new upstream version 20161114 (rhbz#1394984)

* Tue Aug 30 2016 Fabian Affolter <mail@fabian-affolter.ch> - 20160814-1
- Update to new upstream version 20160814 (rhbz#20160814)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 20151017-1
- Update to new upstream version 20151017 (rhbz#1272715)

* Fri Jun 26 2015 Fabian Affolter <mail@fabian-affolter.ch> - 20150606-1
- Update to new upstream version 20150606

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140123-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140123-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 25 2014 Fabian Affolter <mail@fabian-affolter.ch> - 20140123-1
- Update to new upstream version 20130123

* Tue Jan 14 2014 Fabian Affolter <mail@fabian-affolter.ch> - 20140114-1
- Update to new upstream version 20130114

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130610-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Fabian Affolter <mail@fabian-affolter.ch> - 20130610-1
- Update to new upstream version 20130610

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120601-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Fabian Affolter <mail@fabian-affolter.ch> - 20120601-1
- Update to new upstream version 20120601

* Sun Feb 26 2012 Fabian Affolter <mail@fabian-affolter.ch> - 20120225-1
- Update to new upstream version 20120225

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110305-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 06 2011 Fabian Affolter <mail@fabian-affolter.ch> - 20110305-1
- Update to new upstream version 20110305

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Fabian Affolter <mail@fabian-affolter.ch> - 20101010-1
- Update to new upstream version 20101002

* Thu Sep 02 2010 Fabian Affolter <mail@fabian-affolter.ch> - 20100901-1
- Update to new upstream version 20100901

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20060917-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20060917-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Fabian Affolter <mail@fabian-affolter.ch> - 20060917-4
- Change %%build section acc. #469590 comment #5

* Sat Nov 08 2008 Fabian Affolter <mail@fabian-affolter.ch> - 20060917-3
- Change %%build section and License acc. #469590 comment #3
- Fix %%doc in changelog

* Tue Nov 04 2008 Fabian Affolter <mail@fabian-affolter.ch> - 20060917-2
- Switch to ExclusiveArch
- Remove %%doc from man page and general changes to the man page installation

* Sun Nov 02 2008 Fabian Affolter <mail@fabian-affolter.ch> - 20060917-1
- Initial package for Fedora
