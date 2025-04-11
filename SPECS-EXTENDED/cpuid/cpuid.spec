Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           cpuid
Version:        20241023
Release:        1%{?dist}
Summary:        Dumps information about the CPU(s)

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://www.etallen.com/cpuid.html
Source0:        https://www.etallen.com/%{name}/%{name}-%{version}.src.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-podlators

Requires:       perl-autodie

ExclusiveArch:  %{ix86} x86_64

%description
cpuid dumps detailed information about x86 CPU(s) gathered from the CPUID
instruction, and also determines the exact model of CPU(s). It supports Intel,
AMD, and VIA CPUs, as well as older Transmeta, Cyrix, UMC, NexGen, and Rise
CPUs. 

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64 -DVERSION=%{version}" LDFLAGS="$RPM_LD_FLAGS"

%install
install -Dp -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dp -m 0755 cpuinfo2cpuid %{buildroot}%{_bindir}/cpuinfo2cpuid
install -Dp -m 0644 %{name}.man.gz %{buildroot}%{_mandir}/man1/%{name}.1.gz

%files
%doc ChangeLog FUTURE
%license LICENSE
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_bindir}/cpuinfo2cpuid

%changelog
* Tue Dec 17 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 20241023-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified
