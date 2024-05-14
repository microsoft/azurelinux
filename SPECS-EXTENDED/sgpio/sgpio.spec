Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: SGPIO captive backplane tool
Name: sgpio
Version: 1.2.0.10
Release: 28%{?dist}
License: GPLv2+
URL: https://sources.redhat.com/lvm2/wiki/DMRAID_Eventing
Source0: %{_distro_sources_url}/%{name}-1.2-0.10-src.tar.gz
# there is no official download link for the latest package
#Source: https://sources.redhat.com/lvm2/wiki/DMRAID_Eventing?action=AttachFile&do=get&target=sgpio-1.2.tgz
Patch0: sgpio-1.2-makefile.patch
Patch1: sgpio-1.2-coverity.patch
BuildRequires:  gcc
BuildRequires: dos2unix

%description
Intel SGPIO enclosure management utility

%prep
%setup -q -n sgpio
dos2unix --keepdate Makefile README
%patch 0 -p1 -b .makefile
%patch 1 -p1 -b .coverity
chmod a-x *

%build
#@@@ workaround for #474755 - remove with next update
make clean
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT SBIN_DIR=$RPM_BUILD_ROOT%{_sbindir} MANDIR=$RPM_BUILD_ROOT%{_mandir}

%files
%license LICENSE_GPL
%doc README
%{_sbindir}/sgpio
%{_mandir}/man1/sgpio.*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0.10-28
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.2.0.10-27
- Update Source0
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0.10-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Jan Synáček <jsynacek@redhat.com> - 1.2.0.10-21
- use distribution LDFLAGS during build (#1548559)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Jan Synáček <jsynacek@redhat.com> - 1.2.0.10-10
- Use strncpy instead of strcpy (coverity)
- Comment makefile patch

* Mon Nov 19 2012 Jan Synáček <jsynacek@redhat.com> - 1.2.0.10-9
- dos2unix'ed the patch
- Call dos2unix before patching and dos2unix Makefile as well
- Use %%{_sbindir} instead of '/sbin'

* Thu Aug 23 2012 Jan Synáček <jsynacek@redhat.com> - 1.2.0.10-8
- Improve spec

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 05 2012 Jan Synáček <jsynacek@redhat.com> 1.2.0.10-6
- Rebuilt for GCC 4.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0.10-3
- rebuild for F12

* Tue Apr 14 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0.10-2
- move the EOL conversion and the removal of
  executable bits from %%install to %%prep section

* Wed Dec 10 2008 Jiri Moskovcak <jmoskovc@redhat.com> 1.2.0_10-1
- initial Fedora release
