# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-theseer-tokenizer
#
# SPDX-FileCopyrightText:  Copyright 2017-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%bcond_without       tests

%global gh_commit    b7489ce515e168639d17feec34b8847c326b0b3c
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_vendor    theseer
%global gh_project   tokenizer
%global ns_vendor    TheSeer
%global ns_project   Tokenizer

Name:           php-%{gh_vendor}-%{gh_project}
Version:        1.3.1
Release: 2%{?dist}
Summary:        Library for converting tokenized PHP source code into XML

License:        BSD-3-Clause
URL:            https://github.com/%{gh_vendor}/%{gh_project}
Source0:        %{name}-%{version}-%{?gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-xmlwriter
BuildRequires:  php-dom
BuildRequires:  php-tokenizer
BuildRequires:  php-pcre
BuildRequires:  php-spl
%if %{with tests}
# Tests
BuildRequires:  phpunit9
%endif
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0

# From composer.json, "require": {
#    "php": "^7.0 || ^8.0",
#    "ext-xmlwriter": "*",
#    "ext-dom": "*",
#    "ext-tokenizer": "*"
Requires:       php(language) >= 7.0
Requires:       php-xmlwriter
Requires:       php-dom
Requires:       php-tokenizer
# From phpcompatinfo report for version 1.1.0
Requires:       php-pcre
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_vendor}/%{gh_project}) = %{version}


%description
A small library for converting tokenized PHP source code into XML
and potentially other formats.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php

%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple classmap autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}


%if %{with tests}
%check
ret=0
for cmdarg in php php81 php82 php83 php84 php85; do
  if which $cmdarg; then
      $cmdarg -d auto_prepend_file=%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}/autoload.php \
        %{_bindir}/phpunit9 \
          --no-coverage --verbose || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc README.md composer.json
%dir %{_datadir}/php/%{ns_vendor}
     %{_datadir}/php/%{ns_vendor}/%{ns_project}


%changelog
* Wed Nov 19 2025 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Fri Nov 14 2025 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0
- re-license spec file to CECILL-2.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 1.2.3-1
- update to 1.2.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 20 2023 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 1.2.1-5
- use SPDX license ID
- switch to phpunit9

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 28 2021 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0
- sources from git snapshot

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Thu Apr  4 2019 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2 (no change)
- switch back to phpunit 7

* Thu Apr  4 2019 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1
- use phpunit8

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 21 2017 Remi Collet <remi@remirepo.net> - 1.1.0-1
- initial package, version 1.1.0
