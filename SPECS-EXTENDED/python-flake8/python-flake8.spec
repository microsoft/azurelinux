Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:             python-flake8
Version:          6.1.0
Release:          1%{?dist}
Summary:          Python code checking using pyflakes, pycodestyle, and mccabe
 
License:          MIT
URL:              https://github.com/PyCQA/flake8
Source:           %{url}/archive/%{version}/flake8-%{version}.tar.gz
 
BuildArch:        noarch
 
BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    python3-pip
BuildRequires:    python3-wheel
BuildRequires:    python%{python3_pkgversion}-pycodestyle
BuildRequires:    python%{python3_pkgversion}-pyflakes
BuildRequires:    python%{python3_pkgversion}-entrypoints
BuildRequires:    python%{python3_pkgversion}-mccabe
 
# tox config mixes coverage and tests, so we specify this manually instead
BuildRequires:    python%{python3_pkgversion}-pytest
 
%description
Flake8 is a wrapper around PyFlakes, pycodestyle, and Ned's McCabe
script. It runs all the tools by launching the single flake8 script,
and displays the warnings in a per-file, merged output.
 
It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.
 
%package -n python%{python3_pkgversion}-flake8
Summary:          %{summary}
 
%description -n python%{python3_pkgversion}-flake8
Flake8 is a wrapper around PyFlakes, pycodestyle, and Ned's McCabe
script. It runs all the tools by launching the single flake8 script,
and displays the warnings in a per-file, merged output.
 
It also adds a few features: files that contain "# flake8: noqa" are
skipped, lines that contain a "# noqa" comment at the end will not
issue warnings, Git and Mercurial hooks are included, a McCabe
complexity checker is included, and it is extendable through
flake8.extension entry points.
 
%prep
%autosetup -p1 -n flake8-%{version}
# Allow pycodestyle 2.12, https://bugzilla.redhat.com/2325146
sed -i 's/pycodestyle>=2.11.0,<2.12.0/pycodestyle>=2.11.0,<2.13.0/' setup.cfg
 
%generate_buildrequires
%pyproject_buildrequires
 
%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files flake8
 
# Backwards-compatibility symbolic links from when we had both Python 2 and 3
ln -s flake8 %{buildroot}%{_bindir}/flake8-3
ln -s flake8 %{buildroot}%{_bindir}/flake8-%{python3_version}
ln -s flake8 %{buildroot}%{_bindir}/python3-flake8
 
%check
%pytest -v

%files -n python%{python3_pkgversion}-flake8 -f %{pyproject_files}
%doc README.rst CONTRIBUTORS.txt
%{_bindir}/flake8
%{_bindir}/flake8-3
%{_bindir}/flake8-%{python3_version}
%{_bindir}/python3-flake8

%changelog
* Tue Apr 22 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 6.1.0-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
