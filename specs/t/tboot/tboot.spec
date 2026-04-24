# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:       Performs a verified launch using Intel TXT
Name:          tboot
Version:       1.11.7
Release: 14%{?dist}
Epoch:         1

License:       BSD-3-Clause
URL:           http://sourceforge.net/projects/tboot/
Source0:       https://sourceforge.net/projects/tboot/files/%{name}/%{name}-%{version}.tar.gz
Patch0:        tboot-gcc14.patch
Patch1:        openssl-no-engine.patch
Patch2:        tboot-sbin.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: perl
BuildRequires: openssl-devel
BuildRequires: zlib-devel
Requires:      grub2-efi-x64-modules
ExclusiveArch: %{ix86} x86_64

%description
Trusted Boot (tboot) is an open source, pre-kernel/VMM module that uses
Intel Trusted Execution Technology (Intel TXT) to perform a measured
and verified launch of an OS kernel/VMM.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%make_build debug=y

%install
%make_install debug=y

%post
# create the tboot grub entry
grub2-mkconfig -o /boot/grub2/grub.cfg

# For EFI based machines ...
if [ -d /sys/firmware/efi ]; then
	echo "EFI detected .."
	[ -d /boot/grub2/x86_64-efi ] || mkdir -pv /boot/grub2/x86_64-efi
	cp -vf /usr/lib/grub/x86_64-efi/relocator.mod /boot/grub2/x86_64-efi/
	cp -vf /usr/lib/grub/x86_64-efi/multiboot2.mod /boot/grub2/x86_64-efi/
fi

%postun
# Remove residual grub efi modules.
[ -d /boot/grub2/x86_64-efi ] && rm -rf /boot/grub2/x86_64-efi
grub2-mkconfig -o /etc/grub2.cfg


%files
%license COPYING
%doc docs/*
%config %{_sysconfdir}/grub.d/20_linux_tboot
%config %{_sysconfdir}/grub.d/20_linux_xen_tboot
%{_bindir}/lcp2_crtpol
%{_bindir}/lcp2_crtpolelt
%{_bindir}/lcp2_crtpollist
%{_bindir}/lcp2_mlehash
%{_bindir}/tb_polgen
%{_bindir}/txt-acminfo
%{_bindir}/txt-parse_err
%{_bindir}/txt-stat
%{_mandir}/man8/lcp2_crtpol.8.gz
%{_mandir}/man8/lcp2_crtpolelt.8.gz
%{_mandir}/man8/lcp2_crtpollist.8.gz
%{_mandir}/man8/lcp2_mlehash.8.gz
%{_mandir}/man8/tb_polgen.8.gz
%{_mandir}/man8/txt-acminfo.8.gz
%{_mandir}/man8/txt-parse_err.8.gz
%{_mandir}/man8/txt-stat.8.gz
/boot/tboot.gz
/boot/tboot-syms

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 David Cantrell <dcantrell@redhat.com> - 1:1.11.7-12
- Patch Makefiles to install to /usr/bin rather than /usr/sbin (#2341415)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Jun Miao <jun.miao@intel.com> - 1:1.11.3-10
- Update to v1.11.6 release

* Sun Jul 28 2024 Jun Miao <jun.miao@intel.com> - 1:1.11.3-9
- Update to v1.11.3 release

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 03 2024 Jun Miao <jun.miao@intel.com> - 1:1.11.2-7
- Update to v1.11.2 release

* Mon Jan 29 2024 Florian Weimer <fweimer@redhat.com> - 1:1.11.1-6
- Suppress GCC 14 allocation size warning

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 01 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.11.1-4
- Add grub2-efi-x64-modules dependency and scriplet

* Fri Sep 22 2023 David Cantrell <dcantrell@redhat.com> - 1:1.11.1-3
- Use %%license for the COPYING file in the %%files section
- Convert the License tag to an SPDX expression

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May 07 2023 Jun Miao <jun.miao@intel.com> - 1:1.11.1-1
- Update to v1.11.1 release

* Sun Apr 23 2023 Jun Miao <jun.miao@intel.com> - 1:1.11.0-2
- Update code sources with the v1.11.0

* Mon Feb 27 2023 Jun Miao <jun.miao@intel.com> - 1:1.11.0-1
- Update to v1.11.0 release

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 20 2022 Jun Miao <jun.miao@intel.com> - 1:1.10.5-1
- Update to v1.10.5 release

* Fri Feb 25 2022 Jun Miao jun.miao@intel.com - 1:1.10.4-2
- Update the tboot-1.10.4.tar.gz source

* Fri Feb 25 2022 Jun Miao <jun.miao@intel.com> - 1:1.10.4-1
- Updated to upstream 1.10.4 release
- Fix the GCC12 build error

* Thu Dec 23 2021 Yunying Sun <yunying.sun@intel.com> - 1:1.10.3-1
- Updated to 1.10.3 which added OpenSSL 3.0.0 support
- Bugzilla 2021901 is fixed with this updated release
- Removed obsolete patch files

* Fri Dec 3 2021 Yunying Sun <yunying.sun@intel.com> - 1:1.10.2-4
- Rebuilt again with OpenSSL 3.0.0 fix patch

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1:1.10.2-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Yunying Sun <yunying.sun@intel.com> - 1:1.10.2-1
- Updated to upstream 1.10.2 release
- Removed standalone patches as both are fixed in 1.10.2
- Adjusted dependencies, removed trousers and added perl
- Updated packaged file list

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 30 2020 Jeff Law <law@redhat.com> - 1:1.9.11-5
- Re-enable -Wstringop-overflow and instead make the problematical
  pointer volatile to avoid the false positive diagnostic

* Thu Oct 29 2020 Jeff Law <law@redhat.com> - 1:1.9.11-4
- Fix buglet exposed by gcc-11 -Warray-parameter
- Temporarily disable -Wstringop-overflow due to false positive in gcc-11

* Wed Jul 29 2020 Jeff Law <law@redhat.com> - 1:1.9.11-3
- Explicitly allow uninitialized variables in a few places that do it
- on purpose

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Apr 19 2020 Filipe Rosset <rosset.filipe@gmail.com> - 1:1.9.11-1
- Update to 1.9.11

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Yunying Sun <yunying.sun@intel.com> - 1:1.9.10-1
- Add patch to fix package build error
- Add build dependency to zlib-devel
- Update to latest release 1.9.10

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Yunying Sun <yunying.sun@intel.com> - 1:1.9.8-1
- Updated to upstream 1.9.8 release

* Tue Sep 4 2018 Yunying Sun <yunying.sun@intel.com> - 1:1.9.7-1
- Updated to upstream 1.9.7 release
- Removed the patch for openssl 1.1 as it is included in 1.9.7 already

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 06 2018 Tomáš Mráz <tmraz@redhat.com> - 1:1.9.6-2
- Patch to build with OpenSSL-1.1.x

* Sun Feb 04 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1:1.9.6-1
- Upgrade to latest upstream version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Gang Wei <gang.wei@intel.com> - 1:1.8.2-1
- Upgrade to latest upstream version which provided security fix for:
  tboot:argument measurement vulnerablity for GRUB2+ELF kernels

* Wed Jun 18 2014 Gang Wei <gang.wei@intel.com> - 1:1.8.1-1
- Upgrade to latest upstream version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 02 2013 Gang Wei <gang.wei@intel.com> - 1:1.7.3-3
- Fix for breaking grub2-mkconfig operation in 32bit case(#929384)

* Wed Feb 20 2013 Gang Wei <gang.wei@intel.com> - 1:1.7.3-2
- Fix version string in log

* Wed Jan 30 2013 David Cantrell <dcantrell@redhat.com> - 1:1.7.3-1
- Upgrade to latest upstream version (#902653)

* Wed Aug 22 2012 Gang Wei <gang.wei@intel.com> - 1:1.7.0-2
- Fix build error with zlib 1.2.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 15 2012 Gang Wei <gang.wei@intel.com> - 1:1.7.0
- 1.7.0 release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110429-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 29 2011 Gang Wei <gang.wei@intel.com> - 20110429-1
- Pull upstream changeset 255, rebuilt in F15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 1 2010 Joseph Cihula <joseph.cihula@intel.com> - 20101005-1.fc13
- Initial import
