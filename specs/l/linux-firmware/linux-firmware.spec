# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

%global _firmwarepath	/usr/lib/firmware
%define _binaries_in_noarch_packages_terminate_build 0

Name:		linux-firmware
Version:	20260221
Release: 2%{?dist}
Summary:	Firmware files used by the Linux kernel
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND MIT AND LicenseRef-Callaway-Redistributable-no-modification-permitted
URL:		http://www.kernel.org/
BuildArch:	noarch

Source0:	https://www.kernel.org/pub/linux/kernel/firmware/%{name}-%{version}.tar.xz

BuildRequires:	make
BuildRequires:	git-core
BuildRequires:	python3
%if %{undefined rhel}
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
License:	GPL-1.0-or-later AND GPL-2.0-or-later AND MIT AND LicenseRef-Callaway-Redistributable-no-modification-permitted
%description whence
This package contains the WHENCE license file which documents the vendor license details.

# GPU firmwares
%package -n amd-gpu-firmware
Summary:	Firmware for AMD GPUs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n amd-gpu-firmware
Firmware for AMD amdgpu and radeon GPUs.

%package -n intel-gpu-firmware
Summary:	Firmware for Intel GPUs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-gpu-firmware
Firmware for Intel GPUs including GuC (Graphics Microcontroller), HuC (HEVC/H.265
Microcontroller) and DMC (Display Microcontroller) firmware for Skylake and later
platforms.

%package -n nvidia-gpu-firmware
Summary:	Firmware for NVIDIA GPUs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n nvidia-gpu-firmware
Firmware for NVIDIA GPUs.

# Microcode updates
%package -n amd-ucode-firmware
Summary:	Microcode updates for AMD CPUs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n amd-ucode-firmware
Microcode updates for AMD CPUs, AMD SEV and AMD TEE.

# WiFi/Bluetooth/WWAN firmwares
%package -n atheros-firmware
Summary:	Firmware for Qualcomm Atheros WiFi/Bluetooth adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n atheros-firmware
Firmware for Qualcomm Atheros ath6k/ath9k/ath10k/ath11k WiFi adapters.

%package -n brcmfmac-firmware
Summary:	Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n brcmfmac-firmware
Firmware for Broadcom/Cypress brcmfmac WiFi/Bluetooth adapters.

%package -n iwlegacy-firmware
Summary:	Firmware for Intel(R) Wireless WiFi Link 3945(A)BG and 4965AGN adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n iwlegacy-firmware
This package contains the firmware required by the iwlegacy driver
for Linux. This includes the 3945(A)BG and 4965AGN WiFi NICs. Usage
of the firmware is subject to the terms and conditions contained
inside the provided LICENSE file. Please read it carefully.

%package -n iwlwifi-dvm-firmware
Summary:	DVM Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n iwlwifi-dvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with DVM firmware support (CONFIG_IWLDVM=y/m). Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlwifi-mvm-firmware
Summary:	MVM Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
# Same hardware, newer firmware with a different driver, enables smooth migration
Requires:	iwlwifi-mld-firmware = %{version}-%{release}
%description -n iwlwifi-mvm-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with MVM firmware support (CONFIG_IWLMVM=y/m).  Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n iwlwifi-mld-firmware
Summary:	MLD Firmware for Intel(R) Wireless WiFi adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n iwlwifi-mld-firmware
This package contains the firmware required by the iwlwifi driver
for Linux built with MLD firmware support (CONFIG_IWLMLD=y/m).  Usage of
the firmware is subject to the terms and conditions contained inside the
provided LICENSE file. Please read it carefully.

%package -n libertas-firmware
Summary:	Firmware for Marvell Libertas SD/USB WiFi Network Adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n libertas-firmware
Firmware for the Marvell Libertas series of WiFi Network Adapters
Including the SD 8686/8787 and USB 8388/8388.

%package -n mt7xxx-firmware
Summary:	Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mt7xxx-firmware
Firmware for Mediatek 7600/7900 series WiFi/Bluetooth adapters

%package -n nxpwireless-firmware
Summary:	Firmware for NXP WiFi/Bluetooth/UWB adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n nxpwireless-firmware
Firmware for NXP WiFi/Bluetooth/UWB adapters.

%package -n realtek-firmware
Summary:	Firmware for Realtek WiFi/Bluetooth adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n realtek-firmware
Firmware for Realtek WiFi/Bluetooth adapters

%package -n qcom-wwan-firmware
Summary:	Firmware for Qualcomm Wireless WAN modems
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qcom-wwan-firmware
Firmware for Qualcomm Snapdragon X-series (SDX) wireless WAN modems used
across numerous WWAN cards from numerous vendors.

%package -n tiwilink-firmware
Summary:	Firmware for Texas Instruments WiFi/Bluetooth adapters
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n tiwilink-firmware
Firmware for Texas Instruments WiFi/Bluetooth adapters

# SMART NIC and network switch firmwares
%package -n liquidio-firmware
Summary:	Firmware for Cavium LiquidIO Intelligent Server Adapter
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n liquidio-firmware
Firmware for Cavium LiquidIO Intelligent Server Adapter

%package -n mlxsw_spectrum-firmware
Summary:	Firmware for Mellanox Spectrum 1/2/3 Switches
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mlxsw_spectrum-firmware
Firmware for Mellanox Spectrumi series 1/2/3 ethernet switches.

%package -n mrvlprestera-firmware
Summary:	Firmware for Marvell Prestera Switchdev/ASIC devices
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mrvlprestera-firmware
Firmware for Marvell Prestera Switchdev/ASIC devices

%package -n netronome-firmware
Summary:	Firmware for Netronome Smart NICs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n netronome-firmware
Firmware for Netronome Smart NICs

%package -n qcom-accel-firmware
Summary:	Firmware for Qualcomm Technologies data center / Open-vRAN Accelerators
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qcom-accel-firmware
Firmware for Qualcomm Technologies data center and Open-vRAN accelerators
including the X100 5G RAN Accelerator Card, the QRU100 5G RAN Platform
and the Cloud AI 100.

%package -n qed-firmware
Summary:	Firmware for Marvell FastLinQ adapters family
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n qed-firmware
Firmware for Marvell FastLinQ adapters family (QDE), this device
supports RoCE (RDMA over Converged Ethernet), iSCSI, iWARP, FCoE
and ethernet including SRIOV, DCB etc.

# Silicon Vendor specific
%package -n mediatek-firmware
Summary:	Firmware for Mediatek SoCs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n mediatek-firmware
Firmware for various compoents in Mediatek SoCs, in particular SCP.

%package -n qcom-firmware
Summary:	Firmware for Qualcomm SoCs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
Requires:	atheros-firmware = %{version}-%{release}
%description -n qcom-firmware
Firmware for various compoents in Qualcomm SoCs including Adreno GPUs,
Venus video encode/decode, Audio DSP, Compute DSP, modem, Sensor DSPs.

# Vision and ISP hardware
%package -n intel-vsc-firmware
Summary:	Firmware files for Intel Visual Sensing Controller (IVSC)
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-vsc-firmware
Firmware files for Intel Visual Sensing Controller (IVSC) for
Tiger Lake, Alder Lake and Raptor Lake SoCs and the IPU3/6 firmware.

# Sound codec hardware
%package -n cirrus-audio-firmware
Summary:	Firmware for Cirrus audio amplifiers and codecs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n cirrus-audio-firmware
Firmware for Cirrus audio amplifiers and codecs

%package -n intel-audio-firmware
Summary:	Firmware for Intel audio DSP amplifiers and codecs
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
Requires:	linux-firmware-whence = %{version}-%{release}
%description -n intel-audio-firmware
Firmware for Intel audio DSP amplifiers and codecs

# Random other hardware
%package -n dvb-firmware
Summary:	Firmware for various DVB broadcast receivers
License:	LicenseRef-Callaway-Redistributable-no-modification-permitted
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
mkdir -p %{buildroot}/%{_firmwarepath}
mkdir -p %{buildroot}/%{_firmwarepath}/updates

make DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} install-xz
%if %{undefined rhel}
make DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwarepath} dedup
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
	-i -e '/^intel\/ipu/d' \
	-i -e '/^intel\/ipu3/d' \
	-i -e '/^intel\/irci_irci/d' \
	-i -e '/^intel\/vsc/d' \
	-i -e '/^isdbt/d' \
	-i -e '/^iwlwifi/d' \
	-i -e '/^intel\/iwlwifi/d' \
	-i -e '/^nvidia\/a/d' \
	-i -e '/^nvidia\/g/d' \
	-i -e '/^nvidia\/tu/d' \
	-i -e '/^lgs8g75/d' \
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
%dir %{_firmwarepath}
%license LICENCE.* LICENSE.* GPL*

%files whence
%license WHENCE

# GPU firmwares
%files -n amd-gpu-firmware
%license LICENSE.radeon LICENSE.amdgpu LICENSE.amdnpu
%{_firmwarepath}/amdgpu/
%{_firmwarepath}/amdnpu/
%{_firmwarepath}/radeon/

%files -n intel-gpu-firmware
%license LICENSE.i915
%{_firmwarepath}/i915/

%files -n nvidia-gpu-firmware
%license LICENCE.nvidia
%dir %{_firmwarepath}/nvidia/
%{_firmwarepath}/nvidia/a*
%{_firmwarepath}/nvidia/g*
%{_firmwarepath}/nvidia/tu*

# Microcode updates
%files -n amd-ucode-firmware
%license LICENSE.amd-ucode
%{_firmwarepath}/amd/
%{_firmwarepath}/amdtee/
%{_firmwarepath}/amd-ucode/

# WiFi/Bluetooth firmwares
%files -n atheros-firmware
%license LICENCE.atheros_firmware
%license LICENSE.QualcommAtheros_ar3k
%license LICENSE.QualcommAtheros_ath10k
%license LICENCE.open-ath9k-htc-firmware
%license qca/NOTICE.txt
%{_firmwarepath}/ar3k/
%{_firmwarepath}/ath6k/
%{_firmwarepath}/ath9k_htc/
%{_firmwarepath}/ath10k/
%{_firmwarepath}/ath11k/
%{_firmwarepath}/ath12k/
%{_firmwarepath}/qca/

%files -n brcmfmac-firmware
%license LICENCE.broadcom_bcm43xx
%license LICENCE.cypress
%{_firmwarepath}/brcm/
%{_firmwarepath}/cypress/

%files -n iwlegacy-firmware
%license LICENCE.iwlwifi_firmware
%{_firmwarepath}/iwlwifi-3945-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-3945-*.ucode*
%{_firmwarepath}/iwlwifi-4965-*.ucode*
%{_firmwarepath}/intel/iwlwifi/iwlwifi-4965-*.ucode*

%files -n iwlwifi-dvm-firmware
%license LICENCE.iwlwifi_firmware
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
%license LICENCE.iwlwifi_firmware
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
%license LICENCE.iwlwifi_firmware
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

%files -n libertas-firmware
%license LICENCE.Marvell LICENCE.OLPC
%dir %{_firmwarepath}/libertas
%dir %{_firmwarepath}/mrvl
%{_firmwarepath}/libertas/*
%{_firmwarepath}/mrvl/sd8787*

%files -n mt7xxx-firmware
%license LICENCE.mediatek
%license LICENCE.ralink_a_mediatek_company_firmware
%dir %{_firmwarepath}/mediatek
%{_firmwarepath}/mediatek/mt76*
%{_firmwarepath}/mediatek/mt791*
%{_firmwarepath}/mediatek/mt7925/
%{_firmwarepath}/mediatek/mt7996/
%{_firmwarepath}/mediatek/BT*
%{_firmwarepath}/mediatek/WIFI*
%{_firmwarepath}/mt76*

%files -n nxpwireless-firmware
%license LICENSE.nxp
%dir %{_firmwarepath}/nxp
%{_firmwarepath}/nxp/*

%files -n qcom-wwan-firmware
%license LICENSE.qcom qcom/NOTICE.txt
%dir %{_firmwarepath}/qcom
%{_firmwarepath}/qcom/sdx*/

%files -n realtek-firmware
%license LICENCE.rtlwifi_firmware.txt
%{_firmwarepath}/rtl_bt/
%{_firmwarepath}/rtlwifi/
%{_firmwarepath}/rtw88/
%{_firmwarepath}/rtw89/

%files -n tiwilink-firmware
%license LICENCE.ti-connectivity
%dir %{_firmwarepath}/ti-connectivity/
%{_firmwarepath}/ti-connectivity/*

# SMART NIC and network switch firmwares
%files -n liquidio-firmware
%license LICENCE.cavium_liquidio
%dir %{_firmwarepath}/liquidio
%{_firmwarepath}/liquidio/*

%files -n mrvlprestera-firmware
%license LICENCE.Marvell
%dir %{_firmwarepath}/mrvl/prestera
%{_firmwarepath}/mrvl/prestera/*

%files -n mlxsw_spectrum-firmware
%dir %{_firmwarepath}/mellanox/
%{_firmwarepath}/mellanox/*

%files -n netronome-firmware
%license LICENCE.Netronome
%dir %{_firmwarepath}/netronome
%{_firmwarepath}/netronome/*

%files -n qcom-accel-firmware
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
%license LICENCE.mediatek
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
%license LICENSE.qcom LICENSE.qcom_yamato qcom/NOTICE.txt
%dir %{_firmwarepath}/qcom
%{_firmwarepath}/qcom/glymur/
%{_firmwarepath}/qcom/kaanapali/
%{_firmwarepath}/a300_p*
%{_firmwarepath}/qcom/*.fw*
%{_firmwarepath}/qcom/*.bin*
%{_firmwarepath}/qcom/*.m*
%{_firmwarepath}/qcom/apq*/
%{_firmwarepath}/qcom/qcm*/
%{_firmwarepath}/qcom/qcs*/
%{_firmwarepath}/qcom/qrb*/
%{_firmwarepath}/qcom/sa*/
%{_firmwarepath}/qcom/sc*/
%{_firmwarepath}/qcom/sdm*/
%{_firmwarepath}/qcom/sm*/
%{_firmwarepath}/qcom/venus-*/
%{_firmwarepath}/qcom/vpu*/
%{_firmwarepath}/qcom/x1*/

# Vision and ISP hardware
%files -n intel-vsc-firmware
%license LICENSE.ivsc
%dir %{_firmwarepath}/intel/ipu/
%dir %{_firmwarepath}/intel/vsc/
%{_firmwarepath}/intel/ipu3-fw.bin*
%{_firmwarepath}/intel/irci_irci_ecr-master_20161208_0213_20170112_1500.bin*
%{_firmwarepath}/intel/ipu/*
%{_firmwarepath}/intel/vsc/*

# Sound codec hardware
%files -n cirrus-audio-firmware
%license LICENSE.cirrus
%dir %{_firmwarepath}/cirrus
%{_firmwarepath}/cirrus/*

%files -n intel-audio-firmware
%license LICENCE.adsp_sst LICENCE.IntcSST2
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
%license LICENSE.dib0700 LICENCE.it913x LICENCE.siano
%license LICENCE.xc4000 LICENCE.xc5000 LICENCE.xc5000c
%dir %{_firmwarepath}/av7110/
%{_firmwarepath}/av7110/*
%{_firmwarepath}/as102_data*
%{_firmwarepath}/cmmb*
%{_firmwarepath}/dvb*
%{_firmwarepath}/isdbt*
%{_firmwarepath}/lgs8g75*
%{_firmwarepath}/sms1xxx*
%{_firmwarepath}/tdmb*
%{_firmwarepath}/v4l-cx2*

%changelog
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

* Tue Nov 25 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20251125-1
- Update to 20251125
- Revert "amdgpu: update GC 11.0.1 firmware"
- QCA: Add Bluetooth firmware for WCN685x uart interface
- qcom: Add ADSP firmware for qcs6490-thundercomm-rubikpi3
- qcom: venus-5.4: update firmware binary for v5.4
- qcom: venus-5.4: remove unused firmware file
- iwlwifi: add Sc/Wh FW for core98-181 release
- amdgpu: DMCUB updates for various ASICs
- rtl_bt: Update RTL8852B BT USB FW to 0x42D3_4E04
- ASoC: tas2781: Add more symbol links on SPI devices
- amdgpu: update numerous firmware
- amdgpu: add vce1 firmware
- mediatek MT7922: update bluetooth firmware to 20251118163447
- update firmware for MT7922 WiFi device
- qcom: update ADSP, CDSP firmware for kaanapali platform, change the license
- qcom: add ADSP, CDSP firmware for sm8750 platform
- rtl_nic: add firmware rtl9151a-1
- qcom: Update aic100 firmware files
- mt76: add firmware for MT7990
- mt76: update firmware for MT7992/MT7996
- cirrus: cs35l57: Add firmware for a few Dell products
- cirrus: cs42l45: Add firmware for Cirrus Logic CS42L45 SDCA codec
- qcom: Add sdx35 Foxconn vendor firmware image file
- Update AMD cpu microcode

* Wed Nov 12 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20251111-1
- Update to 20251111
- rtl_bt: Update RTL8922A BT USB firmware to 0x41C0_C905
- add firmware for mt7987 internal 2.5G ethernet phy
- rtw88: 8822b: Update firmware to v30.20.0
- rtl_nic: add firmware rtl8125k-1
- ASoC: tas2781: Update dsp firmware for HP and ASUS projects
- amdgpu: DMCUB updates for various ASICs
- qcom: add SOCCP firmware for kaanapali platform
- xe: Update GUC to v70.53.0 for BMG, LNL, PTL
- i915: Update GUC to v70.53.0 for DG2, MTL
- rtw89: 8851b: update fw to v0.29.41.5
- rtw89: 8852b: update fw to v0.29.128.0 with format suffix -2
- rtw89: 8852b: update fw to v0.29.29.14
- rtw89: 8852bt: update fw to v0.29.127.0 with format suffix -1
- Update firmware file for Intel BlazarI/BlazarU core
- Create audio folder in ti folder, and move all the audio firmwares into it
- amdgpu: DMCUB updates for various ASICs
- Update AMD cpu microcode
- mediatek MT7925: update bluetooth firmware to 20251015213201
- rtl_bt: Add firmware and config files for RTL8761CUV
- Update AMD cpu microcode
- qcom: add ADSP firmware for kaanapali platform
- amdgpu: DMCUB updates for various ASICs
- mediatek MT7920: update bluetooth firmware to 20251020151255
- update firmware for MT7920/MT7922/MT7925 WiFi device
- amd-ucode: Fix minimum revisions in README
- cirrus: cs35l41: Rename various Asus Laptop firmware files to not have Speaker ID
- mediatek MT7922: update bluetooth firmware to 20251020143443

* Tue Oct 21 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20251021-1
- Update to 20251021
- Revert "update firmware for MT7922 WiFi device"
- QCA: Update Bluetooth WCN6856 firmware 2.1.0-00653 to 2.1.0-00659
- iwlwifi: add Bz/Fm and gl FW for core98-161 release
- iwlwifi: update Bz/Hr and Bz/Gf firmwares for core98-161 release
- iwlwifi: update ty/So/Ma firmwares for core98-161 release
- iwlwifi: update cc/Qu/QuZ firmwares for core98-161 release
- intel: qat: Fix missing link
- amdgpu: DMCUB updates for various ASICs
- nvidia: add generic bootloader for GSP-enabled systems
- qcom: sync audioreach firmwares from v1.0.0 build
- qcom: vpu: rename firmware binaries
- Intel IPU7: Update product signed firmware binary
- i915: DMC Xe2LPD v2.29 / Xe3LPD v2.32 / Xe3LPD_3002 v2.27
- WHENCE: nvidia: rearrange GSP-RM firmware lines
- Add ISH firmware file for Intel Pather Lake platform
- Update firmware file for Intel Magnetar/BlazarU/BlazarI core

* Sat Oct 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20251011-1
- Update to 20251011
- qcom: add CDSP firmware for kaanapali platform
- qcom: add version for A650 GMU firmware
- qca: Update Bluetooth WCN6750 1.1.3-00091 firmware to 1.1.3-00100
- qcom: Add firmwares for Kaanapali GPU
- qcom: Update A623 GMU fw
- qcom: Fix QCS615 chipset's GPU secure fw
- qcom: Update DSP firmware for sa8775p platform
- amdgpu: DMCUB updates for various ASICs
- WHENCE: remove link for Kaanapali video firmware
- intel_vpu: Update NPU firmware
- Add Dell ISH firmware for Intel Lunar Lake systems
- Update VCN for Navi1x, Green Sardine and Renoir
- qcom: vpu: update video firmware binary for SM8550
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x3BAC_ADBA
- qcom: vpu: add video firmware for Kaanapali
- qcom: Update DSP firmware for qcs8300 platform.
- qcom: Add Audio topology for HAMOA-EVK
- intel/ish:Add ISH firmware file for Intel Lunar Lake platform
- mediatek: update firmware version info for MT7986/81/16
- ql2500_fw: update ISP25xx Firmware
- qcom: Update aic100 firmware files
- qcom: Add audio topology and ADSP firmware for qcs6490-radxa-dragon-q6a
- mediatek: mtk_wed: drop links for mt7988
- qcom: Update DSP firmware for qcs8300 platform.
- powervr: update firmware for Imagination Technologies BXS-4-64 GPU
- qcom: Update DSP firmware for sa8775p platform.
- ath12k: WCN7850 hw2.0: update board-2.bin
- qcom: move LEMANS EVK firmware to correct location

* Fri Sep 26 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250917-2
- Adjust various mediatek firmware packaging

* Wed Sep 24 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250917-1
- Update to 20250917
- first phase split out newer iwlwifi firmware for newer driver
- handle move of iwlwifi firmware to subdir (FINALLY!!)
- amdgpu: lots of firmware (131!) updates
- update firmware for en8811h 2.5G ethernet phy
- intel/ish: Add firmware for LENOVO THINKPAD X1 2-in-1 Gen 10
- mediatek MT7922: update bluetooth firmware to 20250903123504
- update firmware for MT7922 WiFi device
- qcom: move Monaco EVK topology from qcs8275 to qcs8300 subdir
- qcom: Add Audio topology for MONACO-EVK
- qcom: add CDSP firmware for qcs615 platform
- qcom: Add Audio topology for LEMANS-EVK
- ath12k: WCN7850 hw2.0@ncm865: add to WLAN.IOE_HMT.1.1-00018-QCAHMTSWPL_V1.0_V2.0_SILICONZ-1
- update firmware for MT7925 WiFi device
- mediatek MT7925: update bluetooth firmware to 20250825220109
- qcom: vpu: update firmware binaries to fix encoder drain handling
- xe: Update GUC to v70.49.4 for BMG, LNL, PTL
- i915: Update GUC to v70.49.4 for ADL-P, DG1, DG2, MTL, TGL
- qcom: add ADSP firmware for qcs615 platform
- rtl_bt: Update RTL8822C BT USB firmware to 0x2B66_D962
- iwlwifi: add Bz-HR FW for core90-93 release
- Fix link entry for qat_895xcc.bin
- Move QAT firmware to intel/ subdirectory
- Move all iwlwifi top level files to intel/ directory
- Revert "intel/ish: Add firmware for LENOVO THINKPAD X1 2-in-1 Gen 10"
- ath11k: Support WCN6855 hw2.1 with NFA firmware variant
- intel_vpu: Update NPU firmware
- intel/ish: Add firmware for LENOVO THINKPAD X1 2-in-1 Gen 10
- cirrus: cs35l56: Update firmware for Cirrus Amps for some Lenovo laptops
- ath11k: WCN6855 hw2.0@nfa765: add to WLAN.HSP.1.1-04685-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- cirrus: cs35l56: Add firmware for Cirrus Amps for some Lenovo laptops
- qcom: Add firmware binary for SM8650.
- Link rtl8723b_config.bin to rtl8723bs
- rtw89: 8922a: update fw to v0.35.80.3
- rtw89: 8852c: update fw to v0.27.129.4
- rtw89: 8852c: update fw to v0.27.129.3
- qcom: add CDSP firmware for x1e80100 platform
- iwlwifi: add Bz/gl FW for core97-84 release
- iwlwifi: update ty/So/Ma firmwares for core97-84 release
- iwlwifi: update cc/Qu/QuZ firmwares for core97-84 release
- realtek: rt1321: Add patch firmware of MCU
- mediatek: Add MT8189 SCP firmware
- panthor: Add firmware for more Mali GPUs
- qca: Update Bluetooth WCN6750 1.1.3-00069 firmware to 1.1.3-00091

* Sun Aug 10 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250808-1
- Update to 20250808
- Split out QCom Datacenter/Open-vRAN accelerator firmware
- Split out QCom 4G/5G WWan Adapters
- qcom: Add QDSP firmware file for Qualcomm QDU100 device.
- ath12k: WCN7850 hw2.0: update to WLAN.HMT.1.1.c5-00302-QCAHMTSWPL_V1.0_V2.0_SILICONZ-1.115823.3
- ath12k: QCN9274 hw2.0: update to WLAN.WBE.1.5-01651-QCAHKSWPL_SILICONZ-1
- ath11k: WCN6855 hw2.0: update board-2.bin
- ath11k: QCA6698AQ hw2.1: update to WLAN.HSP.1.1-04650-QCAHSPSWPL_V1_V2_SILICONZ_IOE-2
- ath11k: QCA2066 hw2.1: update to WLAN.HSP.1.1-03926.13-QCAHSPSWPL_V2_SILICONZ_CE-2.52297.9
- ath11k: QCA2066 hw2.1: update board-2.bin
- qcom: Update xbl_config firmware file.
- qcom: Add QDU100 firmware image files required for booting.
- Add firmware for airoha-npu driver
- update firmware for MT7925 WiFi device
- mediatek MT7925: update bluetooth firmware to 20250721233113
- qcom: Update DSP firmware for qcm6490 platform
- qcom: update Venus firmware file for v6.0
- i915: Xe3LPD DMC v2.29
- Update AMD cpu microcode
- qcom: Add QCS6490 symlink for QUPv3 firmware
- qcom: Add firmware binary for SM8750.
- amdgpu: various firmware updates
- cirrus: cs35l41/cs35l56: Update Firmwares for Dell/ASUS laptops
- qcom: Add Audio topology for QCS6490 RB3Gen2
- intel_vpu: Update NPU firmware
- rtw89: Updated firmware for 8852b/8852bt/8922a/8852c/8922a
- qcom: Update gpu firmwares of QCS615 chipset
- Update firmware file for Intel WiFi Solar/BlazarU/BlazarI core

* Tue Jul 08 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250708-1
- Update to 20250708
- Drop incorrect nvidia ghost entries
- xe: Add fan_control v203.0.0.0 for BMG
- Update AMD cpu microcode
- amdgpu: Add DCN 3.6/PSP 14.0.5/SDMA 6.1.3/GC 11.5.3
- mediatek MT7921: update bluetooth firmware to 20250625154126
- qcom/adreno: document firmware revisions
- qcom/adreno: move A610 and A702 ZAP files to Adreno driver section
- qcom: Add sdx61 Foxconn vendor firmware image file
- Revert "Update firmware file for Intel Pulsar core"
- xe: First GuC/HuC release for Pantherlake
- update firmware for MT7921 WiFi device
- rtw89: 8922a: update fw to v0.35.80.0
- rtw89: 8852c: update fw to v0.27.129.1
- rtw89: 8852c: update fw to v0.27.128.0

* Fri Jun 27 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250627-1
- Update to 20250627
- amdgpu: A metric ton of fixes for their GPU firmware
- WHENCE: various updates
- qcom: update firmware binary for SM8550
- qcom: venus-5.4: add the firmware binary for qcs615
- brcm: Fix symlinks for Khadas VIM SDIO wifi config
- mediatek: Update mt8186 SCP firmware
- qcom: add gpu firmwares for X1P42100 chipset

* Fri Jun 13 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250613-1
- Update to 20250613
- Upgrade path for nvidia firmware changes (thanks Denys Vlasenko)
- QCA: Update WCN785x btusb firmware to 2.0.0-00799-5
- rtl_nic: update firmware of RTL8153A
- qcom: sc8280xp: Updated power FW for X13s
- update firmware for MT7986/MT7981/MT7916
- cirrus: cs35l41: Add Firmware for ASUS NUC using CS35L41
- Revert "iwlwifi: add Bz/gl FW for core96-76 release"
- amdgpu: DMCUB updates for various ASICs
- mediatek MT7922: update bluetooth firmware to 20250523103438
- mediatek MT7921: update bluetooth firmware to 20250523111333
- update firmware for MT7921/MT7922 WiFi device
- xe: Update GUC to v70.45.2 for BMG, LNL
- i915: Update GUC to v70.45.2 for DG2
- xe: Update LNL GSC to v104.0.5.1429
- amdgpu: DMCUB updates for various ASICs
- qcom: add QUPv3 firmware for QCS8300 platform
- Intel IPU7: Add firmware binary files
- ice: update wireless_edge package to 1.3.23.0
- ice: update comms package to 1.3.55.0
- ice: update package to 1.3.43.0
- Update firmware for Intel Pulsar/BlazarI/Quasar/Solar/Magnetar/BlazarU core
- iwlwifi: add Bz/gl/ty/So/Ma/cc/Qu/QuZ FW for core96-76 release
- iwlwifi: update firmwares for 8000 series
- iwlwifi: update 7265D firmware
- mediatek MT7925: update bluetooth firmware to 20250526153203
- update firmware for MT7925 WiFi device
- qcom: sc8280xp: FW blob updates for X13s
- brcm: Add symlinks for Khadas VIM SDIO wifi config to AW-CM256SM.txt
- ath12k: WCN7850 hw2.0: update to WLAN.HMT.1.1.c5-00284.1-QCAHMTSWPL_V1.0_V2.0_SILICONZ-3
- cirrus: cs35l41: Fix firmware links for several ASUS laptops
- cirrus: cs35l41: Add Firmware for various HP Agusta Laptops using CS35L41 HDA
- Adjust QUPv3 driver name
- cnm: Add Chips&Media wave633c firmware for NXP i.MX9
- qcom: add QUPv3 firmware for QCM6490 platform
- mediatek: Add mt8196 VCP firmware
- cirrus: cs35l41: Add Firmware for various ACER Laptops using CS35L41 HDA
- nvidia: add GSP-RM version 570.144 firmware images
- amdgpu: DMCUB updates for various ASICs
- powervr: add firmware for Imagination Technologies BXS-4-64 GPU
- rtl_bt: Update RTL8822C BT USB and UART firmware to 0x7C20
- brcmfmac: Add a couple of NanoPi devices
- rtl_nic: add firmware rtl8127a-1
- cnm: update chips&media wave521c firmware.
- intel_vpu: Update NPU firmware
- intel: avs: Update topology file for Digital Microphone Array
- amdgpu: updates for dcn 3.20 and dcn 4.01 firmware to 0.1.10.0

* Fri May 09 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250509-1
- Update to 20250509
- Amphion: Update vpu firmware
- amd_pmf: Update AMD PMF TA Firmware to v3.1
- amdgpu: update dcn 4.01 firmware to 0.1.8.0
- qcom: Add link for SM8350 GPU firmware
- cirrus: cs35l56: Add/update firmware for Cirrus Amps for some ASUS/Lenovo laptops
- update firmware for MT7925 WiFi device
- mediatek MT7925: update bluetooth firmware to 20250425073330
- rtw89: 8852c: add tables for dynamic antenna TXPWR
- rtw89: 8922a: update fw to v0.35.71.0
- brcm: Add NVRAM file for Radxa Rock Pi X mini PC
- i915: Update Xe3LPD DMC to v2.23
- rtl_bt: Update RTL8852B BT USB FW to 0x098B_154B
- ath11k: WCN6855 hw2.0: update board-2.bin
- ath11k: IPQ5018 hw1.0: update to WLAN.HK.2.6.0.1-01300-QCAHKSWPL_SILICONZ-1
- ath12k: WCN7850 hw2.0: update to WLAN.HMT.1.1.c5-00284-QCAHMTSWPL_V1.0_V2.0_SILICONZ-3
- ath12k: QCN9274 hw2.0: update board-2.bin
- qcom: vpu: update video firmware binary for SA8775p
- iwlwifi: add/update firmwares to core95-82 release
- iwlwifi: add Bz-hr FW for core93-123 release
- qcom: add QUPv3 firmware for QCS9100 platform
- ASoC: tas2781: Swap channel for SPI projects.
- bmi260: Add BMI260 IMU initial configuration data file
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x1881_BA06
- rtw89: 8922a: update element RF TXPWR to R40
- rtw89: 8852c: update element RF TXPWR to R78
- rtw89: 8852c: add fw v0.27.125.0 with format version 2
- Revert "rtw89: 8852c: update fw to v0.27.125.0"
- qcom: vpu: add video firmware binary for qcm6490
- amdgpu: many firmware updates
- intel: ish: Update license file for ISH
- intel: avs: Update topology file for I2S for many codecs
- intel: avs: Update topology file for HDMI/HDAudio codecs
- intel: avs: Update topology file for Digital Microphone Array
- xe: Update GUC to v70.44.1 for BMG and LNL
- i915: Update GUC to v70.44.1 for i915 platforms

* Thu Apr 10 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250410-1
- Update to 20250410
- qcom:x1e80100: Iris Support for Lenovo T14s G6 Qualcomm platform
- qcom:x1e80100: Support for Lenovo Yoga Slim 7 Snapdragon platform
- Mellanox: Add new mlxsw_spectrum firmware xx.2014.4012
- add firmware for Aeonsemi AS21x1x 1G/2.5G/5G/10G Ethernet Phy
- QCA: Add 8 bluetooth nvm files for WCN785x btusb
- QCA: Update WCN785x btusb firmware to 2.0.0-00790-3
- qcom: update firmware binary for SM8250
- mediatek: Add new mt8188/mt8195 SOF firmware
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x17E9_16ED
- intel_vpu: Update NPU firmware
- cirrus: cs35l56: Correct filenames of SSID 103c8e1b and 103c8e1c
- rtl_bt: Update RTL8852BT/RTL8852BE-VT BT USB FW to 0x0471_70A6
- amdgpu: update dcn 3.5 and dcn 3.5.1 firmware to 9.0.27.0
- amdgpu: update dcn 3.1.4 firmware to 8.0.78.0
- amdgpu: update dcn 4.01 firmware to 0.1.3.0
- amdgpu: update dcn 3.5 firmware to 0.1.0.0
- cirrus: cs35l41: Add Firmware for various HP Laptops using CS35L41 HDA
- cirrus: Add cs35l56 firmware symlinks for Asus UM5606KA
- qcom: Add DSP firmware for QCS8300 platform
- mediatek: Add MT8188 SCP firmware
- Update firmware file for Intel BlazarI core
- qcom: Add Audio firmware for Lenovo Slim 7x/T14s
- amdgpu: DMCUB updates for various ASICs
- rtw88: Add firmware v33.6.0 for RTL8814AE/RTL8814AU
- rtw89: 8922a: update fw to v0.35.64.0
- rtw89: 8852c: update fw to v0.27.125.0
- iwlwifi: add Bz/gl FW for core94-91 release
- iwlwifi: update ty/So/Ma/cc/Qu/QuZ firmwares for core94-91 release

* Tue Mar 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250311-1
- Update to 20250311
- amdgpu: many firmware updates
- qcom: Update gpu firmwares for qcs8300 chipset
- add firmware for qat_420xx devices
- amdgpu: DMCUB updates for various ASICs
- i915: Update Xe3LPD DMC to v2.20
- update firmware for MT7920/MT7925 WiFi device
- mediatek MT7920/MT7925 bluetooth firmware update
- Update firmware file for Intel BlazarI/BlazarU core
- intel_vpu: Add firmware for 37xx and 40xx NPUs
- QCA: Add Bluetooth firmwares for QCA2066 with USB transport
- QCA: Add two bluetooth firmware nvm files for QCA2066
- QCA: Update Bluetooth QCA2066 firmware to 2.1.0-00653
- QCA: Update Bluetooth WCN685x 2.1 firmware to 2.1.0-00653
- cirrus: cs35l41: Add firmware and tuning for ASUS Commercial/Consumer laptops
- ASoC: tas2781: Update dsp firmware for Gemtree project
- xe: Update GUC to v70.40.2 for BMG, LNL
- cirrus: cs35l41: Add firmware and tunings for CS35L41 driver for Steam Deck
- ath11k: QCN9074 hw1.0: update to WLAN.HK.2.9.0.1-02175-QCAHKSWPL_SILICONZ-2
- ath11k: QCA6698AQ hw2.1: update to WLAN.HSP.1.1-04604-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- ath11k: QCA6698AQ hw2.1: update board-2.bin
- rtw89: 8852bt: update fw to v0.29.122.0 and BB parameter to 07
- Update AMD SEV firmware
- qca: update WCN3988 firmware
- amdgpu: Update ISP FW for isp v4.1.1
- qcom: add firmware for Adreno A225
- cirrus: cs35l56: Add / update firmware for Cirrus CS35L56 for ASUS/Dell/HP/Lenovo laptops
- update firmware for en8811h 2.5G ethernet phy
- ASoC: tas2781: Change regbin firmwares for single device

* Tue Feb 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250211-1
- Update to 20250211
- i915: Update Xe2LPD DMC to v2.28
- ASoC: tas2781: Add regbin firmware by index for single device
- rtl_bt: Update RTL8852B BT USB FW to 0x0474_842D
- iwlwifi: add Bz/gl/ty/So/Ma FW for core93-123 release
- iwlwifi: update cc/Qu/QuZ firmwares for core93-82 release
- ASoC: tas2781: Add dsp firmware for new projects
- amdgpu: DMCUB update for DCN401
- ath12k: WCN7850 hw2.0: update board-2.bin
- ath12k: QCN9274 hw2.0: update to WLAN.WBE.1.4.1-00199-QCAHKSWPL_SILICONZ-1
- ath12k: QCN9274 hw2.0: update board-2.bin
- ath11k: WCN6750 hw1.0: update board-2.bin
- ath11k: QCN9074 hw1.0: update to WLAN.HK.2.9.0.1-02146-QCAHKSWPL_SILICONZ-1
- ath11k: QCA6698AQ hw2.1: add to WLAN.HSP.1.1-04479-QCAHSPSWPL_V1_V2_SILICONZ_IOE-1
- ath11k: QCA6698AQ hw2.1: add board-2.bin
- ath11k: QCA6390 hw2.0: update board-2.bin
- ath11k: QCA2066 hw2.1: update to WLAN.HSP.1.1-03926.13-QCAHSPSWPL_V2_SILICONZ_CE-2.52297.6
- ath11k: QCA2066 hw2.1: update board-2.bin
- ath11k: IPQ8074 hw2.0: update to WLAN.HK.2.9.0.1-02146-QCAHKSWPL_SILICONZ-1
- ath11k: IPQ6018 hw1.0: update to WLAN.HK.2.7.0.1-02409-QCAHKSWPL_SILICONZ-1
- ath11k: add device-specific firmware for QCM6490 boards
- qca: add more WCN3950 1.3 NVM files
- qca: add firmware for WCN3950 chips
- qca: move QCA6390 firmware to separate section
- qca: restore licence information for WCN399x firmware
- qca: Update Bluetooth WCN6750 1.1.0-00476 firmware to 1.1.3-00069
- qcom:x1e80100: Support for Lenovo T14s G6 Qualcomm platform
- Update FW files for MRVL SD8997 chips
- i915: Update Xe2LPD DMC to v2.27
- qca: Update Bluetooth WCN6856 firmware 2.1.0-00642 to 2.1.0-00650
- rtl_bt: Update RTL8852B BT USB FW to 0x049B_5037
- amdgpu: Update ISP FW for isp v4.1.1
- QCA: Add Bluetooth firmware for QCA6698
- amlogic: update firmware for w265s2
- mediatek MT7925: update bluetooth firmware to 20250113153307
- update firmware for MT7925 WiFi device
- amdgpu: LOTS of firmware updates
- qcom: update SLPI firmware for RB5 board
- amdgpu: DMCUB updates for various AMDGPU ASICs
- qcom: add DSP firmware for SA8775p platform
- qcom: correct venus firmware versions
- qcom: add missing version information
- Update firmware (v10) for mt7988 internal
- iwlwifi: add Bz FW for core90-93 release
- wilc3000: add firmware for WILC3000 WiFi device
- rtw89: 8852b: update fw to v0.29.29.8
- rtw89: 8852c: update fw to v0.27.122.0
- rtw89: 8922a: update fw to v0.35.54.0
- rtw89: 8852bt: update fw to v0.29.110.0
- rtw89: 8852b: update fw to v0.29.29.7
- cirrus: cs35l56: Correct some links to address the correct amp instance
- Update firmware file for Intel Bluetooth Magnetar/BlazarU/Solar core

* Fri Jan 10 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 20250109-1
- Update to 20250109
- cirrus: cs35l41: Add Firmware for Ayaneo system 1f660105
- rtl_bt: Add separate config for RLT8723CS Bluetooth part
- amdgpu: revert some firmwares
- WHENCE: Link the Raspberry Pi CM5 and 500 to the 4B
- Add support to install files/symlinks in parallel.
- rtl_bt: Update RTL8852B BT USB FW to 0x04BE_1F5E
- cnm: update chips&media wave521c firmware.
- rtl_nic: add firmware rtl8125bp-2
- qcom: venus-5.4: update firmware binary for sc7180 and qcs615
- cirrus: cs35l56: Correct filenames of SSID 17aa3832
- cirrus: cs35l56: Add and update firmware for various Cirrus CS35L54/CS35L56 laptops
- cirrus: cs35l56: Correct SSID order for 103c8d01 103c8d08 10431f43
- rtl_nic: add firmware rtl8125d-2
