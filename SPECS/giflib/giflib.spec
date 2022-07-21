Name:           giflib
Summary:        A library and utilities for processing GIFs
Version:        5.2.1
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.sourceforge.net/projects/giflib/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Move quantize.c back into libgif.so (#1750122)
Patch0:         giflib_quantize.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  xmlto

%description
giflib is a library for reading and writing gif images.

%package        devel
Summary:        Development files for programs using the giflib library
Requires:       %{name} = %{version}-%{release}

%description    devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library.

%package        utils
Summary:        Programs for manipulating GIF format image files
Requires:       %{name} = %{version}-%{release}

%description    utils
The giflib-utils package contains various programs for manipulating GIF
format image files.

%prep
%autosetup -p1

%build
%make_build CFLAGS="%{optflags} -fPIC" LDFLAGS="%{__global_ldflags}"

%install
%make_install PREFIX="%{_prefix}" LIBDIR="%{_libdir}"
find %{buildroot} -name '*.a' -print -delete

%ldconfig_scriptlets

%files
%license COPYING
%doc ChangeLog NEWS README
%{_libdir}/libgif.so.7*

%files devel
%doc doc/*
%{_libdir}/libgif.so
%{_includedir}/gif_lib.h

%files utils
%{_bindir}/gif*
%{_mandir}/man1/*.1*

%changelog
* Mon Jul 11 2022 Olivia Crain <oliviacrain@microsoft.com> - 5.2.1-6
- Promote to mariner-official-base repo
- Lint spec
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2.1-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Sandro Mani <manisandro@gmail.com> - 5.2.1-3
- Move quantize.c back into libgif.so (#1750122)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Sandro Mani <manisandro@gmail.com> - 5.2.1-1
- Update to 5.2.1

* Mon Apr 01 2019 Sandro Mani <manisandro@gmail.com> - 5.1.9-1
- Update to 5.1.9

* Wed Mar 20 2019 Sandro Mani <manisandro@gmail.com> - 5.1.8-1
- Update to 5.1.8

* Mon Mar 11 2019 Sandro Mani <manisandro@gmail.com> - 5.1.7-1
- Update to 5.1.7

* Sat Feb 23 2019 Sandro Mani <manisandro@gmail.com> - 5.1.6-2
- Fix broken soname

* Mon Feb 18 2019 Sandro Mani <manisandro@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 5.1.4-1
- Update to 5.1.4

* Thu Feb  8 2018 Florian Weimer <fweimer@redhat.com> - 4.1.6-22
- Build libungif with linker flags from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.6-20
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 4.1.6-17
- Fix compilation errors when -Werror=format-security

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 4.1.6-14
- Link libungif with -z now too

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.1.6-10
- Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.1.6-8
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 09 2009 Robert Scheck <robert@fedoraproject.org> 4.1.6-2
- Solved multilib problems with documentation (#465208, #474538)
- Removed static library from giflib-devel package (#225796 #c1)

* Mon Apr 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1.6-1
- update to 4.1.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.3-9
- Autorebuild for GCC 4.3

* Tue Mar 13 2007 Karsten Hopp <karsten@redhat.com> 4.1.3-8
- add BR libXt-devel, otherwise X support will be disabled

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 4.1.3-7
- buildrequires libICE-devel, libSM-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 4.1.3-6
- Switch requires to modular X

* Wed Sep 21 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-5
- Merge an option on the empty library link line.
- Obsolete libungif progs package.
- Rename -progs to -utils as FC packages seem to have moved in this direction
  for subpackages.
 
* Tue Sep 20 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-4
- Modify the way we provide libungif compatibility by building an empty
  library that requires libgif.
- Remove chmod in install.  It doesn't seem to be necessary.
- Add a patch to fix a problem with long being 64 bit on x86_64 but the code
  assuming it was 32 bit.
  
* Mon Sep 19 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-1
- Port package from libungif to giflib.
