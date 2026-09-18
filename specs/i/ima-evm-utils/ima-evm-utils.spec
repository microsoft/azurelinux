# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# If the soname gets bumped we need to ship a compat library to be able
# to bootstrap and rebuild rpm else we end up with chicken and egg problem.
%global bootstrap 0

%if 0%{bootstrap}
%global compat_soversion 4
%endif

Name:    ima-evm-utils
Version: 1.6.2
Release: 6%{?dist}
Summary: IMA/EVM support utilities
License: GPL-2.0-or-later
Url:     https://github.com/linux-integrity/
Source0: %{url}/ima-evm-utils/releases/download/v%{version}/%{name}-%{version}.tar.gz

# IMA setup tools
Source2: dracut-98-integrity.conf
Source3: ima-add-sigs.sh
Source4: ima-setup.sh
Source100: policy-01-appraise-executable-and-lib-signatures
Source101: policy-02-keylime-remote-attestation
Source200: policy_list

%if 0%{bootstrap}
# compat source and patches
Source10: ima-evm-utils-1.5.tar.gz
BuildRequires: openssl-devel-engine
%endif

BuildRequires: asciidoc
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: keyutils-libs-devel
BuildRequires: libtool
BuildRequires: libxslt
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: tpm2-tss-devel
Requires: %{name}-libs = %{version}-%{release}
Requires: rpm-plugin-ima
Requires: keyutils
Requires: attr

%description
The Trusted Computing Group(TCG) run-time Integrity Measurement Architecture
(IMA) maintains a list of hash values of executables and other sensitive
system files, as they are read or executed. These are stored in the file
systems extended attributes. The Extended Verification Module (EVM) prevents
unauthorized changes to these extended attributes on the file system.
ima-evm-utils is used to prepare the file system for these extended attributes.

%package libs
Summary: Libraries for %{name}
License: LGPL-2.0-or-later

# to avoid ima-evm-utils and rpm-plugin-ima being installed on upgrade
# to Fedora 41 - https://bugzilla.redhat.com/show_bug.cgi?id=2319827
Obsoletes: ima-evm-utils < 1.6

%description libs
This package contains the libraries for applications to use
ima-evm-utils functionality.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package provides the header files for %{name}

%prep
%autosetup -p1

%if 0%{bootstrap}
mkdir compat/
pushd compat/
tar -zxf %{SOURCE10} --strip-components=1
popd
%endif

%build
autoreconf -vif
%configure --disable-static --disable-engine
%make_build

%if 0%{bootstrap}
pushd compat/
autoreconf -vif
%configure --disable-static --disable-engine
%make_build
popd
%endif

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete

%if 0%{bootstrap}
pushd compat/src/.libs/
install -p libimaevm.so.%{compat_soversion}.0.0 %{buildroot}%{_libdir}/libimaevm.so.%{compat_soversion}.0.0
ln -s -f %{buildroot}%{_libdir}/libimaevm.so.%{compat_soversion}.0.0 %{buildroot}%{_libdir}/libimaevm.so.%{compat_soversion}
popd
%endif

%ldconfig_scriptlets

# IMA setup tools
install -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/ima/dracut-98-integrity.conf

mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/ima/policies
while IFS= read -r policy_file
do
  install -m 644 %{_sourcedir}/policy-"$policy_file" $RPM_BUILD_ROOT%{_datadir}/ima/policies/"$policy_file"
done < %{SOURCE200}

install -D %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/ima-add-sigs
install -D %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/ima-setup

%files
%license LICENSES.txt COPYING
%doc NEWS README AUTHORS
%{_bindir}/evmctl
%{_mandir}/man1/evmctl*

# IMA setup tools
%{_datadir}/ima/policies
%{_datadir}/ima/dracut-98-integrity.conf
%{_bindir}/ima-add-sigs
%{_bindir}/ima-setup

%files libs
%license LICENSES.txt COPYING.LGPL
# if you need to bump the soname version, coordinate with dependent packages
%{_libdir}/libimaevm.so.5*
%if 0%{bootstrap}
%{_libdir}/libimaevm.so.%{compat_soversion}*
%endif

%files devel
%{_pkgdocdir}/*.sh
%{_includedir}/imaevm.h
%{_libdir}/libimaevm.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 03 2025 Coiby Xu <coxu@redhat.com> - 1.6.2-5
- release 1.6.2-5

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 31 2024 Coiby Xu <coxu@redhat.com> - 1.6.2-3
- Skip unsupported file systems for sample appraisal rule

* Fri Oct 18 2024 Adam Williamson <awilliam@redhat.com> - 1.6.2-2
- ima-evm-utils-libs obsoletes ima-evm-utils < 1.6 for rhbz#2319827

* Sat Aug 31 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Fri Aug 30 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-2
- Fix sign_hash when built without openssl engine support (rhbz#2297927)

* Thu Aug 29 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- Update project URLs

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6-1
- Update to 1.6

* Wed Jul 03 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6-0
- Bootstrap 1.6
- Update license for new details
- Spec file updates

* Thu Jun 06 2024 Coiby Xu <coxu@redhat.com> - 1.5-5
- add ima-evm-utils-libs subpackage (rpm-sign-libs can depend on ima-evm-utils-libs instead)
- add some IMA setup tools

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5-1
- Disable bootstrap

* Wed Jun 07 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5-0.1
- Update to 1.5
- Streamline bootstrap process a little
- Bootstrap mode
- Update download URL

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Björn Esser <besser82@fedoraproject.org> - 1.4-4
- Build without compat bootstrap sub package

* Thu Jan 20 2022 Björn Esser <besser82@fedoraproject.org> - 1.4-3
- Build with compat bootstrap sub package

* Tue Jan 18 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-2
- Add compat bootstrap sub package

* Mon Nov 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-1
- Update to 1.4

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.3.2-4
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Bruno Meneguele <bmeneg@redhat.com> - 1.3.2-1
- Rebase to new upstream v1.3.2 minor release

* Tue Aug 11 2020 Bruno Meneguele <bmeneg@redhat.com> - 1.3.1-1
- Rebase to new upstream v1.3.1 minor release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-2
- Fix devel deps

* Sun Jul 26 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-1
- Update to 1.3
- Use tpm2-tss instead of tss2
- Minor spec cleanups

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.2.1-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 31 2019 Bruno E. O. Meneguele <bmeneg@redhat.com> - 1.2.1-2
- Add pull request to correct lib soname version, wich was bumped to 1.0.0

* Wed Jul 31 2019 Bruno E. O. Meneguele <bmeneg@redhat.com> - 1.2.1-1
- Rebase to upstream v1.2.1
- Remove both patches that were already solved in upstream version
- Add runtime dependency of tss2 to retrieve PCR bank data from TPM2.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.1-4
- Add patch to remove dependency from libattr-devel package

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.1-2
- Remove libtool files
- Run ldconfig scriptlets after un/installing
- Add -devel subpackage to handle include files and examples
- Disable any static file in the package

* Fri Feb 16 2018 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.1-1
- New upstream release
- Support for OpenSSL 1.1 was added directly to the source code in upstream,
  thus removing specific patch for it
- Docbook xsl stylesheet updated to a local path

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0-4
- Switch to %%ldconfig_scriptlets

* Fri Dec 01 2017 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.0-3
- Add OpenSSL 1.1 API support for the package, avoiding the need of
  compat-openssl10-devel package

* Mon Nov 20 2017 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.0-2
- Adjusted docbook xsl path to match the correct stylesheet
- Remove only *.la files, considering there aren't any *.a files

* Tue Sep 05 2017 Bruno E. O. Meneguele <brdeoliv@redhat.com> - 1.0-1
- New upstream release
- Add OpenSSL 1.0 compatibility package, due to issues with OpenSSL 1.1
- Remove libtool files
- Run ldconfig after un/installation to update *.so files
- Add -devel subpackage to handle include files and examples

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Lubomir Rintel <lkundrak@v3.sk> - 0.9-3
- Fix FTBFS

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 31 2014 Avesh Agarwal <avagarwa@redhat.com> - 0.9-1
- New upstream release
- Applied a patch to fix man page issues.
- Updated spec file

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 27 2013 Vivek Goyal <vgoyal@redhat.com> - 0.6-1
- Initial package
