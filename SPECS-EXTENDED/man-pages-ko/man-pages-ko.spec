Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Korean(Hangul) Man(manual) Pages from the Korean Manpage Project
Name: man-pages-ko
Version: 20050219
Release: 39%{?dist}
License: Copyright only
#Vendor: Korean Manpage Project Team.
URL: https://man.kldp.org/
Source0: https://kldp.net/frs/download.php/1918/%{name}-%{version}.tar.gz
# The original version of the copyright text is on the upstream wiki:
# https://man.kldp.org/wiki/ManPageCopyright
Source1: Man_Page_Copyright
# Patch for utf-8 conversion (original patch includes euc-kr and iso-8859-1)
Patch0: %{name}-%{version}.patch
BuildArch: noarch
Summary(ko): 한글 Manpage 프로젝트에 의한 한글 Manpage 
Requires: man-pages-reader
Supplements: (man-pages and langpacks-ko)

%description
Korean translation of the official manpages from LDP and
another useful manpages from various packages. It's done
by the Korean Manpage Project <https://man.kldp.org> which
is maintained by Korean Manpage Project Team.

%description -l ko
한글 Manpage 프로젝트에서 비롯된 한글 Manpages.
이는 한글 Manpage 프로젝트 팀이 관리하는 한글 Manpage
프로젝트 <https://man.kldp.org>에 의한 것입니다.

%prep
%setup -q -c %{name}-%{version}
%patch 0 -p0
find . -name CVS -exec rm -rf {} \;
cp -p %{SOURCE1} COPYING

#conflict with man
rm -f ./man1/man.1 ./man1/whatis.1 ./man5/man.config.5 
#conflict with shadow-utils in Fedora 9
rm -f ./man8/vipw.8
#conflict with rpms in Fedora 9
rm -f ./man8/rpm.8 ./man8/rpm2cpio.8
# Bug 468501
rm -f ./man1/cpio.1
# Non-free man-pages (bz1334290)
rm man2/sysinfo.2
rm man2/getitimer.2

%build 
for i in man?; do
    for j in $i/*; do
        case "$j" in
            man7/iso_8859-1.7 | man7/iso_8859-7.7)
                ;;
            *)
                iconv -f EUC-KR -t UTF-8 $j -o $j.out
		touch -r $j $j.out
                mv $j.out $j
                ;;
        esac
    done
done


%install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/ko
cp -a man? $RPM_BUILD_ROOT%{_mandir}/ko/

%files
%license COPYING
%{_mandir}/ko/man*/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 20050219-39
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:20050219-38
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 2:20050219-30
- remove non-free man-pages

* Sat Feb 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 2:20050219-29
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:20050219-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Daiki Ueno <dueno@redhat.com> - 2:20050219-23
- Preserve timestamp of converted files

* Thu Nov 15 2012 Daiki Ueno <dueno@redhat.com> - 2:20050219-22
- Drop buildroot preparation from %%intall and %%clean
- Drop BuildRoot
- Drop %%defattr from %%doc
- Add comment to explain what the patch0 is for

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 04 2010 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-18
- Bug 582963 - man-pages-ko: Change requires tag from man to man-pages-reader

* Wed Mar 03 2010 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-17
- Resolves: #555195 (for package wrangler).

* Wed Mar 03 2010 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-15
- Resolves: #555195
- Fixed Fedora 569430 (Wrong directory ownership)

* Tue Jan 14 2010 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-14
- Resolves: #555195
- Build for package wrangler.

* Thu Jan 14 2010 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-11
- Build for package wrangler.

* Wed Dec 16 2009 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-10
- Add full URL to source.
- Fixed the Source1 path.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2:20050219-9.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:20050219-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-7
- Fix Bug 468501 - There were file conflicts when cheeking the packages 
  to be installed in Fedora-10-beta-x86_6.

* Mon Sep 15 2008 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-5
- Fix Bug 462197 -  File conflict between man-pages-ko and rpm

* Mon Aug 04 2008 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-4
- Fix the file conflict with rpm-4.5.90

* Tue Feb 05 2008 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-3
- Correct Licence information.
- Add Korean summary and description

* Tue Jan 08 2008 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-2
- Bug 427684: man-pages fileconflict
- Fix the conflict with vipw.8 (in shadow-utils)


* Thu Dec 06 2007 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-1
- Fix the conflict with man-1.6e-3.fc7

* Thu Dec 06 2007 Ding-Yi Chen <dchen at redhat dot com> - 2:20050219-0
- man7/iso_8859-1.7 and man7/iso_8859-7.7 are back.
- Upstream change version scheme.

* Mon Feb 05 2007 Parag Nemade <pnemade@redhat.com> - 1:1.48-15.2
- Rebuild of package as pert of Core/Extras Merge

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.48-15.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 23 2004 Miloslav Trmac <mitr@redhat.com> - 1:1.48-15
- Recode also man.1x to UTF-8

* Mon Jun 21 2004 Alan Cox <alan@redhat.com>
- man isn't required (there are multiple man page readers), as per other
  man packages

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Akira TAGOH <tagoh@redhat.com> 1.48-11
- removed man.1 and man.config.5, because the latest man contains those manpages.

* Tue Oct 28 2003 Leon Ho <llch@redhat.com>
- convert to utf-8 on build time
- modify logic in install

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not include a Vendor: tag

* Thu Feb 20 2003 David Joo <djoo@redhat.com>
- bug #83614 fixed

* Mon Jan 27 2003 Jeremy Katz <katzj@redhat.com> 1:1.48-7
- add an epoch to fix upgrades from 8.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 10 2003 David Joo <djoo@redhat.com>
- Spelling mistakes fixed in specfile
- bug #81420 fixed

* Fri Dec 20 2002 David Joo <djoo@redhat.com>
- Updated to New version
- sgid bug fixed <#79965>

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild in current collection instance

* Mon Aug 12 2002 Bill Nottingham <notting@redhat.com>
- fix group

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb  1 2002 Bill Nottingham <notting@redhat.com>
- remove %%post/%%preun; they cause errors
- s/%%{prefix}/%%{_mandir}/g

* Thu Jan 31 2002 David Joo <davidjoo@redhat.com>
- Rebuilt against RHL 8.0

* Sun Jun 3 2001 Bae, Sunghoon <plodder@kldp.org>
- removed ftpcount, ftpwho, ftpshut, proftpd man pages
  because proftpd has it 
- changed man cache directory to /var/cache/man

* Tue May 23 2000 KIM KyungHeon <tody@teoal.sarang.net>
- changed name of spec file
- added some contents of spec (for relocatable)
- modified korean description
- fixed using 'makewhatis' command
- fixed expression in %%files tag

* Sun Apr  23 2000 Bae, Sunghoon <plodder@kldp.org>
- modify .spec

* Sat Apr  22 2000 Chongkyoon, Rim <hermes44@secsm.org>
- modify .spec

* Tue Apr  4 2000 Bae, Sunghoon <plodder@kldp.org>
- First Release

