Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: pnm2ppa
Summary: Drivers for printing to HP PPA printers
Version: 1.04
Release: 50%{?dist}
URL: http://sourceforge.net/projects/pnm2ppa 
Source: http://download.sourceforge.net/pnm2ppa/pnm2ppa-%{version}.tar.gz
# Following sourcelink is dead currently.
Source1: http://www.httptech.com/ppa/files/ppa-0.8.6.tar.gz
# Upstream sync.
Patch2: pbm2ppa-20000205.diff
# Use RPM_OPT_FLAGS.
Patch3: pnm2ppa-redhat.patch
# Don't return a local variable out of scope (bug #704568).
Patch4: pnm2ppa-coverity-return-local.patch
# add ldflags to Makefile
Patch5: pnm2ppa-ldflags.patch
# FTBFS with GCC 10
Patch6: pnm2ppa-gcc10.patch
# fix argument reading for non x86_64 archs - use int instead of char
Patch7: pnm2ppa-optargs-read.patch
License: GPLv2+

# gcc is no longer in buildroot by default
BuildRequires: gcc

# foomatic is needed for using the filters in CUPS
Requires: foomatic

%description
Pnm2ppa is a color driver for HP PPA host-based printers such as the
HP710C, 712C, 720C, 722C, 820Cse, 820Cxi, 1000Cse, and 1000Cxi.
Pnm2ppa accepts Ghostscript output in PPM format and sends it to the
printer in PPA format.

Install pnm2ppa if you need to print to a PPA printer.

%prep
%setup -q

#pbm2ppa source
%setup -q -T -D -a 1 
%patch2 -p0 -b .20000205
%patch3 -p1 -b .rh
%patch4 -p1 -b .coverity-return-local
%patch5 -p1 -b .ldflags
%patch6 -p1 -b .gcc10
%patch7 -p1 -b .optargs-read

for file in docs/en/LICENSE pbm2ppa-0.8.6/LICENSE; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done

%build
# set redhat build flags
%set_build_flags
%make_build
pushd pbm2ppa-0.8.6
%make_build
popd


%install
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
make INSTALLDIR=$RPM_BUILD_ROOT%{_bindir} CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
    MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install 
install -p -m 0755 utils/Linux/detect_ppa $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 utils/Linux/test_ppa $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 pbm2ppa-0.8.6/pbm2ppa  $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 pbm2ppa-0.8.6/pbmtpg   $RPM_BUILD_ROOT%{_bindir}
install -p -m 0644 pbm2ppa-0.8.6/pbm2ppa.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 0644 pbm2ppa-0.8.6/pbm2ppa.1   $RPM_BUILD_ROOT%{_mandir}/man1

chmod 644 docs/en/LICENSE
mkdir -p pbm2ppa
for file in CALIBRATION CREDITS INSTALL INSTALL-MORE LICENSE README ; do
  install -p -m 0644 pbm2ppa-0.8.6/$file pbm2ppa/$file
done


%files 
%license docs/en/LICENSE
%doc docs/en/CREDITS docs/en/INSTALL docs/en/README
%doc docs/en/RELEASE-NOTES docs/en/TODO
%doc docs/en/INSTALL.REDHAT.txt docs/en/COLOR.txt docs/en/CALIBRATION.txt
%doc docs/en/INSTALL.REDHAT.html docs/en/COLOR.html docs/en/CALIBRATION.html
%doc test.ps
%doc pbm2ppa
%{_bindir}/pnm2ppa
%{_bindir}/pbm2ppa
%{_bindir}/pbmtpg
%{_bindir}/calibrate_ppa
%{_bindir}/test_ppa
%{_bindir}/detect_ppa
%{_mandir}/man1/pnm2ppa.1*
%{_mandir}/man1/pbm2ppa.1*
%config(noreplace) %{_sysconfdir}/pnm2ppa.conf
%config(noreplace) %{_sysconfdir}/pbm2ppa.conf

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.04-50
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.04-49
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Tue Aug 04 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-48
- fix argument reading for non x86_64 archs - use int instead of char

* Mon Aug 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-47
- add foomatic as a dependency, because pnm2ppa drivers are not available as a driver without it

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-45
- FTBFS with GCC 10

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-41
- correcting license

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-39
- ship license in %%license tag

* Thu Mar 01 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-38
- 1548734 - pnm2ppa: Partial Fedora build flags injection

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-37
- gcc is no longer in buildroot by default

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1:1.04-35
- remove old stuff https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MRWOMRZ6KPCV25EFHJ2O67BCCP3L4Y6N/

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.04-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Tim Waugh <twaugh@redhat.com> - 1:1.04-25
- Fixed license tag.  pnm2ppa is GPLv2+; pbm2ppa is GPLv2.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 20 2011 Tim Waugh <twaugh@redhat.com> - 1:1.04-22
- Don't return a local variable out of scope (bug #704568).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> - 1:1.04-20
- Merge-review cleanup (#226303)

* Fri Mar  5 2010 Tim Waugh <twaugh@redhat.com> - 1:1.04-19
- Consistent use of macros.
- Removed ancient obsoletes tag.
- Clean buildroot in install section not prep section.
- Make setup quiet.
- Use noreplace for config files.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Tim Waugh <twaugh@redhat.com> 1:1.04-16
- Removed patch fuzz.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 1:1.04-15
- Rebuild for GCC 4.3.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.04-14
- Added dist tag.
- Fixed summary.
- Better buildroot tag.
- More specific license tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.04-13.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Tim Waugh <twaugh@redhat.com> 1:1.04-13
- Rebuild for new GCC.

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 1:1.04-12
- s/Copyright:/License:/.
- s/Serial:/Epoch:/.
- Rebuilt.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Dec 11 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Upgrade to 1.04, editied the pbm2ppa patch to add <string.h>
- to pbmtpg.c, which uses strmp, edited the redhat patch to
- apply cleanly.

* Thu Aug 17 2000 Bill Nottingham <notting@redhat.com>
- tweak summary

* Thu Aug  3 2000 Bill Nottingham <notting@redhat.com>
- build upstream package

* Tue Jul 11 2000 Duncan Haldane <duncan_haldane@users.sourceforge.net>
- updated for 1.0 release.

* Mon Jul 10 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- remove execute bits from config file and man-page

* Sun Apr 09 2000 <duncan_haldane@users.sourceforge.net>
- added optional updated rhs-printfilter  files

* Thu Feb 10 2000 Bill Nottingham <notting@redhat.com>
- adopt upstream package

* Sun Feb 6 2000 <duncan_haldane@users.sourceforge.net>
- new pnm2ppa release,  and add pbm2ppa driver.

* Thu Jan 6 2000 <duncan_haldane@users.sourceforge.net>
- created rpm



