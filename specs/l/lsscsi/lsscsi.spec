# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        List SCSI devices (or hosts) and associated information
Name:           lsscsi
Version:        0.32
Release:        14%{?dist}
License:        GPL-2.0-or-later
# official git repository: https://github.com/doug-gilbert/lsscsi
Source0:        http://sg.danny.cz/scsi/%{name}-%{version}.tgz
URL:            http://sg.danny.cz/scsi/lsscsi.html
BuildRequires:  gcc
BuildRequires:  make

%description
Uses information provided by the sysfs pseudo file system in Linux kernel
2.6 series to list SCSI devices or all SCSI hosts. Includes a "classic"
option to mimic the output of "cat /proc/scsi/scsi" that has been widely
used prior to the lk 2.6 series.

Author:
--------
    Doug Gilbert <dgilbert(at)interlog(dot)com>


%prep
%autosetup -p1

%build
%configure
%make_build


%install
%make_install


%files
%doc ChangeLog INSTALL README CREDITS AUTHORS COPYING
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 12 2024 Tomas Bzatek <tbzatek@redhat.com> - 0.32-11
- Use a SPDX license tag

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Dan Horák <dan[at]danny.cz> - 0.32-3
- update to 0.32 final

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Tomas Bzatek <tbzatek@redhat.com> - 0.32-1
- Update to 0.32 upstream snapshot

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.31-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Feb 21 2020 Dan Horák <dan[at]danny.cz> - 0.31-1
- update to 0.31 (#1758436)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Dan Horák <dan[at]danny.cz> - 0.30-1
- update to 0.30

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Dan Horák <dan[at]danny.cz> - 0.28-8
- fix FTBFS

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Dec 06 2014 Dan Horák <dan[at]danny.cz> - 0.28-1
- update to 0.28

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 17 2013 Dan Horák <dan[at]danny.cz> - 0.27-1
- update to 0.27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Dan Horák <dan[at]danny.cz> - 0.26-1
- update to 0.26

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Dan Horák <dan[at]danny.cz> - 0.25-1
- update to 0.25

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May  6 2010 Dan Horák <dan[at]danny.cz> - 0.23-2
- fix path separator for FC devices (#589327)
- fix for kernels with unified string representation of NULL (#589860)

* Sun Dec  6 2009 Dan Horák <dan[at]danny.cz> - 0.23-1
- update to 0.23

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Dan Horák <dan[at]danny.cz> - 0.22-1
- update to 0.22

* Tue Nov  4 2008 Dan Horák <dan[at]danny.cz> - 0.21-2
- add disttag

* Tue Nov  4 2008 Dan Horák <dan[at]danny.cz> - 0.21-1
- update to 0.21
- update urls

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-6
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-5
- Autorebuild for GCC 4.3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.17-4
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 - Chip Coldwell <coldwell@redhat.com> 0.17-3
- bump the EVR for FC6 rebuild
* Mon Jul 17 2006 - Chip Coldwell <coldwell@redhat.com> 0.17-2
- modify spec file to meet Fedora Project packaging guidelines
* Mon Feb 06 2006 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.17-1
- fix disappearance of block device names in lk 2.6.16-rc1
* Fri Dec 30 2005 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.16-1
- wlun naming, osst and changer devices
* Tue Jul 19 2005 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.15-1
- does not use libsysfs, add filter argument, /dev scanning
* Fri Aug 20 2004 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.13-1
- add 'timeout'
* Sun May 9 2004 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.12-1
- rework for lk 2.6.6, device state, host name, '-d' for major+minor
* Fri Jan 09 2004 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.11-1
- rework for lk 2.6.1
* Tue May 06 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.10-1
- adjust HBA listing for lk > 2.5.69
* Fri Apr 04 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.09-1
- fix up sorting, GPL + copyright notice
* Sun Mar 2 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.08-1
- start to add host listing support (lk >= 2.5.63)
* Fri Feb 14 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.07-1
- queue_depth name change in sysfs (lk 2.5.60)
* Mon Jan 20 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.06-1
- osst device file names fix
* Sat Jan 18 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.05-1
- output st and osst device file names (rather than "-")
* Thu Jan 14 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.04-1
- fix multiple listings of st devices (needed for lk 2.5.57)
* Thu Jan 09 2003 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.03-1
- add --generic option (list sg devices), scsi_level output
* Wed Dec 18 2002 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.02-1
- add more options including classic mode
* Fri Dec 13 2002 - Doug Gilbert <dgilbert(at)interlog(dot)com> 0.01-1
- original
