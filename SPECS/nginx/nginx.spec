%global nginx_user nginx
%global njs_version 0.7.12
%global opentelemetry_cpp_contrib_git_commit 37e4466d882cbddff6f607a20fe327060de76166

Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
# Currently on "stable" version of nginx from https://nginx.org/en/download.html.
# Note: Stable versions are even (1.20), mainline versions are odd (1.21)
Version:        1.22.1
Release:        11%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://nginx.org/
Source0:        https://nginx.org/download/%{name}-%{version}.tar.gz
Source1:        nginx.service
Source2:        https://github.com/nginx/njs/archive/refs/tags/%{njs_version}.tar.gz#/%{name}-njs-%{njs_version}.tar.gz
Source3:        https://github.com/open-telemetry/opentelemetry-cpp-contrib/archive/%{opentelemetry_cpp_contrib_git_commit}.tar.gz#/opentelemetry-cpp-contrib-%{opentelemetry_cpp_contrib_git_commit}.tar.gz
Patch0:         CVE-2023-44487.patch
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  pcre2-devel
BuildRequires:  readline-devel
BuildRequires:  which
BuildRequires:  zlib-devel
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-mimetypes

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%package filesystem
Summary:        The basic directory layout for the Nginx server
BuildArch:      noarch
Requires(pre):  shadow-utils

%description filesystem
The nginx-filesystem package contains the basic directory layout
for the Nginx server including the correct permissions for the
directories.

%package otel_ngx_module
License:        Apache-2.0
Summary:        OpenTelemetry Nginx Module
BuildRequires:  grpc-devel
BuildRequires:  opentelemetry-cpp-devel
BuildRequires:  protobuf-devel
Requires:       opentelemetry-cpp

%description otel_ngx_module
The OpenTelemetry module for Nginx

%prep
%autosetup -p1
pushd ../
mkdir nginx-njs
tar -C nginx-njs -xf %{SOURCE2}
mkdir otel-cpp-contrib
tar -C otel-cpp-contrib -xf %{SOURCE3}
# The following change is a build break in upstream and a PR has been raised to fix it.
# PR: https://github.com/open-telemetry/opentelemetry-cpp-contrib/pull/314
sed -i \
        '/\#include <opentelemetry\/sdk\/trace\/processor.h>$/a \#include <opentelemetry\/sdk\/trace\/batch_span_processor_options.h>' \
        otel-cpp-contrib/opentelemetry-cpp-contrib-%{opentelemetry_cpp_contrib_git_commit}/instrumentation/nginx/src/otel_ngx_module.cpp
popd

%build
sh configure \
    --add-module=../nginx-njs/njs-%{njs_version}/nginx   \
    --add-dynamic-module=../otel-cpp-contrib/opentelemetry-cpp-contrib-%{opentelemetry_cpp_contrib_git_commit}/instrumentation/nginx   \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf    \
    --error-log-path=%{_var}/log/nginx/error.log   \
    --group=%{nginx_user} \
    --http-log-path=%{_var}/log/nginx/access.log   \
    --lock-path=%{_var}/run/nginx.lock             \
    --pid-path=%{_var}/run/nginx.pid               \
    --prefix=%{_sysconfdir}/nginx              \
    --sbin-path=%{_sbindir}/nginx                 \
    --user=%{nginx_user} \
    --with-stream_ssl_module \
    --with-http_auth_request_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_realip_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-ipv6 \
    --with-pcre \
    --with-stream \
    --with-compat

%make_build

%install
%make_install
install -vdm755 %{buildroot}%{_libdir}/systemd/system
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/nginx/log
ln -sfv %{_var}/opt/nginx/log %{buildroot}%{_var}/log/nginx
install -p -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/nginx.service

# Using the ones provided through the "nginx-mimetype" package.
rm -f %{buildroot}%{_sysconfdir}/%{name}/mime.types

%pre filesystem
getent group %{nginx_user} > /dev/null || groupadd -r %{nginx_user}
getent passwd %{nginx_user} > /dev/null || \
    useradd -r -d %{_localstatedir}/lib/nginx -g %{nginx_user} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0

%files
%defattr(-,root,root)
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/koi-utf
%config(noreplace) %{_sysconfdir}/%{name}/koi-win
%config(noreplace) %{_sysconfdir}/%{name}/mime.types.default
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params.default
%{_sysconfdir}/%{name}/html/*
%{_sysconfdir}/%{name}/win-utf
%{_sbindir}/*
%{_libdir}/systemd/system/nginx.service
%dir %{_var}/opt/nginx/log
%{_var}/log/nginx

%files filesystem
%dir %{_sysconfdir}/%{name}

%files otel_ngx_module
%license ../otel-cpp-contrib/opentelemetry-cpp-contrib-%{opentelemetry_cpp_contrib_git_commit}/LICENSE
%{_sysconfdir}/%{name}/modules/otel_ngx_module.so

%changelog
* Thu Oct 05 2023 Dan Streetman <ddstreet@ieee.org> - 1.22.1-11
- Fix CVE-2023-44487

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.22.1-10
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Aug 17 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.22.1-9
- Add otel_ngx_module subpackage

* Thu Aug 10 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.22.1-8
- Configure with `--with-stream_ssl_module` to enable support for stream proxy server with SSL/TLS

* Mon Jul 31 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.22.1-7
- Configure with `--with-compat` to enable dynamic modules compatibility

* Wed Jul 12 2023 Pete Birley <petebirley@microsoft.com> - 1.22.1-6
- Enable building with http_gunzip_module

* Mon Apr 17 2023 Olivia Crain <oliviacrain@microsoft.com> - 1.22.1-5
- Upgrade bundled njs version to 0.7.12 to fix CVE-2020-19692, CVE-2020-19695
- Use SPDX expression in license tag

* Tue Apr 04 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.22.1-4
- Enable building with ngx_http_gzip_static_module

* Mon Mar 27 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.22.1-3
- Enable building with ngx_http_realip_module

* Wed Nov 30 2022 Jon Slobodzian <joslobo@microsoft.com> - 1.22.1-2
- Enable http2 support

* Fri Oct 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.22.1-1
- Move to stable release 

* Tue Oct 25 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.2-1
- Upgrade to 1.23.2 (fixes CVE-2022-41741 and CVE-2022-41742)

* Tue Apr 19 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.20.2-2
- Addressing CVE-2021-3618.

* Wed Feb 23 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.20.2-1
- Upgrading to latest version 1.20.2 from "stable" branch.

* Wed Oct 13 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.1-2
- Split out "nginx-filesystem" using Fedora 34 spec (license: MIT) as guidance.
- Removing conflicts with "nginx-mimetypes" over "mime.types".
- Fixed changelog history to include version update.

* Fri Jun 11 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.20.1-1
- Update to version 1.20.1 to resolve CVE-2021-23017

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.1-4
- Merge the following releases from 1.0 to dev branch
- lihl@microsoft.com, 1.16.1-3: Used autosetup, Added patch to resolve CVE-2019-20372
- nicolasg@microsoft.com, 1.16.1-4: nopatch for CVE-2009-4487

* Wed Feb 10 2021 Henry Li <lihl@microsoft.com> - 1.16.1-3
- Add Provides for nginx-filesystem from nginx

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.16.1-2
- Added %%license line automatically

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 1.16.1-1
- Update to version 1.16.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.15.3-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Mar 15 2019 Keerthana K <keerthanak@vmware.com> - 1.15.3-4
- Enable http_stub_status_module.

* Wed Nov 07 2018 Ajay Kaher <akaher@vmware.com> - 1.15.3-3
- mark config files as non replaceable on upgrade.

* Mon Sep 17 2018 Keerthana K <keerthanak@vmware.com> - 1.15.3-2
- Adding http_auth_request_module and http_sub_module.

* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 1.15.3-1
- Upgrade to version 1.15.3

* Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> - 1.13.8-3
- Restarting nginx on failure.

* Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> - 1.13.8-2
- adding module njs.

* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 1.13.8-1
- Update to version 1.13.8 to support nginx-ingress

* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com> - 1.13.5-2
- Fixed the log file directory structure

* Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.13.5-1
- Update to version 1.13.5

* Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.11.13-2
- adding module stream to nginx.

* Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.11.13-1
- update to 1.11.13

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 1.10.0-5
- Add patch for CVE-2016-4450

* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> - 1.10.0-4
- Removed packaging of debug files

* Fri Jul 8 2016 Divya Thaluru <dthaluru@vmware.com> - 1.10.0-3
- Modified default pid filepath and fixed nginx systemd service

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.10.0-2
- GA - Bump release of all rpms

* Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.10.0-1
- Initial build. First version
