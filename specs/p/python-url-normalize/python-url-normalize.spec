# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname url-normalize

Name: python-%{srcname}
Version: 1.4.3
Release: 10%{?dist}
Summary: Python URI normalizator

License: MIT
Url: https://github.com/niksite/url-normalize
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# https://github.com/niksite/url-normalize/pull/28
Patch0:         https://github.com/niksite/url-normalize/pull/28.patch#/python-url-normalize-poetry-core.patch

BuildArch: noarch
BuildRequires: python3-devel
# needed for check
BuildRequires: python3dist(pytest)

%global _description %{expand:

URI Normalization function
 * Take care of IDN domains.
 * Always provide the URI scheme in lowercase characters.
 * Always provide the host, if any, in lowercase characters.
 * Only perform percent-encoding where it is essential.
 * Always use uppercase A-through-F characters when percent-encoding.
 * Prevent dot-segments appearing in non-relative URI paths.
 * For schemes that define a default authority, use an empty authority if the
   default is desired.
 * For schemes that define an empty path to be equivalent to a path of "/",
   use "/".
 * For schemes that define a port, use an empty port if the default is desired
 * All portions of the URI must be utf-8 encoded NFC from Unicode strings

Inspired by Sam Ruby's urlnorm.py:
    http://intertwingly.net/blog/2004/08/04/Urlnorm
This fork author: Nikolay Panov (<pythonista@npanov.com>)
}

%description %_description

%generate_buildrequires
%pyproject_buildrequires

%package -n python3-%{srcname}
Summary: %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p 1 -n %{srcname}-%{version}

# supplied tox.ini causes check to fail, will use pytest instead
rm tox.ini

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files url_normalize

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.4.3-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.3-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.4.3-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.4.3-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 29 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 1.4.3-1
- initial specfile
- 1.4.3 release

