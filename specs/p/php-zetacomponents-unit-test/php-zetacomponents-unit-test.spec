# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-zetacomponents-unit-test
#
# Copyright (c) 2015-2024 Remi Collet
# License: CC-BY-SA-4.0
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    179fd95f1ed1292a5fb639a89f482dfce2038758
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   UnitTest
%global cname        unit-test
%global ezcdir       %{_datadir}/php/ezc

Name:           php-%{gh_owner}-%{cname}
Version:        1.2.6
Release:        3%{?dist}
Summary:        Zeta UnitTest Component

License:        Apache-2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

BuildArch:      noarch
BuildRequires:  php-fedora-autoloader-devel

# From phpcompatinfo report for 1.0.2
Requires:       php(language) > 5.3
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       phpunit9
# Also use Exception for Base, skipped to avoid circular dep.
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
UnitTest is an internal component which extends PhpUnit to facilitate test
running and reports of the components themselves.

For this reason, there is no tutorial for this component. If you really want
to use it for some reason it's sane to expect some community support on IRC or
the mailing list.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple autoloader
%{_bindir}/phpab \
   --template fedora \
   --output src/autoloader.php \
   src


%install
mkdir -p %{buildroot}%{ezcdir}/autoload

: The library
cp -pr src \
       %{buildroot}%{ezcdir}/%{gh_project}
: For ezcBase autoloader
cp -pr src/*_autoload.php \
       %{buildroot}%{ezcdir}/autoload


%files
%license LICENSE* CREDITS
%doc ChangeLog
%doc composer.json
%doc docs design
%dir %{ezcdir}
%dir %{ezcdir}/autoload
     %{ezcdir}/autoload/*_autoload.php
     %{ezcdir}/%{gh_project}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct  7 2024 Remi Collet <remi@remirepo.net> - 1.2.6-1
- update to 1.2.6

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Remi Collet <remi@remirepo.net> - 1.2.5-1
- update to 1.2.5

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Remi Collet <remi@remirepo.net> - 1.2.4-1
- update to 1.2.4

* Mon Jul 18 2022 Remi Collet <remi@remirepo.net> - 1.2.3-1
- update to 1.2.3
- switch to phpunit9

* Tue Feb 15 2022 Remi Collet <remi@remirepo.net> - 1.1.7-1
- update to 1.1.7

* Mon Jan 24 2022 Remi Collet <remi@remirepo.net> - 1.1.5-1
- update to 1.1.5

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug  9 2021 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3
- switch to phpunit8

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 27 2019 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- fix depedency on phpunit (EL-6)

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- add upstream patch for LICENSE file

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package
- open https://github.com/zetacomponents/UnitTest/issues/4 License
- open https://github.com/zetacomponents/UnitTest/pull/5 phpunit 4
