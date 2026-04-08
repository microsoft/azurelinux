# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# spec file for php-theseer-directoryscanner
#
# SPDX-FileCopyrightText:  Copyright 2014-2025 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#
%global gh_commit    4cdce31c1b5120779a01225b5b0968f9321342d6
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   DirectoryScanner
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    DirectoryScanner
%global pear_channel pear.netpirates.net

%if 0%{?fedora}
%bcond_without  tests
%else
%bcond_with     tests
%endif

Name:           php-theseer-directoryscanner
Version:        1.3.3
Release:        12%{?dist}
Summary:        A recursive directory scanner and filter

License:        BSD-2-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{name}-%{version}.tar.gz

# minimal fix to allow phpunit9
Patch0:         %{name}-tests.patch

BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
%if %{with tests}
BuildRequires:  phpunit9
%endif

# From composer.json
Requires:       php(language) >= 5.3.1
# From phpcompatinfo report for 1.3.0
Requires:       php-fileinfo

Provides:       php-composer(theseer/directoryscanner) = %{version}
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
A recursive directory scanner and filter.


%prep
%setup -q -n %{gh_project}-%{gh_commit}
%patch -P0 -p1


%build
# Empty build section, most likely nothing required.


%install
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}


%check
%if %{with tests}
cat << 'EOF' | tee bs.php
<?php
require_once '%{buildroot}%{php_home}/%{gh_project}/autoload.php';
EOF

ret=0
for cmd in php php81 php82 php83 php84; do
  if which $cmd; then
    $cmd %{_bindir}/phpunit9 \
         --bootstrap bs.php \
         --verbose \
         --no-coverage \
         --do-not-cache-result \
         --test-suffix=.test.php \
         --no-configuration \
         tests || ret=1
  fi
done
exit $ret
%endif


%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%license LICENSE
%doc composer.json
%dir %{php_home}
%{php_home}/%{gh_project}


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Remi Collet <remi@remirepo.net> - 1.3.3-11
- use phpunit9
- re-license spec file to CECILL-2.1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Remi Collet <remi@remirepo.net> - 1.3.3-8
- use phpunit7 FTBFS #2261513

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec  6 2021 Remi Collet <remi@remirepo.net> - 1.3.3-2
- disable test suite on EL

* Mon Jul 26 2021 Remi Collet <remi@remirepo.net> - 1.3.3-1
- update to 1.3.3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 10 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- Update to 1.3.2 (no change)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- update to 1.3.1
- switch from pear to github sources
- enable test suite

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- initial package, version 1.3.0
