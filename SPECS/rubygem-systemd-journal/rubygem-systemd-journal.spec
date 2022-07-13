%global debug_package %{nil}
%global gem_name systemd-journal
Summary:        Ruby bindings for reading/writing to the systemd journal
Name:           rubygem-%{gem_name}
Version:        1.4.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ledbettj/systemd-journal
Source0:        https://github.com/ledbettj/systemd-journal/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-ffi
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Provides the ability to navigate and read entries from the systemd
journal in ruby, as well as write events to the journal.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.4.2-1
- Update to v1.4.2.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 1.3.3-1
- License verified
- Original version for CBL-Mariner
