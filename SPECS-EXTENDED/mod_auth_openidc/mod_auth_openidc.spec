Vendor:         Microsoft Corporation
Distribution:   Mariner
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
%{!?_httpd_moddir: %{expand: %%global _httpd_moddir %%{_libdir}/httpd/modules}}
%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %{_sysconfdir}/httpd/conf.d}}

# Optionally build with hiredis if --with hiredis is passed
%{!?_with_hiredis: %{!?_without_hiredis: %global _without_hiredis --without-hiredis}}
# It is an error if both or neither required options exist.
%{?_with_hiredis: %{?_without_hiredis: %{error: both _with_hiredis and _without_hiredis}}}
%{!?_with_hiredis: %{!?_without_hiredis: %{error: neither _with_hiredis nor _without_hiredis}}}

# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

%global httpd_pkg_cache_dir /var/cache/httpd/mod_auth_openidc

Name:		mod_auth_openidc
Version:	2.4.9.4
Release:	1%{?dist}
Summary:	OpenID Connect auth module for Apache HTTP Server

License:	ASL 2.0
URL:		https://github.com/zmartzone/mod_auth_openidc
Source0:	https://github.com/zmartzone/mod_auth_openidc/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:	httpd-devel
BuildRequires:	openssl-devel
BuildRequires:	curl-devel
BuildRequires:	jansson-devel
BuildRequires:	pcre-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cjose-devel
BuildRequires:	jq-devel
%{?_with_hiredis:BuildRequires: hiredis-devel}
Requires:	httpd-mmn

%description
This module enables an Apache 2.x web server to operate as
an OpenID Connect Relying Party and/or OAuth 2.0 Resource Server.

%prep
%setup -q

%build
# workaround rpm-buildroot-usage
export MODULES_DIR=%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'
autoreconf
%configure \
  --with-jq=/usr/lib64/ \
  %{?_with_hiredis} \
  %{?_without_hiredis}

%{make_build}

%check
export MODULES_DIR=%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'
%{make_build} test

%install
mkdir -p $RPM_BUILD_ROOT%{_httpd_moddir}
make install MODULES_DIR=$RPM_BUILD_ROOT%{_httpd_moddir}

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_modconfdir}
echo 'LoadModule auth_openidc_module modules/mod_auth_openidc.so' > \
	$RPM_BUILD_ROOT%{_httpd_modconfdir}/10-auth_openidc.conf

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_confdir}
install -m 644 auth_openidc.conf $RPM_BUILD_ROOT%{_httpd_confdir}
# Adjust httpd cache location in install config file
sed -i 's!/var/cache/apache2/!/var/cache/httpd/!' $RPM_BUILD_ROOT%{_httpd_confdir}/auth_openidc.conf
install -m 700 -d $RPM_BUILD_ROOT%{httpd_pkg_cache_dir}
install -m 700 -d $RPM_BUILD_ROOT%{httpd_pkg_cache_dir}/metadata
install -m 700 -d $RPM_BUILD_ROOT%{httpd_pkg_cache_dir}/cache


%files
%if 0%{?rhel} && 0%{?rhel} < 7
%doc LICENSE.txt
%else
%license LICENSE.txt
%endif
%doc ChangeLog
%doc AUTHORS
%doc README.md
%{_httpd_moddir}/mod_auth_openidc.so
%config(noreplace) %{_httpd_modconfdir}/10-auth_openidc.conf
%config(noreplace) %{_httpd_confdir}/auth_openidc.conf
%dir %attr(0700, apache, apache) %{httpd_pkg_cache_dir}
%dir %attr(0700, apache, apache) %{httpd_pkg_cache_dir}/metadata
%dir %attr(0700, apache, apache) %{httpd_pkg_cache_dir}/cache

%changelog
* Tue Oct 11 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.9.4-1
- Upgrade to 2.4.9.4

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.2.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun May 10 2020 Jakub Hrozek <jhrozek@redhat.com> - 2.4.2.1-1
- New upstream version 2.4.2.1
- Resolves: rhbz#1805104 - CVE-2019-20479 mod_auth_openidc: open redirect
                           issue exists in URLs with slash and backslash
                           [fedora-all]
- Resolves: rhbz#1816883 - mod_auth_openidc-2.4.2.1 is available

* Thu Feb 13 2020 Tom Stellard <tstellar@redhat.com> - 2.4.1-2
- Use make_build macro instead of just make
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Mon Feb  3 2020 Jakub Hrozek <jhrozek@redhat.com> - 2.4.1-1
- New upstream version 2.4.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.4.0.4-1
- New upstream version 2.4.0.4

* Fri Oct  4 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.4.0.3-1
- New upstream version 2.4.0.3

* Fri Aug 23 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.4.0
- New upstream version 2.4.0
- Resolves: rhbz#1374884 - mod_auth_openidc-2.4.0 is available

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 16 2018  <jdennis@redhat.com> - 2.3.7-3
- update test-segfault.patch to match upstream

* Tue Aug 14 2018  <jdennis@redhat.com> - 2.3.7-2
- Resolves: rhbz# 1614977 - fix unit test segfault,
  the problem was not limited exclusively to s390x, but s390x provoked it.

* Wed Aug  1 2018  <jdennis@redhat.com> - 2.3.7-1
- upgrade to upstream 2.3.7

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 2.3.5-1
- Rebase to 2.3.5

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.10.1-7
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 18 2017 John Dennis <jdennis@redhat.com> - 1.8.10.1-3
- Resolves: #1423956 fails to build with openssl 1.1.x
  Also rolls up all fixes to jose library before the change over to cjose

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 John Dennis <jdennis@redhat.com> - 1.8.10.1-1
- Upgrade to new upstream
  See /usr/share/doc/mod_auth_openidc/ChangeLog for details

* Tue Mar 29 2016 John Dennis <jdennis@redhat.com> - 1.8.8-4
- Add %%check to run test

* Wed Mar 23 2016 John Dennis <jdennis@redhat.com> - 1.8.8-3
- Make building with redis support optional (defaults to without)

* Mon Mar 21 2016 John Dennis <jdennis@redhat.com> - 1.8.8-2
- Add missing unpackaged files/directories

  Add to doc: README.md, DISCLAIMER, AUTHORS
  Add to httpd/conf.d: auth_openidc.conf
  Add to /var/cache: /var/cache/httpd/mod_auth_openidc/cache
                     /var/cache/httpd/mod_auth_openidc/metadata

* Thu Mar 10 2016 Jan Pazdziora <jpazdziora@redhat.com> 1.8.8-1
- Update to 1.8.8 (#1316528)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 09 2016 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.8.7-1
- Update to 1.8.7 (#1297080)

* Sat Nov 07 2015 Jan Pazdziora <jpazdziora@redhat.com> 1.8.6-1
- Initial packaging for Fedora 23.
