%global	gem_name test-unit-ruby-core

Name:		rubygem-%{gem_name}
Version:	1.0.6
Release:	1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	Additional test assertions for Ruby standard libraries
# SPDX confirmed
License:	BSD-2-Clause OR Ruby
URL:		https://github.com/ruby/test-unit-ruby-core

Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1:	%{gem_name}-%{version}-additional.tar.gz
# Source1 is created by $ bash %%SOURCE2 %%version
Source2:	test-unit-ruby-core-create-missing-files.sh
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel

BuildArch:		noarch

%description
Additional test assertions for Ruby standard libraries.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -b 1

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

# Install additional files
cp -a \
	BSDL \
	COPYING \
	README.md \
	%{buildroot}%{gem_instdir}/

rm -f %{buildroot}%{gem_cache}

%check
# No available test suite currently
exit 0

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/README.md
%license	%{gem_instdir}/BSDL
%license	%{gem_instdir}/COPYING
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Fri Dec 06 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.0.6-1
- Initial CBL-Mariner import from Fedora 41.
- License verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.6-1
- 1.0.6

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.5-1
- 1.0.5

* Wed Sep 13 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.3-1
- 1.0.3

* Thu Aug 31 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.2-1
- 1.0.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul  7 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-2
- Fix comment for source

* Thu Jun 22 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.1-1
- Initial package
