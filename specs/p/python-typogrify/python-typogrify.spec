# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name typogrify

Name:           python-%{pypi_name}
Version:        2.0.7
Release:        27%{?dist}
Summary:        Filters to enhance web typography, with support for Django & Jinja templates

# typogrify/packages/titlecase/__init__.py is MIT
License:        BSD-3-Clause AND MIT
URL:            https://github.com/mintchaos/typogrify
Source:         %{pypi_source %{pypi_name}}
BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
Typogrify provides a set of custom filters that automatically apply various
transformations to plain text in order to yield typographically-improved HTML.
While often used in conjunction with Jinja_ and Django_ template systems, the
filters can be used in any environment.}

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %_description


%prep
%autosetup -n %{pypi_name}-%{version}
# remove shebang line from the python scripts
for lib in $(find -type f -name '*.py'); do
 sed -i.python -e '1{\@^#!@d}' $lib
done

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{pypi_name}

%check
# importing typogrify.templatetags.jinja_filters needs jinja2 installed
# importing typogrify.templatetags.typogrify_tags needs django installed
%pyproject_check_import -e typogrify.templatetags.jinja_filters -e typogrify.templatetags.typogrify_tags

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.7-27
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.7-26
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.0.7-24
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 23 2024 Carl George <carlwgeorge@fedoraproject.org> - 2.0.7-22
- Port to pyproject macros

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.7-20
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.7-16
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.7-13
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-11
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.7-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.7-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.7-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.7-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 José Matos <jamatos@fedoraproject.org> - 2.0.7-2
- fix source url and summary.
- remove shebang lines from python scripts.


* Sat Sep  1 2018 José Matos <jamatos@fedoraproject.org> - 2.0.7-1
- initial package.
