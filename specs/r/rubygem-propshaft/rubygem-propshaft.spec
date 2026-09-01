# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from propshaft-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name propshaft

Name: rubygem-%{gem_name}
Version: 1.1.0
Release: 2%{?dist}
Summary: Deliver assets for Rails
License: MIT
URL: https://github.com/rails/propshaft
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone http://github.com/rails/propshaft.git && cd propshaft
# git archive -v -o propshaft-1.1.0-tests.tar.gz v1.1.0 test/
Source1: %{gem_name}-%{version}%{?prerelease}-tests.tar.gz

BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.7.0
BuildRequires: rubygem(actioncable)
BuildRequires: rubygem(railties)
BuildArch: noarch

%description
Propshaft is an asset pipeline library for Rails. It's built for an era where
bundling assets to save on HTTP connections is no longer urgent, where
JavaScript and CSS are either compiled by dedicated Node.js bundlers or served
directly to the browsers, and where increases in bandwidth have made the need
for minification less pressing. These factors allow for a dramatically simpler
and faster asset pipeline compared to previous options, like Sprockets.


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
ln -s %{builddir}/test .

# Remove Bundler usage.
sed -i '/Bundler.require/ s/^/#/' test/dummy/config/application.rb

# Rails 7.0 returns just `500` error code. Can be enabled with Rails 8.0, where
# this test passes just fine.
sed -i "/get sample_load_nonexistent_assets_url/i\      skip" \
  test/propshaft_integration_test.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
)

%files
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 21 2025 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Initial package
