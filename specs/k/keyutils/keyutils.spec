# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define libapivermajor 1
%define libapiversion %{libapivermajor}.10

# % define buildid .local

Name:    keyutils
Version: 1.6.3
Release: 6%{?buildid}%{?dist}
Summary: Linux Key Management Utilities
License: GPL-2.0-or-later AND LGPL-2.1-or-later
Url:   https://git.kernel.org/pub/scm/linux/kernel/git/dhowells/keyutils.git

Source0: %{url}/snapshot/keyutils-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: glibc-kernheaders >= 2.4-9.1.92
BuildRequires: make
BuildRequires: g++
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package libs
Summary: Key utilities library

%description libs
This package provides a wrapper library for the key management facility system
calls.

%package libs-devel
Summary: Development package for building Linux key management utilities
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description libs-devel
This package provides headers and libraries for building key utilities.

%prep
%setup -q

%build
make \
	NO_ARLIB=1 \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{_datadir}/%{name} \
	RELEASE=.%{release} \
	NO_GLIBC_KEYERR=1 \
	CFLAGS="-Wall $RPM_OPT_FLAGS" \
	LDFLAGS="%{?__global_ldflags}"

%install
make \
	NO_ARLIB=1 \
	DESTDIR=$RPM_BUILD_ROOT \
	ETCDIR=%{_sysconfdir} \
	LIBDIR=%{_libdir} \
	USRLIBDIR=%{_libdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	INCLUDEDIR=%{_includedir} \
	SHAREDIR=%{_datadir}/%{name} \
	install

%ldconfig_scriptlets libs

%files
%doc README
%license LICENCE.GPL
%config(noreplace) %{_sysconfdir}/*
%{_bindir}/keyctl
%{_sbindir}/key.dns_resolver
%{_sbindir}/request-key
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files libs
%license LICENCE.LGPL
%{_libdir}/libkeyutils.so.%{libapiversion}
%{_libdir}/libkeyutils.so.%{libapivermajor}
%{_mandir}/man7/*

%files libs-devel
%{_libdir}/libkeyutils.so
%{_includedir}/keyutils.h
%{_libdir}/pkgconfig/libkeyutils.pc
%{_mandir}/man3/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Pavel Reichl <preichl@redhat.com> - 1.6.3-1
- Update to upstream version 1.6.3
- Related: rhbz#2121553

* Mon Oct 16 2023 Pavel Reichl <preichl@redhat.com> - 1.6.1-8
- Convert License tag to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan  5 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- Spec cleanups

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 David Howells <dhowells@redhat.com> - 1.6-1
- Apply various specfile cleanups from Fedora.
- request-key: Provide a command line option to suppress helper execution.
- request-key: Find least-wildcard match rather than first match.
- Remove the dependency on MIT Kerberos.
- Fix some error messages
- keyctl_dh_compute.3: Suggest /proc/crypto for list of available hashes.
- Fix doc and comment typos.
- Add public key ops for encrypt, decrypt, sign and verify (needs linux-4.20).
- Add pkg-config support for finding libkeyutils.

* Tue Aug 28 2018 David Howells <dhowells@redhat.com> 1.5.11-1
- Add keyring restriction support.
- Add KDF support to the Diffie-Helman function.
- DNS: Add support for AFS config files and SRV records

* Sat Jul 21 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.10-8
- Spec cleanups, add gcc build requires

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.10-6
- Escape macros in %%changelog

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.10-4
- Switch to %%ldconfig_scriptlets

* Wed Mar 15 2017 David Howells <dhowells@redhat.com> - 1.5.10-1
- Include sys/types.h in keyutils.h.
- The dns resolver needs limits.h.
- Overhaul of all manual pages.
- Some manual pages moved to Linux man-pages project.
- Add Diffie-Helman keyctl function.

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 1.5.9-7
- Pass ldflags into the build so hardening works

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.5.9-3
- Fix license handling

* Fri Feb 21 2014 David Howells <dhowells@redhat.com> - 1.5.9-1
- Add manpages for get_persistent.
- Fix memory leaks in keyctl_describe/read/get_security_alloc().
- Use keyctl_describe_alloc in dump_key_tree_aux rather than open coding it.
- Exit rather than returning from act_xxx() functions.
- Fix memory leak in dump_key_tree_aux.
- Only get the groups list if we need it.
- Don't trust sscanf's %%n argument.
- Use the correct path macros in the specfile.
- Avoid use realloc when the memory has no content.
- Fix a bunch of issues in key.dns_resolver.
- Fix command table searching in keyctl utility.
- Fix a typo in the permissions mask constants.
- Improve the keyctl_read manpage.
- Add man7 pages describing various keyrings concepts.

* Fri Oct 4 2013 David Howells <dhowells@redhat.com> - 1.5.8-1
- New lib symbols should go in a new library minor version.

* Wed Oct 2 2013 David Howells <dhowells@redhat.com> - 1.5.7-1
- Provide a utility function to find a key by type and name.
- Allow keyctl commands to take a type+name arg instead of a key-id arg.
- Add per-UID get_persistent keyring function.

* Thu Aug 29 2013 David Howells <dhowells@redhat.com> - 1.5.6-1
- Fix the request-key.conf.5 manpage.
- Fix the max depth of key tree dump (keyctl show).
- The input buffer size for keyctl padd and pinstantiate should be larger.
- Add keyctl_invalidate.3 manpage.

* Wed Nov 30 2011 David Howells <dhowells@redhat.com> - 1.5.5-1
- Fix a Makefile error.

* Wed Nov 30 2011 David Howells <dhowells@redhat.com> - 1.5.4-1
- Fix the keyctl padd command and similar to handle binary input.
- Make keyctl show able to take a keyring to dump.
- Make keyctl show able to take a flag to request hex key IDs.
- Make keyctl show print the real ID of the root keyring.

* Tue Nov 15 2011 David Howells <dhowells@redhat.com>
- Allow /sbin/request-key to have multiple config files.

* Wed Aug 31 2011 David Howells <dhowells@redhat.com>
- Adjust the manual page for 'keyctl unlink' to show keyring is optional.
- Add --version support for the keyutils version and build date.

* Thu Aug 11 2011 David Howells <dhowells@redhat.com> - 1.5.3-1
- Make the keyutils rpm depend on the same keyutils-libs rpm version.

* Tue Jul 26 2011 David Howells <dhowells@redhat.com> - 1.5.2-1
- Use correct format spec for printing pointer subtraction results.

* Tue Jul 19 2011 David Howells <dhowells@redhat.com> - 1.5.1-1
- Fix unread variables.
- Licence file update.

* Thu Mar 10 2011 David Howells <dhowells@redhat.com> - 1.5-1
- Disable RPATH setting in Makefile.
- Add -I. to build to get this keyutils.h.
- Make CFLAGS override on make command line work right.
- Make specfile UTF-8.
- Support KEYCTL_REJECT.
- Support KEYCTL_INSTANTIATE_IOV.
- Add AFSDB DNS lookup program from Wang Lei.
- Generalise DNS lookup program.
- Add recursive scan utility function.
- Add bad key reap command to keyctl.
- Add multi-unlink variant to keyctl unlink command.
- Add multi key purge command to keyctl.
- Handle multi-line commands in keyctl command table.
- Move the package to version to 1.5.

* Tue Mar 1 2011 David Howells <dhowells@redhat.com> - 1.4-4
- Make build guess at default libdirs and word size.
- Make program build depend on library in Makefile.
- Don't include $(DESTDIR) in MAN* macros.
- Remove NO_GLIBC_KEYSYS as it is obsolete.
- Have Makefile extract version info from specfile and version script.
- Provide RPM build rule in Makefile.
- Provide distclean rule in Makefile.

* Fri Dec 17 2010 Diego Elio Pettenò <flameeyes@hosting.flameeyes.eu> - 1.4-3
- Fix local linking and RPATH.

* Thu Jun 10 2010 David Howells <dhowells@redhat.com> - 1.4-2
- Fix prototypes in manual pages (some char* should be void*).
- Rename the keyctl_security.3 manpage to keyctl_get_security.3.

* Fri Mar 19 2010 David Howells <dhowells@redhat.com> - 1.4-1
- Fix the library naming wrt the version.
- Move the package to version to 1.4.

* Fri Mar 19 2010 David Howells <dhowells@redhat.com> - 1.3-3
- Fix spelling mistakes in manpages.
- Add an index manpage for all the keyctl functions.

* Thu Mar 11 2010 David Howells <dhowells@redhat.com> - 1.3-2
- Fix rpmlint warnings.

* Fri Feb 26 2010 David Howells <dhowells@redhat.com> - 1.3-1
- Fix compiler warnings in request-key.
- Expose the kernel function to get a key's security context.
- Expose the kernel function to set a processes keyring onto its parent.
- Move libkeyutils library version to 1.3.

* Tue Aug 22 2006 David Howells <dhowells@redhat.com> - 1.2-1
- Remove syscall manual pages (section 2) to man-pages package [BZ 203582]
- Don't write to serial port in debugging script

* Mon Jun 5 2006 David Howells <dhowells@redhat.com> - 1.1-4
- Call ldconfig during (un)installation.

* Fri May 5 2006 David Howells <dhowells@redhat.com> - 1.1-3
- Don't include the release number in the shared library filename
- Don't build static library

* Fri May 5 2006 David Howells <dhowells@redhat.com> - 1.1-2
- More bug fixes from Fedora reviewer.

* Thu May 4 2006 David Howells <dhowells@redhat.com> - 1.1-1
- Fix rpmlint errors

* Mon Dec 5 2005 David Howells <dhowells@redhat.com> - 1.0-2
- Add build dependency on glibc-kernheaders with key management syscall numbers

* Tue Nov 29 2005 David Howells <dhowells@redhat.com> - 1.0-1
- Add data pipe-in facility for keyctl request2

* Mon Nov 28 2005 David Howells <dhowells@redhat.com> - 1.0-1
- Rename library and header file "keyutil" -> "keyutils" for consistency
- Fix shared library version naming to same way as glibc.
- Add versioning for shared library symbols
- Create new keyutils-libs package and install library and main symlink there
- Install base library symlink in /usr/lib and place in devel package
- Added a keyutils archive library
- Shorten displayed key permissions list to just those we actually have

* Thu Nov 24 2005 David Howells <dhowells@redhat.com> - 0.3-4
- Add data pipe-in facilities for keyctl add, update and instantiate

* Fri Nov 18 2005 David Howells <dhowells@redhat.com> - 0.3-3
- Added stdint.h inclusion in keyutils.h
- Made request-key.c use request_key() rather than keyctl_search()
- Added piping facility to request-key

* Thu Nov 17 2005 David Howells <dhowells@redhat.com> - 0.3-2
- Added timeout keyctl option
- request_key auth keys must now be assumed
- Fix keyctl argument ordering for debug negate line in request-key.conf

* Thu Jul 28 2005 David Howells <dhowells@redhat.com> - 0.3-1
- Must invoke initialisation from perror() override in libkeyutils
- Minor UI changes

* Wed Jul 20 2005 David Howells <dhowells@redhat.com> - 0.2-2
- Bump version to permit building in main repositories.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.2-1
- Don't attempt to define the error codes in the header file.
- Pass the release ID through to the makefile to affect the shared library name.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-3
- Build in the perror() override to get the key error strings displayed.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-2
- Need a defattr directive after each files directive.

* Tue Jul 12 2005 David Howells <dhowells@redhat.com> - 0.1-1
- Package creation.
