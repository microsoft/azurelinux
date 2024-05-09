%global debug_package %{nil}
%global gem_name hirb
Summary:        A mini view framework for console/irb that's easy to use
Name:           rubygem-%{gem_name}
Version:        0.7.3
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://tagaholic.me/hirb/
Source0:        https://github.com/cldwalker/hirb/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Hirb provides a mini view framework for console applications and
uses it to improve ripl(irb)'s default inspect output.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build .gemspec

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.7.3-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.7.3-1
- License verified
- Original version for CBL-Mariner
