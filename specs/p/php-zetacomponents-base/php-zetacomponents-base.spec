# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-zetacomponents-base
#
# Copyright (c) 2015-2022 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit    b6ae5f6177f6e51c5fc3514800e1c3fb076ec4be
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zetacomponents
%global gh_project   Base
%global cname        base
%global ezcdir       %{_datadir}/php/ezc

%if 0%{?fedora}
%bcond_without  tests
%bcond_without  phpab
%else
%bcond_with     tests
%bcond_with     phpab
%endif

Name:           php-%{gh_owner}-%{cname}
Version:        1.9.4
Release:        9%{?dist}
Summary:        Zeta Base Component

Group:          Development/Libraries
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            http://zetacomponents.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        autoloader.php

# Use old PEAR layout
Patch0:         %{name}-layout.patch

BuildArch:      noarch
%if %{with phpab}
BuildRequires:  %{_bindir}/phpab
%endif
%if %{with tests}
BuildRequires:  phpunit9
BuildRequires:  %{_bindir}/convert
BuildRequires:  php-composer(%{gh_owner}/unit-test) >= 1.2.3
BuildRequires:  php-posix
%endif

# From phpcompatinfo report for 1.9
Requires:       php(language) > 5.3
Requires:       php-pcre
Requires:       php-posix
Requires:       php-simplexml
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{cname}) = %{version}


%description
This is the base package of the Zeta components, offering the basic
support that all Components need. In the first version this will be the
autoload support.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch -P0 -p0


%build
%if %{with phpab}
: Generate a simple autoloader
%{_bindir}/phpab \
   --output src/autoloader.php \
   src
%else
cp %{SOURCE1} src/autoloader.php
%endif


%install
mkdir -p %{buildroot}%{ezcdir}/autoload

: The library
cp -pr src \
       %{buildroot}%{ezcdir}/%{gh_project}
: For ezcBase autoloader
cp -pr src/*_autoload.php \
       %{buildroot}%{ezcdir}/autoload


%check
%if %{with tests}
: Ignore test relying on composer layout
rm tests/file_find_recursive_test.php

: Create test autoloader
mkdir vendor
cat <<EOF | tee vendor/autoload.php
<?php
require '%{ezcdir}/UnitTest/autoloader.php';
require '$PWD/src/autoloader.php';
EOF

: Run test test suite
ret=0
for cmd in php php80 php81 php82; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit9 || ret=1
  fi
done
exit $ret
%else
: Test suite disabled
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE* CREDITS
%doc ChangeLog
%doc composer.json
%doc docs design
%dir %{ezcdir}
%dir %{ezcdir}/autoload
     %{ezcdir}/autoload/*_autoload.php
     %{ezcdir}/%{gh_project}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul  24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.9.4-7
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Remi Collet <remi@remirepo.net> - 1.9.4-1
- update to 1.9.4

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Remi Collet <remi@remirepo.net> - 1.9.3-4
- switch to phpunit9

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec  6 2021 Remi Collet <remi@remirepo.net> - 1.9.3-2
- disable test suite on EL
- add autoloader from sources on EL

* Mon Jul 26 2021 Remi Collet <remi@remirepo.net> - 1.9.3-1
- update to 1.9.3

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Remi Collet <remi@remirepo.net> - 1.9.1-1
- Update to 1.9.1

* Mon Oct 30 2017 Remi Collet <remi@fedoraproject.org> - 1.9-6
- fix FTBFS from Koschei, add patch for tests from
  https://github.com/zetacomponents/Base/pull/8

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.9-2
- add upstream patch for LICENSE file

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.9-1
- initial package
- open https://github.com/zetacomponents/UnitTest/issues/4 License
