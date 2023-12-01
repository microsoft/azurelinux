%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%global grubefiname grubx64.efi
%global grubpxeefiname grubx64-noprefix.efi
%endif
%ifarch aarch64
%global buildarch aarch64
%global grubefiname grubaa64.efi
%global grubpxeefiname grubaa64-noprefix.efi
%endif
Summary:        Signed GRand Unified Bootloader for %{buildarch} systems
Name:           grub2-efi-binary-signed-%{buildarch}
Version:        2.06
Release:        12%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/grub
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        grub2-efi-binary-%{version}-%{release}.%{buildarch}.rpm
Source1:        grub2-efi-binary-noprefix-%{version}-%{release}.%{buildarch}.rpm
Source2:        %{grubefiname}
Source3:        %{grubpxeefiname}

%description
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     grub2-efi-binary
Summary:        GRand Unified Bootloader
Group:          Applications/System

# Some distros split 'grub2' into more subpackages. For now we're bundling it all together
# inside the default package and adding these 'Provides' to make installation more user-friendly
# for people used to other distributions.
%ifarch x86_64
Provides:       grub2-efi-x64 = %{version}-%{release}
%endif

%description -n grub2-efi-binary
This package contains the GRUB EFI image signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%package -n     grub2-efi-binary-noprefix
Summary:        GRand Unified Bootloader
Group:          Applications/System

%description -n grub2-efi-binary-noprefix
This package contains the GRUB EFI image with no prefix directory set and is signed for secure boot. The package is
specifically created for installing on %{buildarch} systems

%prep

%build

%install
mkdir -p %{buildroot}/boot/efi/EFI/BOOT
cp %{SOURCE2} %{buildroot}/boot/efi/EFI/BOOT/%{grubefiname}
cp %{SOURCE3} %{buildroot}/boot/efi/EFI/BOOT/%{grubpxeefiname}

%files -n grub2-efi-binary
/boot/efi/EFI/BOOT/%{grubefiname}

%files -n grub2-efi-binary-noprefix
/boot/efi/EFI/BOOT/%{grubpxeefiname}

%changelog
* Wed Oct 18 2023 Gary Swalling <gaswal@microsoft.com> - 2.06-12
- Bump release number to match grub release number

* Tue Aug 29 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.06-11
- Bump release number to match grub release number

* Thu Jun 08 2023 Daniel McIlvaney <damcilva@microsoft.com> - 2.06-10
- CVE-2022-3775

* Wed Apr 05 2023 Andy Zaugg <azaugg@linkedin.com> - 2.06-9
- Adding XFS support to GRUB

* Thu Dec 29 2022 Mykhailo Bykhovtsev <mbykhovtsev@microsoft@microsoft.com> - 2.06-8
- Fix CVE-2022-2601 (Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com>).

* Thu Sep 08 2022 Zhichun Wan <zhichunwan@microsoft.com> - 2.06-7
- Bump release number to match grub release number

* Thu Jul 28 2022 Minghe Ren <mingheren@microsoft.com> - 2.06-6
- Bump release number to match grub release number

* Tue Jul 19 2022 Henry Li <lihl@microsoft.com> - 2.06-5
- Bump release number to match grub release number

* Fri Jul 08 2022 Henry Li <lihl@microsoft.com> - 2.06-4
- Bump release number to match grub release number
- Add grub2-efi-binary-noprefix subpackage for the additional efi binary with no prefix directory set

* Mon Feb 28 2022 Henry Li <lihl@microsoft.com> - 2.06-3
- Bump release number to match grub release number

* Thu Feb 17 2022 Andrew Phelps <anphel@microsoft.com> - 2.06-2
- Bump release number to match grub release number

* Wed Feb 09 2022 Chris Co <chrco@microsoft.com> - 2.06-1
- Update to 2.06

* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 2.06~rc1-8
- Bump release number to match grub release number
- License verified

* Tue Sep 14 2021 Andrew Phelps <anphel@microsoft.com> - 2.06~rc1-7
- Update release to be aligned with unsigned version.

* Tue Jul 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.06~rc1-6
- Update release to be aligned with unsigned version.
- Adding 'Provides' for 'grub2-efi-x64'.

* Tue May 25 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.06~rc1-5
- Update release to be aligned with unsigned version

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-4
- Commonize to one spec instead of having a spec per arch
- Define a new grub2-efi-binary subpackage which contains the signed collateral

* Fri Apr 02 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.06~rc1-3
- Update release to be aligned with unsigned version

* Fri Mar 26 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-2
- Update release to be aligned with unsigned version

* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-1
- Update to 2.06-rc1
- Incorporate SBAT data

* Wed Dec 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-26
- Updating release to be aligned with the unsigned bits.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Updating release to be aligned with the unsigned bits.

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> 2.02-24
- Original version for CBL-Mariner.
