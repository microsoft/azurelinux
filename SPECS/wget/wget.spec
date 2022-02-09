Summary:        A network utility to retrieve files from the Web
Name:           wget
Version:        1.21.2
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/wget/wget.html
Group:          System Environment/NetworkingPrograms
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  openssl-devel
%if %{with_check}
BuildRequires:  perl
%endif
Requires:       openssl

%description
The Wget package contains a utility useful for non-interactive
downloading of files from the Web.

%prep
%setup -q

%build
./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --with-ssl=openssl
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/etc
cat >> %{buildroot}/etc/wgetrc <<-EOF
#   default root certs location
    ca_certificate=/etc/pki/tls/certs/ca-bundle.trust.crt
    ca_directory = /etc/ssl/certs
EOF
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}
%{_fixperms} %{buildroot}/*

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan HTTP::Daemon
make  %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) /etc/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Wed Jan 26 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.21.2-1
- Update to version 1.21.2.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.3-4
- Removing the explicit %%clean stage.

* Fri Nov 13 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.3-3
- Adding 'local::lib' perl5 library to fix test dependencies.

* Wed Oct 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.20.3-2
- Updating certificate bundle path to include full set of trust information.

* Mon Jun 08 2020 Joe Schmitt <joschmit@microsoft.com> 1.20.3-1
- Update to version 1.20.3 to resolve CVE-2019-5953.
- Use https for URL.
- License verified.
- Remove sha1 macro.
- Fix macro in changelog.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.19.5-4
- Added %%license line automatically

* Fri May 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.19.5-3
- Removing *Requires for "ca-certificates".
- Adding "ca_directory" to wget's configuration.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.19.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.19.5-1
- Updated to latest version

* Tue Dec 19 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-4
- Fix CVE-2017-6508

* Mon Nov 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-3
- Fix CVE-2017-13089 and CVE-2017-13090

* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.19.1-2
- Install HTTP::Daemon perl module for the tests to pass.

* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.19.1-1
- Updated to version 1.19.1.

* Tue Nov 29 2016 Anish Swaminathan <anishs@vmware.com>  1.18-1
- Upgrade wget versions - fixes CVE-2016-7098

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.17.1-3
- Modified %%check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.17.1-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.17.1-1
- Upgrade version

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.15-1
- Initial build.  First version
