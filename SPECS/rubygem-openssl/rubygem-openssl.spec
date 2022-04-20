%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name openssl
Summary:        OpenSSL provides SSL, TLS and general purpose cryptography
Name:           rubygem-openssl
Version:        3.0.0
Release:        2%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/openssl
Source0:        https://github.com/ruby/openssl/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(openssl) = %{version}-%{release}

%description
OpenSSL provides SSL, TLS and general purpose cryptography. It wraps the
OpenSSL library.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.0-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.0-1
- License verified
- Included descriptions from Fedora 33 spec (license: MIT).
- Original version for CBL-Mariner
