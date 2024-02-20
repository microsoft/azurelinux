%global gem_name ffi
Summary:        Ruby FFI
Name:           rubygem-ffi
Version:        1.16.3
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/ffi/ffi
# Using the source code from the gem to include the 'libffi' submodule.
# The upstream depends on the existence of the 'libffi' submodule, even
# if the system's version of 'libffi' ends up being used.
# Submodules are not included in GitHub release tarballs.
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:  git
BuildRequires:  libffi-devel
BuildRequires:  ruby

Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby-FFI is a gem for programmatically loading dynamically-linked native libraries,
binding functions within them, and calling those functions from Ruby code. Moreover,
a Ruby-FFI extension works without changes on CRuby (MRI), JRuby, Rubinius and TruffleRuby.

%prep
%autosetup -p1 -n %{gem_name}-%{version}
# Making sure gemspec finds the git repositories it's relying on for listing the files.
submodule_dir="ext/ffi_c/libffi"
git init .
git init $submodule_dir
git add . -- ":!$submodule_dir"
git -C $submodule_dir add .

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem -- --enable-system-libffi

%files
%defattr(-,root,root,-)
%license LICENSE
%{gemdir}

%changelog
* Thu Feb 08 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.3-2
- Re-enabled the debuginfo package.

* Wed Jan 31 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.3-1
- Upgrading to the latest version.
- Switched to using the gem as source to include the 'libffi' submodule.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.15.5-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.15.5-1
- Update to v1.15.5.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.13.1-1
- License verified
- Original version for CBL-Mariner
