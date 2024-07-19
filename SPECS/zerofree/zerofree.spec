Summary:        Utility to force unused ext2/3/4 inodes and blocks to zero
Name:           zerofree
Version:        1.1.1
Release:        7%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://frippery.org/uml/
Source0:        https://frippery.org/uml/%{name}-%{version}.tgz
Source1:        https://frippery.org/uml/sparsify.c
Source2:        https://frippery.org/uml/index.html

BuildRequires:  e2fsprogs-devel
BuildRequires:  clang

%description
zerofree is a utility to set unused filesystem inodes and blocks of an
ext2/3/4 filesystem to zero.  This can improve the compressibility and
privacy of an ext2/3/4 filesystem.

This tool was inspired by the ext2fs privacy (i.e. secure deletion)
patch described in a Linux kernel mailing list thread.

WARNING: The filesystem to be processed should be unmounted or mounted
read-only.  The tool tries to check this before running, but you
should be careful.

%prep
%setup -q
cp -p %{SOURCE1} .
cp -p %{SOURCE2} .

%build
make CC="clang %{optflags}"
clang %{optflags} sparsify.c -o sparsify -lext2fs

%install
install -D -p -m 755 zerofree %{buildroot}%{_sbindir}/zerofree
install -D -p -m 755 sparsify %{buildroot}%{_sbindir}/sparsify

%files
%license COPYING
%doc index.html
%{_sbindir}/zerofree
%{_sbindir}/sparsify

%changelog
* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-7
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Robert Scheck <robert@fedoraproject.org> - 1.1.1-1
- Upgrade to 1.1.1

* Mon Feb 19 2018 Robert Scheck <robert@fedoraproject.org> - 1.1.0-1
- Upgrade to 1.1.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 06 2016 Robert Scheck <robert@fedoraproject.org> - 1.0.3-6
- Build with ext4 support for RHEL 5 (#862934, thanks to Mike Swanson)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.
- New upstream version of sparsify.c.
- Fix the license.
- Modernize the spec file.
- Remove sparsify patch (equivalent patch has gone upstream).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-10
- Patch sparsify to work with e2fsprogs >= 1.42.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-7
- Include zerofree(8) man page from Debian (RHBZ#596732).

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-5
- Include the index file as a source file.
- Improve the description, remove spelling mistakes and other typos.
- Use the upstream SRPM directly, unpacking source from it.
- Fix use of dist macro.
- Pass the RPM OPTFLAGS to C compiler (should also fix debuginfo pkg).
- Use 'cp -p' to preserve timestamps when copying index.html file.
- Fix the defattr line.
- License is GPL+ (any version of the GPL including 1).
- Use a simpler install command to install the binary.
- Fix the upstream URL to point to the real original project.
- Add the sparsify command.

* Thu May 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-1
- Initial packaging for Fedora, based on R P Herrold's package.

* Wed May 13 2009 R P Herrold <info@owlriver.com> - 1.0.1-1
- initial packaging
