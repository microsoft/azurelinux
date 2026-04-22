## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global  _hardened_build     1
%global  nginx_user          nginx

# Disable strict symbol checks in the link editor.
# See: https://src.fedoraproject.org/rpms/redhat-rpm-config/c/078af19
%undefine _strict_symbol_defs_build

%bcond_with geoip

# nginx gperftools support should be disabled for RHEL >= 8
# see: https://bugzilla.redhat.com/show_bug.cgi?id=1931402
%if 0%{?rhel} >= 8
%global with_gperftools 0
%else
# gperftools exists only on selected arches
# gperftools *detection* is failing on ppc64*, possibly only configure
# bug, but disable anyway.
%ifnarch s390 s390x ppc64 ppc64le
%global with_gperftools 1
%endif
%endif

%global with_aio 1

%if 0%{?fedora} > 40 || 0%{?rhel} > 9
%bcond_with engine
%else
%bcond_without engine
%endif

%if 0%{?fedora} > 22
%global with_mailcap_mimetypes 1
%endif

# kTLS requires OpenSSL 3.0 (default in F36+ and EL9+, available in EPEL8)
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 8
%global with_ktls 1
%endif

# Build against OpenSSL 3 on EL8
%if 0%{?rhel} == 8
%global openssl_pkgversion 3
%endif

# Cf. https://www.nginx.com/blog/creating-installable-packages-dynamic-modules/
%global nginx_abiversion %{version}

%global nginx_moduledir %{_libdir}/nginx/modules
%global nginx_moduleconfdir %{_datadir}/nginx/modules
%global nginx_srcdir %{_usrsrc}/%{name}-%{version}-%{release}

# Do not generate provides/requires from nginx sources
%global __provides_exclude_from ^%{nginx_srcdir}/.*$
%global __requires_exclude_from ^%{nginx_srcdir}/.*$


Name:              nginx
Epoch:             2
Version:           1.28.2
Release:           %autorelease

Summary:           A high performance web server and reverse proxy server
License:           BSD-2-Clause
URL:               https://nginx.org

Source0:           https://nginx.org/download/nginx-%{version}.tar.gz
Source1:           https://nginx.org/download/nginx-%{version}.tar.gz.asc
# Keys are found here: https://nginx.org/en/pgp_keys.html
Source3:           https://nginx.org/keys/arut.key
Source4:           https://nginx.org/keys/pluknet.key
Source5:           https://nginx.org/keys/sb.key
Source6:           https://nginx.org/keys/thresh.key
Source10:          nginx.service
Source11:          nginx.logrotate
Source12:          nginx.conf
Source13:          nginx-upgrade
Source14:          nginx-upgrade.8
Source15:          macros.nginxmods.in
Source16:          nginxmods.attr
Source17:          nginx-ssl-pass-dialog
Source18:          nginx@.service
Source19:          nginx.sysusers
Source20:          nginx.tmpfiles
Source102:         nginx-logo.png
Source200:         README.dynamic
Source220:         instance.conf

# removes -Werror in upstream build scripts.  -Werror conflicts with
# -D_FORTIFY_SOURCE=2 causing warnings to turn into errors.
Patch0:            0001-remove-Werror-in-upstream-build-scripts.patch

# downstream patch - fix PIDFile race condition (rhbz#1869026)
# rejected upstream: https://trac.nginx.org/nginx/ticket/1897
Patch1:            0002-fix-PIDFile-handling.patch

# downstream patch - Add ssl-pass-phrase-dialog helper script for
# encrypted private keys with pass phrase decryption
Patch2:            0003-Add-SSL-passphrase-dialog.patch

# downstream patch - Disable ENGINE support by default for F41+
Patch3:            0004-Disable-ENGINE-support.patch

# downstream patch - Compile perl module with O2
Patch4:            0005-Compile-perl-module-with-O2.patch

# upstream patch - https://github.com/nginx/nginx/pull/1089
Patch5:            0006-Clarify-binding-behavior-of-t-option.patch

BuildRequires:     make
BuildRequires:     gcc
BuildRequires:     gnupg2
%if 0%{?with_gperftools}
BuildRequires:     gperftools-devel
%endif
BuildRequires:     libxcrypt-devel
BuildRequires:     openssl%{?openssl_pkgversion}-devel
BuildRequires:     pcre2-devel
%if 0%{?fedora} || 0%{?rhel} > 8
BuildRequires:     zlib-ng-devel
%else
BuildRequires:     zlib-devel
%endif

Requires:          nginx-filesystem = %{epoch}:%{version}-%{release}
Requires:          system-logos-httpd

Provides:          webserver
Recommends:        logrotate
Requires:          %{name}-core = %{epoch}:%{version}-%{release}

BuildRequires:     systemd
BuildRequires:     systemd-rpm-macros
%{?systemd_requires}
# For external nginx modules
Provides:          nginx(abi) = %{nginx_abiversion}

%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.

%package core
Summary: nginx minimal core
%if 0%{?with_mailcap_mimetypes}
Requires:          nginx-mimetypes
%endif
Requires:          openssl%{?openssl_pkgversion}-libs
Requires(pre):     nginx-filesystem
Conflicts:         nginx < 1:1.20.2-4

%description core
nginx minimal core

%package all-modules
Summary:           A meta package that installs all available Nginx modules
BuildArch:         noarch

%if %{with geoip}
Requires:          nginx-mod-http-geoip = %{epoch}:%{version}-%{release}
%endif
Requires:          nginx-mod-http-image-filter = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-http-perl = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-http-xslt-filter = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-mail = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-stream = %{epoch}:%{version}-%{release}

%description all-modules
Meta package that installs all available nginx modules.

%package filesystem
Summary:           The basic directory layout for the Nginx server
BuildArch:         noarch
# RHEL 9 compat, remove after RHEL 9 EOL
%{?sysusers_requires_compat}


%description filesystem
The nginx-filesystem package contains the basic directory layout
for the Nginx server including the correct permissions for the
directories.

%if %{with geoip}
%package mod-http-geoip
Summary:           Nginx HTTP geoip module
BuildRequires:     GeoIP-devel
Requires:          nginx(abi) = %{nginx_abiversion}
Requires:          GeoIP

%description mod-http-geoip
%{summary}.
%endif

%package mod-http-image-filter
Summary:           Nginx HTTP image filter module
BuildRequires:     gd-devel
Requires:          nginx(abi) = %{nginx_abiversion}
Requires:          gd

%description mod-http-image-filter
%{summary}.

%package mod-http-perl
Summary:           Nginx HTTP perl module
BuildRequires:     perl-devel
BuildRequires:     perl-generators
BuildRequires:     perl(ExtUtils::Embed)
Requires:          nginx(abi) = %{nginx_abiversion}
Requires:          perl(constant)

%description mod-http-perl
%{summary}.

%package mod-http-xslt-filter
Summary:           Nginx XSLT module
BuildRequires:     libxslt-devel
Requires:          nginx(abi) = %{nginx_abiversion}

%description mod-http-xslt-filter
%{summary}.

%package mod-mail
Summary:           Nginx mail modules
Requires:          nginx(abi) = %{nginx_abiversion}

%description mod-mail
%{summary}.

%package mod-stream
Summary:           Nginx stream modules
Requires:          nginx(abi) = %{nginx_abiversion}

%description mod-stream
%{summary}.

%package mod-devel
Summary:           Nginx module development files
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          make
Requires:          gcc
Requires:          gd-devel
%if 0%{?with_gperftools}
Requires:          gperftools-devel
%endif
%if %{with geoip}
Requires:          GeoIP-devel
%endif
Requires:          libxslt-devel
Requires:          openssl%{?openssl_pkgversion}-devel
Requires:          pcre2-devel
Requires:          perl-devel
Requires:          perl(ExtUtils::Embed)
Requires:          zlib-devel

%description mod-devel
%{summary}.


%prep
# Combine all keys from upstream into one file
cat %{S:3} %{S:4} %{S:5} %{S:6} > %{_builddir}/%{name}.gpg
%{gpgverify} --keyring='%{_builddir}/%{name}.gpg' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
cp %{SOURCE200} %{SOURCE10} %{SOURCE12} %{SOURCE18} %{SOURCE220} .

%if 0%{?openssl_pkgversion}
sed \
  -e 's|\(ngx_feature_path=\)$|\1%{_includedir}/openssl%{openssl_pkgversion}|' \
  -e 's|\(ngx_feature_libs="\)|\1-L%{_libdir}/openssl%{openssl_pkgversion} |' \
  -i auto/lib/openssl/conf
%endif

# Prepare template config for instances
sed -e '/^error_log /s|error\.log|@INSTANCE@_error.log|' \
    -e '/^pid /s|nginx\.pid|nginx-@INSTANCE@.pid|' \
    -e '/^ *access_log/s|access\.log|@INSTANCE@_access.log|' \
    nginx.conf >> instance.conf
touch -r %{SOURCE12} instance.conf

# Prepare sources for installation
cp -a ../%{name}-%{version} ../%{name}-%{version}-%{release}-src
mv ../%{name}-%{version}-%{release}-src .


%build
# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}
# So the perl module finds its symbols:
nginx_ldopts="$RPM_LD_FLAGS -Wl,-E -O2"
if ! ./configure \
    --prefix=%{_datadir}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --modules-path=%{nginx_moduledir} \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --http-log-path=%{_localstatedir}/log/nginx/access.log \
    --http-client-body-temp-path=%{_localstatedir}/lib/nginx/tmp/client_body \
    --http-proxy-temp-path=%{_localstatedir}/lib/nginx/tmp/proxy \
    --http-fastcgi-temp-path=%{_localstatedir}/lib/nginx/tmp/fastcgi \
    --http-uwsgi-temp-path=%{_localstatedir}/lib/nginx/tmp/uwsgi \
    --http-scgi-temp-path=%{_localstatedir}/lib/nginx/tmp/scgi \
    --pid-path=/run/nginx.pid \
    --lock-path=/run/lock/subsys/nginx \
    --user=%{nginx_user} \
    --group=%{nginx_user} \
    --with-compat \
    --with-debug \
%if 0%{?with_aio}
    --with-file-aio \
%endif
%if 0%{?with_gperftools}
    --with-google_perftools_module \
%endif
    --with-http_addition_module \
    --with-http_auth_request_module \
    --with-http_dav_module \
    --with-http_degradation_module \
    --with-http_flv_module \
%if %{with geoip}
    --with-http_geoip_module=dynamic \
    --with-stream_geoip_module=dynamic \
%endif
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_image_filter_module=dynamic \
    --with-http_mp4_module \
    --with-http_perl_module=dynamic \
    --with-http_random_index_module \
    --with-http_realip_module \
    --with-http_secure_link_module \
    --with-http_slice_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-http_sub_module \
    --with-http_v2_module \
    --with-http_v3_module \
    --with-http_xslt_module=dynamic \
    --with-mail=dynamic \
    --with-mail_ssl_module \
%if 0%{?with_ktls}
    --with-openssl-opt=enable-ktls \
%endif
%if %{without engine}
    --without-engine \
%endif
    --with-pcre \
    --with-pcre-jit \
    --with-stream=dynamic \
    --with-stream_realip_module \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-threads \
    --with-cc-opt="%{optflags} $(pcre2-config --cflags)" \
    --with-ld-opt="$nginx_ldopts"; then
  : configure failed
  cat objs/autoconf.err
  exit 1
fi

%make_build


%install
%make_install INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

install -p -D -m 0644 ./nginx.service \
    %{buildroot}%{_unitdir}/nginx.service
install -p -D -m 0644 ./nginx@.service \
    %{buildroot}%{_unitdir}/nginx@.service
install -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/systemd/system/nginx.service.d
install -p -d -m 0755 %{buildroot}%{_unitdir}/nginx.service.d

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/nginx/conf.d
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/nginx/default.d

install -p -d -m 0700 %{buildroot}%{_localstatedir}/lib/nginx
install -p -d -m 0700 %{buildroot}%{_localstatedir}/lib/nginx/tmp
install -p -d -m 0700 %{buildroot}%{_localstatedir}/log/nginx

install -p -d -m 0755 %{buildroot}%{_datadir}/nginx/html
install -p -d -m 0755 %{buildroot}%{nginx_moduleconfdir}
install -p -d -m 0755 %{buildroot}%{nginx_moduledir}

install -p -m 0644 ./nginx.conf \
    %{buildroot}%{_sysconfdir}/nginx

rm -f %{buildroot}%{_datadir}/nginx/html/index.html
rm -f %{buildroot}%{_datadir}/nginx/html/50x.html

ln -s ../../testpage/index.html \
      %{buildroot}%{_datadir}/nginx/html/index.html
install -p -m 0644 %{SOURCE102} \
    %{buildroot}%{_datadir}/nginx/html
ln -s nginx-logo.png %{buildroot}%{_datadir}/nginx/html/poweredby.png
mkdir -p %{buildroot}%{_datadir}/nginx/html/icons

# Symlink for the powered-by-$DISTRO image:
ln -s ../../../pixmaps/poweredby.png \
      %{buildroot}%{_datadir}/nginx/html/icons/poweredby.png

%if 0%{?rhel} >= 9
ln -s ../../pixmaps/system-noindex-logo.png \
      %{buildroot}%{_datadir}/nginx/html/system_noindex_logo.png
%endif

%if 0%{?with_mailcap_mimetypes}
rm -f %{buildroot}%{_sysconfdir}/nginx/mime.types
%endif

install -p -D -m 0644 %{_builddir}/nginx-%{version}/objs/nginx.8 \
    %{buildroot}%{_mandir}/man8/nginx.8

install -p -D -m 0755 %{SOURCE13} %{buildroot}%{_bindir}/nginx-upgrade
install -p -D -m 0644 %{SOURCE14} %{buildroot}%{_mandir}/man8/nginx-upgrade.8

for i in ftdetect ftplugin indent syntax; do
    install -p -D -m644 contrib/vim/${i}/nginx.vim \
        %{buildroot}%{_datadir}/vim/vimfiles/${i}/nginx.vim
done

%if %{with geoip}
echo 'load_module "%{nginx_moduledir}/ngx_http_geoip_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-http-geoip.conf
%endif
echo 'load_module "%{nginx_moduledir}/ngx_http_image_filter_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-http-image-filter.conf
echo 'load_module "%{nginx_moduledir}/ngx_http_perl_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-http-perl.conf
echo 'load_module "%{nginx_moduledir}/ngx_http_xslt_filter_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-http-xslt-filter.conf
echo 'load_module "%{nginx_moduledir}/ngx_mail_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-mail.conf
echo 'load_module "%{nginx_moduledir}/ngx_stream_module.so";' \
    > %{buildroot}%{nginx_moduleconfdir}/mod-stream.conf

# Install files for supporting nginx module builds
## Install source files
mkdir -p %{buildroot}%{_usrsrc}
mv %{name}-%{version}-%{release}-src %{buildroot}%{nginx_srcdir}
## Install rpm macros
mkdir -p %{buildroot}%{_rpmmacrodir}
sed -e "s|@@NGINX_ABIVERSION@@|%{nginx_abiversion}|g" \
    -e "s|@@NGINX_MODDIR@@|%{nginx_moduledir}|g" \
    -e "s|@@NGINX_MODCONFDIR@@|%{nginx_moduleconfdir}|g" \
    -e "s|@@NGINX_SRCDIR@@|%{nginx_srcdir}|g" \
    %{SOURCE15} > %{buildroot}%{_rpmmacrodir}/macros.nginxmods
## Install dependency generator
install -Dpm0644 %{SOURCE16} %{buildroot}%{_fileattrsdir}/nginxmods.attr

# install http-ssl-pass-dialog
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m755 $RPM_SOURCE_DIR/nginx-ssl-pass-dialog \
        $RPM_BUILD_ROOT%{_libexecdir}/nginx-ssl-pass-dialog

# install sysusers file
install -p -D -m 0644 %{SOURCE19} %{buildroot}%{_sysusersdir}/nginx.conf

# tmpfiles.d configuration
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 644 -p %{SOURCE20} %{buildroot}%{_tmpfilesdir}/nginx.conf

%pre filesystem
# RHEL 9 compat, remove after RHEL 9 EOL
%sysusers_create_compat %{SOURCE19}

%post
%systemd_post nginx.service

%if %{with geoip}
%post mod-http-geoip
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi
%endif

%post mod-http-image-filter
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%post mod-http-perl
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%post mod-http-xslt-filter
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%post mod-mail
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%post mod-stream
if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun nginx.service

%postun
%systemd_postun nginx.service
if [ $1 -ge 1 ]; then
    /usr/bin/nginx-upgrade >/dev/null 2>&1 || :
fi

%files
%{_datadir}/nginx/html/*
%{_bindir}/nginx-upgrade
%{_datadir}/vim/vimfiles/ftdetect/nginx.vim
%{_datadir}/vim/vimfiles/ftplugin/nginx.vim
%{_datadir}/vim/vimfiles/syntax/nginx.vim
%{_datadir}/vim/vimfiles/indent/nginx.vim
%{_mandir}/man3/nginx.3pm*
%{_mandir}/man8/nginx.8*
%{_mandir}/man8/nginx-upgrade.8*
%{_unitdir}/nginx.service
%{_unitdir}/nginx@.service
%{_libexecdir}/nginx-ssl-pass-dialog

%files core
%license LICENSE
%doc CHANGES README.md README.dynamic instance.conf
%{_sbindir}/nginx
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%if ! 0%{?with_mailcap_mimetypes}
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%endif
%config(noreplace) %{_sysconfdir}/nginx/mime.types.default
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf.default
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/win-utf
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%attr(770,%{nginx_user},root) %dir %{_localstatedir}/lib/nginx
%attr(770,%{nginx_user},root) %dir %{_localstatedir}/lib/nginx/tmp
%{_tmpfilesdir}/nginx.conf
%ghost %attr(640,%{nginx_user},root) %{_localstatedir}/log/nginx/access.log
%ghost %attr(640,%{nginx_user},root) %{_localstatedir}/log/nginx/error.log
%dir %{nginx_moduledir}
%dir %{nginx_moduleconfdir}

%files all-modules

%files filesystem
%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/default.d
%dir %{_sysconfdir}/systemd/system/nginx.service.d
%dir %{_unitdir}/nginx.service.d
%attr(711,root,root) %dir %{_localstatedir}/log/nginx
%{_sysusersdir}/nginx.conf

%if %{with geoip}
%files mod-http-geoip
%{nginx_moduleconfdir}/mod-http-geoip.conf
%{nginx_moduledir}/ngx_http_geoip_module.so
%endif

%files mod-http-image-filter
%{nginx_moduleconfdir}/mod-http-image-filter.conf
%{nginx_moduledir}/ngx_http_image_filter_module.so

%files mod-http-perl
%{nginx_moduleconfdir}/mod-http-perl.conf
%{nginx_moduledir}/ngx_http_perl_module.so
%dir %{perl_vendorarch}/auto/nginx
%{perl_vendorarch}/nginx.pm
%{perl_vendorarch}/auto/nginx/nginx.so

%files mod-http-xslt-filter
%{nginx_moduleconfdir}/mod-http-xslt-filter.conf
%{nginx_moduledir}/ngx_http_xslt_filter_module.so

%files mod-mail
%{nginx_moduleconfdir}/mod-mail.conf
%{nginx_moduledir}/ngx_mail_module.so

%files mod-stream
%{nginx_moduleconfdir}/mod-stream.conf
%{nginx_moduledir}/ngx_stream_module.so

%files mod-devel
%{_rpmmacrodir}/macros.nginxmods
%{_fileattrsdir}/nginxmods.attr
%{nginx_srcdir}/


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2:1.28.2-2
- Latest state for nginx

* Wed Feb 04 2026 Felix Kaechele <felix@kaechele.ca> - 2:1.28.2-1
- Update to 1.28.2
- fixes CVE-2026-1642
- move log directory to nginx-filesystem subpackage (PR#20)
- delete Maxim Dounin's key, it's no longer listed on the nginx website

* Wed Feb 04 2026 Nicolas Chauvet <kwizart@gmail.com> - 2:1.28.1-6
- Move log/nginx in filesystem sub-package

* Tue Jan 27 2026 Luboš Uhliarik <luhliari@redhat.com> - 2:1.28.1-5
- Clarify binding behavior of -t option.

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.28.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 02 2026 Felix Kaechele <felix@kaechele.ca> - 2:1.28.1-3
- cleanups and fixes
- remove RHEL 7 compatibility
- add RHEL 9 compatibility and EOL comments
- restore RHEL 8 compatibility

* Sat Dec 27 2025 Aleksei Bavshin <alebastr@fedoraproject.org> - 2:1.28.1-2
- Fix crash in stream SSL configuration (rhbz#2421955)

* Wed Dec 24 2025 Felix Kaechele <felix@kaechele.ca> - 2:1.28.1-1
- update to 1.28.1

* Thu Nov 20 2025 Luboš Uhliarik <luhliari@redhat.com> - 2:1.28.0-5
- Remove 50x.html from the nginx-core package

* Tue Sep 16 2025 Luboš Uhliarik <luhliari@redhat.com> - 2:1.28.0-4
- Add tmpfiles.d rules for /var directories (bootc compatibility)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.28.0-2
- Perl 5.42 re-rebuild updated packages

* Tue Jul 08 2025 Luboš Uhliarik <luhliari@redhat.com> - 2:1.28.0-1
- update to 1.28.0
- rewritten 0003-Add-SSL-passphrase-dialog.patch
- README renamed to README.md

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.26.3-2
- Perl 5.42 rebuild

* Thu Feb 06 2025 Felix Kaechele <felix@kaechele.ca> - 2:1.26.3-1
- update to 1.26.3
- fixes SSL session reuse vulnerability (CVE-2025-23419)
- drop zlib-ng patch, the issue was addressed upstream

* Wed Feb 05 2025 Luboš Uhliarik <luhliari@redhat.com> - 2:1.26.2-6
- Use systemd-sysusers

* Mon Feb 03 2025 Joe Orton <jorton@redhat.com> - 2:1.26.2-5
- Add systemd instantiated service nginx@.service, allowing e.g. "systemctl
  start nginx@foobar.service" to start an instance of nginx using
  /etc/nginx/foobar.conf as the configuration.

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 2:1.26.2-4
- Add explicit BR: libxcrypt-devel

* Sat Feb 01 2025 Felix Kaechele <felix@kaechele.ca> - 2:1.26.2-3
- Add zlib-ng patch to fix rhbz#2343318

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 16 2024 Felix Kaechele <felix@kaechele.ca> - 2:1.26.2-1
- Update to 1.26.2
- fixes CVE-2024-7347

* Wed Jul 31 2024 Luboš Uhliarik <luhliari@redhat.com> - 2:1.26.1-6
- Compile perl module with -O2 optimalization

* Wed Jul 31 2024 Luboš Uhliarik <luhliari@redhat.com> - 2:1.26.1-5
- Add -O2 to nginx.so

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Luboš Uhliarik <luhliari@redhat.com> - 2:1.26.1-3
- Disable ENGINE support by default for F41+, add engine bcond

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2:1.26.1-2
- Perl 5.40 rebuild

* Fri May 31 2024 Luboš Uhliarik <luhliari@redhat.com> - 2:1.26.1-1
- Increase nginx's epoch to avoid possible regression in CentOS/RHEL
  (CS-2046)

* Thu May 30 2024 Felix Kaechele <felix@kaechele.ca> - 1:1.26.1-1
- update to 1.26.1
- fixes CVE-2024-32760, CVE-2024-31079, CVE-2024-35200, CVE-2024-34161

* Wed May 22 2024 Luboš Uhliarik <luhliari@redhat.com> - 1:1.26.0-3
- Fix possible segfault introduced in patch which adds ssl-pass-phrase-
  dialog directive
- Add back Maxim's PGP removed by mistake
- Add actual fix of the patch

* Wed May 22 2024 Luboš Uhliarik <luhliari@redhat.com> - 1:1.26.0-2
- Fix possible segfault introduced in patch which adds ssl-pass-phrase-
  dialog directive

* Sun Apr 28 2024 Felix Kaechele <felix@kaechele.ca> - 1:1.26.0-1
- update to 1.26.0
- add Sergey Kandaurov's PGP public key
- add Roman Arutyunyan's PGP public key
- remove Maxim Dounin's PGP public key
- enable experimental HTTP/3 module
- refresh patches
- update default config http2 directive
- remove outdated custom error pages, reducing maintenance burden

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.24.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.24.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 09 2023 Felix Kaechele <felix@kaechele.ca> - 1:1.24.0-6
- Use SPDX license identifier in License tag

* Mon Aug 07 2023 Luboš Uhliarik <luhliari@redhat.com> - 1:1.24.0-5
- Related: #2224582 - Running nginx with systemctl and entering ssl private
  key's pass phrase

* Fri Jul 21 2023 Luboš Uhliarik <luhliari@redhat.com> - 1:1.24.0-4
- Resolves: #2224582 - Running nginx with systemctl and entering ssl
  private key's pass phrase
- added new ssl_pass_phrase_dialog directive which enables setting external
  program for entering password for encrypted private key

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.24.0-2
- Perl 5.38 rebuild

* Tue Apr 11 2023 Felix Kaechele <felix@kaechele.ca> - 1:1.24.0-1
- update to 1.24.0
- update maxim.key (same key, new expiry date)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 19 2022 Felix Kaechele <felix@kaechele.ca> - 1:1.22.1-1
- update 1.22.1
- build against OpenSSL 3 on EL8
- enable kTLS support

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Luboš Uhliarik <luhliari@redhat.com> - 1:1.22.0-3
- Fix nginx downgrade issue after introducing core sub-package

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.22.0-2
- Perl 5.36 rebuild

* Wed May 25 2022 Felix Kaechele <heffer@fedoraproject.org> - 1:1.22.0-1
- update to 1.22.0
- switch to pcre2
- drop CVE-2021-3618 patch, it's upstreamed
- add signing key of Konstantin Pavlov
- add stream_geoip_module and stream_realip_module

* Thu Mar 24 2022 Honza Horak <hhorak@redhat.com> - 1:1.20.2-4
- Introduce core sub-package for having a daemon only with a minimal footprint

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.2-1
- update to 1.20.2

* Mon Oct 18 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.1-9
- fix installation of nginxmods.attr for EPEL 7

* Mon Oct 18 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.1-8
- Fix "file size changed while zipping" when rotating logs (rhbz#1980948,2015249,2015243)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1:1.20.1-7
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 10 2021 Neal Gompa <ngompa@datto.com> - 1:1.20.1-6
- Add -mod-devel subpackage for building external nginx modules (rhbz#1989778)

* Mon Aug 09 2021 Luboš Uhliarik <luhliari@redhat.com> - 1:1.20.1-5
- Add symlink used by system-logos-httpd

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.1-3
- fix for CVE-2021-3618 (rhbz#1975651)

* Tue Jun 01 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.1-2
- use different fix for rhbz#1683388 as it introduced permissions issues in 1:1.20.0-2

* Tue May 25 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.1-1
- update to 1.20.1 (fixes CVE-2021-23017)

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.20.0-4
- Perl 5.34 rebuild

* Fri Apr 30 2021 Lubos Uhliarik <luhliari@redhat.com> - 1:1.20.0-3
- Related: #1636235 - centralizing default index.html on nginx

* Wed Apr 21 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.0-2
- sync rawhide and EPEL7 spec files again
- systemd service reload now checks config file (rhbz#1565377)
- drop nginx requirement on nginx-all-modules (rhbz#1708799)
- let nginx handle log creation on logrotate (rhbz#1683388)
- have log directory owned by root (rhbz#1390183, CVE-2016-1247)
- remove obsolete --with-ipv6 (src PR#8)
- correction: pcre2 is actually not supported by nginx, reintroduce pcre

* Wed Apr 21 2021 Felix Kaechele <heffer@fedoraproject.org> - 1:1.20.0-1
- update to 1.20.0
- sync with mainline spec file
- order configure options alphabetically for easier comparinggit
- add --with-compat option (rhbz#1834452)
- add patch to fix PIDFile race condition (rhbz#1869026)
- use pcre2 instead of pcre (rhbz#1938984)
- add Wants=network-online.target to systemd unit (rhbz#1943779)

* Mon Feb 22 2021 Lubos Uhliarik <luhliari@redhat.com> - 1:1.18.0-5
- Resolves: #1931402 - drop gperftools module

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.18.0-2
- Perl 5.32 rebuild

* Fri Apr 24 2020 Felix Kaechele <heffer@fedoraproject.org> - 1:1.18.0-1
- Update to 1.18.0
- Increased types_hash_max_size to 4096 in default config
- Add gpg source verification
- Add Recommends: logrotate
- Drop location / from default config (rhbz#1564768)
- Drop default_sever from default config (rhbz#1373822)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 15 2019 Warren Togami <warren@blockstream.com>
- add conditionals for EPEL7, see rhbz#1750857

* Tue Aug 13 2019 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.16.1-1
- Update to upstream release 1.16.1
- Fixes CVE-2019-9511, CVE-2019-9513, CVE-2019-9516

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.16.0-4
- Perl 5.30 rebuild

* Tue May 14 2019 Stephen Gallagher <sgallagh@redhat.com> - 1.16.0-3
- Move to common default index.html
- Resolves: rhbz#1636235

* Tue May 07 2019 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.16.0-2
- Add missing directory for vim plugin

* Fri Apr 26 2019 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.16.0-1
- Update to upstream release 1.16.0

* Mon Mar 04 2019 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.15.9-1
- Update to upstream release 1.15.9
- Enable ngx_stream_ssl_preread module
- Remove redundant conditionals

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.14.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:1.14.1-4
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Dec 11 2018 Joe Orton <jorton@redhat.com> - 1:1.14.1-3
- fix unexpanded paths in nginx(8)

* Tue Nov 20 2018 Luboš Uhliarik <luhliari@redhat.com> - 1:1.14.1-2
- new version 1.14.1
- Resolves: #1584426 - Upstream Nginx 1.14.0 is now available
- Resolves: #1647255 - CVE-2018-16845 nginx: Denial of service and memory
  disclosure via mp4 module
- Resolves: #1647259 - CVE-2018-16843 nginx: Excessive memory consumption
  via flaw in HTTP/2 implementation
- Resolves: #1647258 - CVE-2018-16844 nginx: Excessive CPU usage via flaw
  in HTTP/2 implementation

* Mon Aug 06 2018 Luboš Uhliarik <luhliari@redhat.com> - 1:1.12.1-14
- add requires on perl(constant) for mod-http-perl

* Mon Jul 30 2018 Luboš Uhliarik <luhliari@redhat.com> - 1:1.12.1-13
- don't build with geoip by default

* Thu Jul 19 2018 Joe Orton <jorton@redhat.com> - 1:1.12.1-12
- add build conditional for geoip support

* Mon Jul 16 2018 Tadej Janež <tadej.j@nez.si> - 1:1.12.1-11
- Add gcc to BuildRequires to account for
  https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.12.1-9
- Perl 5.28 rebuild

* Mon May 14 2018 Luboš Uhliarik <luhliari@redhat.com> - 1:1.12.1-8
- Related: #1573942 - nginx fails on start

* Wed May 02 2018 Luboš Uhliarik <luhliari@redhat.com> - 1:1.12.1-7
- Resolves: #1573942 - nginx fails on start

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Björn Esser <besser82@fedoraproject.org> - 1:1.12.1-5
- Add patch to apply glibc bugfix if really needed only
- Disable strict symbol checks in the link editor

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:1.12.1-4
- Rebuilt for switch to libxcrypt

* Tue Oct 24 2017 Joe Orton <jorton@redhat.com> - 1:1.12.1-3
- rebuild

* Tue Sep 19 2017 Remi Collet <remi@fedoraproject.org> - 1:1.12.1-2
- own system drop-in directories #1493036

* Tue Aug 15 2017 Joe Orton <jorton@redhat.com> - 1:1.12.1-1
- update to 1.12.1 (#1469924)
- enable http_auth_request_module (Tim Niemueller, #1471106)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.12.0-2
- Perl 5.26 rebuild

* Tue May 30 2017 Luboš Uhliarik <luhliari@redhat.com> - 1:1.12.0-1
- new version 1.12.0

* Wed Feb  8 2017 Joe Orton <jorton@redhat.com> - 1:1.10.3-1
- update to upstream release 1.10.3

* Mon Oct 31 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.2-1
- update to upstream release 1.10.2

* Tue May 31 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.1-1
- update to upstream release 1.10.1

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.10.0-4
- Perl 5.24 rebuild

* Sun May  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.10.0-3
- Enable AIO on aarch64 (rhbz 1258414)

* Wed Apr 27 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.0-2
- only Require nginx-all-modules for EPEL and current Fedora releases

* Wed Apr 27 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.0-1
- update to upstream release 1.10.0
- split dynamic modules into subpackages
- spec file cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.1-1
- update to upstream release 1.8.1
- CVE-2016-0747: Insufficient limits of CNAME resolution in resolver
- CVE-2016-0746: Use-after-free during CNAME response processing in resolver
- CVE-2016-0742: Invalid pointer dereference in resolver

* Sun Oct 04 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-14
- consistently use '%%global with_foo' style of logic
- remove PID file before starting nginx (#1268621)

* Fri Sep 25 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:1.8.0-13
- Use nginx-mimetypes from mailcap (#1248736)
- Mark LICENSE as %%license

* Thu Sep 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-12
- also build with gperftools on aarch64 (#1258412)

* Wed Aug 12 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1:1.8.0-11
- nginx.conf: added commented-out SSL configuration directives (#1179232)

* Fri Jul 03 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-10
- switch back to /bin/kill in logrotate script due to SELinux denials

* Tue Jun 16 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-9
- fix path to png in error pages (#1232277)
- optimize png images with optipng

* Sun Jun 14 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-8
- replace /bin/kill with /usr/bin/systemctl kill in logrotate script (#1231543)
- remove After=syslog.target in nginx.service (#1231543)
- replace ExecStop with KillSignal=SIGQUIT in nginx.service (#1231543)

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.8.0-7
- Perl 5.22 rebuild

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-6
- revert previous change

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-5
- move default server to default.conf (#1220094)

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-4
- add TimeoutStopSec=5 and KillMode=mixed to nginx.service
- set worker_processes to auto
- add some common options to the http block in nginx.conf
- run nginx-upgrade on package update
- remove some redundant scriptlet commands
- listen on ipv6 for default server (#1217081)

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-3
- improve nginx-upgrade script

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-2
- add --with-pcre-jit

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-1
- update to upstream release 1.8.0

* Thu Apr 09 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.7.12-1
- update to upstream release 1.7.12

* Sun Feb 15 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.7.10-1
- update to upstream release 1.7.10
- remove systemd conditionals

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-4
- fix package ownership of directories

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-3
- add vim files (#1142849)

* Mon Sep 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-2
- create nginx-filesystem subpackage (patch from Remi Collet)
- create /etc/nginx/default.d as a drop-in directory for configuration files
  for the default server block
- clean up nginx.conf

* Wed Sep 17 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-1
- update to upstream release 1.6.2
- CVE-2014-3616 nginx: virtual host confusion (#1142573)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.6.1-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-2
- add logic for EPEL 7

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-1
- update to upstream release 1.6.1
- (#1126891) CVE-2014-3556: SMTP STARTTLS plaintext injection flaw

* Wed Jul 02 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.6.0-3
- Fix FTBFS on aarch64 (#1115559)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.0-1
- update to upstream release 1.6.0

* Tue Mar 18 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.7-1
- update to upstream release 1.4.7

* Wed Mar 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.6-1
- update to upstream release 1.4.6

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-2
- avoid multiple index directives (#1065488)

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-1
- update to upstream release 1.4.5

* Wed Nov 20 2013 Peter Borsa <peter.borsa@gmail.com> - 1:1.4.4-1
- Update to upstream release 1.4.4
- Security fix BZ 1032267

* Sun Nov 03 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.3-1
- update to upstream release 1.4.3

* Fri Aug 09 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 1:1.4.2-3
- Add in conditionals to build for non-systemd targets

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.2-2
- Perl 5.18 rebuild

* Fri Jul 19 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.2-1
- update to upstream release 1.4.2

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.1-3
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 1:1.4.1-2
- rebuild for new GD 2.1.0

* Tue May 07 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.1-1
- update to upstream release 1.4.1 (#960605, #960606):
  CVE-2013-2028 stack-based buffer overflow when handling certain chunked
  transfer encoding requests

* Sun Apr 28 2013 Dan Horák <dan[at]danny.cz> - 1:1.4.0-2
- gperftools exist only on selected arches

* Fri Apr 26 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.0-1
- update to upstream release 1.4.0
- enable SPDY module (new in this version)
- enable http gunzip module (new in this version)
- enable google perftools module and add gperftools-devel to BR
- enable debugging (#956845)
- trim changelog

* Tue Apr 02 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.8-1
- update to upstream release 1.2.8

* Fri Feb 22 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-2
- make sure nginx directories are not world readable (#913724, #913735)

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-1
- update to upstream release 1.2.7
- add .asc file

* Tue Feb 05 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-6
- use 'kill' instead of 'systemctl' when rotating log files to workaround
  SELinux issue (#889151)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-5
- uncomment "include /etc/nginx/conf.d/*.conf by default but leave the
  conf.d directory empty (#903065)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-4
- add comment in nginx.conf regarding "include /etc/nginf/conf.d/*.conf"
  (#903065)

* Wed Dec 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-3
- use correct file ownership when rotating log files

* Tue Dec 18 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-2
- send correct kill signal and use correct file permissions when rotating
  log files (#888225)
- send correct kill signal in nginx-upgrade

* Tue Dec 11 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-1
- update to upstream release 1.2.6

* Sat Nov 17 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.5-1
- update to upstream release 1.2.5

* Sun Oct 28 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.4-1
- update to upstream release 1.2.4
- introduce new systemd-rpm macros (#850228)
- link to official documentation not the community wiki (#870733)
- do not run systemctl try-restart after package upgrade to allow the
  administrator to run nginx-upgrade and avoid downtime
- add nginx man page (#870738)
- add nginx-upgrade man page and remove README.fedora
- remove chkconfig from Requires(post/preun)
- remove initscripts from Requires(preun/postun)
- remove separate configuration files in "/etc/nginx/conf.d" directory
  and revert to upstream default of a centralized nginx.conf file
  (#803635) (#842738)

* Fri Sep 21 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.3-1
- update to upstream release 1.2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.1-2
- Perl 5.16 rebuild

* Sun Jun 10 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.1-1
- update to upstream release 1.2.1

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.0-2
- Perl 5.16 rebuild

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.0-1
- update to upstream release 1.2.0

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-4
- add nginx-upgrade to replace functionality from the nginx initscript
  that was lost after migration to systemd
- add README.fedora to describe usage of nginx-upgrade
- nginx.logrotate: use built-in systemd kill command in postrotate script
- nginx.service: start after syslog.target and network.target
- nginx.service: remove unnecessary references to config file location
- nginx.service: use /bin/kill instead of "/usr/sbin/nginx -s" following
  advice from nginx-devel
- nginx.service: use private /tmp

* Mon May 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-3
- fix incorrect postrotate script in nginx.logrotate

* Thu Apr 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-2
- renable auto-cc-gcc patch due to warnings on rawhide

* Sat Apr 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-1
- update to upstream release 1.0.15
- no need to apply auto-cc-gcc patch
- add %%global _hardened_build 1

* Thu Mar 15 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.14-1
- update to upstream release 1.0.14
- amend some %%changelog formatting

* Tue Mar 06 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.13-1
- update to upstream release 1.0.13
- amend --pid-path and --log-path

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-5
- change pid path in nginx.conf to match systemd service file

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-3
- fix %%pre scriptlet

* Mon Feb 20 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-2
- update upstream URL
- replace %%define with %%global
- remove obsolete BuildRoot tag, %%clean section and %%defattr
- remove various unnecessary commands
- add systemd service file and update scriptlets
- add Epoch to accommodate %%triggerun as part of systemd migration

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.12-1
- Update to 1.0.12

* Thu Nov 17 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.10-1
- Bugfix: a segmentation fault might occur in a worker process if resolver got a big DNS response. Thanks to Ben Hawkes.
- Bugfix: in cache key calculation if internal MD5 implementation wasused; the bug had appeared in 1.0.4.
- Bugfix: the module ngx_http_mp4_module sent incorrect "Content-Length" response header line if the "start" argument was used. Thanks to Piotr Sikora.

* Thu Oct 27 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.8-1
- Update to new 1.0.8 stable release

* Fri Aug 26 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.5-1
- Update nginx to Latest Stable Release

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-3
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-2
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53.5
- Extract out default config into its own file (bug #635776)

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-4
- Revert ownership of log dir

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-3
- Change ownership of /var/log/nginx to be 0700 nginx:nginx
- update init script to use killproc -p
- add reopen_logs command to init script
- update init script to use nginx -q option

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-2
- Fix linking of perl module

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-1
- Update to new stable 0.8.53

* Sat Jul 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-2
- add Provides: webserver (bug #619693)

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-1
- Update to new stable 0.7.67
- fix bugzilla #591543

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.65-2
- Mass rebuild with perl-5.12.0

* Mon Feb 15 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.65-1
- Update to new stable 0.7.65
- change ownership of logdir to root:root
- add support for ipv6 (bug #561248)
- add random_index_module
- add secure_link_module

* Fri Dec 04 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.64-1
- Update to new stable 0.7.64

## END: Generated by rpmautospec
