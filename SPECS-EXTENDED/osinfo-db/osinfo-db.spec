Vendor:         Microsoft Corporation
Distribution:   Mariner
# -*- rpm-spec -*-

Summary: osinfo database files
Name: osinfo-db
Version: 20210202
Release: 2%{?dist}
License: LGPLv2+
Source0: https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.xz
Source1: https://fedorahosted.org/releases/l/i/libosinfo/%{name}-%{version}.tar.xz.asc
URL: http://libosinfo.org/
BuildRequires: intltool
BuildRequires: osinfo-db-tools
BuildArch: noarch
Requires: hwdata

%description
The osinfo database provides information about operating systems and
hypervisor platforms to facilitate the automated configuration and
provisioning of new virtual machines

%install
osinfo-db-import  --root %{buildroot} --dir %{_datadir}/osinfo %{SOURCE0}

%files
%dir %{_datadir}/osinfo/
%{_datadir}/osinfo/VERSION
%{_datadir}/osinfo/LICENSE
%{_datadir}/osinfo/datamap
%{_datadir}/osinfo/device
%{_datadir}/osinfo/os
%{_datadir}/osinfo/platform
%{_datadir}/osinfo/install-script
%{_datadir}/osinfo/schema

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20210202-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Feb 02 2021 Fabiano Fidêncio <fidencio@redhat.com> - 20210202-1
- Update to new release (v20210202)

* Fri Dec 18 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20201218-1
- Update to new release (v20201218)

* Thu Nov 19 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20201119-1
- Update to new release (v20201119)

* Thu Oct 15 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20201015-1
- Update to new release (v20201015)

* Sun Oct 11 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20201011-1
- Update to new release (v20201011)

* Thu Aug 13 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200813-1
- Update to new release (v20200813)

* Tue Aug 04 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200804-1
- Update to new release (V20200804)

* Sat May 30 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200529-1
- Update to new release (v20200529)

* Fri May 15 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200515-1
- Update to new release (v20200515)

* Wed Mar 25 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200325-1
- Update to new release (v20200325)

* Mon Feb 03 2020 Fabiano Fidêncio <fidencio@redhat.com> - 20200203-1
- Update to new release (v20200203)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191125-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20191125-1
- Update to new release (v20191125)

* Fri Nov 08 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20191108-1
- Update to new release (v20191108)

* Fri Sep 20 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20190920-1
- Update to new release (v20190920)

* Thu Sep 05 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20190905-1
- Update to new release
- Resolves: rhbz#1746028 - libosinfo missing rhel7.7 in database

* Mon Aug 05 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20190805-1
- Update to new release

* Fri Jul 26 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20190627-1
- Update to new release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190611-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Fabiano Fidêncio <fidencio@redhat.com> - 20190611-1
- Update to new release

* Sat May 04 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190504-1
- Update to new release

* Tue Mar 19 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190319-1
- Update to new release

* Mon Mar 04 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190304-1
- Update to new release

* Fri Mar 01 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190301-1
- Update to new release

* Mon Feb 18 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190218-1
- Update to new release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190120-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Fabiano Fidêncio <fidencio@redhat.org> - 20190120-1
- Update to new release

* Fri Dec 14 2018 Fabiano Fidêncio <fidencio@redhat.org> - 20181214-1
- Update to new release

* Mon Dec 03 2018 Fabiano Fidêncio <fidencio@redhat.org> - 20181203-1
- Update to new release

* Mon Nov 19 2018 Fabiano Fidêncio <fidencio@redhat.org> - 20181116-1
- Update to new release

* Thu Nov 01 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20181101-1
- Update to new release

* Thu Oct 11 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20181011-1
- Update to new release

* Thu Sep 20 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180920-1
- Update to new release

* Mon Sep 03 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180903-1
- Update to new release

* Fri Jul 20 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180720-1
- Update to new release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180612-1
- Update to new release

* Thu May 31 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180531-1
- Update to new release

* Mon May 14 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180514-1
- Update to new release

* Wed May 02 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180502-1
- Update to new release

* Mon Apr 16 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180416-1
- Update to new release

* Sun Mar 25 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180325-1
- Update to new release

* Sun Mar 18 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180318-1
- Update to new release

* Sun Mar 11 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 20180311-1
- Update to new release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170813-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 13 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170813-1
- Update to new release

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170423-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 23 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170423-1
- Update to new release

* Sun Mar 26 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170326-1
- Update to new release

* Sat Feb 25 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170225-1
- Update to new release

* Sat Feb 11 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170211-1
- Update to new release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170121-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 21 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170121-2
- 20170121-1 used an incorrect tarball

* Sat Jan 21 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170121-1
- Update to new release

* Sat Jan 14 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170114-1
- Update to new release

* Sat Jan 07 2017 Fabiano Fidêncio <fabiano@fidencio.org> - 20170107-1
- Update to new release

* Wed Oct 26 2016 Daniel P. Berrange <berrange@redhat.com> - 20161026-1
- Update to new release

* Fri Jul 29 2016 Daniel P. Berrange <berrange@redhat.com> - 20160728-1
- Initial package after split from libosinfo (rhbz #1361596)
