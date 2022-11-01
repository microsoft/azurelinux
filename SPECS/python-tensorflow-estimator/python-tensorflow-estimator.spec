%global pypi_name tensorflow-estimator

Summary:        A high-level TensorFlow API that greatly simplifies machine learning programming
Name:           python-%{pypi_name}
Version:        2.10
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.org/project/%{pypi_name}/
Source0:        https://github.com/tensorflow/estimator/archive/v${version}.tar.gz#/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  bazel
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip


Requires:  python3-wrapt

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -p1 -n estimator-%{version}


%build
bazel build //tensorflow_estimator/tools/pip_package:build_pip_package
bazel-bin/tensorflow_estimator/tools/pip_package/build_pip_package ${srcdir}/estimator_pip

%install


%check
pip3 install more_itertools pluggy pytest
%py3_check_import tomli
# assert the properly built package has no runtime requires
# if it does, we need to change the bootstrap metadata
test -f %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
! grep '^Requires-Dist:' %{buildroot}%{python3_sitelib}/tomli-%{version}.dist-info/METADATA
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.md
%doc CHANGELOG.md
%license LICENSE

%changelog
* Thu Jul 22 2021 Petr Viktorin <pviktori@redhat.com> - 1.0.4-1
- Initial package
