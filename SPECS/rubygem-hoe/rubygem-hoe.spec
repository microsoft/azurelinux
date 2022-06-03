%global debug_package %{nil}
%global gem_name hoe
Summary:        Rake/Rubygems helper for project Rakefiles
Name:           rubygem-hoe
Version:        3.18.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/seattlerb/hoe
Source0:        https://github.com/seattlerb/hoe/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Source1:        hoe.gemspec
BuildRequires:  git
BuildRequires:  ruby
BuildRequires:  rubygem-rdoc
Requires:       rubygem-rake
Provides:       rubygem(hoe) = %{version}-%{release}

%description
Hoe is a rake/rubygems helper for project Rakefiles. It helps you manage, maintain, and release your project and includes a dynamic plug-in system allowing for easy extensibility. Hoe ships with plug-ins for all your usual project tasks including rdoc generation, testing, packaging, deployment, and announcement.

%prep
%setup -q -n %{gem_name}-%{version}
cp %{SOURCE1} .

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.18.1-4
- Cleanup

* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.18.1-1
- License verified
- Original version for CBL-Mariner
