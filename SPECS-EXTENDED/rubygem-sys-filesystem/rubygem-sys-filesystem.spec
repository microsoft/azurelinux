%global gem_name sys-filesystem

Name:           rubygem-%{gem_name}
Version:        1.4.3
Release:        6%{?dist}
Summary:        Interface for gathering filesystem information

License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://rubygems.org/gems/sys-filesystem
Source:         https://github.com/djberg96/sys-filesystem/archive/refs/tags/sys-filesystem-1.4.3.tar.gz#/rubygem-sys-filesystem-1.4.3.tar.gz

BuildRequires:  rubygems-devel

BuildArch:      noarch

%description
%{summary}.

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
%{summary}.

%prep
%autosetup -n %{gem_name}-%{gem_name}-%{version}
 
%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

rm -vr %{buildroot}%{gem_instdir}/{certs,spec}
rm -v %{buildroot}%{gem_cache}

%files
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}

%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/{{README,CHANGES,MANIFEST}.md,examples}
%{gem_instdir}/{Gemfile,Rakefile,%{gem_name}.gemspec}

%changelog
* Wed Oct 30 2024 Jyoti Kanase <v-jykanase@microsoft.com> - 1.4.3-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Igor Raits <igor.raits@gmail.com> - 1.4.3-2
- fixup! Initial import

* Fri Mar 03 2023 Igor Raits <igor.raits@gmail.com> - 1.4.3-1
- Initial import
