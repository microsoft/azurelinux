# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without httpd
%bcond_without nginx

Name:           web-assets
Version:        5
Release:        24%{?dist}
Summary:        A simple framework for bits pushed to browsers
License:        MIT
URL:            https://fedoraproject.org/wiki/User:Patches/PackagingDrafts/Web_Assets
Source0:        LICENSE
Source1:        README.devel
Source2:        macros.web-assets
Source3:        httpd-web-assets.conf
Source4:        nginx-web-assets.conf
BuildArch:      noarch
BuildRequires:  coreutils

%description
%{summary}.

%package filesystem
Summary:        The basic directory layout for Web Assets
#there's nothing copyrightable about a few directories and symlinks
License:        LicenseRef-Not-Copyrightable
Requires:       fonts-filesystem

%description filesystem
%{summary}.

%package devel
Summary:        RPM macros for Web Assets packaging
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}

%description devel
%{summary}.

%if %{with httpd}
%package httpd
Summary:        Web Assets aliases for the Apache HTTP daemon
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}
Requires:       httpd

%description httpd
%{summary}.
%endif

%if %{with nginx}
%package nginx
Summary:        Web Assets aliases for the nginx daemon
License:        MIT
Requires:       web-assets-filesystem = %{version}-%{release}
Requires:       nginx

%description nginx
%{summary}.
%endif

%prep
%setup -c -T
cp %{SOURCE0} LICENSE
cp %{SOURCE1} README.devel

%build
#nothing to do

%install
mkdir -p %{buildroot}%{_datadir}/web-assets
mkdir -p %{buildroot}%{_datadir}/javascript
ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/javascript
ln -sf ../javascript %{buildroot}%{_datadir}/web-assets/js
ln -sf ../fonts %{buildroot}%{_datadir}/web-assets/fonts
install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.web-assets
%if %{with httpd}
install -Dpm0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/web-assets.conf
%endif
%if %{with nginx}
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/nginx/default.d/web-assets.conf
%endif

%if %{with httpd}
%post httpd
[ -x %{_bindir}/systemctl ] && reload-or-try-restart httpd.service || :

%postun httpd
[ -x %{_bindir}/systemctl ] && reload-or-try-restart httpd.service || :
%endif

%if %{with nginx}
%post nginx
[ -x %{_bindir}/systemctl ] && systemctl reload-or-try-restart nginx.service || :

%postun nginx
[ -x %{_bindir}/systemctl ] && systemctl reload-or-try-restart nginx.service || :
%endif

%files filesystem
%{_datadir}/web-assets
%{_datadir}/javascript

%files devel
%{_rpmconfigdir}/macros.d/macros.web-assets
%license LICENSE
%doc README.devel

%if %{with httpd}
%files httpd
%config(noreplace) %{_sysconfdir}/httpd/conf.d/web-assets.conf
%license LICENSE
%endif

%if %{with nginx}
%files nginx
%config(noreplace) %{_sysconfdir}/nginx/default.d/web-assets.conf
%license LICENSE
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 23 2022 Petr Pisar <ppisar@redhat.com> - 5-17
- Make a dependency on systemd optional for restarting httpd

* Tue Mar 22 2022 Petr Menšík <pemensik@redhat.com> - 5-16
- Add nginx aliases support

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
