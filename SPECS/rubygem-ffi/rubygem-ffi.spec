%global debug_package %{nil}
%global gem_name ffi
Summary:        Ruby FFI
Name:           rubygem-ffi
Version:        1.15.5
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ffi/ffi
Source0:        https://github.com/ffi/ffi/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove_missing_files.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby-FFI is a gem for programmatically loading dynamically-linked native libraries,
binding functions within them, and calling those functions from Ruby code. Moreover,
a Ruby-FFI extension works without changes on CRuby (MRI), JRuby, Rubinius and TruffleRuby.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE file to buildroot from Source0
cp LICENSE %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.13.1-1
- License verified
- Original version for CBL-Mariner
