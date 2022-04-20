%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name minitest
Summary:        Minitest provides a complete suite of testing facilities
Name:           rubygem-minitest
Version:        5.13.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/seattlerb/minitest
# The upstream source doesn't contain gemspec file. This source has been taken from ruby-2.7.4.tar.xz
Source0:        %{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem-minitest = %{version}-%{release}
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
* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.13.0-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
