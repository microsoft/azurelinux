#disable the httpd stuff while we're waiting on getting the path issues
#cleared up
%global enable_httpd 1

Name:           web-assets
Version:        5
Release:        13%{?dist}
Summary:        A simple framework for bits pushed to browsers
BuildArch:      noarch

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://fedoraproject.org/wiki/User:Patches/PackagingDrafts/Web_Assets

Source1:        LICENSE
Source2:        macros.web-assets
Source3:        web-assets.conf
Source4:        README.devel

%description
%{summary}.

%package filesystem
Summary:        The basic directory layout for Web Assets
#there's nothing copyrightable about a few directories and symlinks
License:        Public Domain

%description filesystem
%{summary}.

%package devel
Summary:        RPM macros for Web Assets packaging
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}

%description devel
%{summary}.

%if 0%{?enable_httpd}
%package httpd
Summary:        Web Assets aliases for the Apache HTTP daemon
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}
Requires:       httpd
Requires(post): systemd
Requires(postun): systemd

%description httpd
%{summary}.
%endif

%prep
%setup -c -T
cp %{SOURCE1} LICENSE
cp %{SOURCE4} README.devel

%build
#nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/web-assets
mkdir -p %{buildroot}%{_datadir}/javascript

ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/javascript
ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/js
ln -sf ../fonts %{buildroot}%{_datadir}/web-assets/fonts

install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.web-assets

%if 0%{?enable_httpd}
install -Dpm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/web-assets.conf

%post httpd
systemctl reload-or-try-restart httpd.service || :

%postun httpd
systemctl reload-or-try-restart httpd.service || :
%endif

%files filesystem
%{_datadir}/web-assets
%{_datadir}/javascript

%files devel
%{_rpmconfigdir}/macros.d/macros.web-assets
%license LICENSE
%doc README.devel

%if 0%{?enable_httpd}
%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/web-assets.conf
%license LICENSE
%endif

%changelog
* Fri Oct 03 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 5-13
- Fix for license path issue
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 5-1
- switch to dot-prefixed Aliases
- order Aliases for compatibility with older Apache releases
- enable webfonts
- enable symlinks in %%{_webassetdir} and %%{_jsdir}
- re-enable httpd subpackage

* Sat Aug 24 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 4-2
- tighten dependency on filesystem from other packages
- add brief README to -devel

* Fri Aug 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 4-1
- temporarily disable httpd stuff while we're waiting on sorting out the
  directory

* Tue Jul 30 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3-1
- rename directories per discussion on lists
- provide a /_sysassets/js shortcut

* Fri Jul 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2-1
- rename the license now that we have proper git
- prefix httpd-exported directory with an underscore (thanks to Joe Orton)
- add "Require all granted" (thanks to Remi Collet)
- alias /usr/share/javascript explictly

* Thu Jul 11 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1-1
- initial package
