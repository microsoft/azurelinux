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

BuildRequires:  A

%description
Test spec A.

%prep

%build

%install

%check

%files
%defattr(-,root,root)

%changelog
* Tue Aug 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Spec created.
