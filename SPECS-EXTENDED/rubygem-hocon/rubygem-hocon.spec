# Generated from hocon-0.9.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name hocon
 
Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 1%{?dist}
Summary: HOCON Config Library
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License: Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://github.com/puppetlabs/ruby-hocon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
 
# SOURCE1 contains the upstream tag of the project from github
# in particular this includes the spec directory which was not
# included in the gemfile.
# https://github.com/puppetlabs/ruby-hocon/issues/65
# was originally resolved.
# However the rspec files were then removed again for a bizare reason.
# https://tickets.puppetlabs.com/browse/PA-2942
Source1: https://github.com/puppetlabs/ruby-hocon/archive/%{version}/ruby-hocon-%{version}.tar.gz
 
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 1.9.0
BuildArch: noarch

%description
A port of the Java Typesafe Config
library to Ruby.
https://github.com/typesafehub/config

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
sed -i 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/' bin/hocon
 
# unpack only the spec files from SOURCE1.
tar zxf %{SOURCE1} ruby-hocon-%{version}/spec --strip-components 1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install
%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{gem_instdir}/bin/hocon %{buildroot}/%{_bindir}/hocon

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/spec
%{gem_spec}
%{_bindir}/hocon

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/HISTORY.md
%doc %{gem_instdir}/README.md

%changelog
* Thu Dec 05 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.4.0-1
- Update to version 1.4.0

* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.1-2
- Build from .tar.gz source.

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.3.1-1
- Original version for CBL-Mariner
- License verified
