Summary:        Test package A
Name:           A
Epoch:          1
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Azure Linux

# B is the source of the "%%macro_from_B" macro
BuildRequires:  B

%description
Test spec A.

%prep

%generate_buildrequires
%macro_from_B

%build

%install

%check

%files
%defattr(-,root,root)

%changelog
* Tue Aug 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Spec created.
