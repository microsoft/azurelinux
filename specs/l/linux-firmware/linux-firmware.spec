# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

%global _firmwarepath	/usr/lib/firmware
%define _binaries_in_noarch_packages_terminate_build 0

Name:		linux-firmware
Version:	20260916
Release: 5%{?dist}
Summary:	Firmware files used by the Linux kernel
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND MIT AND LicenseRef-Fedora-Firmware
URL:		http://www.kernel.org/
BuildArch:	noarch

Source0:	https://www.kernel.org/pub/linux/kernel/firmware/%{name}-%{version}.tar.xz

BuildRequires:	make
BuildRequires:	git-core
BuildRequires:	python3
%if %{undefined rhel}
BuildRequires:	parallel
# Not required but de-dupes FW so reduces size
BuildRequires:	rdfind
%endif

Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	((linux-firmware = %{version}-%{release}) if linux-firmware)
Recommends:	qcom-wwan-firmware
Recommends:	amd-gpu-firmware
Recommends:	amd-ucode-firmware
Recommends:	atheros-firmware
Recommends:	brcmfmac-firmware
Recommends:	cirrus-audio-firmware
Recommends:	intel-audio-firmware
Recommends:	intel-gpu-firmware
Recommends:	mt7xxx-firmware
Recommends:	nvidia-gpu-firmware
Recommends:	nxpwireless-firmware
Recommends:	realtek-firmware
Recommends:	tiwilink-firmware

%description
This package includes firmware files required for some devices to
operate.

%package whence
Summary:	WHENCE License file
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND MIT AND LicenseRef-Fedora-Firmware
%description whence
This package contains the WHENCE license file which documents the vendor license details.

# GPU firmwares
%package -n amd-gpu-firmware
Summary:	Firmware for AMD GPUs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n amd-gpu-firmware
Firmware for AMD amdgpu and radeon GPUs.

%package -n intel-gpu-firmware
Summary:	Firmware for Intel GPUs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
Recommends:	intel-npu-firmware
%description -n intel-gpu-firmware
Firmware for Intel GPUs including GuC (Graphics Microcontroller), HuC (HEVC/H.265
Microcontroller) and DMC (Display Microcontroller) firmware for Skylake and later
platforms.

%package -n intel-npu-firmware
Summary:	Firmware for Intel VPU/NPU accelerators
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-npu-firmware
Firmware for Intel NPU and VPU accelerators for Intel Core Ultra Series 1-3.

%package -n nvidia-gpu-firmware
Summary:	Firmware for NVIDIA GPUs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n nvidia-gpu-firmware
Firmware for NVIDIA GPUs.

# Microcode updates
%package -n amd-ucode-firmware
Summary:	Microcode updates for AMD CPUs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n amd-ucode-firmware
Microcode updates for AMD CPUs, AMD SEV and AMD TEE.

# WiFi/Bluetooth/WWAN firmwares
%package -n atheros-firmware
Summary:	Firmware for Qualcomm Atheros WiFi/Bluetooth adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n atheros-firmware
Firmware for Qualcomm Atheros ath6k/ath9k/ath10k/ath11k WiFi adapters.

%package -n brcmfmac-firmware
Summary:	Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n brcmfmac-firmware
Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters.

%package -n iwlegacy-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 3945(A)BG and 4965AGN adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n iwlegacy-firmware
This package contains the firmware required by the iwlegacy driver
for Linux. This includes the 3945(A)BG and 4965AGN WiFi NICs. Usage
of the firmware is subject to the terms and conditions contained
inside the provided LICENSE file. Please read it carefully.

%package -n iwlwifi-dvm-firmware
Summary:	DVM Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	iwlbluetooth-firmware = %{version}-%{release}
%description -n iwlwifi-dvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with DVM firmware support (CONFIG_IWLDVM=y/m). Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlwifi-mvm-firmware
Summary:	MVM Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	iwlbluetooth-firmware = %{version}-%{release}
# Same hardware, newer firmware with a different driver, enables smooth migration
Requires:	iwlwifi-mld-firmware = %{version}-%{release}
%description -n iwlwifi-mvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with MVM firmware support (CONFIG_IWLMVM=y/m).  Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlwifi-mld-firmware
Summary:	MLD Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	iwlbluetooth-firmware = %{version}-%{release}
%description -n iwlwifi-mld-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with MLD firmware support (CONFIG_IWLMLD=y/m).  Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlbluetooth-firmware
Summary:	Bluetooth Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n iwlbluetooth-firmware
This package contains the firmware required by the iwlwifi devices that
support bluetooth.

%package -n libertas-firmware
Summary:	Firmware for Marvell Libertas SD/USB WiFi Network Adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n libertas-firmware
Firmware for the Marvell Libertas series of WiFi Network Adapters
Including the SD 8686/8787 and USB 8388/8388.

%package -n mt7xxx-firmware
Summary:	Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mt7xxx-firmware
Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters

%package -n nxpwireless-firmware
Summary:	Firmware for NXP WiFi/Bluetooth/UWB adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n nxpwireless-firmware
Firmware for NXP WiFi/Bluetooth/UWB adapters.

%package -n realtek-firmware
Summary:	Firmware for Realtek WiFi/Bluetooth adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n realtek-firmware
Firmware for Realtek WiFi/Bluetooth adapters

%package -n qcom-wwan-firmware
Summary:	Firmware for Qualcomm Wireless WAN modems
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qcom-wwan-firmware
Firmware for Qualcomm Snapdragon X-series (SDX) wireless WAN modems used
across numerous WWAN cards from numerous vendors.

%package -n tiwilink-firmware
Summary:	Firmware for Texas Instruments WiFi/Bluetooth adapters
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n tiwilink-firmware
Firmware for Texas Instruments WiFi/Bluetooth adapters

# SMART NIC and network switch firmwares
%package -n liquidio-firmware
Summary:	Firmware for Cavium LiquidIO Intelligent Server Adapter
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n liquidio-firmware
Firmware for Cavium LiquidIO Intelligent Server Adapter

%package -n mlxsw_spectrum-firmware
Summary:	Firmware for Mellanox Spectrum 1/2/3 Switches
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mlxsw_spectrum-firmware
Firmware for Mellanox Spectrumi series 1/2/3 ethernet switches.

%package -n mrvlprestera-firmware
Summary:	Firmware for Marvell Prestera Switchdev/ASIC devices
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mrvlprestera-firmware
Firmware for Marvell Prestera Switchdev/ASIC devices

%package -n netronome-firmware
Summary:	Firmware for Netronome Smart NICs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n netronome-firmware
Firmware for Netronome Smart NICs

%package -n qcom-accel-firmware
Summary:	Firmware for Qualcomm Technologies data center / Open-vRAN Accelerators
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qcom-accel-firmware
Firmware for Qualcomm Technologies data center and Open-vRAN accelerators
including the X100 5G RAN Accelerator Card, the QRU100 5G RAN Platform
and the Cloud AI 100.

%package -n qed-firmware
Summary:	Firmware for Marvell FastLinQ adapters family
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qed-firmware
Firmware for Marvell FastLinQ adapters family (QDE), this device
supports RoCE (RDMA over Converged Ethernet), iSCSI, iWARP, FCoE
and ethernet including SRIOV, DCB etc.

# Silicon Vendor specific
%package -n mediatek-firmware
Summary:	Firmware for Mediatek SoCs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mediatek-firmware
Firmware for various compoents in Mediatek SoCs, in particular SCP.

%package -n qcom-firmware
Summary:	Firmware for Qualcomm SoCs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	atheros-firmware = %{version}-%{release}
%description -n qcom-firmware
Firmware for various compoents in Qualcomm SoCs including Adreno GPUs,
Venus video encode/decode, Audio DSP, Compute DSP, modem, Sensor DSPs.

# Vision and ISP hardware
%package -n intel-vsc-firmware
Summary:	Firmware files for Intel Visual Sensing Controller (IVSC)
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-vsc-firmware
Firmware files for Intel Visual Sensing Controller (IVSC) for
Tiger Lake, Alder Lake and Raptor Lake SoCs and the IPU3/6 firmware.

# Sound codec hardware
%package -n cirrus-audio-firmware
Summary:	Firmware for Cirrus audio amplifiers and codecs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n cirrus-audio-firmware
Firmware for Cirrus audio amplifiers and codecs

%package -n intel-audio-firmware
Summary:	Firmware for Intel audio DSP amplifiers and codecs
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-audio-firmware
Firmware for Intel audio DSP amplifiers and codecs

# Random other hardware
%package -n dvb-firmware
Summary:	Firmware for various DVB broadcast receivers
License:	LicenseRef-Fedora-Firmware
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n dvb-firmware
Firmware for various DVB broadcast receivers. These include the
Siano DTV devices, devices based on Conexant chipsets (cx18,
cx23885, cx23840, cx231xx), Xceive xc4000/xc5000, DiBcom dib0700,
Terratec H5 DRX-K, ITEtech IT9135 Ax and Bx, and av7110.

%prep
%autosetup -S git -p1

%build

%install
install -dm 0755 %{buildroot}/%{_firmwarepath}/updates

%make_build DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} install-xz
%if %{undefined rhel}
%make_build DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} dedup
%endif

#Cleanup files we don't want to ship
pushd %{buildroot}/%{_firmwarepath}
# Remove firmware shipped in separate packages already
# Perhaps these should be built as subpackages of linux-firmware?
rm -rf ess korg sb16 yamaha

# Remove firmware for Creative CA0132 HD as it's in alsa-firmware
rm -f ctefx.bin* ctspeq.bin*

# Remove source files we don't need to install
rm -rf carl9170fw
rm -rf cis/{src,Makefile}
rm -f atusb/ChangeLog
rm -f av7110/{Boot.S,Makefile}
rm -f dsp56k/{bootstrap.asm,concat-bootstrap.pl,Makefile}
rm -f iscis/{*.c,*.h,README,Makefile}
rm -f keyspan_pda/{keyspan_pda.S,xircom_pgs.S,Makefile}
rm -f usbdux/*dux */*.asm

# No need to install old firmware versions where we also provide newer versions
# which are preferred and support the same (or more) hardware
rm -f libertas/sd8686_v8*
rm -f libertas/usb8388_v5.bin*

# Remove superfluous infra files
rm -f check_whence.py Makefile README
popd

# Create file list but exclude firmwares that we place in subpackages
FILEDIR=`pwd`
pushd %{buildroot}/%{_firmwarepath}
find . \! -type d > $FILEDIR/linux-firmware.files
find . -type d | sed -e '/^.$/d' > $FILEDIR/linux-firmware.dirs
popd
sed -i -e 's:^./::' linux-firmware.{files,dirs}
sed \
	-i -e '/^a300_p/d' \
	-i -e '/^amdgpu/d' \
	-i -e '/^amdnpu/d' \
	-i -e '/^amd/d' \
	-i -e '/^amdtee/d' \
	-i -e '/^amd-ucode/d' \
	-i -e '/^ar3k/d' \
	-i -e '/^ath6k/d' \
	-i -e '/^ath9k_htc/d' \
	-i -e '/^ath10k/d' \
	-i -e '/^ath11k/d' \
	-i -e '/^ath12k/d' \
	-i -e '/^as102_data/d' \
	-i -e '/^av7110/d' \
	-i -e '/^brcm/d' \
	-i -e '/^cirrus/d' \
	-i -e '/^cmmb/d' \
	-i -e '/^cypress/d' \
	-i -e '/^dvb/d' \
	-i -e '/^i915/d' \
	-i -e '/^intel\/avs/d' \
	-i -e '/^intel\/catpt/d' \
	-i -e '/^intel\/IntcSST2.bin/d' \
	-i -e '/^intel\/dsp_fw/d' \
	-i -e '/^intel\/fw_sst/d' \
	-i -e '/^intel\/ibt/d' \
	-i -e '/^intel\/ipu/d' \
	-i -e '/^intel\/ipu3/d' \
	-i -e '/^intel\/irci_irci/d' \
	-i -e '/^intel\/vpu/d' \
	-i -e '/^intel\/vsc/d' \
	-i -e '/^isdbt/d' \
	-i -e '/^iwlwifi/d' \
	-i -e '/^intel\/iwlwifi/d' \
	-i -e '/^nvidia\/a/d' \
	-i -e '/^nvidia\/g/d' \
	-i -e '/^nvidia\/tu/d' \
	-i -e '/^libertas/d' \
	-i -e '/^liquidio/d' \
	-i -e '/^mellanox/d' \
	-i -e '/^mediatek/d' \
	-i -e '/^mrvl\/prestera/d' \
	-i -e '/^mrvl\/sd8787/d' \
	-i -e '/^mt76/d' \
	-i -e '/^netronome/d' \
	-i -e '/^nxp/d' \
	-i -e '/^qca/d' \
	-i -e '/^qcom/d' \
	-i -e '/^qed/d' \
	-i -e '/^radeon/d' \
	-i -e '/^rtl_bt/d' \
	-i -e '/^rtlwifi/d' \
	-i -e '/^rtw88/d' \
	-i -e '/^rtw89/d' \
	-i -e '/^sms1xxx/d' \
	-i -e '/^tdmb/d' \
	-i -e '/^ti-connectivity/d' \
	-i -e '/^v4l-cx2/d' \
	-i -e '/^xe/d' \
	linux-firmware.{files,dirs}
sed -i -e 's!^!/usr/lib/firmware/!' linux-firmware.{files,dirs}
sed -i -e 's/^/"/;s/$/"/' linux-firmware.files
sed -e 's/^/%%dir /' linux-firmware.dirs >> linux-firmware.files

# temporary workaround for directory->symlink changes/migration
%pretrans -n nvidia-gpu-firmware -p <lua>
path = "/usr/lib/firmware/nvidia/ad103"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end
path = "/usr/lib/firmware/nvidia/ad104"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end
path = "/usr/lib/firmware/nvidia/ad106"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end
path = "/usr/lib/firmware/nvidia/ad107"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end


%files -f linux-firmware.files
%license LICENSES/*
%dir %{_firmwarepath}

%files whence
%license LICENSE WHENCE

# GPU firmwares
%files -n amd-gpu-firmware
%license LICENSES/LICENSE.radeon LICENSES/LICENSE.amdgpu LICENSES/LICENSE.amdnpu
%{_firmwarepath}/amdgpu/
%{_firmwarepath}/amdnpu/
%{_firmwarepath}/radeon/

%files -n intel-gpu-firmware
%license LICENSES/LICENSE.i915
%license LICENSES/LICENSE.xe
%{_firmwarepath}/i915/
%{_firmwarepath}/xe/

%files -n intel-npu-firmware
%license LICENSES/LICENSE.intel_vpu
%dir %{_firmwarepath}/intel/vpu/
%{_firmwarepath}/intel/vpu/*

%files -n nvidia-gpu-firmware
%license LICENSES/LICENCE.nvidia
%dir %{_firmwarepath}/nvidia/
%{_firmwarepath}/nvidia/a*
%{_firmwarepath}/nvidia/g*
%{_firmwarepath}/nvidia/tu*

# Microcode updates
%files -n amd-ucode-firmware
%license LICENSES/LICENSE.amd-ucode
%{_firmwarepath}/amd/
%{_firmwarepath}/amdtee/
%{_firmwarepath}/amd-ucode/

# WiFi/Bluetooth firmwares
%files -n atheros-firmware
%license LICENSES/LICENCE.atheros_firmware
%license LICENSES/LICENSE.QualcommAtheros_ar3k
%license LICENSES/LICENSE.QualcommAtheros_ath10k
%license LICENSES/LICENCE.open-ath9k-htc-firmware
%license LICENSES/NOTICE.qca
%{_firmwarepath}/ar3k/
%{_firmwarepath}/ath6k/
%{_firmwarepath}/ath9k_htc/
%{_firmwarepath}/ath10k/
%{_firmwarepath}/ath11k/
%{_firmwarepath}/ath12k/
%{_firmwarepath}/qca/

%files -n brcmfmac-firmware
%license LICENSES/LICENCE.broadcom_bcm43xx
%license LICENSES/LICENCE.cypress
%{_firmwarepath}/brcm/
%{_firmwarepath}/cypress/

%files -n iwlegacy-firmware
%license LICENSES/LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-3945-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-3945-*.ucode*
%{_firmwarepath}/iwlwifi-4965-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-4965-*.ucode*

%files -n iwlwifi-dvm-firmware
%license LICENSES/LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-1??-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-1??-*.ucode*
%{_firmwarepath}/iwlwifi-1000-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-1000-*.ucode*
%{_firmwarepath}/iwlwifi-20?0-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-20?0-*.ucode*
%{_firmwarepath}/iwlwifi-5??0-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-5??0-*.ucode*
%{_firmwarepath}/iwlwifi-60?0-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-60?0-*.ucode*
%{_firmwarepath}/iwlwifi-6000g2?-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-6000g2?-*.ucode*

%files -n iwlwifi-mvm-firmware
%license LICENSES/LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-316?-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-316?-*.ucode*
%{_firmwarepath}/iwlwifi-726?-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-726?-*.ucode*
%{_firmwarepath}/iwlwifi-7265D-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-7265D-*.ucode*
%{_firmwarepath}/iwlwifi-8000C-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-8000C-*.ucode*
%{_firmwarepath}/iwlwifi-8265-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-8265-*.ucode*
%{_firmwarepath}/iwlwifi-9??0-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-9??0-*.ucode*
%{_firmwarepath}/iwlwifi-cc-a0-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-cc-a0-*.ucode*
%{_firmwarepath}/iwlwifi-gl-c0*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-gl-c0*
%{_firmwarepath}/iwlwifi-ma-b0*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-ma-b0*
%{_firmwarepath}/iwlwifi-Qu*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-Qu*.ucode*
%{_firmwarepath}/iwlwifi-ty-a0*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-ty-a0*
%{_firmwarepath}/iwlwifi-so-a0*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-so-a0*
%{_firmwarepath}/iwlwifi-bz-b0*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-bz-b0*
%exclude %{_firmwarepath}/iwlwifi-bz-b0*9[7-9].ucode*
%exclude %{_firmwarepath}/iwlwifi-bz-b0*1??.ucode*
%exclude %{_firmwarepath}/intel/iwlwifi/iwlwifi-bz-b0*9[7-9].ucode*
%exclude %{_firmwarepath}/intel/iwlwifi/iwlwifi-bz-b0*1??.ucode*
%exclude %{_firmwarepath}/iwlwifi-gl-c0*9[7-9].ucode*
%exclude %{_firmwarepath}/iwlwifi-gl-c0*1??.ucode*
%exclude %{_firmwarepath}/intel/iwlwifi/iwlwifi-gl-c0*9[7-9].ucode*
%exclude %{_firmwarepath}/intel/iwlwifi/iwlwifi-gl-c0*1??.ucode*

%files -n iwlwifi-mld-firmware
%license LICENSES/LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-bz-b0*9[7-9].ucode*
%{_firmwarepath}/iwlwifi-bz-b0*1??.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-bz-b0*9[7-9].ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-bz-b0*1??.ucode*
%{_firmwarepath}/iwlwifi-gl-c0*9[7-9].ucode*
%{_firmwarepath}/iwlwifi-gl-c0*1??.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-gl-c0*9[7-9].ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-gl-c0*1??.ucode*
%{_firmwarepath}/iwlwifi-sc-a0-*1??.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-sc-a0-*1??.ucode*

%files -n iwlbluetooth-firmware
%license LICENSES/LICENCE.ibt_firmware
%{_firmwarepath}/intel/ibt*

%files -n libertas-firmware
%license LICENSES/LICENCE.Marvell LICENSES/LICENCE.OLPC
%dir %{_firmwarepath}/libertas
%dir %{_firmwarepath}/mrvl
%{_firmwarepath}/libertas/*
%{_firmwarepath}/mrvl/sd8787*

%files -n mt7xxx-firmware
%license LICENSES/LICENCE.mediatek
%license LICENSES/LICENCE.ralink_a_mediatek_company_firmware
%dir %{_firmwarepath}/mediatek
%{_firmwarepath}/mediatek/mt76*
%{_firmwarepath}/mediatek/mt791*
%{_firmwarepath}/mediatek/mt7925/
%{_firmwarepath}/mediatek/mt7927/
%{_firmwarepath}/mediatek/mt7996/
%{_firmwarepath}/mediatek/BT*
%{_firmwarepath}/mediatek/WIFI*
%{_firmwarepath}/mt76*

%files -n nxpwireless-firmware
%license LICENSES/LICENSE.nxp
%dir %{_firmwarepath}/nxp
%{_firmwarepath}/nxp/*

%files -n qcom-wwan-firmware
%license LICENSES/LICENSE.qcom LICENSES/NOTICE.qcom
%dir %{_firmwarepath}/qcom
%{_firmwarepath}/qcom/sdx*/

%files -n realtek-firmware
%license LICENSES/LICENCE.rtlwifi_firmware.txt
%{_firmwarepath}/rtl_bt/
%{_firmwarepath}/rtlwifi/
%{_firmwarepath}/rtw88/
%{_firmwarepath}/rtw89/

%files -n tiwilink-firmware
%license LICENSES/LICENCE.ti-connectivity
%dir %{_firmwarepath}/ti-connectivity/
%{_firmwarepath}/ti-connectivity/*

# SMART NIC and network switch firmwares
%files -n liquidio-firmware
%license LICENSES/LICENCE.cavium_liquidio
%dir %{_firmwarepath}/liquidio
%{_firmwarepath}/liquidio/*

%files -n mrvlprestera-firmware
%license LICENSES/LICENCE.Marvell
%dir %{_firmwarepath}/mrvl/prestera
%{_firmwarepath}/mrvl/prestera/*

%files -n mlxsw_spectrum-firmware
%dir %{_firmwarepath}/mellanox/
%{_firmwarepath}/mellanox/*

%files -n netronome-firmware
%license LICENSES/LICENCE.Netronome
%dir %{_firmwarepath}/netronome
%{_firmwarepath}/netronome/*

%files -n qcom-accel-firmware
%license LICENSES/LICENSE.qcom LICENSES/NOTICE.qcom
%dir %{_firmwarepath}/qcom
%dir %{_firmwarepath}/qcom/aic100
%dir %{_firmwarepath}/qcom/qdu100
%{_firmwarepath}/qcom/aic100/*
%{_firmwarepath}/qcom/qdu100/*

%files -n qed-firmware
%dir %{_firmwarepath}/qed
%{_firmwarepath}/qed/*

# Silicon Vendor specific
%files -n mediatek-firmware
%license LICENSES/LICENCE.mediatek
%dir %{_firmwarepath}/mediatek
%{_firmwarepath}/mediatek/mt798?*
%{_firmwarepath}/mediatek/mt8173/
%{_firmwarepath}/mediatek/mt8183/
%{_firmwarepath}/mediatek/mt8186/
%{_firmwarepath}/mediatek/mt8188/
%{_firmwarepath}/mediatek/mt8189/
%{_firmwarepath}/mediatek/mt8192/
%{_firmwarepath}/mediatek/mt8195/
%{_firmwarepath}/mediatek/mt8196/
%{_firmwarepath}/mediatek/sof/
%{_firmwarepath}/mediatek/sof-tplg/

%files -n qcom-firmware
%license LICENSES/LICENSE.qcom LICENSES/LICENSE.qcom_yamato LICENSES/NOTICE.qcom
%dir %{_firmwarepath}/qcom
%{_firmwarepath}/a300_p*
%{_firmwarepath}/qcom/eliza/
%{_firmwarepath}/qcom/glymur/
%{_firmwarepath}/qcom/hawi/
%{_firmwarepath}/qcom/kaanapali/
%{_firmwarepath}/qcom/maili/
%{_firmwarepath}/qcom/nord/
%{_firmwarepath}/qcom/*.fw*
%{_firmwarepath}/qcom/*.bin*
%{_firmwarepath}/qcom/*.m*
%{_firmwarepath}/qcom/apq*/
%{_firmwarepath}/qcom/qcm*/
%{_firmwarepath}/qcom/qcs*/
%{_firmwarepath}/qcom/qrb*/
%{_firmwarepath}/qcom/sa*/
%{_firmwarepath}/qcom/shikra/
%{_firmwarepath}/qcom/sc*/
%{_firmwarepath}/qcom/sdm*/
%{_firmwarepath}/qcom/sm*/
%{_firmwarepath}/qcom/venus-*/
%{_firmwarepath}/qcom/vpu*/
%{_firmwarepath}/qcom/x1*/

# Vision and ISP hardware
%files -n intel-vsc-firmware
%license LICENSES/LICENSE.ivsc
%dir %{_firmwarepath}/intel/ipu/
%dir %{_firmwarepath}/intel/vsc/
%{_firmwarepath}/intel/ipu3-fw.bin*
%{_firmwarepath}/intel/irci_irci_ecr-master_20161208_0213_20170112_1500.bin*
%{_firmwarepath}/intel/ipu/*
%{_firmwarepath}/intel/vsc/*

# Sound codec hardware
%files -n cirrus-audio-firmware
%license LICENSES/LICENSE.cirrus
%dir %{_firmwarepath}/cirrus
%{_firmwarepath}/cirrus/*

%files -n intel-audio-firmware
%license LICENSES/LICENCE.adsp_sst LICENSES/LICENCE.IntcSST2
%dir %{_firmwarepath}/intel/
%dir %{_firmwarepath}/intel/avs/
%dir %{_firmwarepath}/intel/catpt/
%{_firmwarepath}/intel/avs/*
%{_firmwarepath}/intel/catpt/*
%{_firmwarepath}/intel/dsp_fw*
%{_firmwarepath}/intel/fw_sst*
%{_firmwarepath}/intel/IntcSST2.bin*

# Random other hardware
%files -n dvb-firmware
%license LICENSES/LICENSE.dib0700 LICENSES/LICENCE.it913x LICENSES/LICENCE.siano
%license LICENSES/LICENCE.xc4000 LICENSES/LICENCE.xc5000 LICENSES/LICENCE.xc5000c
%dir %{_firmwarepath}/av7110/
%{_firmwarepath}/av7110/*
%{_firmwarepath}/as102_data*
%{_firmwarepath}/cmmb*
%{_firmwarepath}/dvb*
%{_firmwarepath}/isdbt*
%{_firmwarepath}/sms1xxx*
%{_firmwarepath}/tdmb*
%{_firmwarepath}/v4l-cx2*

%changelog
* Wed Sep 16 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260916-1
- Update to 20260916
- Update to license field for current redist license string
- Split out Intel VPU firmware
- A lot of AMDGPU reverts/partial revert and updates
- qcom: add ADSP firmware for maili platform
- intel_vpu: Update NPU firmware
- rtl_nic: add firmware rtl8261d.bin for RTL8261d
- qcom: vpu: add Gen2 firmware binary for sc8280xp
- qcom/sdm845: Let SHIFT6mq use the provided Wi-Fi firmware
- WHENCE: add missing symlink for TaiqiCat (TQC) A01
- ath10k: WCN3990: hw1.0: add shikra firmware files
- cirrus: cs35l57: Add firmware for Cirrus Amps for a Lenovo laptop

* Sat Sep 12 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260910-2
- Split out Intel Bluetooth into subpackage
- Fix location of Intel Xe GPU firmware

* Thu Sep 10 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260910-1
- Update to 20260910
- cirrus: cs35l56: Update firmware for Cirrus Amps for some HP laptops
- qcom: Update ADSP firmware for sa8775p platform
- cs35l56: Add non-spkid firmware names for Thinkbook 16P Gen6 (17AA3921)
- QCA: Add Bluetooth firmware for WCN7750 on Maili platform
- qcom: point qcs8300 firmawre to sa8775p instance
- qcom: update ADSP firmware for qcs615 platform
- qcom: Add ADSP firmware for sc8280xp-radxa-dragon-q8b
- qcom: vpu: Update video firmware binary for Glymur
- qcom: sdm845: Add GPU firmware for SHIFT6mq
- qcom: Update ADSP firmware for QCM6490 platform
- amdgpu: DMCUB updates for various ASICs
- cirrus: Version and cleanup of SDCA FW files
- cirrus: cs35l41: Add Firmware for ASUS Zenbook Laptop using CS35L41 HDA
- QCA: Add Bluetooth firmware hmtnv20.b201/b202 for WCN7850 on Nord platform
- ath12k: QCC2072 hw1.0: update to WLAN.COL.1.0.c2-00277-QCACOLSWPL_V1_TO_SILICONZ-1
- [cypress]: Update firmware for cyfmac43455 SDIO
- QCA: Update Bluetooth QCA6698 firmware to 2.1.2-00079
- amdgpu: DMCUB updates for various ASICs
- amdgpu: add VCN 5.3.0 firmware
- qcom: update CDSP firmware for x1e80100 platform
- qcom: add QUPv3/HPASS/NSP firmware for nord
- Update firmware file for Intel BlazarIW/BlazarU/Scorpius core
- qcom/sa8775p: update signature on cdsp1 firmware
- cirrus: cs35l54: Add Cirrus CS35L54 firmware mappings for an HP laptop
- Upload firmware for tas2573 stereo
- intel: avs: Add AudioDSP base firmware for LKF platforms
- intel: avs: Update AudioDSP firmware for APL-based platforms
- intel: avs: Update AudioDSP firmware for SKL-based platforms
- intel: catpt: Update AudioDSP firmware for BDW platforms
- mediatek MT7925: update bluetooth firmware to 20260813113236
- update firmware for MT7925 WiFi device
- copy-firmware: Do not fail without GNU parallel
- QCA: Update Bluetooth WCN3988 firmware 2.1.5.c5-00042 to 2.1.5.c5-00060
- amdgpu: add a number of new firmwares
- amdgpu: DMCUB update for DCN314
- qca: Update Bluetooth QCC2072 UART interface firmware from 1.1.0-00295 to 1.1.0-00340
- iwlwifi: add Hr/Gf/Bz/Sc FW for core24.70-49 release
- iwlwifi: update cc/Qu/QuZ/ty/So/Ma firmwares for core24.70-49 release
- cirrus: cs42l45: Add CS42L45 SDCA codec firmware for Samsung laptops
- cirrus: cs42l45: Add new SSIDs for Dell laptops
- cirrus: cs35l56: Add firmware for Cirrus Amps for an ASUS laptop
- cirrus: cs35l56: Add Cirrus CS35L56 firmware mappings for some Dell laptops
- WHENCE: Move qcom qcdxkmsuc8[23]80.mbn firmwares to Adreno section
- WHENCE: Separate qcom SoC remoteproc firmwares
- amdgpu: DMCUB updates for various ASICs
- Revert "amdgpu: update GC 10.3.6 firmware"
- qcom: add CDSP firmware for eliza platform
- qcom: vpu: add Gen2 firmware binary for Eliza
- ath12k: QCC2072 hw1.0: update to WLAN.COL.1.0.c2-00228-QCACOLSWPL_V1_TO_SILICON-1
- cirrus: cs35l63: Add Cirrus CS35L63 firmware mappings for some Dell laptops

* Fri Aug 14 2026 Stephen Gallagher <sgallagh@redhat.com> - 20260810-2
- Allow building on systems lacking 'parallel`, such as Fedora ELN

* Tue Aug 11 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260810-1
- Update to 20260810
- amdgpu: numerous firmware updates
- update firmware for MT7922 WiFi device
- morsemicro: add firmware for mm8108 support
- ath10k: WCN3990 hw1.0: update board-2.bin
- Update firmware for an8811hb 2.5G ethernet phy
- xe: Update GUC to v70.72.1 for BMG, LNL, PTL, NVL-S
- mediatek MT7922: update bluetooth firmware to 20260724143815
- airoha: update AN7583 NPU firmwares to version 0.5
- qcom: Add gpu firmwares for Eliza chipset
- cirrus: cs35l57: Add firmware for Cirrus Amps for some Samsung laptops
- rtw89: 8922d: add fw 0.35.113.2
- qcom: venus-5.4: fix vp9 decoder assertion failure
- qla2xxx: Add ql2900_fw.bin firmware for 29xx adapters
- qcom: Update qdsp6sw firmware for shikra platform
- amdgpu: DMCUB updates for various ASICs
- intel_vpu: Update NPU firmware
- qcom: Update DSP firmware for qcs8300 platform
- tas2783: Add firmware for new soundwire devices
- rtw88: add firmware v41.0.0 for RTL8723B
- Update AMD cpu microcode
- Add firmware file for Intel BlazarIW
- Update firmware file for Intel BlazarI/BlazarU/Scorpius core
- amdgpu: DMCUB updates for various ASICs
- qcom: add ADSP firmware for hawi platform
- powervr: add firmware for Imagination Technologies BXM-4-64 GPU
- qcom: Update DSP firmware for sa8775p platform
- xe: Release GuC firmware for NVL-S
- cirrus: cs35l56: Update firmware for the ASUS UX5406SA
- qcom: vpu: add Gen2 firmware binary for Purwa
- cirrus: cs42l45: Update CS42L45 SDCA codec firmware for Dell laptops
- QCA: Add Bluetooth firmware for WCN6855 ROM 1.0
- iwlwifi: add Bz/Sc/Hr/Gf FW for core24.60-33 release
- iwlwifi: update ty/So/Ma/cc/Qu/QuZ firmwares for core24.60-33 release
- cirrus: cs35l56: Add firmware for Cirrus Amps for a few Dell laptops
- ueagle-atm: sadly drop unlicensed files
- qcom: sync audioreach firmwares from v1.0.4 build
- QCA: Update Bluetooth QCA6698 firmware to 2.1.2-00072
- amdgpu: DMCUB updates for various ASICs
- tas2781: Add firmware for new HP projects
- rtw89: 8852a: add TX power track R34
- Update AMD SEV firmware

* Tue Jun 23 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260622-1
- Update to 20260622
- Update LICENSE locations
- Move Intel XE firmware to intel-gpu subpackage
- nxp: add firmware for IW61x WiFi device
- mediatek MT7922: update bluetooth firmware to 20260605203811
- mediatek MT7925: update bluetooth firmware to 20260605184935
- update firmware for MT7922/MT7925 WiFi device
- amdgpu: DMCUB updates for various ASICs
- qcom: add LPAICP/qdsp6sw firmware for shikra platform
- update firmware for MT7986/MT7981/MT7996/MT7992/MT7990
- qcom: Update ADSP firmware for Kaanapali platform
- qcom: update CDSP/ADSP firmware for glymur platform
- QCA: Add bluetooth firmware nvm files for USI/NFA725B
- Add firmware file for Intel BlazarIW
- Update firmware file for Intel BlazarI/BlazarU/Scorpius core
- qcom: update ADSP firmware for qcs615 platform
- cirrus: cs42l45: Update CS42L45 SDCA codec firmware for Dell laptops
- rtl_bt: Update RTL8852A BT USB firmware to 0x244F_91B6
- realtek: rt1321: Update the patch code to v1.10
- amdgpu: DMCUB updates for various ASICs
- QCA: Update Bluetooth WCN3950 firmware 1.3.0-00108 to 1.3.0-00184
- qcom: update CDSP firmware for shikra platform
- qcom: Update ADSP firmware for Glymur platform
- Remove a number of firmwares with unknown licenses
- LICENSES: update GPL-2.0 text and references
- LICENSES: rename GPL-3 to GPL-3.0-only
- LICENSES: rename Apache-2 to Apache-2.0
- Move firmware licenses to a LICENSES/ directory
- qcom: update ADSP firmware for sm8750 platform
- QCA: Update Bluetooth WCN6856 firmware 2.1.0-00666 to 2.1.0-00669
- qcom: Update DSP firmware for sa8775p/qcs8300 platform
- amdgpu: Update DMCUB fw for DCN314
- amdgpu: revert yellow carp/vangogh/sienna cichlid/navy flounder/dimgrey cavefish/beige_goby VCN firmware
- qcom: update CDSP firmware for x1e80100 platform
- cirrus: cs35l56: Add firmware for Cirrus Amps for a Dell laptop
- Add RCA firmware files for tas257x projects
- intel_vpu: Update NPU firmware
- cirrus: cs35l63: Add Cirrus CS35L63 firmware mappings for various Dell laptops
- cirrus: cs35l56: Add/Update firmware for Cirrus Amps for a couple of Lenovo laptops
- QCA: Add BCS calibration binary for QCC2072
- QCA: Update Bluetooth firmware for QCC2072 UART interface
- amdgpu: DMCUB updates for various ASICs
- rtl_nic: add firmware rtl8261c.bin for RTL8261c
- cirrus: cs35l56: Add Cirrus CS35L56 firmware mappings for two Dell laptops
- i915: Xe3LPD DMC v2.36/Xe3LPD_3002 DMC v2.31/Xe3p_LPD DMC v2.37
- cirrus: cs35l56: Add firmware for Cirrus Amps for some Lenovo laptops
- cirrus: cs42l45: Add/Update CS42L45 SDCA codec firmware for Lenovo laptops
- qcom: Add gpu firmwares for Shikra chipset
- cirrus: cs35l56: Update firmware for Cirrus Amps for some Dell laptops
- rtw89: 8852b: update fw to v0.29.29.18
- rtw89: 8852bt: update fw to v0.29.122.2
- amdgpu: Update gc 11.0.1 microcode

* Tue May 19 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260519-1
- Update to 20260519
- ASoC: tas2783: Add Firmware files for tas2783A projects
- add firmware for MT7927 WiFi device
- Add HP ISH firmware for Intel Panther Lake systems
- ti: Add PCM6240 firmware with multiple audio profiles support
- qcom: add CDSP firmware for shikra platform
- amdgpu: updates for various ASICs
- qcom: update ADSP firmware for x1e80100 platform
- qcom: Add cdsp1r.jsn for sa8775p platform
- Add firmware for Lontium LT9611C
- xe: Update GUC to v70.65.0 for LNL, BMG, PTL
- rtl_bt: Add missing rtl8761a_config.bin for RTL8761AU
- Add Dell ISH firmware 581.7783.0 for Intel Panther Lake systems.
- qcom: update ADSP firmware for x1e80100 platform
- linux-firmware:Add firmware for Lontium LT7911EXC bridge
- qcom/x1e80100/dell: mark that qcom/NOTICE.txt is applicable too
- qcom: Update CDSP firmware for Kaanapali platform
- qcom: vpu: add Gen2 firmware binary for Agatti
- amdgpu: DMCUB updates for various ASICs
- Add firmware file for Intel BlazarIGfp2/BlazarIW/ScorpiusGfp2
- Update firmware file for Intel BlazarI/BlazarU/BlazarU-HrPGfP/Scorpius core
- qcom: Update ADSP firmware for Glymur platform
- mediatek MT7925: update bluetooth firmware to 20260414153243
- update firmware for MT7925 WiFi device
- Revert "Update firmware file for Intel Quasar core"
- qcom: Add gpdspr.jsn for qcs8300 platform
- ath12k: QCC2072 hw1.0: add to WLAN.COL.1.0.c2-00074-QCACOLSWPL_V1_TO_SILICONZ-1
- ath12k: QCC2072 hw1.0: add board-2.bin
- ath12k: IPQ5424 hw1.0: add to WLAN.WBE.1.6-01275-QCAHKSWPL_SILICONZ-1
- ath12k: IPQ5424 hw1.0: add board-2.bin
- qcom: Update ADSP firmware for Kaanapali platform
- cirrus: cs35l56: Add firmware for Cirrus Amps for some Lenovo laptops (17aa235c 17aa235d)
- QCA: Update Bluetooth WCN6856 firmware 2.1.0-00665 to 2.1.0-00666
- amdgpu: DMCUB updates for DCN36
- Update AMD cpu microcode
- powervr: update Imagination Rogue firmware images
- qcom: Update ADSP firmware for Kaanapali platform
- i915: Xe3LPD DMC v2.34
- i915: Xe3LPD_3002 DMC v2.29
- qcom: Update ADSP firmware for QCM6490 platform
- firmware/amdgpu: Update DMCUB fw to Release 0.1.55.0
- mediatek: vpu: drop old sym link

* Sat Apr 11 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260410-1
- Update to 20260410
- amdgpu: Revert Yellow Carp DMUB fw to 0x4000045
- qcom: sync audioreach firmwares from v1.0.3 build
- intel_vpu: Update NPU firmware
- Revert "rtl_bt: Update RTL8822C BT USB and UART firmware to 0x0673"
- nvidia: add acr/bl symlink for booting GSP-RM on GA100
- qcom: add QUPv3 firmware for shikra
- xe: Update GUC to v70.60.0 for LNL, BMG, PTL
- qcom: update ADSP firmware for sm8750 platform
- qcom: update CDSP firmware for glymur platform
- cirrus: cs35l41: Add support for new HP laptops
- cirrus: cs35l41: Add support for new ASUS laptops
- cirrus: cs35l41: Add support for ASUS GZ302EAC and add 15.5dB bincfg
- qcom: vpu: add video firmware for SM8450
- cirrus: cs35l56: Add firmware for Cirrus Amps for some ASUS laptops
- cirrus: cs35l56: Add firmware for Cirrus Amps for some Lenovo laptops
- iwlwifi: add Bz/Sc/Hr/Gf FW for core103-40 release
- iwlwifi: update ty/So/Ma firmwares for core103-40 release
- amdgpu: DMCUB updates for various ASICs
- xe: Update PTL GSC to v105.0.2.1397
- add firmware for Moxa mux50u devices
- rtl_bt: Update RTL8852B BT USB FW to 0x127C_FD78
- ath11k: WCN6855 hw2.0@nfa765: update to WLAN.HSP.1.1-04866.5-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- ath11k: QCA6698AQ hw2.1: update to WLAN.HSP.1.1-04866.5-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- update firmware for qat_4xxx/qat_402xx/qat_420xx devices
- update firmware for an8811hb 2.5G ethernet phy
- qcom: Add FW blobs for DELL XPS13 9345
- amdgpu: DMCUB updates for various ASICs
- cirrus: cs35l63: Update firmware for Cirrus Amps for some Dell laptops
- cirrus: cs35l63: Fix Cirrus Amp firmware links for some Dell laptops
- Add firmware file for Intel BlazarIW/BlazarIGfp2
- iwlwifi: add Bz/Wh FW for core102-56 release
- ath12k: WCN7850 hw2.0: update to WLAN.HMT.1.1.c7-00108-QCAHMTSWPL_V1.0_V2.0_SILICONZ_UPSTREAM-3
- mediatek MT7921: update bluetooth firmware to 20260224111243
- mediatek MT7920: update bluetooth firmware to 20260224111231
- Add LENOVO ISH firmware v5.8.1.7720 for X1 Carbon (Gen 14) and X1 2-in-1 (Gen 11)
- Add ISH firmware file for Intel Wildcat Lake platform
- Update firmware for MT7920/MT7921 WiFi device
- Intel Bluetooth: Update firmware file for Intel Bluetooth AX201
- Add firmware file for Intel ScorpiusGfp2 core
- iwlwifi: Update firmware file for Intel Quasar/Scorpius/BlazarIGfP/BlazarI/BlazarU-HrPGfP/BlazarU core
- intel_vpu: Update NPU firmware
- amdgpu: DMCUB updates for various ASICs
- qcom: add QUPv3 firmware for QCS615 platform
- Add LENOVO ISH firmware v5.8.0.7720 for X9-15 2025

* Tue Mar 10 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260309-1
- Update to 20260309
- mediatek MT7922: update bluetooth firmware to 20260224103448
- update firmware for MT7922 WiFi device
- cirrus: cs42l45: Add CS42L45 SDCA codec firmware for Dell laptops
- cirrus: cs35l63: Add firmware for Cirrus CS35L63 for various Dell laptops
- Remove duplicate fw and Rename Lenovo ISH LNLM firmware files accordingly
- amdgpu: updates for various GPUs/ASICs
- Add firmware file for Intel BlazarIGfp2 core
- QCA: Update Bluetooth QCA6698 firmware to 2.1.2-00069
- qcom: Update CDSP firmware for QCM6490 platform
- add firmware for Lontium LT8713SX DP hub
- qcom: sync audioreach firmwares from v1.0.2 build
- qcom: update ADSP, CDSP firmware for sm8750  platform
- qcom: update ADSP dtb.mbn for glymur platform
- qca: Update Bluetooth WCN6750 1.1.3-00105 firmware to 1.1.3-00106
- QCA: Update Bluetooth WCN6856 firmware 2.1.0-00659 to 2.1.0-00665
- Renaming the file back for HP EliteBook X Flip G1i
- amdnpu: Restore old NPU firmware for compatibility
- cirrus: cs42l45: Add CS42L45 SDCA codec firmware for Dell laptops
- lenovo: remove obsolete ish_lnlm_53c4ffad_2a17559f.bin firmware
- update firmware for MT7902 BT device
- update firmware for MT7902 WiFi device

* Sun Feb 22 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260221-1
- Update to 20260221
- qcom: vpu: fix SC7280 VPU Gen2 firmware and add compatibility symlink
- amdgpu: DMCUB updates for various ASICs
- qcom: Update DSP firmware for qcs8300 platform
- cirrus: cs35l41: Add Firmware for ASUS Zenbook Laptop using CS35L41 HDA
- qcom: Update DSP firmware for sa8775p platform
- rtw89: 8851b: add format-1 for fw v0.29.41.5 with fw elements
- rtw89: 8852a: add format-1 for fw v0.13.36.2 with fw elements
- rtw89: 8852bt: add regd and diag_mac and update txpwr to R09
- rtw89: 8852b: update txpwr element to R43
- rtw89: 8852b: add format-2 with v0.29.29.15 and fw elements
- Revert "rtw89: 8852b: update fw to v0.29.128.0 with format suffix -2"
- xe: Update GUC to v70.58.0 for LNL, BMG, PTL
- ath11k: WCN6855 hw2.0: update board-2.bin
- ath11k: QCA6390 hw2.0: update board-2.bin
- qcom: Add gpu firmwares for Glymur chipset
- qcom: vpu: add video firmware for Glymur
- qcom: add QUPv3 firmware for x1e80100 platform
- Bluetooth: Add symbolic links for Intel Solar JfP2/1, Solar, Pulsar, AX201 firmware variants
- ath10k: WCN3990 hw1.0: update board-2.bin
- qcom: add ADSP, CDSP firmware for glymur platform
- ASoC: tas2783: Add Firmware files for tas2783A
- Update firmware file for Intel Solar core
- mediatek MT7921: update bluetooth firmware to 20251223091725
- rtl_bt: Update RTL8822C BT USB and UART firmware to 0x0673
- ath12k: WCN7850 hw2.0: update board-2.bin
- ath12k: QCN9274 hw2.0: update to WLAN.WBE.1.6-01243-QCAHKSWPL_SILICONZ-1
- ath11k: WCN6855 hw2.0: update board-2.bin
- ath11k: QCA6698AQ hw2.1: update board-2.bin
- Add firmware for airoha-npu-7581 driver used for MT7990 offloading
- Add Dell ISH firmware for Intel panther lake systems
- update Aeonsemi AS21x1x firmware to 1.9.1
- rtl_nic: add firmware rtl8125cp-1 for RTL8125cp
- ice: update DDP LAG package to 1.3.2.0
- cirrus: cs35l56: Add WHENCE links for 17aa233c spkid0 firmware
- rtw89: 8922a: update REGD R73-R08, txpwr R46 and element of diag MAC
- rtw89: 8852c: update REGD R73-R60, txpwr R82 and element of diag MAC
- Update firmware for NPU PHX, STX and STX HALO
- qcom: Update ADSP and add CDSP firmware for qcs6490-radxa-dragon-q6a
- qcom: Remove ADSP SensorPD json for Radxa Dragon Q6A
- intel/ish: Add Lenovo ISH firmware support for X1 and X9 systems
- cirrus: cs42l45: Add CS42L45 SDCA codec firmware for Lenovo laptops
- cirrus: cs42l45: Add CS42L45 SDCA codec firmware for Dell laptops
- cirrus: cs35l57 cs35l63: Add firmware for Cirrus Amps for some Lenovo laptops
- cirrus: cs35l56 cs35l57: Add and update firmware for some Dell laptops
- Intel IPU7: Update firmware binary for Panther Lake
- update firmware for MT7921 WiFi device
- Add firmware file for Intel ScorpiusGfp2 core
- Update firmware file for Intel Scorpius/BlazarIGfP/BlazarI/BlazarU-HrPGfP/BlazarU core
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x06EB_C65F
- Add firmware for airoha-npu-7583 driver
- iwlwifi: add Bz/Sc, Hr/Gf FW for core102-56 release
- iwlwifi: update ty/So/Ma firmwares for core102-56 release
- xe: Add GSC 105.0.2.1301 for PTL
- mediatek: rename MT8188 SCP firmware
- qcom: Update DSP firmware for QCM6490 platform
- qcom: sync audioreach firmwares from v1.0.1 build

* Sun Jan 11 2026 Peter Robinson <pbrobinson@fedoraproject.org> - 20260110-1
- Update to 20260110
- update firmware for MT7925 WiFi device
- mediatek MT7925: update bluetooth firmware to 20260106153314
- mediatek MT7920: update bluetooth firmware to 20260105151350
- mediatek MT7922: update bluetooth firmware to 20260106153735
- update firmware for MT7922 WiFi device
- Mellanox: Add new mlxsw_spectrum firmware xx.2016.3900
- amdgpu: Update dcn314, dcn315 firmware to 0.1.42.0
- qcom: Update DSP firmware for sa8775 platform
- QCA: Add Bluetooth firmware for QCC2072 uart interface
- i915: Xe3p_LPD DMC v2.33
- qcom: Update DSP firmware for qcs8300 platform
- update firmware for MT7920 WiFi device
- qcom: Update aic100 firmware files
- qca: Update Bluetooth WCN6750 1.1.3-00100 firmware to 1.1.3-00105
- firmware: Revert kernel_boot.elf due to license compliance issue
- add firmware for an8811hb 2.5G ethernet phy
- i915: Xe3LPD_3002 DMC v2.28
- i915: Xe3LPD DMC v2.33
- intel_vpu: Add firmware for 50xx NPUs and update older ones
- Update AMD SEV firmware
- amdgpu: DMCUB updates for various ASICs
- qcom: venus-5.4: fix ELF segment alignment to 4 bytes
- mediatek MT7925: update bluetooth firmware to 20251210093205
- update firmware for MT7925 WiFi device
- rcar_gen4_pcie: add firmware for Renesas R-Car Gen4 PCIe controller
- qcom: Update CDSP firmware for qcm6490 platform
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x488C_DB55
- iwlwifi: Add firmware file for Intel Scorpius core
- rtw89: 8852b: update fw to v0.29.29.15
- cirrus: cs35l41: Update firmware and tuning for various HP laptops
- cirrus: cs35l41: Add support for new HP Clipper laptop
- qcom: drop compatibility a640_zap.mdt symlink
- qcom: add version for a530v3_gpmu.fw2
- xe: Update GUC to v70.55.3 for BMG, PTL
- iwlwifi: add Bz/Sc FW for core101-82 release
- iwlwifi: Add Sc/Gf firmware for core101-82 release
- iwlwifi: update ty/So/Ma firmwares for core101-82 release
- iwlwifi: update cc/Qu/QuZ firmwares for core101-82 release
- amdgpu: DMCUB updates for various ASICs
- qcom: Add firmwares for sm8150/sm8450/sm8550/sm8650/sm8750 GPUs
- ath10k: WCN3990 hw1.0: update board-2.bin
- ath10k: QCA9888 hw2.0: update board-2.bin
- ath10k: QCA4019 hw1.0: update board-2.bin
- cirrus: cs35l41: Add support for new HP laptops
- Revert "amdgpu: update GC 11.5.0 firmware"
- Update amd-ucode copyright information
- Update AMD cpu microcode
- Update firmware file for Intel Scorpius core
- Update firmware file for Intel BlazarIGfP core
- Update firmware file for Intel BlazarI core
- Update firmware file for Intel BlazarU-HrPGfP core
- Update firmware file for Intel BlazarU core
- ath11k: QCA6698AQ hw2.1: update to WLAN.HSP.1.1-04866-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- ath11k: QCA2066 hw2.1: update board-2.bin
- qcom: update ADSP firmware for x1e80100 platform, change the license
- qcom: reorder ADSP, CDSP firmware entries for qcs8300 in WHENCE
- Reapply "amdgpu: update SMU 14.0.3 firmware"
- Revert "amdgpu: update SMU 14.0.3 firmware"
- Revert "amdgpu: update GC 10.3.6 firmware"
- Revert "amdgpu: update GC 11.5.1 firmware"
- update firmware for MT7925 WiFi device
- mediatek MT7925: update bluetooth firmware to 20251124093155
- intel_vpu: Update NPU firmware
- qcom: vpu: update video firmware binary for SM8250
- xe: Update GUC to v70.54.0 for BMG, PTL
