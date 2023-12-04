Summary:        The Sysstat package contains utilities to monitor system performance and usage activity
Name:           sysstat
Version:        12.7.4
Release:        1%{?dist}
License:        GPL-2.0-only
URL:            http://sebastien.godard.pagesperso-orange.fr/
Group:          Development/Debuggers
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cronie-anacron

Requires:       cronie-anacron

%description
 The Sysstat package contains utilities to monitor system performance and usage activity. Sysstat contains the sar utility, common to many commercial Unixes, and tools you can schedule via cron to collect and historize performance and activity data.

%prep
%autosetup -p1

%build
%configure \
            --enable-install-cron \
            --enable-copy-only \
            --disable-file-attr \
            sa_lib_dir=%{_libdir}/sa \
            --disable-stripping
make %{?_smp_mflags}

%install
make install
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/sysstat.service %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-summary.timer %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-summary.service %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-collect.timer %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/cron/sysstat-collect.service %{buildroot}/usr/lib/systemd/system/

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/*
%config(noreplace) %{_sysconfdir}/cron.d/*
%exclude %{_sysconfdir}/rc.d/init.d/sysstat
%{_bindir}/*
%{_libdir}/sa/*
%{_datadir}/doc/%{name}-%{version}/*
%{_mandir}/man*/*
%{_libdir}/systemd/system/*


%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 12.7.4-1
- Auto-upgrade to 12.7.4 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 12.7.1-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri May 26 2023 Rachel Menge <rachelmenge@microsoft.com> - 12.7.1-2
- Patch to fix CVE-2023-33204

* Fri Nov 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.7.1-1
- Upgrading to version 12.7.1 to fix CVE-2022-39377.

* Mon Jan 03 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 12.5.4-1
- Updating to version 12.5.4.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.3.3-4
- Removing the explicit %%clean stage.

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.3.3-3
- Updating dependencies from "cronie" to "cronie-anacron" after splitting of "cronie".

* Mon Nov 16 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.3.3-2
- Removing %%check section as the package doesn't have a test suite.

* Mon Jun 08 2020 Ruying Chen <v-ruyche@microsoft.com> - 12.3.3-1
- Update to 12.3.3

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 12.1.2-4
- Added %%license line automatically

* Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.1.2-3
- Fixed "Source0" tag and moved to GitHub sources.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 12.1.2-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 03 2019 Keerthana K <keerthanak@vmware.com> - 12.1.2-1
- Update to 12.1.2 to fix CVEs.

* Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> - 12.0.1-1
- Updated to 12.0.1 release

* Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 11.4.3-2
- Ensure debuginfo

* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 11.4.3-1
- Update to version 11.4.3

* Thu Jan 05 2017 Xiaolin Li <xiaolinl@vmware.com> - 11.4.2-1
- Updated to version 11.4.2 and enable install cron.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 11.2.0-3
- GA - Bump release of all rpms

* Wed May 4 2016 Divya Thaluru <dthaluru@vmware.com> - 11.2.0-2
- Adding systemd service file

* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 11.2.0-1
- Update to 11.2.0-1.

* Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 11.1.8-1
- Initial build.  First version
