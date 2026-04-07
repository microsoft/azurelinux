# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global github_owner    kevin1024
%global github_name     pytest-httpbin
%global modname         pytest_httpbin

%global desc Pytest-httpbin creates a pytest fixture that is dependency-injected into your \
tests. It automatically starts up a HTTP server in a separate thread running \
a local instance of httpbin (a web service for testing HTTP libraries) and \
provides your test with the URL in the fixture.

%global sum Fixture providing local instance of httpbin test service

Name:           python-%{github_name}
Version:        2.1.0
Release:        6%{?dist}
Summary:        %{sum}

# License is included in-line in README.md
License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
# NOTE: the source includes a CA trust bundle (certs/cacert.pem). We
# don't replace it with the system-wide trust bundle because it's only
# used for httpbin itself and contains only the self-signed cert,
# valid only for 127.0.0.1, that the test server uses. We can't
# replace it because we can't actually securely have the test server
# use a cert that would be trusted by the system-wide trust bundle.
%global ghversion %(v=%{version}; echo $v | sed -r "s,[\\^~],,g")
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/v%{ghversion}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
%{desc}

#################################################################################
%package -n python3-%{github_name}
Summary:        %{sum}

%description -n python3-%{github_name}
%{desc}

This package provides the Python 3 implementation.

#################################################################################
%prep
%autosetup -n %{github_name}-%{ghversion} -p1

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{modname}

#################################################################################
%check
# we don't use tox because upstream's tox config is a bit odd and has
# an unsatisfiable dependency that's only relevant to Github Actions
%pytest

#################################################################################
%files -n python3-%{github_name} -f %{pyproject_files}
%doc DESCRIPTION.rst README.md

#################################################################################
%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.1.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Adam Williamson <awilliam@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 2.0.0-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.12

* Thu May 11 2023 Adam Williamson <awilliam@redhat.com> - 2.0.0-1
- Update to 2.0.0 final, re-enable fixed test

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0~rc1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Adam Williamson <awilliam@redhat.com> - 2.0.0~rc1-1
- Update to 2.0.0~rc1, disable a broken test

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.0.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Update to 1.0.0
- Resolves rhbz#1676023

* Sat May 30 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-13
- Drop manual requires to support usage with pytest4

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-12
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Adam Williamson <awilliam@redhat.com> - 0.3.0-6
- Disable Python 2 build on F30+
- Drop all EPEL compat bits for now as we can't build on EPEL

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-4
- Make sure not to autouse fixtures from the API

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Adam Williamson <awilliam@redhat.com> - 0.3.0-1
- New release 0.3.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.2.3-6
- Remove useless (and broken) requires on python3-pkgversion-macros

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Adam Williamson <awilliam@redhat.com> - 0.2.3-4
- Drop some unnecessary requirements

* Thu Dec 29 2016 Adam Williamson <awilliam@redhat.com> - 0.2.3-3
- Ensure we own all packaged dirs

* Thu Dec 29 2016 Adam Williamson <awilliam@redhat.com> - 0.2.3-2
- Fix subpackage names

* Thu Dec 29 2016 Adam Williamson <awilliam@redhat.com> - 0.2.3-1
- Initial package
