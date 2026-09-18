# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from rack-session-2.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rack-session

Name: rubygem-%{gem_name}
Version: 2.1.1
Release: 2%{?dist}
Summary: A session implementation for Rack
License: MIT
URL: https://github.com/rack/rack-session
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rack/rack-session.git && cd rack-session
# git archive -v -o rack-session-2.1.1-tests.tar.gz v2.1.1 test/
Source1: rack-session-%{version}-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.5
BuildRequires: rubygem(base64)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(rack)
BuildArch: noarch

%description
A session implementation for Rack.


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



%check
( cd .%{gem_instdir}
cp -a %{builddir}/test .

# Avoid minitest-global_expectations in exchange of lot of deprecation warnings.
# https://github.com/rack/rack/pull/1394
mkdir -p test/minitest/global_expectations
echo 'require "minitest/autorun"' > test/minitest/global_expectations/autorun.rb

ruby -Itest -e 'Dir.glob "./test/**/spec_*.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
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
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Vít Ondruch <vondruch@redhat.com> - 2.1.1-1
- Update to Rack::Session 2.1.1
- Rack::Session Session Persistence Vulnerability (CVE-2025-46336)
  Resolves: rhbz#2365151

* Fri Feb 07 2025 Vít Ondruch <vondruch@redhat.com> - 2.1.0-1
- Initial package (fedora#2344660).
