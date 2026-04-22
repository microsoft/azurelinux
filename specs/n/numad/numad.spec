# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: numad
Version: 0.5
Release: 48.20150602git%{?dist}
Summary: NUMA user daemon

License: LGPL-2.1-only
URL: https://pagure.io/numad
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   git clone https://pagure.io/numad.git numad-0.5git
#   tar --exclude-vcs -cJf numad-0.5git.tar.xz numad-0.5git/
Source0: %{name}-%{version}git.tar.xz

Patch0: 0000-remove-conf.patch
Patch1: 0001-numad_log-fix-buffer-overflow.patch
Patch2: 0002-recognize--m-option-correctly.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd-rpm-macros

%description
Numad, a daemon for NUMA (Non-Uniform Memory Architecture) systems,
that monitors NUMA characteristics and manages placement of processes
and memory to minimize memory latency and thus provide optimum performance.

%prep
%autosetup -n %{name}-%{version}git

%build
%make_build CFLAGS="$CFLAGS"

%install
install -D -p -m 644 {,%{buildroot}%{_unitdir}/}numad.service
install -D -p -m 644 {,%{buildroot}%{_sysconfdir}/logrotate.d/%{name}/}numad.logrotate
%make_install prefix=%{buildroot}/usr

%files
%config(noreplace) %{_sysconfdir}/logrotate.d/numad
%{_bindir}/numad
%{_mandir}/man8/numad.8.*
%{_unitdir}/numad.service

%post
%systemd_post numad.service

%preun
%systemd_preun numad.service

%postun
%systemd_postun numad.service

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-47.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-46.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-45.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-44.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-43.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.5-42.20150602git
- recognize the -m option
- modernize the specfile
    - use recommended systemd macros
    - fix manual pages installation
    - sort file list and BuildRequires
    - use modern make macros
    - simplify %%install section

* Wed Sep 06 2023 Lukas Nykryn <lnykryn@redhat.com> - 0.5-41.20150602git
- fix buffer overflow

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-40.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.5-39.20150602git
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-38.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-37.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-36.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-35.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-34.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 24 2020 Jan Synáček <jsynacek@redhat.com> - 0.5-33.20150602git
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-32.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-31.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-30.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Jan Synáček <jsynacek@redhat.com> - 0.5-29.20150602git
- Remove all mentions of the default config file, which is not used anyway

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-28.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-27.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Jan Synáček <jsynacek@redhat.com> - 0.5-26.20150602git
- Remove initscripts from Requires (#1592372)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-25.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-24.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-23.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Dan Horák <dan[at]danny.cz> - 0.5-22.20150602git
- Enable on s390x

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-21.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-20.20150602git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Jan Synáček <jsynacek@redhat.com> - 0.5-19.20150602git
- Update to 20150602

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-18.20140620git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-17.20140620git
- Update to 20140620

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-16.20140225git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-15.20140225git
- Update to the correct upstream version of 20140225

* Fri Feb 28 2014 Jan Synáček <jsynacek@redhat.com> - 0.5-14.20140225git
- Update to 20140225
- Resolves: #1071221

* Mon Jan 20 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.5-13.20130814git
- Don't order service after syslog.target (#1055209).
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.
- Fix build with -Werror=format-security.

* Wed Aug 14 2013 Jan Synáček <jsynacek@redhat.com> - 0.5-12.20130814git
- Update to 20130814

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-11.20121130git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-10.20121130git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-9.20121130git
- Update and comment the Makefile patch
- Related: #825153

* Mon Dec 03 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-8.20121130git
- Update to 20121130
- Update spec: fix command to generate tarball

* Tue Oct 16 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-7.20121015git
- Update to 20121015
- Add Makefile patch
- Update spec: update command to generate tarball

* Wed Aug 22 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-6.20120522git
- add systemd-rpm macros
- Resolves: #850236

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5.20120522git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Jan Synáček <jsynacek@redhat.com> - 0.5-4.20120522git
- update source (20120522) and manpage

* Tue Mar 06 2012 Jan Synáček <jsynacek@redhat.com> 0.5-3.20120221git
- update source
- drop the patch

* Fri Feb 24 2012 Jan Synáček <jsynacek@redhat.com> 0.5-2.20120221git
- add BuildRequires: systemd-units

* Wed Feb 15 2012 Jan Synáček <jsynacek@redhat.com> 0.5-1.20120221git
- spec update

* Fri Feb 10 2012 Bill Burns <bburns@redhat.com> 0.5-1
- initial version
