## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Disable the growpart subpackage in EPEL, as RHEL ships it on its own
%if 0%{?epel}
%bcond_with growpart
%else
%bcond_without growpart
%endif

Summary:	Cloud image management utilities
Name:		cloud-utils
Version:	0.33
Release:	%autorelease
License:	GPL-3.0-only
URL:		https://github.com/canonical/%{name}

Source:		%{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch

Requires:	%{name}-growpart
Requires:	%{name}-cloud-localds
Requires:	%{name}-write-mime-multipart
Requires:	%{name}-ec2metadata
Requires:	%{name}-resize-part-image
Requires:	%{name}-mount-image-callback
Requires:	%{name}-vcs-run

%description
This package provides a useful set of utilities for managing cloud images.

The tasks associated with image bundling are often tedious and repetitive. The
cloud-utils package provides several scripts that wrap the complicated tasks
with a much simpler interface.


%if %{with growpart}
%package growpart
Summary:	A script for growing a partition

Requires:	gawk
Requires:	util-linux
Recommends:	lvm2


%description growpart
This package provides the growpart script for growing a partition. It is
primarily used in cloud images in conjunction with the dracut-modules-growroot
package to grow the root partition on first boot.
%endif


%package cloud-localds
Summary:	A script for creating a nocloud configuration disk for cloud-init

Recommends:	tar
Recommends:	dosfstools
Recommends:	mtools
Recommends:	genisoimage
Recommends:	qemu-img


%description cloud-localds
This package provides the cloud-localds script, which creates a disk-image
with user-data and/or meta-data for cloud-init.


%package write-mime-multipart
Summary:	A utilty for creating mime-multipart files


%description write-mime-multipart
This package provides the write-mime-multipart script, which creates
mime multipart files that can be consumed by cloud-init as user-data.


%package ec2metadata
Summary:	A script to query and display EC2 AMI instance metadata


%description ec2metadata
This package provides the ec2metadata script, which can be used to query and
display EC2 instance metadata rekated to an AMI instance.


%package resize-part-image
Summary:	A script for resizing cloud images

Requires:	file
Requires:	gzip
Requires:	e2fsprogs
Requires:	gawk
Requires:	tar


%description resize-part-image
This package provides the resize-part-image script, which can be used to
resize a partition image and the contained filesystem to a new size.


%package mount-image-callback
Summary:	A script to run commands over cloud image contents

Requires:	gawk
Requires:	util-linux
Recommends:	qemu-img


%description mount-image-callback
This package provides the mount-image-callback script, which mounts a cloud
image to a temporary mountpoint and runs a specified command on the contents.


%package vcs-run
Summary:	Script to run commands over a VCS repository contents

Recommends:	breezy
Recommends:	git-core
Recommends:	mercurial
Recommends:	wget


%description vcs-run
This package provides the vcs-run script, which fetches a code repository
into a temporary directory and runs a user-specified command in it.


%prep
%setup -q

%build

%install

# Create the target directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

# Install binaries and manpages
install -pm 0755 bin/* %{buildroot}%{_bindir}/
install -pm 0644 man/* %{buildroot}%{_mandir}/man1/

# Exclude Ubuntu-specific tools
rm %{buildroot}%{_bindir}/*ubuntu*

# Exclude the cloud-run-instances manpage
rm -f %{buildroot}%{_mandir}/man1/cloud-run-instances.*

# Exclude euca2ools wrappers and manpages
rm -f %{buildroot}%{_bindir}/cloud-publish-*
rm -f %{buildroot}%{_mandir}/man1/cloud-publish-*

%if %{without growpart}
rm -f %{buildroot}%{_bindir}/growpart
rm -f %{buildroot}%{_mandir}/man1/growpart.*
%endif


%files
%doc ChangeLog
%license LICENSE


%if %{with growpart}
%files growpart
%doc ChangeLog
%license LICENSE
%{_bindir}/growpart
%doc %{_mandir}/man1/growpart.*
%endif


%files cloud-localds
%doc ChangeLog
%license LICENSE
%{_bindir}/cloud-localds
%doc %{_mandir}/man1/cloud-localds.*


%files write-mime-multipart
%doc ChangeLog
%license LICENSE
%{_bindir}/write-mime-multipart
%doc %{_mandir}/man1/write-mime-multipart.*


%files ec2metadata
%doc ChangeLog
%license LICENSE
%{_bindir}/ec2metadata


%files resize-part-image
%doc ChangeLog
%license LICENSE
%{_bindir}/resize-part-image
%doc %{_mandir}/man1/resize-part-image.*


%files mount-image-callback
%doc ChangeLog
%license LICENSE
%{_bindir}/mount-image-callback


%files vcs-run
%doc ChangeLog
%license LICENSE
%{_bindir}/vcs-run


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.33-12
- Latest state for cloud-utils

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Vitaly Kuznetsov <vkuznets@redhat.com> - 0.33-8
- Drop obsolete gdisk soft dependency

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.33-5
- Fix EPEL8 subpackage conflict

* Thu Sep 14 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.33-4
- Split each tool into its own subpackage

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.33-3
- Use install instead of mkdir and cp

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.33-2
- Fix Requires/Recommends

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.33-1
- Update to version 0.33

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-21
- Convert License field to SPDX

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-20
- Use %%{name} in Requires

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-19
- Use Recommends for weak dependency

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-18
- Use the %%{buildroot} macro

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-17
- Remove unnecessary definition of %%license

* Tue Sep 05 2023 Ondrej Mosnáček <omosnacek@gmail.com> - 0.31-16
- Switch to rpmautospec

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Juerg Haefliger <juergh@gmail.com> - 0.31-5
- Bump the release number to differentiate from the previous version which didn't build.

* Thu Oct 24 2019 Juerg Haefliger <juergh@gmail.com> - 0.31-4
- Drop euca2ools dependency (retired package) and wrapper scripts [bz#1762325].

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Juerg Haefliger <juergh@gmail.com> - 0.31-2
- Add new cloud-utils-0.31.tar.gz sources.

* Mon Mar 18 2019 Juerg Haefliger <juergh@gmail.com> - 0.31-1
- Requires python3 instead of python2 [bz#1530224].
- Drop python2-paramiko dependency (no longer required).
- Drop cloud-run-instances manpage (script no longer included).
- Rebase to upstream release 0.31
- mount-image-callback: mount with -o 'rw' or -o 'ro' (LP: #1663722)
- mount-image-callback: run blockdev and udevadm settle on nbd devices. (LP: #1741096, 1741300)
- mount-image-callback: Drop support for mounting lxd containers. (LP: #1715994)
- growpart: fix bug that stopped GPT disks from being grown past 2TB. (LP: #1762748)
- mount-image-callback: mention --help and -C/--cd-mountpoint in Usage
- growpart: fix bug when resizing a middle partition with sgdisk (LP: #1706751) [Fred De Backer]
- growpart: Resolve symbolic links before operating. [Kevin Locke] (LP: #1744406)
- growpart: fix bug occurring if start sector and size were the same. [Lars Kellogg-Stedman] (LP: #1807171)
- debian/control: drop Suggests on lxc1
- debian/tests/control: add test growpart-start-matches-size.
- White space cleanup.  Remove trailing space and tabs.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.30-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 Sinny Kumari <sinnykumari@fedoraproject.org> - 0.30-1
- Rebase to upstream release 0.30
- Resolves RHBZ#1515835 - growpart fails to resize partition on aarch64
- Remove patches in spec file because they are already available in 0.30
- Fix rpmlint issues on spec file
- Remove LICENSE file, already shipped with 0.30 source tar
- cloud-run-instances binary has been dropped in 0.28
- mount-image-callback and vcs-run binaries has been introduced in 0.28

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 03 2016 Adam Williamson <awilliam@redhat.com> - 0.27-16
- backport fix for RHBZ #1327337 (growpart fail with newer util-linux-ng)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Juerg Haefliger <juergh@gmail.com> - 0.27-13
- [1197894] sfdisk dropped --show-pt-geometry option

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 0.27-12
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov 22 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-10
- [966574] growpart spits out a non-fatal error

* Fri Aug 16 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-9
- Prevent building of debuginfo packages.
- Fix 32-bit arch type.

* Fri Aug 16 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-8
- Make the package a no-noarch package on EPEL so that the build of the main
  package can be prevented for the arches that don't support it [bz#986809].

* Tue Aug 06 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-7
- Build the growpart subpackage on all EPEL architectures [bz#986809].

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-5
- Don't make gdisk a hard requirement for cloud-utils-growpart to save some
  space on systems that don't use GPT partitions.

* Mon Jun 17 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-4
- Break out the growpart script into its own subpackage to prevent pulling a
  boatload of unnecessary dependencies into a cloud image.

* Mon Apr  8 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-3
- 3rd attempt to fix the spec file to only build on x86_64 for EPEL.

* Fri Apr  5 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-2
- Yet another spec file fix to only build on x86_64 for EPEL.

* Tue Apr  2 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-1
- Update to upstream release 0.27.
- Fix spec file to only build on x86_64 for EPEL.

* Tue Feb 12 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-0.2.bzr216
- Add GPL-3 license.
- Exclude Ubuntu-specific tools.
- Fix some spec file issues per reviewers comments.

* Tue Feb  5 2013 Juerg Haefliger <juergh@gmail.com> - 0.27-0.1.bzr216
- Initial build based on upstream revision bzr216.

## END: Generated by rpmautospec
