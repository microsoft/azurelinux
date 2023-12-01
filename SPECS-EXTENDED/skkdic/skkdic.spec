%global         githash     1ca80982c5a32c82bfc5e98e1fe9d8751ab44946
%global         shorthash   %(TMP=%githash ; echo ${TMP:0:10})
%global         gitdate     Wed, 17 Feb 2021 00:09:15 +0900
%global         gitdate_num 20210217

%global         githash_tools     0fe2106fbc052445c611e6c5b2a79899d740edcb

%undefine        _changelog_trimtime

Summary:	Dictionaries for SKK (Simple Kana-Kanji conversion program)
Name:		skkdic
Version:	%{gitdate_num}
Release:	1%{?dist}
# See Source2
License:	GPLv2+ and CC-BY-SA and Unicode and Public Domain and MIT

Source0:	https://github.com/skk-dev/dict/archive/%{githash}/%{name}-%{gitdate_num}.git%{githash}.tar.gz
Source1:	https://raw.githubusercontent.com/skk-dev/skktools/%{githash_tools}/unannotation.awk
Source2:	license-investigation.txt
Source3:	%{name}-LICENSE.txt
Source200:	README-skkdic.rh.ja

URL:		https://skk-dev.github.io/dict/
BuildArch:	noarch

BuildRequires: make

%description
This package includes the SKK dictionaries, including the large dictionary
SKK-JISYO.L and pubdic+ dictionary.

%prep
%setup -q -c -T -a 0
mv %{SOURCE3} ./LICENSE.txt
ln -sf dict-%{githash} src
mkdir tools

cp -p %SOURCE200 .
cp -p %SOURCE1 tools

pushd src
cp -a zipcode/README.md zipcode/README-zipcode.md
popd

%build
pushd src

for dic in \
	SKK-JISYO.L.unannotated \
	SKK-JISYO.wrong
do
	rm -f $dic
	make $dic
done

popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/skk

pushd src
for f in SKK-JISYO* zipcode/SKK-JISYO*
do
	install -p -m 644 $f $RPM_BUILD_ROOT%{_datadir}/skk
done
gzip -9 ChangeLog

popd

%files
%license LICENSE.txt
%doc	src/ChangeLog.gz
%doc	README-skkdic.rh.ja
%doc	src/committers.md
%doc	src/edict_doc.html
%doc	src/zipcode/README-zipcode.md

%{_datadir}/skk/

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 20210217-1
- Upgrade using Fedora 35 version of spec (license: MIT) 

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200128-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sat May  8 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20210217-1.git1ca80982c5
- Source switched to github
- Update to github latest git
- license investigated again and updated, especially for SKK-JISYO.edict

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200128-3.T1339
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200128-2.T1339
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20200128-1.T1339
- Update to the latest data

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181016-3.T1609
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181016-2.T1609
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20181016-1.T1609
- Update to the latest data

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170102-5.T1100
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170102-4.T1100
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170102-3.T1100
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170102-2.T1100
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20170102-1.T0100
- Update to the latest data

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151206-2.T0100
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 06 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20151206-1.T0100
- Update to the latest data

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150508-2.T1030
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May  8 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20150508-1.T1030
- Update to the latest data

* Tue Nov 18 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20141118-1.T0000
- Update to the latest data

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131114-8.T1121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20131114-7.T1121
- Update to the latest data

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130104-6.T1435
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130104-5.T1435
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 20130104-4.T1435
- Update to the latest data

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111016-3.T0540
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111016-2.T0540
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 20111016-1.T0540
- Update for F16

* Wed Mar 09 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 20110309-1.T1520
- Update dictionaries

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090929-2.T0800
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 20090929-1.T0800
- Update for F12Beta

* Wed Aug  5 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 20090805-1.T0306
- Update for F12Alpha
- A bit clean up for spec file

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080904-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080904-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 20080904-1
- fix license tag
- update source files

* Tue Sep 23 2006 Ryo Dairiki <ryo-dairiki@users.sourceforge.net> - 20050614-2
- mass rebuilding

* Tue Jun 14 2005 Jens Petersen <petersen@redhat.com> - 20050614-1
- initial import to Fedora Extras
- update to latest dictionaries

* Wed Sep 22 2004 Jens Petersen <petersen@redhat.com> - 20040922-1
- update to latest dictionaries
- update url
- gzip ChangeLog since it is growing fast

* Thu Apr 15 2004 Jens Petersen <petersen@redhat.com> - 20040415-1
- update to latest
- update README-skkdic.rh.ja and convert it to utf-8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Jens Petersen <petersen@redhat.com> - 20030211-1
- update dictionaries
- move rh readme file into cvs
- don't build unannotated dictionaries

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 20020724-2
- rebuild

* Wed Jul 24 2002 Jens Petersen <petersen@redhat.com> 20020724-1
- update dictionaries

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Jens Petersen <petersen@redhat.com> 20020220-2
- rebuild in new environment

* Tue Feb 20 2002 Jens Petersen <petersen@redhat.com> 20020220-1
- update to latest dictionaries
- put source in one bzip2ed tar file
- tidy spec file
- make unannotated
- include SKK-JISYO.pubdic+

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Jun 23 2001 SATO Satoru <ssato@redhat.com>
- update and add more dictionaries: (jinmei,) law, okinawa, geo
- add README files

* Mon Jan 22 2001 SATO Satoru <ssato@redhat.com>
- update dictionaris
- add cdb-dictionaries
- clean up SPEC

* Mon Dec 28 2000 SATO Satoru <ssato@redhat.com>
- add many extra dictionaries
- clean up SPEC

* Tue Sep  5 2000 SATO Satoru <ssato@redhat.com>
- Initial release
