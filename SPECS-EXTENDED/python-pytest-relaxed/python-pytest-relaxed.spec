Name:           python-pytest-relaxed
Version:        2.0.2
Release:        3%{?dist}
Summary:        Relaxed test discovery/organization for pytest

License:        BSD-2-Clause
URL:            https://github.com/bitprophet/pytest-relaxed
Source:         %{url}/archive/%{version}/pytest-relaxed-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This package provides relaxed test discovery for pytest.

It is the spiritual successor to python3-spec, but is built for pytest instead
of nosetests, and rethinks some aspects of the design (such as increased
ability to opt-in to various behaviors).}

%description %_description

%package -n python3-pytest-relaxed
Summary:        %{summary}

%description -n python3-pytest-relaxed %_description


%prep
%autosetup -p1 -n pytest-relaxed-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files pytest_relaxed


%check
%pyproject_check_import
%pytest


%files -n python3-pytest-relaxed -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.2-2
- Rebuilt for Python 3.13

* Tue Apr 16 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 2.0.2-1
- Update to 2.0.2
- Fixes: rhbz#2209340

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.12

* Sat Mar 04 2023 Jiří Kučera <jkucera@redhat.com> - 2.0.0-1
- Update to 2.0.0
  Resolves: #2157782

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5^20220502git000bba0e-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon May 02 2022 Miro Hrončok <mhroncok@redhat.com> - 1.1.5^20220502git000bba0e-1
- Initial package from upstream pull request #22
  https://github.com/bitprophet/pytest-relaxed/pull/22

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.5-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Paul Howarth <paul@city-fan.org> - 1.1.5-9
- Avoid FTBFS with pytest 5

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-6
- Make the release strictly bigger than the last two builds (rhbz #1788771)

* Mon Oct 07 2019 Othman Madjoudj <athmane@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5 (rhbz #1697355)

* Sun Oct 06 2019 Othman Madjoudj <athmane@fedoraproject.org> - 1.1.5-5
- Drop python2 subpackage (python2 eol)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Paul Howarth <paul@city-fan.org> - 1.1.5-1
- Update to 1.1.5
- Re-enable the test suite

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-5
- Disable the test suite until a version compatible with pytest > 3.3 is available

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-2
- Minor packaging fixes

* Thu Nov 16 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1.0.0-1
- Initial spec

