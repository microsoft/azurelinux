%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ffi
Summary:        Ruby FFI
Name:           rubygem-ffi
Version:        1.13.1
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildRequires:  ruby >= 2.3.0

%description
Ruby-FFI is a gem for programmatically loading dynamically-linked native libraries,
binding functions within them, and calling those functions from Ruby code. Moreover,
a Ruby-FFI extension works without changes on CRuby (MRI), JRuby, Rubinius and TruffleRuby.
Discover why you should write your next extension using Ruby-FFI.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.13.1-1
- License verified
- Original version for CBL-Mariner