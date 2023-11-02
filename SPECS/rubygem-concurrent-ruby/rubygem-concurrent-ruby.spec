%global debug_package %{nil}
%global gem_name concurrent-ruby
Summary:        Modern concurrency tools for Ruby
Name:           rubygem-concurrent-ruby
Version:        1.2.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby-concurrency/concurrent-ruby
Source0:        https://github.com/ruby-concurrency/concurrent-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove_jar.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(concurrent-ruby) = %{version}-%{release}

%description
Modern concurrency tools including agents, futures, promises,
thread pools, supervisors, and more. Inspired by Erlang,
Clojure, Scala, Go, Java, JavaScript, and classic concurrency patterns.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add lib folder to buildroot from Source0
cp -r lib/ %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gem_instdir}/lib
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.2-1
- Auto-upgrade to 1.2.2 - Azure Linux 3.0 - package upgrades

* Tue May 31 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.10-4
- Cleanup

* Tue May 03 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.10-3
- Add lib/ from source

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.10-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.10-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
