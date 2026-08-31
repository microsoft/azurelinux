# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gem_name kramdown-parser-gfm

Name:           rubygem-%{gem_name}
Summary:        Kramdown parser for GitHub-flavored markdown
Version:        1.1.0
Release:        16%{?dist}

# SPDX confirmed
License:        MIT

URL:            https://github.com/kramdown/parser-gfm
Source0:        https://rubygems.org/gems/%{gem_name}-%{version}.gem

# upstream patch to make test suite compatible with kramdown 2.2.0
Patch0:         %{url}/commit/ad48572.patch

BuildArch:      noarch

BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  ruby >= 2.3

BuildRequires:  rubygem(kramdown) >= 2.0.0
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rouge)

%description
kramdown-parser-gfm provides a kramdown parser for the GFM dialect of
Markdown.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

BuildArch: noarch

%description    doc
Documentation for %{name}.


%prep
%setup -q -n %{gem_name}-%{version}
%patch -P0 -p1


%build
gem build ../%{gem_name}-%{version}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# move a broken test out of the way
mv test/testcases/codeblock_fenced.text test/testcases/codeblock_fenced.disabled

ruby -I'lib' -e 'Dir.glob "./test/**test_*.rb", &method(:require)'

# move the broken test back
mv test/testcases/codeblock_fenced.disabled test/testcases/codeblock_fenced.text
popd


%files
%license %{gem_instdir}/COPYING

%dir %{gem_instdir}

%{gem_libdir}
%{gem_spec}

%exclude %{gem_instdir}/VERSION

%exclude %{gem_cache}

%files doc
%doc %{gem_docdir}

%doc %{gem_instdir}/CONTRIBUTERS

%{gem_instdir}/test


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 15 2020 Fabio Valentini <decathorpe@gmail.com> - 1.1.0-5
- Include upstream patch to make test suite compatible with kramdown 2.2.0.
- Fixes RHBZ#1865414

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 26 2019 Fabio Valentini <decathorpe@gmail.com> - 1.1.0-1
- Initial package

