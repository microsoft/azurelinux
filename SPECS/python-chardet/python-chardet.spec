Summary:        A Universal Character Encoding Detector in Python
Name:           python-chardet
Version:        5.2.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/chardet/chardet
#Source0:       https://github.com/chardet/chardet/archive/refs/tags/%{version}.tar.gz
Source0:        chardet-%{version}.tar.gz
# Hand-written for Fedora in groff_man(7) format based on --help output
Source1:        chardetect.1

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%package -n     python3-chardet
Summary:        python3-chardet
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
Requires:       python3
%if 0%{?with_check}
BuildRequires:  python3-pytest
%endif

%description -n python3-chardet
chardet is a universal character encoding detector in Python.

%prep
%autosetup -n chardet-%{version}

# Since pdflatex cannot handle Unicode inputs in general:
echo "latex_engine = 'xelatex'" >> docs/conf.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files chardet
install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 '%{SOURCE1}'

%check
# We cannot run the upstream tests because they would require data files with
# problematic license status.
%pyproject_check_import

%files -n python3-chardet
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/chardetect
%{_mandir}/man1/chardetect.1*

%changelog
* Thu May 09 2024 Betty Lakes <bettylakes@microsoft.com> - 5.2.0-1
- Upgrade to 5.2.0

* Thu Feb 10 2022 Nick Samson <nisamson@microsoft.com> - 4.0.0-1
- Updated to 4.0.0, updated source URL.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 3.0.4-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.0.4-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 3.0.4-4
- Renaming python-pytest to pytest

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> - 3.0.4-3
- Update URL.
- Update License.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.0.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 3.0.4-1
- Initial packaging.
