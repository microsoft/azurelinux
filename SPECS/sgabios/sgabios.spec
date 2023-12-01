%global hash 72f39d4
%global date 20180715
# Sgabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}
Summary:        Serial graphics BIOS option rom
Name:           sgabios
Version:        0.%{date}git
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/qemu/sgabios
# There are no upstream releases.  This archive is prepared as follows:
#
# git clone https://github.com/qemu/sgabios
# cd sgabios
# hash=`git log -1 --format='%h'`
# date=`git log -1 --format='%cd' --date=short | tr -d -`
# git archive --prefix sgabios-${date}-git${hash}/ ${hash} | xz -7e > ../openbios-${date}-git${hash}.tar.xz
Source0:        %{_mariner_sources_url}/%{name}-%{date}-git%{hash}.tar.xz
BuildRequires:  gcc
Requires:       %{name}-bin = %{version}-%{release}
ExclusiveArch:  x86_64

%description
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.

%package        bin
Summary:        Sgabios for x86
BuildArch:      noarch

%description bin
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.

%prep
%autosetup -n sgabios-%{date}-git%{hash}

%build
unset MAKEFLAGS
make HOSTCC=gcc

%install
mkdir -p %{buildroot}%{_datadir}/sgabios
install -m 0644 sgabios.bin %{buildroot}%{_datadir}/sgabios

%files
%doc design.txt

%files bin
%license COPYING
%dir %{_datadir}/sgabios/
%{_datadir}/sgabios/sgabios.bin

%changelog
* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20180715git-8
- Updating source URL.

* Tue Dec 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.20180715git-7
- Lint spec
- License verified
- Remove cross-compilation pieces

* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 0.20180715git-6
- Remove epoch

* Tue Jun 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 1:0.20180715git-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn off cross-compilation

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20180715git-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20180715git-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20180715git-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Cole Robinson <crobinso@redhat.com> - 1:0.20180715.git-1
- Update to qemu sgabios 72f39d4

* Mon Jul 23 2018 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20170427git-3
- Add explicit BuildRequires for GCC (Resolves: #1606338)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20170427git-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 25 2018 Cole Robinson <crobinso@redhat.com> - 1:0.20170427git-1
- Switch to qemu sgabios repo, which has an extra bugfix

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-12
- Allow disabling cross-compilation

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1:0.20110622svn-3
- Root sgabios package is noarch too because it only contains docs

* Thu Oct 25 2012 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-2
- Cross compile (fixes bug #869876).

* Wed Oct 17 2012 Cole Robinson <crobinso@redhat.com> - 1:0.20110622svn-2
- Fix deps with epoch bump

* Mon Oct 15 2012 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-1
- Move date from release to version (requires epoch bump).

* Sun Aug 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0-1.1.20110622svn
- Fix date in release string.
  NB: To make this version > than the previous, I had to use 1.1.20110622
  instead of 0.1.20110622, since the old second field was 20110623.
- Unset MAKEFLAGS, since parallel make breaks the build.
- Bring the spec file up to modern standards.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.20110623SVN
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.20110622SVN
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.0-0.20110621SVN
- Updates per review.

* Tue Jun 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.1-0.20110621SVN
- Created initial package
