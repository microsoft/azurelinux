# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for php-sebastian-git-state1
#
# SPDX-FileCopyrightText:  Copyright 2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%bcond_without       tests

# Sources
%global gh_owner     sebastianbergmann
%global gh_project   git-state
# Packagist
%global pk_vendor    sebastian
%global pk_project   %{gh_project}
# Namespace
%global major        1
%global php_home     %{_datadir}/php
%global ns_vendor    SebastianBergmann
%global ns_project   GitState

Name:           php-%{pk_vendor}-%{pk_project}%{major}
Version:        1.0.0
Release: 2%{?dist}
Summary:        Describing the state of a Git checkout, version %{major}

License:        BSD-3-Clause
URL:            https://github.com/%{gh_owner}/%{gh_project}
# run makesrc.sh to create a git snapshot with test suite
Source0:        %{name}-%{version}.tgz
Source1:        makesrc.sh


BuildArch:      noarch
BuildRequires:  php(language) >= 8.4.1
BuildRequires:  php-posix
# Autoloader
BuildRequires:  php-fedora-autoloader-devel
%if %{with tests}
# from composer.json, "require-dev": {
#        "phpunit/phpunit": "^13.0"
BuildRequires:  phpunit13
%endif

# from composer.json, "require": {
#        "php": ">=8.4.1"
Requires:       php(language) >= 8.4.1
# From phpcompatinfo report for 1.0.0
# Only core, pcre, standard
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


%description
Library for describing the state of a Git checkout.

This package provides version %{major} of %{pk_vendor}/%{pk_project} library.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php


%prep
%setup -q -n %{gh_project}-%{version}


%build
# Generate the Autoloader
%{_bindir}/phpab \
   --template fedora \
   --output src/autoload.php \
   src


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}


%if %{with tests}
%check
mkdir vendor
ln -s %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php vendor/autoload.php

: Run tests
ret=0
for cmd in php php84 php85; do
  if which $cmd; then
   $cmd -d auto_prepend_file=%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}%{major}/autoload.php \
     %{_bindir}/phpunit13 || ret=1
  fi
done
exit $ret
%endif


%files
%license LICENSE
%doc composer.json
%doc README.md
%dir %{php_home}/%{ns_vendor}
     %{php_home}/%{ns_vendor}/%{ns_project}%{major}


%changelog
* Fri Apr  3 2026 Remi Collet <remi@remirepo.net> - 1.0.0-1
- initial package
