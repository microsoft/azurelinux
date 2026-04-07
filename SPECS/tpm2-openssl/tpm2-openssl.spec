# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:tpm2-openssl
Version: 1.2.0
Release: 7%{?candidate:.%{candidate}}%{?dist}
Summary: Provider for integration of TPM 2.0 to OpenSSL 3.0

License: BSD-3-Clause
URL: https://github.com/tpm2-software/tpm2-openssl
Source0: https://github.com/tpm2-software/%{name}/%{?candidate:archive/refs/tags}%{!?candidate:releases/download}/%{version}%{?candidate:-%{candidate}}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz
Source1: https://github.com/tpm2-software/%{name}/%{?candidate:archive/refs/tags}%{!?candidate:releases/download}/%{version}%{?candidate:-%{candidate}}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz.asc
Source2: gpgkey-B7201FE8031B07AF11F5423C6329CFCB6BE6FD76.gpg
# Will be included in Source0 after https://github.com/tpm2-software/tpm2-openssl/pull/100
Source3: run-with-simulator

# https://bugzilla.redhat.com/show_bug.cgi?id=2301337
Patch1: 0001-tests-rsa_pki-default-to-sha256.patch
Patch2: 0002-tests-do-not-test-sha1-by-default.patch

BuildRequires: gnupg2
BuildRequires: gcc
BuildRequires: make
BuildRequires: pkg-config
BuildRequires: autoconf automake libtool autoconf-archive
BuildRequires: tpm2-tss-devel
BuildRequires: openssl-devel >= 3.0.0

# Test dependencies
BuildRequires: dbus-daemon
BuildRequires: iproute
BuildRequires: openssl
BuildRequires: procps-ng
BuildRequires: swtpm
BuildRequires: tpm2-abrmd tpm2-abrmd-selinux
BuildRequires: tpm2-tools


%description
Makes the TPM 2.0 accessible via the standard OpenSSL API and command line
tools, adding TPM support to (almost) any OpenSSL 3.0-based application.

%prep
gpgv2 --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1 -n %{name}-%{version}%{?candidate:-%{candidate}}

%build
%if "%{?candidate:true}" == "true"
  sed -e '/^git.*$/d' -i bootstrap
  echo "%{version}%{?candidate:-%{candidate}}" > VERSION
  ./bootstrap
%endif
%configure
%{make_build}

%check
cp %{SOURCE3} %{_builddir}/%{name}-%{version}%{?candidate:-%{candidate}}/test/
./test/run-with-simulator swtpm skip-build

%install
%make_install

%files
%doc docs
%license LICENSE
%{_libdir}/ossl-modules/tpm2.so

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 18 2024 Adrian Freihofer <adrian.freihofer@gmail.com> 1.2.0-5
- Fix tests for F41 https://bugzilla.redhat.com/show_bug.cgi?id=2301337
- Revert exclude broken test on s390

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 30 2024 Adrian Freihofer <adrian.freihofer@gmail.com> 1.2.0-3
- refactor: rpmlint E: use-of-RPM_SOURCE_DIR (adrian.freihofer@gmail.com)
- do not require tpm2-abrmd (adrian.freihofer@gmail.com)

* Sat Mar 23 2024 Adrian Freihofer <adrian.freihofer@gmail.com> 1.2.0-2
- tito: use release tagger (adrian.freihofer@gmail.com)
- Revert "Automatic commit of package [tpm2-openssl] release [1.2.1-1]."
  (adrian.freihofer@gmail.com)
- Automatic commit of package [tpm2-openssl] release [1.2.1-1].
  (adrian.freihofer@gmail.com)
- run-with-simulator: backport from upstream (adrian.freihofer@gmail.com)

* Fri Mar 22 2024 Adrian Freihofer <adrian.freihofer@gmail.com> 1.2.0-1
- new package built with tito

