# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine _auto_set_build_flags

%global gittagdate 20220719
%global gittagcommit 6b6c16b4

# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

%define cross 1
%define targetdir qemu

Name:           SLOF
Version:        %{gittagdate}
Release:        8.git%{gittagcommit}%{?dist}
Summary:        Slimline Open Firmware

License:        BSD-3-Clause
URL:            http://www.openfirmware.info/SLOF

Source0:        https://github.com/aik/SLOF/archive/qemu-slof-%{gittagdate}.tar.gz

# the bundled libc stdbool.h is not compatible with C23
# https://github.com/aik/SLOF/pull/5
Patch0:         0001-libc-fix-build-in-C23-mode.patch

%if 0%{?cross:1}
BuildArch:      noarch
BuildRequires:  gcc-powerpc64-linux-gnu
%else
ExclusiveArch:  ppc64le
BuildArch: noarch
%endif

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Std)
BuildRequires:  perl(Data::Dumper)

%description
Slimline Open Firmware (SLOF) is initialization and boot source code
based on the IEEE-1275 (Open Firmware) standard, developed by
engineers of the IBM Corporation.

The SLOF source code provides illustrates what's needed to initialize
and boot Linux or a hypervisor on the industry Open Firmware boot
standard.

Note that you normally wouldn't need to install this package
separately.  It is a dependency of qemu-system-ppc64.


%prep
%setup -q -n SLOF-qemu-slof-%{gittagdate}
%autopatch -p1

%build
%if 0%{?cross:1}
export CROSS="powerpc64-linux-gnu-"
%else
export CROSS=""
%endif

%make_build qemu V=2

%install
mkdir -p %{buildroot}%{_datadir}/%{targetdir}
install -c -m 0644 boot_rom.bin %{buildroot}%{_datadir}/%{targetdir}/slof.bin


%files
%doc LICENSE
%doc README
%dir %{_datadir}/%{targetdir}
%{_datadir}/%{targetdir}/slof.bin


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20220719-8.git6b6c16b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 01 2025 Cole Robinson <crobinso@redhat.com> - 20220719-7.git6b6c16b4
- Fix build with cross-gcc 15 (Yaakov Selkowitz)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20220719-6.git6b6c16b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220719-5.git6b6c16b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220719-4.git6b6c16b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20220719-3.git6b6c16b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 21 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 20220719-2.git6b6c16b4
- Adjust conditionals for EPEL build

* Sun Aug 20 2023 Cole Robinson <crobinso@redhat.com> - 20220719-1.git6b6c16b4
- Update to SLOF 20220719

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210217-7.git33a7322d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210217-6.git33a7322d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210217-5.git33a7322d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Richard W.M. Jones <rjones@redhat.com> - 20210217-4.git33a7322d
- Unbreak build by undefining _auto_set_build_flags
  See: https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210217-3.git33a7322d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210217-2.git33a7322d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 0.1-git20210217-1
- Update to SLOF 20210217

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20200717-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Cole Robinson <aintdiscole@gmail.com> - 0.1.git20200717-1
- Update to SLOF 20200717

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20200327-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 Cole Robinson <aintdiscole@gmail.com> - 0.1.git20200327-1
- Update to SLOF 20200327

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20191022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Cole Robinson <aintdiscole@gmail.com> - 0.1.git20191022-1
- Update to SLOF 20191022 for qemu-4.2

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20190114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Cole Robinson <aintdiscole@gmail.com> - 0.1.git20190114-1
- Update to SLOF 20190114 for qemu-4.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20180702-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Cole Robinson <crobinso@redhat.com> - 0.1.git20180702-2
- Fix gcc 8.1 build compat (bz #1653655)

* Thu Nov 15 2018 Cole Robinson <crobinso@redhat.com> - 0.1.git20180702-1
- Update to SLOF 20180702 for qemu-3.1

* Tue Jul 31 2018 Cole Robinson <crobinso@redhat.com> - 0.1.git20180621-1
- Update to SLOF 20180621 for qemu-3.0

* Thu Jul 19 2018 Richard W.M. Jones <rjones@redhat.com> - 0.1.git20171214-4
- BR gcc, needed even when cross-compiling to make a build tool.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20171214-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 26 2018 Cole Robinson <crobinso@redhat.com> - 0.1.git20171214-2
- Drop documentation patch

* Thu Mar 22 2018 Cole Robinson <crobinso@redhat.com> - 0.1.git20171214-1
- Update to SLOF 20171214 for qemu-2.12

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20170724-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Paolo Bonzini <pbonzini@redhat.com> - 0.1.git120170724-3
- Add two patches from RHEL

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 0.1.git120170724-2
- Disable cross compilation for RHEL

* Thu Aug 03 2017 Cole Robinson <crobinso@redhat.com> - 0.1.git120170724-1
- Update to SLOF 20170724 for qemu 2.10

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20170303-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 0.1.git20170303-1
- Update to SLOF 20170303 for qemu 2.9

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20161019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Cole Robinson <crobinso@redhat.com> 0.1.git20161019-1
- Update to SLOF 20161019 for qemu 2.8

* Thu Apr 07 2016 Cole Robinson <crobinso@redhat.com> 0.1.git20160223-1
- Update to SLOF 20160223 for qemu 2.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.git20151103-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Cole Robinson <crobinso@redhat.com> 0.1.git20151103-1
- Update to SLOF 20151103 for qemu 2.5

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 0.1.git20150429-1
- Update to SLOF 20150429 for qemu 2.4

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20150313-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Cole Robinson <crobinso@redhat.com> 0.1.git20150313-1
- Update to SLOF 20150313 for qemu 2.3

* Tue Dec 02 2014 Cole Robinson <crobinso@redhat.com> - 0.1.git20141202-1
- Update to SLOF 20141202

* Fri Jul 04 2014 Cole Robinson <crobinso@redhat.com> - 0.1.git20140630-1
- Update to tag qemu-slof-20140630, queued for qemu 2.1

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20140304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 16 2014 Cole Robinson <crobinso@redhat.com> - 0.1.git20140304-1
- Update to qemu 2.0 version of SLOF

* Tue Nov 19 2013 Cole Robinson <crobinso@redhat.com> - 0.1.git20130827-1
- Update to version intended for qemu 1.7

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20130430-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Cole Robinson <crobinso@redhat.com> - 0.1.git20130430-1
- Update to version shipped with qemu 1.5

* Tue Feb 19 2013 Cole Robinson <crobinso@redhat.com> 0.1.git20121018-1
- Update to version shipped with qemu 1.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.git20120731-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 0.1.git20120731-1
- Move date from release to version.

* Fri Sep 14 2012 Paolo Bonzini <pbonzini@redhat.com> - 0-0.1.git20120731
- SLOF packages is very out of date with respect to what qemu expects (bug #855246)
- SLOF package builds wrong version of SLOF (bug #855236)
- build verbosely

* Tue Jul 31 2012 Richard W.M. Jones <rjones@redhat.com> - 0-0.1.git20120217
- Initial release in Fedora.
