Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: User space tool to set up tables of ARP rules in kernel
Name:    arptables
Version: 0.0.5
Release: 3%{?dist}
License: GPLv2+

URL:     https://ebtables.sourceforge.net/
Source0: https://ftp.netfilter.org/pub/arptables/%{name}-%{version}.tar.gz
Source1: arptables.service
Source2: arptables-legacy-helper

BuildRequires:  gcc
BuildRequires: perl-generators
BuildRequires: systemd

%description
The arptables is a user space tool used to set up and maintain
the tables of ARP rules in the Linux kernel. These rules inspect
the ARP frames which they see. arptables is analogous to the iptables
user space tool, but is less complicated.

%package legacy
Summary: Legacy user space tool to set up tables of ARP rules in kernel
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:  arptables-helper

%description legacy
The arptables is a user space tool used to set up and maintain
the tables of ARP rules in the Linux kernel. These rules inspect
the ARP frames which they see. arptables is analogous to the iptables
user space tool, but is less complicated.

Note that it is considered legacy upstream since nftables provides the same
functionality in a much newer code-base. To aid in migration, there is
arptables-nft utility, a drop-in replacement for the legacy one which uses
nftables internally. It is provided by iptables-arptables package.

%package services
Summary: arptables systemd services
%{?systemd_ordering}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: arptables-helper
Obsoletes: arptables-compat < 0.0.4-20

%description services
arptables systemd services

This package provides the systemd arptables service that has been split
out of the base package for better integration with alternatives.

%prep
%autosetup -p1

%build
# Makefile uses $(KERNEL_DIR) to redefine where to look for header files.
# But when it's set to standard system include directory gcc ignores it
# (see gcc(1)). It however looks that the code is not ready for using 
# system headers (instead included ones) so we don't use this option.
make all 'COPT_FLAGS=%{optflags}' 'LDFLAGS=%{build_ldflags}' %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} BINDIR=%{_sbindir} MANDIR=%{_mandir}
pfx=%{buildroot}%{_sbindir}
manpfx=%{buildroot}%{_mandir}/man8
for sfx in "-restore" "-save"; do
	mv $pfx/arptables$sfx $pfx/arptables-legacy$sfx
	touch $pfx/arptables$sfx
	mv $manpfx/arptables${sfx}.8 $manpfx/arptables-legacy${sfx}.8
	touch $manpfx/arptables${sfx}.8
done

install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/arptables.service
mkdir -p %{buildroot}%{_libexecdir}/
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/
touch %{buildroot}%{_libexecdir}/arptables-helper
rm -rf %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
echo '# Configure prior to use' > %{buildroot}%{_sysconfdir}/sysconfig/arptables

%post legacy
pfx=%{_sbindir}/arptables
manpfx=%{_mandir}/man8/arptables
lepfx=%{_libexecdir}/arptables
for sfx in "" "-restore" "-save"; do
	if [ "$(readlink -e $pfx$sfx)" == $pfx$sfx ]; then
		rm -f $pfx$sfx
	fi
	if [ "$(readlink -e $manpfx${sfx}.8.gz)" == $manpfx${sfx}.8.gz ]; then
		rm -f $manpfx${sfx}.8.gz
	fi
done
if [ "$(readlink -e $lepfx-helper)" == $lepfx-helper ]; then
	rm -f $lepfx-helper
fi
%{_sbindir}/update-alternatives --install \
	$pfx arptables $pfx-legacy 10 \
	--slave $pfx-save arptables-save $pfx-legacy-save \
	--slave $pfx-restore arptables-restore $pfx-legacy-restore \
	--slave $manpfx.8.gz arptables-man $manpfx-legacy.8.gz \
	--slave $manpfx-save.8.gz arptables-save-man $manpfx-legacy-save.8.gz \
	--slave $manpfx-restore.8.gz arptables-restore-man $manpfx-legacy-restore.8.gz \
	--slave $lepfx-helper arptables-helper $lepfx-legacy-helper

%preun legacy
%systemd_preun arptables.service

%postun legacy
%systemd_postun_with_restart arptables.service
if [ $1 -eq 0 ]; then
	%{_sbindir}/update-alternatives --remove \
		arptables %{_sbindir}/arptables-legacy
fi

%post services
%systemd_post arptables.service

%preun services
%systemd_preun arptables.service

%postun services
%?ldconfig
%systemd_postun arptables.service

%files legacy
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/arptables-legacy*
%{_libexecdir}/arptables-legacy-helper
%{_mandir}/*/arptables-legacy*
%ghost %{_sbindir}/arptables
%ghost %{_sbindir}/arptables-save
%ghost %{_sbindir}/arptables-restore
%ghost %{_mandir}/man8/arptables.8.gz
%ghost %{_mandir}/man8/arptables-save.8.gz
%ghost %{_mandir}/man8/arptables-restore.8.gz
%ghost %{_libexecdir}/arptables-helper

%files services
%{_unitdir}/arptables.service
%config(noreplace) %{_sysconfdir}/sysconfig/arptables

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.5-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Phil Sutter <psutter@redhat.com> - 0.0.5-1
- New version 0.0.5

* Wed Oct 30 2019 Phil Sutter <psutter@redhat.com> - 0.0.4-20
- Make services sub-package obsolete compat to fix upgrade path

* Tue Oct 22 2019 Phil Sutter <psutter@redhat.com> - 0.0.4-19
- Drop compat sub-package again

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 21 2019 Phil Sutter <psutter@redhat.com> - 0.0.4-17
- Fix upgrade from non-legacy arptables package

* Mon Feb 18 2019 Phil Sutter <psutter@redhat.com> - 0.0.4-16
- Integrate with alternatives
- Split systemd service into sub-package
- Rename arptables RPM into arptables-legacy
- Add recent upstream changes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 21 2018 Florian Weimer <fweimer@redhat.com> - 0.0.4-13
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 16 2013 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-4
- revert previous change, the code is not ready for this

* Mon Sep 16 2013 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-3
- use system kernel headers

* Fri Sep 13 2013 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-2
- install with '-p' (#1007964)

* Fri Sep 13 2013 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-1
- renamed arptables_jf to arptables
