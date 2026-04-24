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

%global gh_commit    7989e43bf381af0eac72e4f0ca5bcbfa81658be4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_vendor    theseer
%global gh_project   tokenizer
%global ns_vendor    TheSeer
%global ns_project   Tokenizer
%global major        2

Name:           php-%{gh_vendor}-%{gh_project}%{major}
Version:        2.0.1
Release: 2%{?dist}
Summary:        Library for converting tokenized PHP source code into XML

License:        BSD-3-Clause
URL:            https://github.com/%{gh_vendor}/%{gh_project}
Source0:        %{name}-%{version}-%{?gh_short}.tgz
Source1:        makesrc.sh

BuildArch:      noarch
BuildRequires:  php(language) >= 8.1
BuildRequires:  php-xmlwriter
BuildRequires:  php-dom
BuildRequires:  php-tokenizer
%if %{with tests}
# Tests
BuildRequires:  phpunit9
%endif
# Autoloader
BuildRequires:  php-fedora-autoloader-devel >= 1.0.0

# From composer.json, "require": {
#    "php": "^8.1",
#    "ext-xmlwriter": "*",
#    "ext-dom": "*",
#    "ext-tokenizer": "*"
Requires:       php(language) >= 8.1
Requires:       php-xmlwriter
Requires:       php-dom
Requires:       php-tokenizer
# From phpcompatinfo report for version 1.1.0
# only pcre and spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{gh_vendor}/%{gh_project}) = %{version}


%description
A small library for converting tokenized PHP source code into XML
and potentially other formats.

Autoloader: %{_datadir}/php/%{ns_vendor}/%{ns_project}%{major}/autoload.php

%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a simple classmap autoloader
%{_bindir}/phpab --template fedora --output src/autoload.php src


%install
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
ret=0
for cmdarg in php php81 php82 php83 php84 php85; do
  if which $cmdarg; then
      $cmdarg -d auto_prepend_file=%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
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
     %{_datadir}/php/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Tue Dec  9 2025 Remi Collet <remi@remirepo.net> - 2.0.1-1
- update to 2.0.1
- rename to php-theseer-tokenizer2
- install /usr/share/php/TheSeer/Tokenizer2
- raise dependency on PHP 8.1

* Wed Nov 19 2025 Remi Collet <remi@remirepo.net> - 1.3.1-1
- update to 1.3.1

* Fri Nov 14 2025 Remi Collet <remi@remirepo.net> - 1.3.0-1
- update to 1.3.0
- re-license spec file to CECILL-2.1

* Tue Mar  5 2024 Remi Collet <remi@remirepo.net> - 1.2.3-1
- update to 1.2.3

* Mon Nov 20 2023 Remi Collet <remi@remirepo.net> - 1.2.2-1
- update to 1.2.2

* Thu Apr 20 2023 Remi Collet <remi@remirepo.net> - 1.2.1-5
- use SPDX license ID
- switch to phpunit9

* Wed Jul 28 2021 Remi Collet <remi@remirepo.net> - 1.2.1-1
- update to 1.2.1

* Mon Jul 13 2020 Remi Collet <remi@remirepo.net> - 1.2.0-1
- update to 1.2.0
- sources from git snapshot

* Fri Jun 14 2019 Remi Collet <remi@remirepo.net> - 1.1.3-1
- update to 1.1.3

* Thu Apr  4 2019 Remi Collet <remi@remirepo.net> - 1.1.2-1
- update to 1.1.2 (no change)
- switch back to phpunit 6 and 7

* Thu Apr  4 2019 Remi Collet <remi@remirepo.net> - 1.1.1-2
- add patch from https://github.com/theseer/tokenizer/pull/4
  and use phpunit7 with 7.1

* Thu Apr  4 2019 Remi Collet <remi@remirepo.net> - 1.1.1-1
- update to 1.1.1
- use phpunit8

* Fri Apr 21 2017 Remi Collet <remi@remirepo.net> - 1.1.0-1
- initial package, version 1.1.0
