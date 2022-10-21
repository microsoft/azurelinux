%global debug_package %{nil}
%global gem_name protocol-hpack
Summary:        A compresssor and decompressor for HTTP 2.0 HPACK
Name:           rubygem-%{gem_name}
Version:        1.4.2
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/protocol-hpack
Source0:        https://github.com/socketry/protocol-hpack/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides a compressor and decompressor
for HTTP 2.0 headers, HPACK, as defined by RFC7541.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build http-hpack

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.4.2-2
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.4.2-1
- License verified
- Original version for CBL-Mariner
