Summary:      Debugedit - obtain debug information from binaries.
Name:         debugedit
Version:      5.0
Release:      3%{?dist}
License:      GPLv3+
URL:          https://sourceware.org/debugedit/
Vendor:       Microsoft Corporation
Distribution:   Azure Linux
Source0:      https://sourceware.org/ftp/%{name}/%{version}/%{name}-%{version}.tar.xz
# This patch prevents errors similar to the following when linking with lld:
#"/bin/debugedit: /usr/src/azl/BUILDROOT/kernel-6.6.29.1-5.azl3.x86_64/lib/modules/6.6.29.1-5.azl3/kernel/drivers/hid/usbhid/usbhid.ko: Unknown DWARF DW_FORM_0x25"
#"Processing files: kernel-devel-6.6.29.1-5.azl3.x86_64"
#"error: Missing build-id in /usr/src/azl/BUILDROOT/kernel-6.6.29.1-5.azl3.x86_64/usr/src/linux-headers-6.6.29.1-5.azl3/scripts/kallsyms"
Patch0:       0001-debugedit-Add-support-for-.debug_str_offsets-DW_FORM.patch
BuildRequires:  help2man

%description
%{summary}

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build_check

%files
%defattr(-,root,root)
%license COPYING3
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Oct 08 2021 Mateusz Malisz <mamalisz@microsoft.com> 5.0-1
- Original version for CBL-Mariner
- License verified
