Name:           gmileka-pkg-10
Version:        1.0.0
Release:        1%{?dist}
Summary:        Dummy package to test sequencing

License:        MIT
URL:            https://example.com/gmileka-pkg-10

Source0:        README

BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  pesign
BuildRequires:  gmileka-pkg-00

%description
A dummy package that includes only a README

%prep
cp %{SOURCE0} README

%build

%install
install -D -m 0644 README \
    %{buildroot}%{_docdir}/%{name}/README

%files
%doc %{_docdir}/%{name}/README

%changelog
* Fri Jun 26 2026 Test User <test@example.com> - 1.0.0-1
- Introduce a package to test sequencing.
