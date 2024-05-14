Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package cim-schema
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon.
#
# The license for this spec file is the MIT/X11 license:
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# norootforbuild

%global major 2
%global minor 43
%global update 0

Name:           cim-schema
Url:            https://www.dmtf.org/
Summary:        Common Information Model (CIM) Schema
Version:        %{major}.%{minor}.%{update}
Release:        11%{?dist}
License:        DMTF
Source0:        https://www.dmtf.org/standards/cim/cim_schema_v%{major}%{minor}%{update}/cim_schema_%{version}Experimental-MOFs.zip
Source1:        https://www.dmtf.org/standards/cim/cim_schema_v%{major}%{minor}%{update}/cim_schema_%{version}Experimental-Doc.zip
Source2:        LICENSE
BuildArch:      noarch

%package docs
Summary:        Common Information Model (CIM) Schema documentation


%description
Common Information Model (CIM) is a model for describing overall
management information in a network or enterprise environment. CIM
consists of a specification and a schema. The specification defines the
details for integration with other management models. The schema
provides the actual model descriptions.



Authors:
--------
    DTMF <https://www.dmtf.org/about/contact>

%description docs
Common Information Model (CIM) schema documentation.

%prep
%setup -q -T -a 1 -c -n %{name}-docs
%setup -q -T -a 0 -c -n %{name}-%{version}

%build
%install
MOFDIR=%{_datadir}/mof
CIMDIR=$MOFDIR/cimv%{version}
%__rm -rf $RPM_BUILD_ROOT
for i in `find . -name "*.mof"`; do
  sed -i -e 's/\r//g' $i
done
install -d $RPM_BUILD_ROOT/$CIMDIR
chmod -R go-wx .
chmod -R a+rX .
%__mv * $RPM_BUILD_ROOT/$CIMDIR/
ln -s cimv%{version} $RPM_BUILD_ROOT/$MOFDIR/cim-current
ln -s cim_schema_%{version}.mof $RPM_BUILD_ROOT/$MOFDIR/cim-current/CIM_Schema.mof
install -d $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/%{_docdir}/%{name}

%files
%dir %{_datarootdir}/mof
%dir %{_datarootdir}/mof/cimv%{version}
%{_datarootdir}/mof/cimv%{version}/*
%{_datarootdir}/mof/cim-current
%doc %{_docdir}/%{name}/LICENSE

%files docs
%doc ../%{name}-docs/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.43.0-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.43.0-1
- Update to CIM Schema 2.43.0, including experimental classes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.38.0-2
- Fix typo in CIM_StoragePool.mof
  Resolves: #1015983

* Tue Sep 03 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.38.0-1
- Update to CIM Schema 2.38.0, including experimental classes

* Thu Aug 29 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.37.0-1
- Update to CIM Schema 2.37.0, including experimental classes
- Fix for unversioned docdir change
  Resolves: #993697 

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.33.0-5
- Fix package to be able do local build

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.33.0-3
- Remove loadmof.sh and rmmof.sh scripts

* Thu Aug 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.33.0-2
- Fix issues found by fedora-review utility in the spec file

* Mon Jul 30 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.33.0-1
- Update to CIM Schema 2.33.0, including experimental classes

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 11 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.29.0-1
- Update to CIM Schema 2.29.0

* Tue Jun 22 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.25.0-2
- Minor spec file fixes

* Tue Jun 22 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.25.0-1
- Uploaded the second source file, so bumping up the release.

* Tue Jun 22 2010 Praveen K Paladugu <praveen_paladugu@dell.com> - 2.25.0-0
- Updating the sources to 2.25.0. Had to update sblim-sfcb to 1.3.8 
- which uses 2.25.0. 

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Matt Domsch <Matt_Domsch@dell.com> - 2.22.0-1.fc12
- add dist tag

* Tue Jul 14 2009 Matt Domsch <Matt_Domsch@dell.com> - 2.22.0-1
- spec license change to MIT per Novell
- remove BR: unzip, it's in the default buildroot already
- add MIT license to spec file

* Wed May 20 2009 Matt Domsch <Matt_Domsch@dell.com> - 2.21.0-1
- upgrade to v2.22.0

* Thu Oct 23 2008 Matt Domsch <Matt_Domsch@dell.com> - 2.19.1-1
- Upgraded to cimv2.19.1Experimental
- now meets Fedora packaging guidelines too
- added -docs subpackage
* Wed May 14 2008 bwhiteley@suse.de
- Upgraded to cimv2.18Experimental
* Thu Jan 17 2008 bwhiteley@suse.de
- Fixed order of includes so that it will import in pegasus.
* Tue Jan 08 2008 bwhiteley@suse.de
- Updated to cimv2.17Experimental (#341800)
* Wed Nov 28 2007 bwhiteley@suse.de
- Updated to cimv2.16Experimental (#341800)
  Remove carriage returns from MOF files.
  Fix broken comment blocks in 2.16 schema.
* Thu Mar 29 2007 bwhiteley@suse.de
- Added unzip to BuildRequires
* Tue Mar 27 2007 bwhiteley@suse.de
- Fixed inclusion of missing file (#258187)
* Tue Mar 13 2007 bart@novell.com
- Added some classes from 2.15 preliminary needed for Xen
  providers (#228365)
* Fri Jan 19 2007 bwhiteley@suse.de
- update to schema version 2.14 (#228365)
* Mon Jan 08 2007 bwhiteley@suse.de
- Combine all qualifiers back into one file (#232667)
* Tue Dec 19 2006 bwhiteley@suse.de
- added loadmof.sh script. (#228349)
* Wed Dec 13 2006 bwhiteley@suse.de
- Updated to schema version cimv2.13.1 (#228365)
* Fri Oct 06 2006 bwhiteley@suse.de
- Updated to schema version cimv2.13
* Mon May 08 2006 bwhiteley@suse.de
- Updated to schema version cimv2.12, required for SMASH 1.0
  compliance (#173777)
* Fri May 05 2006 bwhiteley@suse.de
- removed non-ascii char from CIM_DNSSettingData.mof (was breaking
  some XML parsers) (#172939)
* Fri Feb 10 2006 bwhiteley@suse.de
- fixed execute bit on directories (#149992)
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 17 2006 bwhiteley@suse.de
- Added a symlink cim-current so other packages don't have to hard-
  code cim schema versions.
* Tue Jan 10 2006 bwhiteley@suse.de
- Update to v2.11 Experimental.
- Moved MOFs under /usr/share/mof
* Thu Jan 13 2005 nashif@suse.de
- Update to v2.9 Final
* Tue Oct 12 2004 nashif@suse.de
- Update with cim v2.9
* Tue Feb 17 2004 nashif@suse.de
- Fixed directory permissions
- build as normal user
* Mon Feb 16 2004 nashif@suse.de
- Updated to 2.8 final
* Thu Nov 27 2003 nashif@suse.de
- Initial Release
