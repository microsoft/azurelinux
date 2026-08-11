# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           dash
Version:        0.5.12
Release: 7%{?dist}
Summary:        Small and fast POSIX-compliant shell
# BSD-3-Clause: DASH in general
# GPL-2.0-or-later: From src/mksignames.c
# LicenseRef-Fedora-Public-Domain: From src/bltin/test.c
License:        BSD-3-Clause AND GPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain
URL:            http://gondor.apana.org.au/~herbert/%{name}/
Source0:        http://gondor.apana.org.au/~herbert/%{name}/files/%{name}-%{version}.tar.gz
Provides:   /bin/dash
BuildRequires: gcc
BuildRequires: make

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible. It does this without sacrificing speed where possible. In fact, it is
significantly faster than bash (the GNU Bourne-Again SHell) for most tasks.

%prep
%autosetup -p1

%build
%configure --bindir=%{_bindir}
%make_build

%install
%make_install

%post
grep -q '^/bin/dash$' %{_sysconfdir}/shells || \
    echo '/bin/dash' >> %{_sysconfdir}/shells

%postun
if [ $1 -eq 0 ]; then
    sed -i '/^\/bin\/dash$/d' %{_sysconfdir}/shells
fi

%files
%doc COPYING ChangeLog
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Filipe Rosset <rosset.filipe@gmail.com> - 0.5.12-1
- Update to 0.5.12 fixes rhbz#1842557

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.11.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 01 2023 David Cantrell <dcantrell@redhat.com> - 0.5.11.5-4
- Update License tag to use SPDX license expression

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 23 2022 Tom Callaway <spot@fedoraproject.org> - 0.5.11.5-1
- update to 0.5.11.5

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.5.10.2-6
- Add Provides

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.5.10.2-3
- Move dash binary to /usr/bin/

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 19 2018 Filipe Rosset <rosset.filipe@gmail.com> - 0.5.10.2-1
- upgrade to latest upstream 0.5.10.2 fixes RHBZ #1379016 and #1381509

* Wed Sep 19 2018 Filipe Rosset <rosset.filipe@gmail.com> - 0.5.9-8
- spec cleanup and modernization

* Fri Jul 20 2018 Stephen Gallagher <sgallagh@redhat.com> - 0.5.9-7
- Add BuildRequires: gcc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 15 2016 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.5.9-1
- Rebase to upstream 0.5.9

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.5.8-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Sep 29 2014 Petr Šabata <contyk@redhat.com> - 0.5.8-1
- Update to 0.5.8

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Petr Šabata <contyk@redhat.com> - 0.5.7-10
- Fix FTBFS due to -Werror=format-security (#1037030)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 Petr Šabata <contyk@redhat.com> - 0.5.7-8
- Simplify the installation

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 0.5.7-7
- Correct the License tag once again
- Utilize the %%{name} and %%{_mandir} macros a bit more
- Don't package the INSTALL file

* Mon Jun 10 2013 Petr Šabata <contyk@redhat.com> - 0.5.7-6
- Use the sysconfdir macro in scriptlets

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Petr Šabata <contyk@redhat.com> - 0.5.7-2
- Don't use --fixed-strings in scriptlets grep match (#753887)

* Wed Aug 17 2011 Petr Sabata <contyk@redhat.com> - 0.5.7-1
- 0.5.7 bump

* Mon May 23 2011 Petr Sabata <psabata@redhat.com> - 0.5.6-5
- Try to add dash to /etc/shells every time, not just on new installs (#706138)
- Also, make the grep regexps a bit more strict, just to be sure

* Thu May 19 2011 Petr Sabata <psabata@redhat.com> - 0.5.6-4
- Install/remove dash from /etc/shells (#706138)
- Buildroot and defattr cleanup
- Add INSTALL, COPYING, ChangeLog to doc

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 21 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.5.6-2
- New upstream realease
- Version bump

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Andreas Thienemann <andreas@bawue.net> - 0.5.5.1-2
- Added patch from upstream git to not close stdout on err. This improves
  initramfs use of dash.

* Mon Apr 13 2009 Warren Togami <wtogami@redhat.com> - 0.5.5.1-1
- 0.5.5.1

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Warren Togami <wtogami@redhat.com> 0.5.4-3
- rebuild for gcc-4.3

* Wed Nov 07 2007 Warren Togami <wtogami@redhat.com> 0.5.4-2
- move to /bin/dash
- BSD license tag

* Fri Nov 02 2007 Warren Togami <wtogami@redhat.com> 0.5.4-1
- initial package


