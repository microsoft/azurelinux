Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# Spec file for IBM's TSS for the TPM 2.0
#
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}

%global incname ibmtss

Name:		tss2
Version:	1331
Release:	5%{?dist}
Summary:	IBM's TCG Software Stack (TSS) for TPM 2.0 and related utilities

License:	BSD
URL:		https://sourceforge.net/projects/ibmtpm20tss/
Source0:	https://sourceforge.net/projects/ibmtpm20tss/files/ibmtss%{version}.tar.gz
Patch1: flags-fixup.patch
Patch2: hash_generate.patch
Patch3: picfix.patch

BuildRequires:  gcc
BuildRequires:	help2man
BuildRequires:	openssl-devel
Requires:	openssl

%description
TSS2 is a user space Trusted Computing Group's Software Stack (TSS) for
TPM 2.0.  It implements the functionality equivalent to the TCG TSS
working group's ESAPI, SAPI, and TCTI layers (and perhaps more) but with
a hopefully far simpler interface.

It comes with about 80 "TPM tools" that can be used for rapid prototyping,
education and debugging. 

%package devel
Summary:	Development libraries and headers for IBM's TSS 2.0
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for IBM's TSS 2.0. You will need this in
order to build TSS 2.0 applications.

%prep
%autosetup -p1 -c %{name}-%{version}

%build
# nonstandard variable names are used in place of CFLAGS and LDFLAGS
pushd utils
CCFLAGS="%{optflags}" \
LNFLAGS="%{__global_ldflags}" \
make -f makefile.fedora %{?_smp_mflags} 
popd

%install
# Prefix for namespacing
BIN_PREFIX=tss
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}/%{incname}/
mkdir -p %{buildroot}/%{_mandir}/man1
pushd utils
# Pick out executables and copy with namespacing
for f in *; do
	if [[ -x $f && -f $f && ! $f =~ .*\..* ]]; then
		cp -p $f %{buildroot}/%{_bindir}/${BIN_PREFIX}$f
	fi;
done
cp -p *.so.1.1 %{buildroot}/%{_libdir}
cp -p %{incname}/*.h %{buildroot}/%{_includedir}/%{incname}/
cp -p man/man1/tss*.1 %{buildroot}/%{_mandir}/man1/
popd


# Make symbolic links to the shared lib
pushd %{buildroot}/%{_libdir}
rm -f libibmtss.so.1
ln -sf libibmtss.so.1.1 libibmtss.so.1
rm -f libibmtss.so
ln -sf libibmtss.so.1 libibmtss.so
popd

%ldconfig_scriptlets

%files
%license LICENSE
%{_bindir}/tss*
%{_libdir}/libibmtss.so.1
%{_libdir}/libibmtss.so.1.*
%attr(0644, root, root) %{_mandir}/man1/tss*.1*

%files devel
%{_includedir}/%{incname}
%{_libdir}/libibmtss.so
%doc ibmtss.doc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1331-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1331-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 1331-3
- Ensure tssprintcmd has the compilation compilation flags,
  PIC in particular

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 1331-1
- Rebase to version 1331

* Tue May 28 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 1234-4
- Fix covscan issues
- Fix compile and linker flag issues

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1234-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1234-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Jerry Snitselaar <jsnitsel@redhat.com> - 1234-1
- Version bump.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Merlin Mathesius <mmathesi@redhat.com> - 1027-1
- Version bump. Now supported for all architectures.
- Generate man pages since they are no longer included in source archive.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 05 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-7
- Removed defattr from the devel subpackage 

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-6
- Added s390x arch as another "ExcludeArch"

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-5
- Replaced ExclusiveArch with ExcludeArch 
 
* Mon Sep 19 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-4
- Used ExclusiveArch instead of BuildArch tag
- Removed attr from symlink in devel subpackage 
- Added manpages and modified the Source0
- Added CCFLAGS and LNFLAGS to enforce hardening and optimization

* Wed Aug 17 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-3
- Modified supported arch to ppc64le

* Sat Aug 13 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-2
- Minor spec fixes 

* Tue Aug 09 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-1
- Updated for initial submission 

* Fri Mar 20 2015 George Wilson <gcwilson@us.ibm.com>
- Initial implementation
