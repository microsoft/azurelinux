Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: PAM authorization checker and PAM Basic Authentication provider
Name: mod_authnz_pam
Version: 1.2.1
Release: 2%{?dist}
License: ASL 2.0
URL: https://www.adelton.com/apache/mod_authnz_pam/
Source0: https://www.adelton.com/apache/mod_authnz_pam/%{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: httpd-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig
Requires: httpd-mmn
Requires: pam

# Suppres auto-provides for module DSO per
# https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Summary
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
mod_authnz_pam is a PAM authorization module, supplementing
authentication done by other modules, for example mod_auth_kerb; it
can also be used as full Basic Authentication provider which runs the
[login, password] authentication through the PAM stack.

%prep
%setup -q -n %{name}-%{version}

%build
%{_httpd_apxs} -c -Wc,"%{optflags} -Wall -pedantic -std=c99" -lpam mod_authnz_pam.c
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
echo > authnz_pam.confx
echo "# Load the module in %{_httpd_modconfdir}/55-authnz_pam.conf" >> authnz_pam.confx
cat authnz_pam.conf >> authnz_pam.confx
%else
cat authnz_pam.module > authnz_pam.confx
cat authnz_pam.conf >> authnz_pam.confx
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 .libs/mod_authnz_pam.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_authnz_pam.so

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
install -Dp -m 0644 authnz_pam.module $RPM_BUILD_ROOT%{_httpd_modconfdir}/55-authnz_pam.conf
%endif
install -Dp -m 0644 authnz_pam.confx $RPM_BUILD_ROOT%{_httpd_confdir}/authnz_pam.conf

%files
%doc README LICENSE
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/55-authnz_pam.conf
%endif
%config(noreplace) %{_httpd_confdir}/authnz_pam.conf
%{_httpd_moddir}/*.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jul 15 2020 Jan Pazdziora <jpazdziora@redhat.com> - 1.2.1-1
- 1855338 - rebase to upstream version 1.2.1.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Jan Pazdziora <jpazdziora@redhat.com> - 1.2.0-1
- Add support for mod_authn_socache.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.0-8
- https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-7
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.0-3
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.0-1
- Logging improvements; success logging moved from notice to info level.
- Fix redirect for AuthPAMExpiredRedirect with Basic Auth.
- Fix AuthPAMExpiredRedirect %%s escaping on Apache 2.2.

* Mon Mar 21 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.0.2-1
- 1319166 - the Requires(pre) httpd does not seem to be needed.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Jan Pazdziora <jpazdziora@redhat.com> - 1.0.1-1
- Fix handling of pre-auth / OTP / 2FA situations.

* Thu Jun 25 2015 Jan Pazdziora <jpazdziora@redhat.com> - 1.0.0-1
- Rebase to 1.0.0.
- Add support for AuthPAMExpiredRedirect.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 23 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.3-1
- Fix module loading/configuration for Apache 2.4.
- Set PAM_RHOST.

* Tue May 13 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.2-1
- Silence compile warnings by specifying C99.

* Tue Apr 15 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.1-1
- Fix error message when pam_authenticate step is skipped.

* Wed Mar 19 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9-1
- One more function made static for proper isolation.

* Thu Jan 30 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.8.1-1
- Fixing regression from previous change.

* Thu Jan 30 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.8-1
- 1058805 - .spec changes for Fedora package review.

* Thu Jan 09 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.7-1
- Declare all functions static for proper isolation.

* Wed Jan 08 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.6-1
- Make pam_authenticate_with_login_password available for other modules.
- Reformat documentation to make the Basic Auth usage less prominent.

* Mon Jan 06 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.5-1
- Initial release.
