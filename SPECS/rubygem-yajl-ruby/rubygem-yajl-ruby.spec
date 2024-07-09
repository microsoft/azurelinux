%global debug_package %{nil}
%global gem_name yajl-ruby
# Versions 1.4.2 and 1.4.3 are not available as tags
%global commit e8de283a6d64f0902740fd09e858fc3d7d803161
Summary:        A streaming JSON parsing and encoding library for Ruby
Name:           rubygem-yajl-ruby
Version:        1.4.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/brianmario/yajl-ruby
Source0:        https://github.com/brianmario/yajl-ruby/archive/%{commit}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
a C binding to the YAJL JSON parsing and generation library.

%prep
%autosetup -p1 -n %{gem_name}-%{commit}
# Gemspec uses git to find files
git init .
git add .

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license LICENSE
%{gemdir}

%changelog
* Tue Jul 09 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.4.3-1
- Auto-upgrade to 1.4.3 - CVE-2022-24795
- Use commit hash in source URL since newer tags are not available
- Use git to find files in gemspec instead of patching

* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.1-1
- Auto-upgrade to 1.4.1 - Azure Linux 3.0 - package upgrades

* Tue Aug 23 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.3.1-2
- Fix CVE-2022-24795.

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.3.1-1
- Downgrade to v1.3.1.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.4.1-1
- License verified
- Original version for CBL-Mariner
