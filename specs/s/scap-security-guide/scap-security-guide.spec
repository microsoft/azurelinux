# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SSG build system and tests count with build directory name `build`.
# For more details see:
# https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
%global _vpath_builddir build

Name:		scap-security-guide
Version:	0.1.79
Release: 2%{?dist}
Summary:	Security guidance and baselines in SCAP formats
License:	BSD-3-Clause
URL:		https://github.com/ComplianceAsCode/content/
Source0:	https://github.com/ComplianceAsCode/content/releases/download/v%{version}/scap-security-guide-%{version}.tar.bz2
BuildArch:	noarch

BuildRequires:	libxslt
BuildRequires:	openscap-scanner >= 1.2.5
BuildRequires:	cmake >= 2.8
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-jinja2
BuildRequires:	python%{python3_pkgversion}-PyYAML
BuildRequires:	python%{python3_pkgversion}-setuptools
Requires:	xml-common, openscap-scanner >= 1.2.5

%description
The scap-security-guide project provides a guide for configuration of the
system from the final system's security point of view. The guidance is specified
in the Security Content Automation Protocol (SCAP) format and constitutes
a catalog of practical hardening advice, linked to government requirements
where applicable. The project bridges the gap between generalized policy
requirements and specific implementation guidelines. The system
administrator can use the oscap CLI tool from openscap-scanner package, or the
scap-workbench GUI tool from scap-workbench package to verify that the system
conforms to provided guideline. Refer to scap-security-guide(8) manual page for
further information.

%package	doc
Summary:	HTML formatted security guides generated from XCCDF benchmarks
Requires:	%{name} = %{version}-%{release}

%description	doc
The %{name}-doc package contains HTML formatted documents containing
hardening guidances that have been generated from XCCDF benchmarks
present in %{name} package.

%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
%package	rule-playbooks
Summary:	Ansible playbooks per each rule.
Group:		System Environment/Base
Requires:	%{name} = %{version}-%{release}

%description	rule-playbooks
The %{name}-rule-playbooks package contains individual ansible playbooks per rule.
%endif

%prep
%autosetup -p1

%define cmake_defines_common -DSSG_SEPARATE_SCAP_FILES_ENABLED=OFF -DSSG_BASH_SCRIPTS_ENABLED=OFF -DSSG_BUILD_SCAP_12_DS=OFF
%define cmake_defines_specific %{nil}
%if 0%{?rhel} && ! %{defined eln}
%define cmake_defines_specific -DSSG_PRODUCT_DEFAULT:BOOLEAN=FALSE -DSSG_PRODUCT_RHEL%{rhel}:BOOLEAN=TRUE -DSSG_SCIENTIFIC_LINUX_DERIVATIVES_ENABLED:BOOL=OFF -DSSG_CENTOS_DERIVATIVES_ENABLED:BOOL=OFF -DSSG_ANSIBLE_PLAYBOOKS_PER_RULE_ENABLED:BOOL=ON
%endif
%if 0%{?centos}
%define cmake_defines_specific -DSSG_PRODUCT_DEFAULT:BOOLEAN=FALSE -DSSG_PRODUCT_RHEL%{centos}:BOOLEAN=TRUE -DSSG_SCIENTIFIC_LINUX_DERIVATIVES_ENABLED:BOOL=OFF -DSSG_CENTOS_DERIVATIVES_ENABLED:BOOL=ON
%endif

mkdir -p build
%build
%cmake %{cmake_defines_common} %{cmake_defines_specific}
%cmake_build

%install
%cmake_install
rm %{buildroot}/%{_docdir}/%{name}/README.md
rm %{buildroot}/%{_docdir}/%{name}/Contributors.md

%files
%{_datadir}/xml/scap/ssg/content
%{_datadir}/%{name}/kickstart
%{_datadir}/%{name}/ansible/*.yml
%{_datadir}/%{name}/tailoring
%lang(en) %{_mandir}/man8/scap-security-guide.8.*
%doc %{_docdir}/%{name}/LICENSE
%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
%exclude %{_datadir}/%{name}/ansible/rule_playbooks
%endif

%files doc
%doc %{_docdir}/%{name}/guides/*.html
%doc %{_docdir}/%{name}/tables/*.html

%if ( %{defined rhel} && (! %{defined centos}) && (! %{defined eln}) )
%files rule-playbooks
%defattr(-,root,root,-)
%{_datadir}/%{name}/ansible/rule_playbooks
%endif

%changelog
* Fri Nov 28 2025 Jan Černý <jcerny@redhat.com> - 0.1.79-1
- Upgrade to the latest upstream release

* Mon Sep 08 2025 Matthew Burket <mburket@redhat.com> - 0.1.78-1
- Update to latest upstream release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.78

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Matthew Burket <mburket@redhat.com> - 0.1.77-1
- Update to latest upstream release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.77

* Fri Mar 07 2025 Matthew Burket <mburket@redhat.com> - 0.1.76-2
- Remove expat as a BuildRequires as it is no longer needed

* Tue Feb 25 2025 Evgenii Kolesnikov <ekolesni@redhat.com> - 0.1.76-1
- Update to latest upstream release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.76

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Matthew Burket <mburket@redhat.com> - 0.1.75-1
- Update to latest upstream release
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.75

* Mon Aug 12 2024 Matthew Burket <mburket@redhat.com> - 0.1.74-1
- Update to latest upstream release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.74
- Remove /usr/bin/python3 from BuildRequires

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Jan Černý <jcerny@redhat.com> - 0.1.73-1
- Update to latest upstream release
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.73

* Fri Feb 09 2024 Vojtech Polasek <vpolasek@redhat.com> - 0.1.72-1
- Update to latest upstream SCAP-Security-Guide-0.1.72 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.72

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Vojtech Polasek <vpolasek@redhat.com> - 0.1.71-1
- Update to latest upstream SCAP-Security-Guide-0.1.71 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.71

* Thu Oct 12 2023 Matthew Burket <mburket@redhat.com> - 0.1.70-1
- Update to latest upstream SCAP-Security-Guide-0.1.70 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.70

* Thu Aug 03 2023 Jan Černý <jcerny@redhat.com> - 0.1.69-1
- Update to latest upstream SCAP-Security-Guide-0.1.69 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.69

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Jan Černý <jcerny@redhat.com> - 0.1.68-1
- Update to latest upstream SCAP-Security-Guide-0.1.68 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.68

* Wed Apr 12 2023 Matthew Burket <mburket@redhat.com> - 0.1.67-1
- Update to latest upstream SCAP-Security-Guide-0.1.67 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.67


* Fri Feb 03 2023 Vojtech Polasek <vpolasek@redhat.com> - 0.1.66-1
- Update to latest upstream SCAP-Security-Guide-0.1.66 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.66

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 06 2022 Marcus Burghardt <maburgha@redhat.com> - 0.1.65-1
- Update to latest upstream SCAP-Security-Guide-0.1.65 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.65

* Tue Oct 04 2022 Watson Sato <wsato@redhat.com> - 0.1.64-1
- Update to latest upstream SCAP-Security-Guide-0.1.64 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.64

* Mon Aug 01 2022 Watson Sato <wsato@redhat.com> - 0.1.63-1
- Update to latest upstream SCAP-Security-Guide-0.1.63 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.63

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Vojtech Polasek <vpolasek@redhat.com> - 0.1.62-2
- rebuild, the release did not get propagated into rawhide

* Mon May 30 2022 Vojtech Polasek <vpolasek@redhat.com> - 0.1.62-1
- Update to latest upstream SCAP-Security-Guide-0.1.62 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.62

* Wed May 04 2022 Watson Sato <wsato@redhat.com> - 0.1.61-1
- Update to latest upstream SCAP-Security-Guide-0.1.61 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.61

* Fri Jan 28 2022 Watson Sato <wsato@redhat.com> - 0.1.60-1
- Update to latest upstream SCAP-Security-Guide-0.1.60 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.60

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 01 2021 Watson Sato <wsato@redhat.com> - 0.1.59-1
- Update to latest upstream SCAP-Security-Guide-0.1.59 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.59
- Fix loading of jinja files

* Thu Sep 30 2021 Watson Sato <wsato@redhat.com> - 0.1.58-1
- Update to latest upstream SCAP-Security-Guide-0.1.58 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.58
- Fix license warning.

* Thu Jul 29 2021 Matej Tyc <matyc@redhat.com> - 0.1.57-1
- Update to latest upstream SCAP-Security-Guide-0.1.57 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.57

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Matej Tyc <matyc@redhat.com> - 0.1.56-2
- Updated the packaging according to the RHEL development trends.
- Don't ship 1.2 datastreams and Bash remediations.
- Clean up dependencies and other package metadata.
- Change the RHEL target.

* Wed May 26 2021 Vojtech Polasek <vpolasek@redhat.com> - 0.1.56-1
- Update to latest upstream SCAP-Security-Guide-0.1.56 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.56

* Fri Mar 19 2021 Vojtech Polasek <vpolasek@redhat.com> - 0.1.55-2
- rebuilt

* Fri Mar 19 2021 Vojtech Polasek <vpolasek@redhat.com> - 0.1.55-1
- Update to latest upstream SCAP-Security-Guide-0.1.55 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.55

* Fri Feb 12 2021 Matej Tyc <matyc@redhat.com> - 0.1.54-3
- Moved the spec file closer to the RHEL one.

* Fri Feb 12 2021 Vojtech Polasek <vpolasek@redhat.com> - 0.1.54-2
- fix definition of build directory

* Fri Feb 05 2021 Vojtech Polasek <vpolasek@redhat.com> - 0.1.54-1
- Update to latest upstream SCAP-Security-Guide-0.1.54 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.54

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Vojtech Polasek <vpolasek@redhat.com> - 0.1.53-1
- Update to latest upstream SCAP-Security-Guide-0.1.53 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.53

* Wed Sep 23 2020 Vojtech Polasek <vpolasek@redhat.com> - 0.1.52-3
- revert previous rework, it did not solve the problem

* Wed Sep 23 2020 Vojtech Polasek <vpolasek@redhat.com> - 0.1.52-2
- rewrite solution for CMake out of source builds

* Mon Sep 21 2020 Vojtech Polasek <vpolasek@redhat.com> - 0.1.52-1
- Update to latest upstream SCAP-Security-Guide-0.1.52 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.52

* Tue Aug 04 2020 Jan Černý <jcerny@redhat.com> - 0.1.51-4
- Update for new CMake out of source builds
  https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
- Fix FTBS in Rawhide/F33 (RHBZ#1863741)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.51-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Vojtech Polasek <vpolasek@redhat.com> - 0.1.51-1
- Update to latest upstream SCAP-Security-Guide-0.1.51 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.51

* Mon Mar 23 2020 Watson Sato <wsato@redhat.com> - 0.1.49-1
- Update to latest upstream SCAP-Security-Guide-0.1.49 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.49

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Watson Sato <wsato@redhat.com> - 0.1.48-1
- Update to latest upstream SCAP-Security-Guide-0.1.48 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.48

* Mon Dec 09 2019 Matěj Týč <matyc@redhat.com> - 0.1.47-2
- Hotfix of the XML parsing fix.

* Mon Dec 09 2019 Matěj Týč <matyc@redhat.com> - 0.1.47-1
- Update to latest upstream SCAP-Security-Guide-0.1.47 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.47
- Fixed XML parsing of remediation functions.

* Mon Jul 29 2019 Watson Sato <wsato@redhat.com> - 0.1.45-1
- Update to latest upstream SCAP-Security-Guide-0.1.45 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.45

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Watson Yuuma Sato <wsato@redhat.com> - 0.1.44-1
- Update to latest upstream SCAP-Security-Guide-0.1.44 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.44

* Fri Feb 22 2019 Watson Yuuma Sato <wsato@redhat.com> - 0.1.43-1
- Update to latest upstream SCAP-Security-Guide-0.1.43 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.43
- Update URL and source URL

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.42-1
- Update to latest upstream SCAP-Security-Guide-0.1.42 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.42
- Fix man page build dependency on derivative content

* Mon Oct 01 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.41-1
- Update to latest upstream SCAP-Security-Guide-0.1.41 release:
  https://github.com/ComplianceAsCode/content/releases/tag/v0.1.41
- Fix Licence of this package

* Wed Jul 25 2018 Matěj Týč <matyc@redhat.com> - 0.1.40-1
- Update to latest upstream SCAP-Security-Guide-0.1.40 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.40
- Update to use Python3 for build.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 04 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.39-2
- Add python version to python2-jinja2 package

* Fri May 04 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.39-1
- Update to latest upstream SCAP-Security-Guide-0.1.39 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.39

* Mon Mar 05 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.38-2
- Add python version to python package prefixes

* Mon Mar 05 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.38-1
- Update to latest upstream SCAP-Security-Guide-0.1.38 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.38

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 Watson Yuuma Sato <wsato@redhat.com> - 0.1.37-1
- Update to latest upstream SCAP-Security-Guide-0.1.37 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.37

* Wed Nov 01 2017 Watson Yuuma Sato <wsato@redhat.com> - 0.1.36-1
- Update to latest upstream SCAP-Security-Guide-0.1.36 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.36

* Tue Aug 29 2017 Watson Sato <wsato@redhat.com> - 0.1.35-1
- Update to latest upstream SCAP-Security-Guide-0.1.35 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.35

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Watson Sato <wsato@redhat.com> - 0.1.34-1
- updated to latest upstream release

* Mon May 01 2017 Martin Preisler <mpreisle@redhat.com> - 0.1.33-1
- updated to latest upstream release

* Thu Mar 30 2017 Martin Preisler <mpreisle@redhat.com> - 0.1.32-1
- updated to latest upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 28 2016 Martin Preisler <mpreisle@redhat.com> - 0.1.31-2
- use make_build and make_install RPM macros

* Mon Nov 28 2016 Martin Preisler <mpreisle@redhat.com> - 0.1.31-1
- update to the latest upstream release
- new default location for content /usr/share/scap/ssg
- install HTML tables in the doc subpackage

* Mon Jun 27 2016 Jan iankko Lieskovsky <jlieskov@redhat.com> - 0.1.30-2
- Correct currently failing parallel SCAP Security Guide build

* Mon Jun 27 2016 Jan iankko Lieskovsky <jlieskov@redhat.com> - 0.1.30-1
- Update to latest upstream SCAP-Security-Guide-0.1.30 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.30
- Drop shell library for remediation functions since it is not required
  starting from 0.1.30 release any more

* Thu May 05 2016 Jan iankko Lieskovsky <jlieskov@redhat.com> - 0.1.29-1
- Update to latest upstream SCAP-Security-Guide-0.1.29 release:
  https://github.com/OpenSCAP/scap-security-guide/releases/tag/v0.1.29
- Do not ship Firefox/DISCLAIMER documentation file since it has been removed
  in 0.1.29 upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Šimon Lukašík <slukasik@redhat.com> - 0.1.28-1
- upgrade to the latest upstream release

* Fri Dec 11 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.27-1
- update to the latest upstream release

* Tue Oct 20 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.26-1
- update to the latest upstream release

* Sat Sep 05 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.25-1
- update to the latest upstream release

* Thu Jul 09 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.24-1
- update to the latest upstream release
- created doc sub-package to ship all the guides
- start distributing centos and scientific linux content
- rename java content to jre

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.22-1
- update to the latest upstream release
- only DataStream file is now available for Fedora
- start distributing security baseline for Firefox
- start distributing security baseline for Java RunTime deployments

* Wed Mar 04 2015 Šimon Lukašík <slukasik@redhat.com> - 0.1.21-1
- update to the latest upstream release
- move content to /usr/share/scap/ssg/content

* Thu Oct 02 2014 Šimon Lukašík <slukasik@redhat.com> - 0.1.19-1
- update to the latest upstream release

* Mon Jul 14 2014 Šimon Lukašík <slukasik@redhat.com> - 0.1.5-4
- require only openscap-scanner, not whole openscap-utils package

* Tue Jul 01 2014 Šimon Lukašík <slukasik@redhat.com> - 0.1.5-3
- Rebase the RHEL part of SSG to the latest upstream version (0.1.18)
- Add STIG DISCLAIMER to the shipped documentation

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 27 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.5-1
- Fix fedora-srpm and fedora-rpm Make targets to work again
- Include RHEL-6 and RHEL-7 datastream files to support remote RHEL system scans
- EOL for Fedora 18 support
- Include Fedora datastream file for remote Fedora system scans

* Mon Jan 06 2014 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.4-2
- Drop -compat package, provide openscap-content directly (RH BZ#1040335#c14)

* Fri Dec 20 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.4-1
- Fix remediation for sshd set keepalive (ClientAliveCountMax) and move
  it to /shared
- Add shared remediations for sshd disable empty passwords and
  sshd set idle timeout
- Shared remediation for sshd disable root login
- Add empty -compat subpackage to ensure backward-compatibility with
  openscap-content and firstaidkit-plugin-openscap packages (RH BZ#1040335)
- OVAL check for sshd disable root login
- Fix typo in OVAL check for sshd disable empty passwords
- OVAL check for sshd disable empty passwords
- Unselect no shelllogin for systemaccounts rule from being run by default
- Rename XCCDF rules
- Revert Set up Fedora release name and CPE based on build system properties
- Shared OVAL check for Verify that Shared Library Files Have Root Ownership
- Shared OVAL check for Verify that System Executables Have Restrictive Permissions
- Shared OVAL check for Verify that System Executables Have Root Ownership
- Shared OVAL check for Verify that Shared Library Files Have Restrictive
  Permissions
- Fix remediation for Disable Prelinking rule
- OVAL check and remediation for sshd's ClientAliveCountMax rule
- OVAL check for sshd's ClientAliveInterval rule
- Include descriptions for permissions section, and rules for checking
  permissions and ownership of shared library files and system executables
- Disable selected rules by default
- Add remediation for Disable Prelinking rule
- Adjust service-enable-macro, service-disable-macro XSLT transforms
  definition to evaluate to proper systemd syntax
- Fix service_ntpd_enabled OVAL check make validate to pass again
- Include patch from Šimon Lukašík to obsolete openscap-content
  package (RH BZ#1028706)
- Add OVAL check to test if there's is remote NTP server configured for
  time data
- Add system settings section for the guide (to track system wide
  hardening configurations)
- Include disable prelink rule and OVAL check for it
- Initial OVAL check if ntpd service is enabled. Add package_installed
  OVAL templating directory structure and functionality.
- Include services section, and XCCDF description for selected ntpd's
  sshd's service rules
- Include remediations for login.defs' based password minimum, maximum and
  warning age rules
- Include directory structure to support remediations
- Add SCAP "replace or append pattern value in text file based on variable"
  remediation script generator
- Add remediation for "Set Password Minimum Length in login.defs" rule

* Mon Nov 18 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1.3-1
- Update versioning scheme - move fedorassgrelease to be part of
  upstream version. Rename it to fedorassgversion to avoid name collision
  with Fedora package release.

* Tue Oct 22 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-3
- Add .gitignore for Fedora output directory
- Set up Fedora release name and CPE based on build system properties
- Use correct file paths in scap-security-guide(8) manual page 
  (RH BZ#1018905, c#10)
- Apply further changes motivated by scap-security-guide Fedora RPM review
  request (RH BZ#1018905, c#8):
  * update package description,
  * make content files to be owned by the scap-security-guide package,
  * remove Fedora release number from generated content files,
  * move HTML form of the guide under the doc directory (together
    with that drop fedora/content subdir and place the content
    directly under fedora/ subdir).
- Fixes for scap-security-guide Fedora RPM review request (RH BZ#1018905):
  * drop Fedora release from package provided files' final path (c#5),
  * drop BuildRoot, selected Requires:, clean section, drop chcon for
    manual page, don't gzip man page (c#4),
  * change package's description (c#4),
  * include PD license text (#c4).

* Mon Oct 14 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-2
- Provide manual page for scap-security-guide
- Remove percent sign from spec's changelog to silence rpmlint warning
- Convert RHEL6 'Restrict Root Logins' section's rules to Fedora
- Convert RHEL6 'Set Password Expiration Parameter' rules to Fedora
- Introduce 'Account and Access Control' section
- Convert RHEL6 'Verify Proper Storage and Existence of Password Hashes' section's
  rules to Fedora
- Set proper name of the build directory in the spec's setup macro.
- Replace hard-coded paths with macros. Preserve attributes when copying files.

* Tue Sep 17 2013 Jan iankko Lieskovsky <jlieskov@redhat.com> 0.1-1
- Initial Fedora SSG RPM.
