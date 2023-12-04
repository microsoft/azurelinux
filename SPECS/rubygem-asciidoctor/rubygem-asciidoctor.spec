%global debug_package %{nil}
%global gem_name asciidoctor
Summary:        A fast, open source AsciiDoc implementation in Ruby
Name:           rubygem-%{gem_name}
Version:        2.0.20
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         Microsoft Corporation
Distribution:	Mariner
URL:            https://asciidoctor.org/
Source0:        https://github.com/%{gem_name}/%{gem_name}/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A fast, open source AsciiDoc implementation in Ruby.

%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
 
%description doc
Documentation for %{name}

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} --bindir %{buildroot}%{_bindir} %{gem_name}-%{version}.gem

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%doc %{gem_instdir}/CHANGELOG.adoc
%doc %{gem_instdir}/README.*
%lang(de) %doc %{gem_instdir}/README-de.*
%lang(fr) %doc %{gem_instdir}/README-fr.*
%lang(ja) %doc %{gem_instdir}/README-jp.*
%lang(zh_CN) %doc %{gem_instdir}/README-zh_CN.*
%{gem_instdir}/data
%{gem_libdir}
%{gem_spec}
%{_bindir}/asciidoctor
%{gem_instdir}/bin
%{gem_instdir}/man/asciidoctor.*
%exclude %{gem_cache}
%exclude %{gem_instdir}/asciidoctor.gemspec
 
%files doc
%doc %{gem_docdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.20-1
- Auto-upgrade to 2.0.20 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.17-3
- Add provides, bindir

* Sun Apr 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.17-2
- Fixing build with ruby macros for Ruby 3.1.2.

* Mon Feb 28 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.0.17-1
- Update to v2.0.17.
- Build from .tar.gz source.

* Tue Dec 28 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.0.15-1
- Original version for CBL-Mariner
- License verified