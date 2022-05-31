%global debug_package %{nil}
%global gem_name minitest
Summary:        Minitest provides a complete suite of testing facilities
Name:           rubygem-%{gem_name}
Version:        5.15.0
Release:        1%{?dist}
# minitest source is licensed under MIT and minitest.gemspec is taken from ruby source, licensed under the rest
License:        MIT AND (Ruby OR BSD) AND Public Domain AND MIT AND CC0 AND zlib AND UCD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/seattlerb/minitest
Source0:        https://github.com/minitest/minitest/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
# When updating the version, please make necessary changes in this .gemspec, e.g. update version, dependencies (use https://rubygems.org/gems/minitest)
Source1:        minitest.gemspec
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(minitest) = %{version}-%{release}
BuildArch:      noarch

%description
minitest/unit is a small and incredibly fast unit testing framework.
minitest/spec is a functionally complete spec engine.
minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.
minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.
minitest/pride shows pride in testing and adds coloring to your test
output.

%prep
%setup -q -n %{gem_name}-%{version}
cp %{SOURCE1} .

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add README.rdoc file to buildroot from Source0
cp README.rdoc %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/README.rdoc
%{gemdir}

%changelog
* Tue May 24 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.15.0-1
- Update to v5.15.0
- Get source.tar.gz from upstream, get initial .gemspec from ruby2.7.4 source (license (Ruby OR BSD) AND Public Domain AND MIT AND CC0 AND zlib AND UCD)

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.13.0-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.13.0-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
