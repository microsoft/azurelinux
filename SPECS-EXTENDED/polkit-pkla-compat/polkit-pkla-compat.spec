Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		polkit-pkla-compat
Version:	0.1
Release:	17%{?dist}
Summary:	Rules for polkit to add compatibility with pklocalauthority
# GPLv2-licensed ltmain.sh and Apache-licensed mocklibc are not shipped in
# the binary package.
License:	LGPLv2+
URL:		https://pagure.io/polkit-pkla-compat
Source0:	https://releases.pagure.org/polkit-pkla-compat/polkit-pkla-compat-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:	docbook-style-xsl, libxslt, glib2-devel, polkit-devel
# To ensure the polkitd group already exists when this is installed
Requires(pre): polkit

%global _hardened_build 1

%description
A polkit JavaScript rule and associated helpers that mostly provide
compatibility with the .pkla file format supported in polkit <= 0.105 for users
of later polkit releases.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} V=1

%install
%make_install INSTALL='install -p'

%check
make check

%files
%doc AUTHORS COPYING NEWS README
%dir %attr(0750,root,polkitd) %dir %{_sysconfdir}/polkit-1/localauthority
%dir %{_sysconfdir}/polkit-1/localauthority/*.d
%dir %{_sysconfdir}/polkit-1/localauthority.conf.d
%config(noreplace) %{_sysconfdir}/polkit-1/rules.d/49-polkit-pkla-compat.rules
%{_bindir}/pkla-admin-identities
%{_bindir}/pkla-check-authorization
%{_mandir}/man8/pkla-admin-identities.8*
%{_mandir}/man8/pkla-check-authorization.8*
%{_mandir}/man8/pklocalauthority.8*
%dir %attr(0750,root,polkitd) %{_localstatedir}/lib/polkit-1
%dir %{_localstatedir}/lib/polkit-1/localauthority
%dir %{_localstatedir}/lib/polkit-1/localauthority/*.d

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Oct 21 2017 Miloslav Trmač <mitr@redhat.com> - 0.1-11
- Update URL: and Source0: to point to Pagure instead of fedorahosted.org
  Resolves: #1502386

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Miloslav Trmač <mitr@redhat.com> - 0.1-2
- Add a comment above License about SRPM-only licenses
- Reword Summary: to avoid a rpmlint warning
- Move INSTALL= to the %%install section

* Tue May  7 2013 Miloslav Trmač <mitr@redhat.com> - 0.1-1
- Initial package
