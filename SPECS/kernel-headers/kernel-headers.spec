%define mariner_version 3

Summary:        Linux API header files
Name:           kernel-headers
Version:        6.1.58.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
#Source0:       https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-%{mariner_version}/%%{version}.tar.gz
Source0:        kernel-%{version}.tar.gz
# Historical name shipped by other distros
Provides:       glibc-kernheaders = %{version}-%{release}
BuildArch:      noarch

%description
The Linux API Headers expose the kernel's API for use by Glibc.

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{mariner_version}-%{version}

%build
make mrproper

%install
cd %{_builddir}/CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{mariner_version}-%{version}
make headers
find usr/include -name '.*' -delete
rm usr/include/Makefile
mkdir -p /%{buildroot}%{_includedir}
cp -rv usr/include/* /%{buildroot}%{_includedir}

%files
%defattr(-,root,root)
%license COPYING
%{_includedir}/*

%changelog
* Fri Oct 27 2023 Rachel Menge <rachelmenge@microsoft.com> - 6.1.58.1-1
- Upgrade to 6.1.58.1

* Mon Oct 23 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.135.1-2
- Bump release to match kernel

* Tue Oct 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.135.1-1
- Auto-upgrade to 5.15.135.1

* Tue Sep 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.133.1-1
- Auto-upgrade to 5.15.133.1

* Tue Sep 22 2023 Cameron Baird <cameronbaird@microsoft.com> - 5.15.131.1-3
- Bump release to match kernel

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.15.131.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 08 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.131.1-1
- Auto-upgrade to 5.15.131.1

* Mon Aug 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.126.1-1
- Auto-upgrade to 5.15.126.1

* Thu Aug 10 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.125.1-2
- Bump release to match kernel

* Wed Aug 09 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.125.1-1
- Auto-upgrade to 5.15.125.1

* Tue Aug 01 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.123.1-1
- Auto-upgrade to 5.15.123.1

* Fri Jul 28 2023 Juan Camposeco <juanarturoc@microsoft.com> - 5.15.122.1-2
- Bump release to match kernel

* Wed Jul 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.122.1-1
- Auto-upgrade to 5.15.122.1

* Wed Jun 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.118.1-1
- Auto-upgrade to 5.15.118.1

* Tue Jun 20 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.116.1-2
- Bump release to match kernel

* Tue Jun 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.116.1-1
- Auto-upgrade to 5.15.116.1

* Wed May 24 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.112.1-2
- Bump release to match kernel

* Tue May 23 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.112.1-1
- Auto-upgrade to 5.15.112.1

* Mon May 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.111.1-1
- Auto-upgrade to 5.15.111.1

* Mon May 15 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.110.1-5
- Bump release to match kernel

* Tue May 09 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.110.1-4
- Bump release to match kernel

* Thu May 04 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.110.1-3
- Bump release to match kernel

* Wed May 03 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.110.1-2
- Bump release to match kernel

* Mon May 01 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.110.1-1
- Auto-upgrade to 5.15.110.1

* Thu Apr 27 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.107.1-4
- Bump release to match kernel

* Wed Apr 26 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.107.1-3
- Bump release to match kernel

* Wed Apr 19 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.107.1-2
- Bump release to match kernel

* Tue Apr 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.107.1-1
- Auto-upgrade to 5.15.107.1

* Tue Apr 11 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.102.1-5
- Bump release to match kernel

* Tue Apr 11 2023 Kanika Nema <kanikanema@microsoft.com> - 5.15.102.1-4
- Bump release number to match kernel release.

* Wed Mar 29 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.102.1-3
- Bump release to match kernel

* Wed Mar 22 2023 Thien Trung Vuong <tvuong@microsoft.com> - 5.15.102.1-2
- Bump release to match kernel

* Tue Mar 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.102.1-1
- Auto-upgrade to 5.15.102.1

* Mon Mar 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.98.1-1
- Auto-upgrade to 5.15.98.1

* Sat Feb 25 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.95.1-1
- Auto-upgrade to 5.15.95.1

* Wed Feb 22 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.94.1-1
- Auto-upgrade to 5.15.94.1

* Wed Feb 15 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.92.1-3
- Bump release to match kernel

* Thu Feb 09 2023 Minghe Ren <mingheren@microsoft.com> - 5.15.92.1-2
- Disable CONFIG_INIT_ON_FREE_DEFAULT_ON

* Mon Feb 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.92.1-1
- Auto-upgrade to 5.15.92.1

* Wed Jan 25 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.90.1-1
- Auto-upgrade to 5.15.90.1

* Sat Jan 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.87.1-1
- Auto-upgrade to 5.15.87.1

* Sat Jan 07 2023 nick black <niblack@microsoft.com> - 5.15.86.1-2
- Add several missing BuildRequires (w/ Rachel Menge)

* Tue Jan 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.86.1-1
- Auto-upgrade to 5.15.86.1

* Fri Dec 23 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.85.1-1
- Auto-upgrade to 5.15.85.1

* Mon Dec 19 2022 Betty Lakes <bettylakes@microsoft.com> - 5.15.82.1-2
- Bump release to match kernel

* Tue Dec 13 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.82.1-1
- Auto-upgrade to 5.15.82.1

* Wed Dec 07 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.81.1-1
- Auto-upgrade to 5.15.81.1

* Mon Dec 05 2022 Betty Lakes <bettylakes@microsoft.com> - 5.15.80.1-2
- Bump release to match kernel

* Tue Nov 29 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.80.1-1
- Auto-upgrade to 5.15.80.1

* Fri Nov 18 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.79.1-1
- Auto-upgrade to 5.15.79.1

* Tue Nov 08 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.77.1-1
- Auto-upgrade to 5.15.77.1

* Wed Oct 26 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.74.1-3
- Bump release to match kernel

* Mon Oct 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.74.1-2
- Bump release to match kernel

* Wed Oct 19 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.74.1-1
- Upgrade to 5.15.74.1

* Fri Oct 07 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.72.1-1
- Upgrade to 5.15.72.1

* Tue Sep 27 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.70.1-1
- Upgrade to 5.15.70.1

* Mon Sep 26 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.69.1-1
- Upgrade to 5.15.69.1

* Thu Sep 22 2022 Chris Co <chrco@microsoft.com> - 5.15.67.1-4
- Bump release number to match kernel release

* Tue Sep 20 2022 Chris Co <chrco@microsoft.com> - 5.15.67.1-3
- Bump release number to match kernel release

* Fri Sep 16 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.67.1-2
- Bump release number to match kernel release

* Thu Sep 15 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.67.1-1
- Upgrade to 5.15.67.1

* Thu Sep 15 2022 Adit Jha <aditjha@microsoft.com> - 5.15.63.1-4
- Bump release number to match kernel release

* Tue Sep 13 2022 Saul Paredes <saulparedes@microsoft.com> - 5.15.63.1-3
- Bump release number to match kernel release

* Tue Sep 06 2022 Nikola Bojanic <t-nbojanic@microsoft.com> - 5.15.63.1-2
- Bump release number to match kernel release

* Mon Aug 29 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.63.1-1
- Upgrade to 5.15.63.1

* Wed Aug 17 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.60.2-1
- Upgrade to 5.15.60.2 to fix arm64 builds

* Tue Aug 02 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.57.1-3
- Bump release number to match kernel release

* Mon Aug 01 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.57.1-2
- Bump release number to match kernel release

* Tue Jul 26 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.57.1-1
- Upgrade to 5.15.57.1

* Fri Jul 22 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.55.1-1
- Upgrade to 5.15.55.1

* Thu Jul 21 2022 Henry Li <lihl@microsoft.com> - 5.15.48.1-6
- Bump release number to match kernel release

* Fri Jul 08 2022 Francis Laniel <flaniel@linux.microsoft.com> - 5.15.48.1-5
- Bump release number to match kernel release

* Mon Jun 27 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.48.1-4
- Bump release number to match kernel release

* Mon Jun 27 2022 Henry Beberman <henry.beberman@microsoft.com> - 5.15.48.1-3
- Bump release number to match kernel release

* Wed Jun 22 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 5.15.48.1-2
- Bump release number to match kernel release

* Fri Jun 17 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.48.1-1
- Update source to 5.15.48.1

* Tue Jun 14 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.15.45.1-2
- Bump release number to match kernel release

* Thu Jun 09 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.45.1-1
- Update source to 5.15.45.1
- Remove make headers_check since it is a noop

* Mon Jun 06 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 5.15.41.1-4
- Bump release number to match kernel release

* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.15.41.1-3
- Bump release number to match kernel release

* Thu May 26 2022 Minghe Ren <mingheren@microsoft.com> - 5.15.41.1-2
- Bump release number to match kernel release

* Tue May 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.41.1-1
- Update source to 5.15.41.1

* Tue May 24 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.37.1-3
- Bump release number to match kernel release

* Mon May 16 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.37.1-2
- Bump release number to match kernel release

* Mon May 09 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.37.1-1
- Update source to 5.15.37.1

* Tue Apr 19 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.34.1-1
- Update source to 5.15.34.1

* Tue Apr 19 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 5.15.32.1-3
- Bump release number to match kernel release

* Tue Apr 12 2022 Andrew Phelps <anphel@microsoft.com> - 5.15.32.1-2
- Bump release number to match kernel release

* Fri Apr 08 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.32.1-1
- Update source to 5.15.32.1

* Tue Apr 05 2022 Henry Li <lihl@microsoft.com> - 5.15.26.1-4
- Bump release number to match kernel release

* Mon Mar 28 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.26.1-3
- Bump release number to match kernel release

* Mon Mar 14 2022 Vince Perri <viperri@microsoft.com> - 5.15.26.1-2
- Bump release number to match kernel release

* Tue Mar 08 2022 cameronbaird <cameronbaird@microsoft.com> - 5.15.26.1-1
- Update source to 5.15.26.1

* Mon Mar 07 2022 George Mileka <gmileka@microsoft.com> - 5.15.18.1-5
- Bump release number to match kernel release

* Fri Feb 25 2022 Henry Li <lihl@microsoft.com> - 5.15.18.1-4
- Bump release number to match kernel release

* Thu Feb 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.18.1-3
- Bump release number to match kernel release

* Thu Feb 24 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.15.18.1-2
- Bump release number to match kernel release

* Mon Feb 07 2022 Cameron Baird <cameronbaird@microsoft.com> - 5.15.18.1-1
- Update source to 5.15.18.1

* Thu Feb 03 2022 Henry Li <lihl@microsoft.com> - 5.15.2.1-5
- Bump release number to match kernel release

* Wed Feb 02 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.2.1-4
- Bump release number to match kernel release

* Thu Jan 27 2022 Daniel Mihai <dmihai@microsoft.com> - 5.15.2.1-3
- Bump release number to match kernel release

* Sun Jan 23 2022 Chris Co <chrco@microsoft.com> - 5.15.2.1-2
- Bump release number to match kernel release

* Thu Jan 06 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.15.2.1-1
- Update source to 5.15.2.1

* Tue Jan 04 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.78.1-3
- Update to kernel release 5.10.78.1-3

* Tue Dec 28 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.78.1-2
- Update to kernel release 5.10.78.1-2

* Tue Nov 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.78.1-1
- Update source to 5.10.78.1
- Add patch to fix SPDX-License-Identifier in headers

* Mon Nov 15 2021 Thomas Crian <thcrain@microsoft.com> - 5.10.74.1-4
- Bump release number to match kernel release
- Lint spec and version the glibc-kernheaders provides

* Thu Nov 04 2021 Andrew Phelps <anphel@microsoft.com> - 5.10.74.1-3
- Bump release number to match kernel release

* Tue Oct 26 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.74.1-2
- Bump release number to match kernel release

* Tue Oct 19 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.74.1-1
- Update source to 5.10.74.1
- License verified

* Thu Oct 07 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.69.1-1
- Update source to 5.10.69.1

* Wed Sep 22 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.64.1-2
- Bump release number to match kernel release

* Mon Sep 20 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.64.1-1
- Update source to 5.10.64.1

* Fri Sep 17 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.60.1-1
- Update source to 5.10.60.1
- Add patch to fix VDSO in HyperV

* Thu Sep 09 2021 Muhammad Falak <mwani@microsoft.com> - 5.10.52.1-2
- Bump release number to match kernel release

* Tue Jul 20 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.52.1-1
- Update source to 5.10.52.1

* Mon Jul 19 2021 Chris Co <chrco@microsoft.com> - 5.10.47.1-2
- Bump release number to match kernel release

* Tue Jul 06 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.47.1-1
- Update source to 5.10.47.1

* Wed Jun 30 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-4
- Bump release number to match kernel release

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.42.1-3
- Bump release number to match kernel release

* Wed Jun 16 2021 Chris Co <chrco@microsoft.com> - 5.10.42.1-2
- Bump release number to match kernel release

* Tue Jun 08 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.42.1-1
- Update source to 5.10.42.1

* Thu Jun 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-2
- Bump release number to match kernel release

* Fri May 28 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.37.1-1
- Update source to 5.10.37.1

* Thu May 27 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-7
- Bump release number to match kernel release

* Wed May 26 2021 Chris Co <chrco@microsoft.com> - 5.10.32.1-6
- Bump release number to match kernel release

* Tue May 25 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.32.1-5
- Bump release number to match kernel release

* Thu May 20 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.32.1-4
- Bump release number to match kernel-signed update

* Mon May 17 2021 Andrew Phelps <anphel@microsoft.com> - 5.10.32.1-3
- Bump release number to match kernel release

* Thu May 13 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-2
- Bump release number to match kernel release

* Mon May 03 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.32.1-1
- Update source to 5.10.32.1

* Thu Apr 22 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-4
- Bump release number to match kernel release

* Mon Apr 19 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-3
- Bump release number to match kernel-signed update

* Thu Apr 15 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.10.28.1-2
- Update to kernel release 5.10.28.1-2

* Thu Apr 08 2021 Chris Co <chrco@microsoft.com> - 5.10.28.1-1
- Update source to 5.10.28.1

* Fri Mar 26 2021 Daniel Mihai <dmihai@microsoft.com> - 5.10.21.1-4
- Update to kernel release 5.10.21.1-4

* Thu Mar 18 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-3
- Update to kernel release 5.10.21.1-3

* Wed Mar 17 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.10.21.1-2
- Update to kernel release 5.10.21.1-2

* Thu Mar 11 2021 Chris Co <chrco@microsoft.com> - 5.10.21.1-1
- Update source to 5.10.21.1

* Fri Mar 05 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-4
- Update to kernel release 5.10.13.1-4

* Thu Mar 04 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.10.13.1-3
- Update to kernel release 5.10.13.1-3

* Mon Feb 22 2021 Thomas Crain <thcrain@microsoft.com> - 5.10.13.1-2
- Update to kernel release 5.10.13.1-2

* Thu Feb 18 2021 Chris Co <chrco@microsoft.com> - 5.10.13.1-1
- Update source to 5.10.13.1

* Tue Feb 16 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-5
- Update to kernel release 5.4.91-5

* Tue Feb 09 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-4
- Update to kernel release 5.4.91-4

* Thu Jan 28 2021 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.91-3
- Update to kernel release 5.4.91-3

* Thu Jan 28 2021 Daniel McIlvaney <damcilva@microsoft.com> - 5.4.91-2
- Update release number to match kernel spec

* Wed Jan 20 2021 Chris Co <chrco@microsoft.com> - 5.4.91-1
- Update source to 5.4.91

* Tue Jan 12 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.4.83-4
- Update release number to match kernel spec

* Sat Jan 09 2021 Andrew Phelps <anphel@microsoft.com> - 5.4.83-3
- Update to kernel release 5.4.83-3

* Mon Dec 28 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.4.83-2
- Update to kernel release 5.4.83-2

* Tue Dec 15 2020 Henry Beberman <henry.beberman@microsoft.com> - 5.4.83-1
- Update source to 5.4.83

* Fri Dec 04 2020 Chris Co <chrco@microsoft.com> - 5.4.81-1
- Update source to 5.4.81

* Mon Oct 26 2020 Chris Co <chrco@microsoft.com> - 5.4.72-1
- Update source to 5.4.72
- Add license file
- Lint spec

* Tue Sep 01 2020 Chris Co <chrco@microsoft.com> - 5.4.51-2
- Update source hash

* Wed Aug 19 2020 Chris Co <chrco@microsoft.com> - 5.4.51-1
- Update source to 5.4.51

* Fri Jun 12 2020 Chris Co <chrco@microsoft.com> - 5.4.42-1
- Update source to 5.4.42

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 5.4.23-2
- Renaming linux-api-headers to kernel-headers

* Tue Dec 10 2019 Chris Co <chrco@microsoft.com> - 5.4.23-1
- Update to Microsoft Linux Kernel 5.4.23.
- Use make headers since with 5.4, headers_install now requires rsync.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.19.52-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
- Update to version 4.19.52

* Tue May 07 2019 Ajay Kaher <akaher@vmware.com> - 4.19.40-1
- Update to version 4.19.40

* Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
- Update to version 4.19.32

* Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
- Update to version 4.19.29

* Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> - 4.19.26-1
- Update to version 4.19.26

* Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
- Update to version 4.19.15

* Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
- Update to version 4.19.6

* Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
- Update to version 4.19.1

* Thu Sep 20 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
- Update to version 4.18.9

* Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
- Update to version 4.14.67

* Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 4.14.54-1
- Update to version 4.14.54

* Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.14.8-1
- Version update

* Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
- Version update

* Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
- Version update

* Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
- Version update

* Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
- Version update

* Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
- Version update

* Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.47-1
- Version update

* Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.43-1
- Version update

* Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.34-1
- Version update

* Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.30-1
- Version update

* Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.28-1
- Version update

* Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.27-1
- Update to linux-4.9.27

* Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.26-1
- Update to linux-4.9.26

* Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.24-1
- Update to linux-4.9.24

* Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.13-1
- Update to linux-4.9.13

* Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.9-1
- Update to linux-4.9.9

* Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.9.2-1
- Update to linux-4.9.2

* Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.9.0-1
- Update to linux-4.9.0

* Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.35-1
- Update to linux-4.4.35

* Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.31-1
- Update to linux-4.4.31

* Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.20-1
- Update kernel version to 4.4.20

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.4.8-2
- GA - Bump release of all rpms

* Thu Apr 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.4.8-1
- Update to linux-4.4.8

* Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 4.2.0-1
- Upgrading kernel version to 4.2.0.

* Wed Aug 12 2015 Sharath George <sharathg@vmware.com> - 4.0.9-1
- Upgrading kernel version.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 3.13.3-1
- Initial build. First version
