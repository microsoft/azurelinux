# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from rackup-2.2.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rackup

Name: rubygem-%{gem_name}
Version: 2.2.1
Release: 3%{?dist}
Summary: A general server command for Rack applications
License: MIT
URL: https://github.com/rack/rackup
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rack/rackup.git && cd rackup
# git archive -v -o rackup-2.2.1-tests.tar.gz v2.2.1 test/
Source1: %{gem_name}-%{version}-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.5
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildRequires: rubygem(webrick)
BuildArch: noarch

%description
A general server command for Rack applications.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs sed -i 's|^#!/usr/bin/env ruby$|#!/usr/bin/ruby|'

%check
( cd .%{gem_instdir}
cp -a %{builddir}/test .

# Avoid minitest-global_expectations in exchange of lot of deprecation warnings.
# https://github.com/rack/rack/pull/1394
mkdir -p test/minitest/global_expectations
echo 'require "minitest/autorun"' > test/minitest/global_expectations/autorun.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/spec_*.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%{_bindir}/rackup
%{gem_instdir}/bin
%{gem_libdir}
%license %{gem_instdir}/license.md
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/readme.md
%doc %{gem_instdir}/releases.md
%doc %{gem_instdir}/security.md

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Vít Ondruch <vondruch@redhat.com> - 2.2.1-2
- Add missing `BR: rubygem(minitest)`

* Mon Jan 13 2025 Vít Ondruch <vondruch@redhat.com> - 2.2.1-1
- Initial package
