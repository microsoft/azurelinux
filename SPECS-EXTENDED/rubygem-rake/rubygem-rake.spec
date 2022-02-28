%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rake
Summary:        A make-like build utility for Ruby
Name:           rubygem-rake
Version:        13.0.6
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://ruby.github.io/rake/
#Source0:        https://github.com/ruby/rake/archive/refs/tags/v%{version}.tar.gz
Source0:        %{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
Rake is a Make-like program implemented in Ruby. Tasks and
dependencies are specified in standard Ruby syntax.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/MIT-LICENSE
%{gemdir}

%changelog
* Mon Feb 28 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 13.0.6-1
- Update to v13.0.6

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 13.0.1-1
- License verified
- Original version for CBL-Mariner