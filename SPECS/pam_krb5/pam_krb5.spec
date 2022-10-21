Summary:        A Pluggable Authentication Module for Kerberos 5
Name:           pam_krb5
Version:        4.11
Release:        2%{?dist}
License:        BSD OR LGPLv2+
Group:          System/Libraries
URL:            https://github.com/rra/pam-krb5
Source0:        %{url}/archive/refs/tags/upstream/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0001:      0001-Drop-module-long-test.patch
BuildRequires:  byacc
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  pam-devel
Requires:       pam
# for testing
%if %{with_check}
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(lib)
%endif

%description
pam-krb5 is a Kerberos v5 PAM module for either MIT Kerberos or
Heimdal.  It supports ticket refreshing by screen savers, configurable
authorization handling, authentication of non-local accounts for
network services, password changing, and password expiration, as well
as all the standard expected PAM features.  It works correctly with
OpenSSH, even with ChallengeResponseAuthentication and
PrivilegeSeparation enabled, and supports extensive configuration
either by PAM options or in krb5.conf or both.  PKINIT is supported
with recent versions of both MIT Kerberos and Heimdal and FAST is
supported with recent MIT Kerberos.

%prep
%setup -q -n pam-krb5-upstream-%{version}

%autopatch -p1

%build
%configure --libdir=%{_libdir}
%make_build

%install
%make_install

# cleanup
find %{buildroot} -type f -name "*.la" -delete -print

%check
make check

%files
%license LICENSE
%doc README NEWS TODO
%{_libdir}/security/*
%{_mandir}/man5/*

%changelog
* Wed Jul 20 2022 Henry Li <lihl@microsoft.com> - 4.11-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified
- Change %{_pam_libdir} to %{_libdir} as the former macro is not supported in CBL-Mariner
- Add with_check macro to gate test requirements

* Wed Feb 23 2022 Pat Riehecky <riehecky@fnal.gov> 4.11-1
- Initial fedora package
- Replaces the deprecated Red Hat pam_krb5 module
