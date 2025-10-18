Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

Summary: Apache module to intercept login form submission and run PAM authentication
Name: mod_intercept_form_submit
Version: 1.2.0
Release: 8%{?dist}
License: ASL 2.0
URL: https://www.adelton.com/apache/mod_intercept_form_submit/
Source0: https://www.adelton.com/apache/mod_intercept_form_submit/%{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: httpd-devel
BuildRequires: pkgconfig
Requires: httpd-mmn
Requires: mod_authnz_pam >= 0.7

# Suppres auto-provides for module DSO per
# https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering#Summary
%{?filter_provides_in: %filter_provides_in %{_libdir}/httpd/modules/.*\.so$}
%{?filter_setup}

%description
mod_intercept_form_submit can intercept submission of application login
forms. It retrieves the login and password information from the POST
HTTP request, runs PAM authentication with those credentials, and sets
the REMOTE_USER environment variable if the authentication passes.

%prep
%setup -q -n %{name}-%{version}

%build
%{_httpd_apxs} -c -Wc,"%{optflags} -Wall -pedantic -std=c99" mod_intercept_form_submit.c
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
echo > intercept_form_submit.confx
echo "# Load the module in %{_httpd_modconfdir}/55-intercept_form_submit.conf" >> intercept_form_submit.confx
cat intercept_form_submit.conf >> intercept_form_submit.confx
%else
cat intercept_form_submit.module > intercept_form_submit.confx
cat intercept_form_submit.conf >> intercept_form_submit.confx
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -Dm 755 .libs/mod_intercept_form_submit.so $RPM_BUILD_ROOT%{_httpd_moddir}/mod_intercept_form_submit.so

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
install -Dp -m 0644 intercept_form_submit.module $RPM_BUILD_ROOT%{_httpd_modconfdir}/55-intercept_form_submit.conf
%endif
install -Dp -m 0644 intercept_form_submit.confx $RPM_BUILD_ROOT%{_httpd_confdir}/intercept_form_submit.conf

%files
%license LICENSE
%doc README docs/*
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/55-intercept_form_submit.conf
%endif
%config(noreplace) %{_httpd_confdir}/intercept_form_submit.conf
%{_httpd_moddir}/*.so

%changelog
* Mon Dec 30 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.2.0-8
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Feb 18 2022 Jan Pazdziora <jpazdziora@redhat.com> - 1.2.0-1
- 2055636 - rebase to upstream version 1.2.0.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.0-7
- https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

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

* Wed Nov 23 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.1.0-1
- Logging improvements.

* Fri May 06 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.0.1-1
- Add support for InterceptGETOnSuccess.

* Mon Mar 21 2016 Jan Pazdziora <jpazdziora@redhat.com> - 1.0.0-1
- 1319094 - the Requires(pre) httpd does not seem to be needed.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.8-1
- 1109923 - Fix module loading/configuration for Apache 2.4.
- Document the runtime dependency on pam_authenticate_with_login_password.
- Comment/code cleanup.

* Tue May 13 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.7-1
- No longer call lookup_identity_hook explicitly, hook order does
  the same.
- Silence compile warnings by specifying C99.

* Tue Apr 15 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.6-1
- Add support for InterceptFormLoginRealms.

* Thu Jan 30 2014 Jan Pazdziora <jpazdziora@redhat.com> - 0.9.5-1
- 1058809 - .spec changes for Fedora package review.
