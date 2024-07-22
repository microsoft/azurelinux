Summary:        CPU Frequency changing related utilities
Name:           cpufrequtils
Version:        008
Release:        5%{?dist}
Group:          System Environment/Base
License:        GPLv2
URL:            https://mirrors.edge.kernel.org/pub/linux/utils/kernel/cpufreq/
Source:         https://mirrors.edge.kernel.org/pub/linux/utils/kernel/cpufreq/%{name}-%{version}.tar.gz
Patch0:         disable-gsic.patch
Patch1:         cpufrequtils-multilib.patch
Patch2:         cpufrequtils-008-aperf-32bit.patch
Patch50:        cpufrequtils-008-no-aperf-on-ppc.patch
BuildRequires:  libsysfs-devel
BuildRequires:  gettext
# pulls in automake and autoconf
BuildRequires:  libtool
ExclusiveArch:  %{ix86} x86_64 ppc ppc64
Provides:       cpufreq-utils = 1:%{version}-%{release}
Obsoletes:      cpufreq-utils < 1:%{version}-%{release}
 
%description
cpufrequtils contains several utilities that can be used to control
the cpufreq interface provided by the kernel on hardware that
supports CPU frequency scaling.
 
%package devel
Summary:        CPU frequency changing utilities development files
Group:          Development/Libraries
License:        GPLv2+
 
%description devel
The cpufrequtils development files.
 
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .aperf-32bit
%ifarch ppc ppc64
%patch50 -p1 -b .no-aperf-on-ppc
%endif
 
%build
make CFLAGS="$RPM_OPT_FLAGS" DEBUG=true
%ifarch %{ix86}
cd debug/i386
make CFLAGS="$RPM_OPT_FLAGS"
%endif
%ifarch x86_64
cd debug/x86_64
make CFLAGS="$RPM_OPT_FLAGS"
%endif
cd ..
 
%install
make DESTDIR=%{buildroot} mandir=%{_mandir} bindir=%{_bindir} includedir=%{_includedir} libdir=%{_libdir} install
 
# Remove libtool lib and static lib
rm -f %{buildroot}%{_libdir}/*.{a,la}
 
%find_lang cpufrequtils
 
%ifarch %{ix86}
cd debug/i386
install centrino-decode %{buildroot}%{_bindir}/centrino-decode
install dump_psb %{buildroot}%{_bindir}/dump_psb
install powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
cd ../..
%endif
%ifarch x86_64
cd debug/x86_64
install powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
cd ../..
%endif
 
chmod -R a-s %{buildroot}
 
%post -p /sbin/ldconfig
 
%postun -p /sbin/ldconfig
 
%files -f cpufrequtils.lang
%defattr(-,root,root,0755)
%doc COPYING
%{_libdir}/libcpufreq.so*
%{_bindir}
%{_mandir}/*/*
 
%files devel
%defattr(-,root,root,0755)
%doc COPYING
%{_includedir}/cpufreq.h
 
%changelog

* Mon Jul 22 2024 Aditya Dubey <adityadubey@microsoft.com> - 008-5
- Onboarding package to azurelinux

* Fri Feb 25 2011 Petr Sabata <psabata@redhat.com> - 008-5
- Build with DEBUG=true to avoid stripping
 
* Thu Feb 10 2011 Petr Sabata <psabata@redhat.com> - 008-4
- General spec file cleanup
- Do not build cpufreq-aperf on PPC/PPC64, rhbz#675829
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Mon Feb  7 2011 Petr Sabata <psabata@redhat.com> - 008-2
- Fixing aperf to work properly on 32bit arches, rhbz#675743
- aperf-32bit.patch
 
* Fri Jul 16 2010 Petr Sabata <psabata@redhat.com> - 008-1
- 008 version bump
- Multilib patch
 
* Thu Jul 08 2010 Petr Sabata <psabata@redhat.com> - 007-2
- Licensing guidelines compliance fix
- New cpufrequtils-devel subpackage created
- Spec file cleanup
 
* Mon Jan 18 2010 Anton Arapov <anton@redhat.com> 007-1
- New upstream release
 
* Wed Nov 11 2009 Anton Arapov <anton@redhat.com> 006-1
- New upstream release
 
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
 
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 005-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
 
* Fri Aug 15 2008 Jarod Wilson <jarod@redhat.com> 005-2
- Fix parallel build
 
* Sun Aug 10 2008 Jarod Wilson <jwilson@redhat.com> 005-1
- New upstream release
 
* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 004-2
- fix license tag
 
* Mon Jul 14 2008 Jarod Wilson <jwilson@redhat.com> 004-1
- New upstream release
 
* Tue May 27 2008 Jarod Wilson <jwilson@redhat.com> 003-1
- New upstream release
- Rename package to match upstream name (old cvs history
  can be found under old package name, cpufreq-utils)
- Drop static and libtool libs
 
* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com>
- Bump and rebuild with gcc 4.3
 
* Tue Jul 11 2006 Karsten Hopp <karsten@redhat.de>
- buildrequire libsysfs-devel
 
* Wed Jul  9 2006 Dave Jones <davej@redhat.com>
- Rebuild against new libsysfs
 
* Wed Jun  7 2006 Dave Jones <davej@redhat.com>
- Upstream -002 release.
 
* Sat Feb 11 2006 Dave Jones <davej@redhat.com>
- rebuild.
 
* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.
 
* Mon Dec 19 2005 Dave Jones <davej@redhat.com>
- New upstream 0.4 release.
 
* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj
 
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt
 
* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- package all files
 
* Mon May  9 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.3
 
* Fri Apr 22 2005 Matthias Saou <http://freshrpms.net/> 0.2-2
- Major spec file cleanup. (#155731)
- Use %%find_lang macro.
- Add missing sysfsutils-devel build requirement.
 
* Fri Apr 15 2005 Florian La Roche <laroche@redhat.com>
- remove empty preun script
 
* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4.
 
* Sun Feb 27 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.2
 
* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Rebuild with -D_FORTIFY_SOURCE=2
 
* Sat Dec  4 2004 Dave Jones <davej@redhat.com>
- Initial packaging
 