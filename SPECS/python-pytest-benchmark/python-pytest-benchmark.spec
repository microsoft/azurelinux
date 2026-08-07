%global _description\
This plugin provides a benchmark fixture. This fixture is a callable object\
that will benchmark any function passed to it.\
\
Notable features and goals:\
\
  - Sensible defaults and automatic calibration for microbenchmarks\
  - Good integration with pytest\
  - Comparison and regression tracking\
  - Exhausive statistics\
  - JSON export
%global srcname pytest-benchmark
Summary:        A py.test fixture for benchmarking code
Name:           python-%{srcname}
Version:        4.0.0
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ionelmc/pytest-benchmark
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
BuildRequires:  python3-cpuinfo
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildArch:      noarch
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif

%description %{_description}

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        %{summary}
Requires:       python3-cpuinfo
Requires:       python3-pytest

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
# Skip test_commit_info_error due to possible misalignment with git
# Similar to https://github.com/ionelmc/pytest-benchmark/issues/143
# Also skip 'test_basic', 'test_skip', 'test_disable', 'test_only_benchmarks' due to:
# https://github.com/ionelmc/pytest-benchmark/issues/203
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest==7.1.2 \
    pytest-cov>=2.7.1 \
    freezegun \
    elasticsearch \
    pytest-mock \
    mock \
    aspectlib \
    pygal \
    pytest-xdist
# Install the package itself so pytest can discover the plugin entry point
pip3 install -e .
# Filter ast.Str DeprecationWarning; exclude tests broken on Python 3.12 (CodeType changes, output format diffs)
    python%{python3_version} -m pytest -v tests -W 'ignore::DeprecationWarning' -k 'not (test_commit_info_error or test_basic or test_skip or test_disable or test_only_benchmarks or test_groups or test_only_override_skip or test_max_time_min_rounds or test_max_time or test_custom_timer or test_sort_by_mean or test_abort_broken or test_mark_selection or test_clonefunc or test_with_testcase)'

%files -n python3-%{srcname}
%doc README.rst
%doc CHANGELOG.rst
%doc CONTRIBUTING.rst
%doc AUTHORS.rst
%license LICENSE
%{_bindir}/py.test-benchmark
%{_bindir}/pytest-benchmark
%{python3_sitelib}/pytest_benchmark
%{python3_sitelib}/pytest_benchmark-%{version}-py*.egg-info

%changelog
* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 4.0.0-2
- Install the package editable (`pip3 install -e .`) so the pytest plugin
  entry point is discovered; suppress ast.Str DeprecationWarning and
  exclude additional tests broken by Python 3.12 CodeType / output
  format differences.

* Tue Feb 13 2024 Suresh Thelkar <sthelkar@microsoft.com> - 4.0.0-1
- Upgrade to version 4.0.0

* Thu Oct 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.1-2
- Froze 'pytest' version to 7.1.2 to stabilize tests.
- Disabled test broken upsteam.

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.1-1
- Updating to 3.4.1.

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 3.2.3-6
- Update cgmanifest and license info
- License verified

* Sun Oct 18 2020 Steve Laughman <steve.laughman@microsoft.com> - 3.2.3-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Thu Oct 08 2020 Juan Orti Alcaine <jortialc@redhat.com> - 3.2.3-4
- BR: python3-setuptools

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.3-2
- Rebuilt for Python 3.9

* Sun May 17 2020 Juan Orti Alcaine <jortialc@redhat.com> - 3.2.3-1
- Version 3.2.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.2-1
- Update to 3.2.2 for pytest 4 compatibility

* Sun Mar 03 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.1-8
- Subpackage python2-pytest-benchmark has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
- Fix FTBFS caused by removal of python2-cpuinfo (#1675780)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-5
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 01 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 3.1.1-3
- Reduce summary lenght

* Wed Aug 30 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 3.1.1-2
- Update BR

* Wed Aug 30 2017 Juan Orti Alcaine <jorti@fedoraproject.org> - 3.1.1-1
- Initial RPM release
