Summary:	A Pluggable Authentication Module for Kerberos 5
Name:		pam_krb5
Version:	4.11
Release:	2%{?dist}
License:	MIT and BSD
Group:		System/Libraries
URL:		https://github.com/rra/pam-krb5
Source0:	%{url}/archive/refs/tags/upstream/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0001:	0001-Drop-module-long-test.patch

Requires:	pam

BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	krb5-devel
BuildRequires:	pam-devel

# for testing
BuildRequires:	perl(lib)
BuildRequires:	perl(Test::Pod)

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

# Make the paths jive to avoid conflicts on multilib systems.
sed -ri -e 's|/lib(64)?/|/\$LIB/|g' %{buildroot}/%{_mandir}/man*/pam_krb5*.5*

# cleanup
rm -f %{buildroot}/%{_libdir}/security/*.la

%check
# https://github.com/rra/pam-krb5/issues/25
# self-tests fail unless a default realm is set.
# That has to be done as someone with write access to /etc/
# which is not the mockbuild user.
#
%{__make} check

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

* Wed Feb 23 2022 Pat Riehecky <riehecky@fnal.gov> 4.11-1
- Initial fedora package
- Replaces the deprecated Red Hat pam_krb5 module
