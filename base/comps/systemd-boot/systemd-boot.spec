Name:           systemd-boot
Version:        253~rc1
Release:        %autorelease
Summary:        UEFI boot manager

License:        LGPLv2+
URL:            https://systemd.io

%global source_rpm_name systemd-boot-unsigned
%global source_rpm_version %(rpm -q --qf '%%{VERSION}-%%{RELEASE}' %{source_rpm_name} | sed 's/.*not installed/unknown/')

%global _binaries_in_noarch_packages_terminate_build 0

# Note: this package just signs an existing binary that was provided by
# %%source_rpm_name. This package should be rebuilt whenever %%source_rpm_name
# is updated or rebuilt in a way that is relevant for the boot loader.
#
# This way we don't need to duplicate the build dependencies and logic
# that is provided by the main systemd package.

BuildRequires:  version(%{source_rpm_name})%{_isa} = %{version}
BuildRequires:  pesign

ExclusiveArch:  %efi

%global _description %{expand:
systemd-boot (short: sd-boot) is a simple UEFI boot manager. It provides a
graphical menu to select the entry to boot and an editor for the kernel command
line. systemd-boot supports systems with UEFI firmware only.

This package contains the signed version that that works with SecureBoot.}

%description %_description

%package -n systemd-boot-%{efi_arch}
Summary:        %{summary}
Version:        %(echo %{source_rpm_version} | sed 's/-.*//')

Provides: systemd-boot-signed-%{efi_arch} = %version-%release
Provides: bundled(%{source_rpm_name}) = %{source_rpm_version}

# Obsolete the package with the version before the split to install all
# obsoleting packages on upgrades (i.e. systemd-udev, systemd-boot-unsigned,
# systemd-boot).
Obsoletes:      systemd-udev < 252.2-2

BuildArch:      noarch

%description -n systemd-boot-%{efi_arch} %_description

Built from %{source_rpm_name}-%{source_rpm_version}.

%build
if [[ "%{source_rpm_version}" = "unknown" ]]; then
   echo "%{source_rpm_version} is not installed, refusing build"
   exit 1
fi

%install
mkdir -p %{buildroot}%{_prefix}/lib/systemd/boot/efi
%pesign -s -i %{_prefix}/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi -o %{buildroot}%{_prefix}/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi.signed

# Copy files over so they become available on other architectures.
# They are renamed to avoid a file conflict between packages.
cp -a %{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub %{buildroot}%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub.alt
cp -a %{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.elf.stub %{buildroot}%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.elf.stub.alt

install -m0644 -Dt %{buildroot}%{_licensedir}/%{name}/ %{_datadir}/licenses/systemd/LICENSE.LGPL2.1

%postun
# This part will need to be updated in bootctl first, and then here.
if [ $1 -ge 1 ] && bootctl is-installed &>/dev/null; then
  echo "Updating systemd-boot…"
  bootctl update || :
fi

%files -n systemd-boot-%{efi_arch}
%license %{_licensedir}/%{name}/LICENSE.LGPL2.1
%dir %{_prefix}/lib/systemd
%dir %{_prefix}/lib/systemd/boot
%dir %{_prefix}/lib/systemd/boot/efi
%{_prefix}/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi.signed
%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub.alt
%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.elf.stub.alt

# Man pages are provided by systemd-udev subpackage.
# If we copied them to this package, we'd need to either rename them
# or worry about file conflicts. Since it is very very unlikely that
# somebody will have this package installed but not the systemd-udev,
# let's not duplicate the page.

%changelog
%autochangelog
