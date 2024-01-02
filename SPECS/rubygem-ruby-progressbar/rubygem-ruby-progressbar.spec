%global debug_package %{nil}
%global gem_name ruby-progressbar
Summary:        Ruby/ProgressBar is a text progress bar library for Ruby
Name:           rubygem-%{gem_name}
Version:        1.13.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/jfelchner/ruby-progressbar
Source0:        https://github.com/jfelchner/ruby-progressbar/archive/refs/tags/releases/v%{version}.tar.gz#/%{gem_name}-releases-v%{version}.tar.gz
Patch0:         remove-pem.patch
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby/ProgressBar is a flexible text progress bar library for
Ruby. The output can be customized with a flexible formatting system including:
percentage, bars of various formats, elapsed time and estimated time remaining.

%prep
%autosetup -p1 -n %{gem_name}-releases-v%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.13.0-1
- Auto-upgrade to 1.13.0 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.11.0-1
- Update to v1.11.0.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.10.1-1
- License verified
- Original version for CBL-Mariner
