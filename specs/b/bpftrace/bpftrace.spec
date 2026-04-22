# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global llvm_compat 18

Name:           bpftrace
Version:        0.24.2
Release: 2%{?dist}
Summary:        High-level tracing language for Linux eBPF
License:        Apache-2.0

URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Arches will be included as upstream support is added and dependencies are
# satisfied in the respective arches
ExclusiveArch:  x86_64 %{power64} aarch64 s390x riscv64

BuildRequires:  gcc-c++
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib-devel
BuildRequires:  llvm%{?llvm_compat}-devel
BuildRequires:  clang%{?llvm_compat}-devel
BuildRequires:  bcc-devel >= 0.19.0-1
BuildRequires:  libbpf-devel
BuildRequires:  libbpf-static
BuildRequires:  binutils-devel
BuildRequires:  cereal-devel
BuildRequires:  lldb-devel
%if ! 0%{?rhel}
BuildRequires:  libpcap-devel
%endif
BuildRequires:  rubygem-asciidoctor
BuildRequires:  xxd
BuildRequires:  libxml2-devel
BuildRequires:  libffi-devel
BuildRequires:  elfutils-devel


%description
BPFtrace is a high-level tracing language for Linux enhanced Berkeley Packet
Filter (eBPF) available in recent Linux kernels (4.x). BPFtrace uses LLVM as a
backend to compile scripts to BPF-bytecode and makes use of BCC for
interacting with the Linux BPF system, as well as existing Linux tracing
capabilities: kernel dynamic tracing (kprobes), user-level dynamic tracing
(uprobes), and tracepoints. The BPFtrace language is inspired by awk and C,
and predecessor tracers such as DTrace and SystemTap


%prep
%autosetup -p1


%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DBUILD_TESTING:BOOL=OFF \
       -DBUILD_SHARED_LIBS:BOOL=OFF \
%if 0%{?llvm_compat}
       -DLLVM_DIR=/usr/lib64/llvm%{llvm_compat}/lib/cmake/llvm/ \
       -DClang_DIR=/usr/lib64/llvm%{llvm_compat}/lib/cmake/clang/ \
%endif
       %{nil}
%cmake_build


%install
# The post hooks strip the binary which removes
# the BEGIN_trigger and END_trigger functions
# which are needed for the BEGIN and END probes
%global __os_install_post %{nil}
%global _find_debuginfo_opts -g

%cmake_install

# Fix shebangs (https://fedoraproject.org/wiki/Packaging:Guidelines#Shebang_lines)
find %{buildroot}%{_datadir}/%{name}/tools -type f -exec \
  sed -i -e '1s=^#!/usr/bin/env %{name}\([0-9.]\+\)\?$=#!%{_bindir}/%{name}=' {} \;


%files
%doc README.md CONTRIBUTING-TOOLS.md
%doc docs/reference_guide.md docs/tutorial_one_liners.md
%license LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/tools
%dir %{_datadir}/%{name}/tools/old
%{_bindir}/%{name}
%{_bindir}/%{name}-aotrt
%{_mandir}/man8/*
%attr(0755,-,-) %{_datadir}/%{name}/tools/*.bt
%attr(0755,-,-) %{_datadir}/%{name}/tools/old/*.bt
%{_datadir}/bash-completion/completions/%{name}


%changelog
* Mon Dec 22 2025 Augusto Caringi <acaringi@redhat.com> - 0.24.2-1
- Rebased to version 0.24.2

* Fri Sep 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.24.0-1
- Rebased to version 0.24.0

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Augusto Caringi <acaringi@redhat.com> - 0.23.5-1
- Rebased to version 0.23.5

* Thu Mar 27 2025 Augusto Caringi <acaringi@redhat.com> - 0.23.0-1
- Rebased to version 0.23.0

* Thu Feb 13 2025 David Abdurachmanov <davidlt@rivosinc.com> - 0.22.1-2
- Enable riscv64

* Wed Jan 29 2025 Augusto Caringi <acaringi@redhat.com> - 0.22.1-1
- Rebased to version 0.22.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 01 2024 Augusto Caringi <acaringi@redhat.com> - 0.21.2-2
- Replaced libdwarf-devel by lldb-devel (BuildRequires)
- Added libpcap-devel (BuildRequires)

* Tue Oct 01 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.21.2-1
- Rebased to version 0.21.2
- Allow building with LLVM 19

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.21.1-1
- Rebased to version 0.21.1

* Wed May 22 2024 Augusto Caringi <acaringi@redhat.com> - 0.20.4-1
- Rebased to version 0.20.4

* Mon Feb 12 2024 Augusto Caringi <acaringi@redhat.com> - 0.20.1-1
- Rebased to version 0.20.1

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Augusto Caringi <acaringi@redhat.com> - 0.19.1-1
- Rebased to version 0.19.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Viktor Malik <vmalik@redhat.com> - 0.18.0-2
- Migrate license to SPDX

* Tue May 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.18.0-1
- Rebased to version 0.18.0

* Tue Jan 31 2023 Augusto Caringi <acaringi@redhat.com> - 0.17.0-1
- Rebased to version 0.17.0

* Fri Jan 27 2023 Augusto Caringi <acaringi@redhat.com> - 0.16.0-6
- Fix compile with GCC 13

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Jerome Marchand <jmarchan@redhat.com> - 0.16.0-4
- Rebuild for libbpf 1.0

* Mon Sep 26 2022 Kenneth Topp <toppk@bllue.org> - 0.16.0-3
- Enable workaround for non OpaquePointers on LLVM-15

* Mon Sep 19 2022 Pete Walter <pwalter@fedoraproject.org> - 0.16.0-2
- Rebuild for llvm 15

* Fri Sep 02 2022 Augusto Caringi <acaringi@redhat.com> - 0.16.0-1
- Rebased to version 0.16.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 05 2022 Augusto Caringi <acaringi@redhat.com> - 0.15.0-1
- Rebased to version 0.15.0

* Tue Apr 19 2022 Jerome Marchand <jmarchan@redhat.com> - 0.14.1-1
- Rebased to version 0.14.1
- Fix cmake build
- Rebuild with bcc 0.24

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 24 2021 Rafael Santos <rdossant@redhat.com> - 0.14.0-1
- Rebased to version 0.14.0

* Mon Aug 09 2021 Augusto Caringi <acaringi@redhat.com> - 0.13.0-1
- Rebased to version 0.13.0

* Tue Aug 03 2021 Rafael Santos <rdossant@redhat.com> - 0.12.1-3
- Rebuilt for bcc-0.21.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 27 2021 Jerome Marchand <jmarchan@redhat.com> - 0.12.1-1
- Rebased to version 0.12.1

* Sun Apr 04 2021 Augusto Caringi <acaringi@redhat.com> - 0.12.0-1
- Rebased to version 0.12.0

* Thu Apr 01 2021 Augusto Caringi <acaringi@redhat.com> - 0.11.4-1
- Rebased to version 0.11.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Tom Stellard <tstellar@redhat.com> - 0.11.0-7
- Rebuild for clang-11.1.0

* Fri Dec 04 2020 Jeff Law <law@redhat.com> - 0.11.0-6
- Fix missing #include for gcc-11

* Fri Nov 13 2020 Jerome Marchand <jmarchan@redhat.com> - 0.11.0-5
- Rebuilt for LLVM 11

* Tue Aug 04 2020 Augusto Caringi <acaringi@redhat.com> - 0.11.0-4
- Fix FTBFS due to cmake wide changes #1863295
- Fix 'bpftrace symbols are stripped' #1865787

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Augusto Caringi <acaringi@redhat.com> - 0.11.0-1
* Rebased to version 0.11.0

* Tue May 19 2020 Augusto Caringi <acaringi@redhat.com> - 0.10.0-2
- Rebuilt for new bcc/libbpf versions

* Tue Apr 14 2020 Augusto Caringi <acaringi@redhat.com> - 0.10.0-1
- Rebased to version 0.10.0
- Dropped support for s390x temporaly due to build error

* Thu Feb 06 2020 Augusto Caringi <acaringi@redhat.com> - 0.9.4-1
- Rebased to version 0.9.4

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.3-1
- Rebased to version 0.9.3

* Thu Aug 01 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.2-1
- Rebased to version 0.9.2

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Augusto Caringi <acaringi@redhat.com> - 0.9.1-1
- Rebased to version 0.9.1

* Thu Apr 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-3
- Rebuilt for bcc 0.9.0

* Mon Apr 22 2019 Neal Gompa <ngompa@datto.com> - 0.9-2
- Fix Source0 reference
- Use make_build macro for calling make

* Mon Apr  1 2019 Peter Robinson <pbrobinson@fedoraproject.org> 0.9-1
- Build on aarch64 and s390x

* Mon Mar 25 2019 Augusto Caringi <acaringi@redhat.com> - 0.9-0
- Updated to version 0.9

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0-2.20181210gitc49b333
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 10 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181210gitc49b333
- Updated to latest upstream (c49b333c034a6d29a7ce90f565e27da1061af971)

* Wed Nov 07 2018 Augusto Caringi <acaringi@redhat.com> - 0.0-1.20181107git029717b
- Initial import
