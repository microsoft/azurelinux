%global debug_package %{nil}
%global __os_install_post %{nil}
%global _firmwarepath    /lib/firmware
%define _binaries_in_noarch_packages_terminate_build   0
Summary:        Linux Firmware
Name:           linux-firmware
Version:        20230804
Release:        1%{?dist}
License:        GPL+ AND GPLv2+ AND MIT AND Redistributable, no modification permitted
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://www.kernel.org/
Source0:        https://git.kernel.org/pub/scm/linux/kernel/git/firmware/%{name}.git/snapshot/%{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       %{name}-broadcom = %{version}-%{release}
Requires:       %{name}-intel = %{version}-%{release}
Requires:       %{name}-qlogic = %{version}-%{release}
Requires:       %{name}-qualcomm = %{version}-%{release}

%description
This package includes firmware files required for some devices to operate.

%package       broadcom
Summary:       Firmware for Broadcom devices

%description   broadcom
Firmware for Broadcom devices.

%package       intel
Summary:       Firmware for Intel devices

%description   intel
Firmware for Intel devices.

%package       qlogic
Summary:       Firmware for QLogic devices

%description   qlogic
Firmware for QLogic devices.

%package       qualcomm
Summary:       Firmware for Qualcomm devices

%description   qualcomm
Firmware for Qualcomm devices.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_firmwarepath}
cp -r bnx2x %{buildroot}%{_firmwarepath}
cp -r qed %{buildroot}%{_firmwarepath}
cp -r brcm %{buildroot}%{_firmwarepath}
cp -r rsi %{buildroot}%{_firmwarepath}
cp rsi_91x.fw %{buildroot}%{_firmwarepath}
cp -r ath10k %{buildroot}%{_firmwarepath}
cp -r i915 %{buildroot}%{_firmwarepath}
cp -r intel %{buildroot}%{_firmwarepath}
cp iwlwifi-8000C-*.ucode %{buildroot}%{_firmwarepath}

%files
%defattr(-,root,root)
%license GPL*
%license WHENCE LICENCE.iwlwifi_firmware
%{_firmwarepath}/rsi
%{_firmwarepath}/rsi_91x.fw
%{_firmwarepath}/iwlwifi-8000C-*.ucode

%files broadcom
%defattr(-,root,root)
%license WHENCE LICENCE.broadcom_bcm43xx LICENCE.cypress
%{_firmwarepath}/bnx2x
%{_firmwarepath}/brcm

%files qlogic
%defattr(-,root,root)
%license WHENCE LICENCE.qla1280
%{_firmwarepath}/qed

%files qualcomm
%defattr(-,root,root)
%license WHENCE LICENSE.QualcommAtheros_ath10k
%{_firmwarepath}/ath10k

%files intel
%defattr(-,root,root)
%license WHENCE LICENSE.i915
%license LICENSE.ipu3_firmware LICENCE.ibt_firmware LICENCE.fw_sst_0f28
%license LICENCE.IntcSST2 LICENCE.adsp_sst LICENSE.ice
%{_firmwarepath}/i915
%{_firmwarepath}/intel

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20230804-1
- Auto-upgrade to 20230804 - Azure Linux 3.0 - package upgrades

* Mon Nov 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 20211216-2
- Split linux-firmware to sub packages.

* Tue Feb 01 2022 Chris Co <chrco@microsoft.com> - 20211216-1
- Update to 20211216.

* Fri Feb 19 2021 Chris Co <chrco@microsoft.com> - 20200316-3
- Add bnx2x and qed firmware.
- Add WHENCE and relevant LICENSE files.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 20200316-2
- Added %%license line automatically

* Thu Mar 19 2020 Henry Beberman <henry.beberman@microsoft.com> 20200316-1
- Update to 20200316. Remove LS1012a binaries. Source0 URL Fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 20190205-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Feb 05 2019 Alexey Makhalov <amakhalov@vmware.com> 20190205-1
- Added ath10k firmware (for ls1012a).
- Use 1:1 folder layout for ppfe firmware.

* Wed Jan 09 2019 Alexey Makhalov <amakhalov@vmware.com> 20190109-1
- Added Compulab Fitlet2 firmware.

* Thu Nov 29 2018 Srinidhi Rao <srinidhir@vmware.com> 20181129-1
- Updated pfe firmware files for NXP LS1012A FRWY board

* Wed Oct 10 2018 Ajay Kaher <akaher@vmware.com> 20181010-1
- Updated brcm firmwares for Rpi B and Rpi B+

* Thu Aug 23 2018 Alexey Makhalov <amakhalov@vmware.com> 20180823-1
- Initial version. RPi3 and Dell Edge Gateway 3001 support.
