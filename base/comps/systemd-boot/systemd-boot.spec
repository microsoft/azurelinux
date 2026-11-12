Name:           systemd-boot
Version:        262
Release:        %autorelease
Summary:        UEFI boot manager

License:        LGPL-2.1-or-later
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

This package contains the signed version that works with SecureBoot.}

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
cp -a %{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub \
   %{buildroot}%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub.alt
cp -a %{_prefix}/lib/systemd/boot/efi/addon%{efi_arch}.efi.stub \
   %{buildroot}%{_prefix}/lib/systemd/boot/efi/addon%{efi_arch}.efi.stub.alt

# Create efi binary hardlink for bootupd discovery
# Note: systemd-boot is hardlinked to the grub%%{efi_arch}.efi filename for shim compatibility
install -dm 0755 %{buildroot}%{_prefix}/lib/efi/systemd-boot/%{version}-%{release}/EFI/%{efi_vendor}
ln %{buildroot}%{_prefix}/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi.signed \
   %{buildroot}%{_prefix}/lib/efi/systemd-boot/%{version}-%{release}/EFI/%{efi_vendor}/grub%{efi_arch}.efi

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
%attr(0644,-,-) %{_prefix}/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi.signed
%{_prefix}/lib/systemd/boot/efi/linux%{efi_arch}.efi.stub.alt
%{_prefix}/lib/systemd/boot/efi/addon%{efi_arch}.efi.stub.alt
%dir %{_prefix}/lib/efi
%dir %{_prefix}/lib/efi/systemd-boot
%dir %{_prefix}/lib/efi/systemd-boot/%{version}-%{release}
%dir %{_prefix}/lib/efi/systemd-boot/%{version}-%{release}/EFI
%dir %{_prefix}/lib/efi/systemd-boot/%{version}-%{release}/EFI/%{efi_vendor}
%{_prefix}/lib/efi/systemd-boot/%{version}-%{release}/EFI/%{efi_vendor}/grub%{efi_arch}.efi

# Man pages are provided by systemd-udev subpackage.
# If we copied them to this package, we'd need to either rename them
# or worry about file conflicts. Since it is very very unlikely that
# somebody will have this package installed but not the systemd-udev,
# let's not duplicate the page.

%changelog
%autochangelog
