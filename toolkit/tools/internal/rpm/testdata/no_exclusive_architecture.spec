Summary:        Test spec file with with no "ExclusiveArch" tag
Name:           no_exclusive_architecture
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Mariner

%description
Test spec. Make sure "ExclusiveArch" tag is not present!

%prep

%build

%install

%files
%defattr(-,root,root)

%changelog
* Mon Oct 11 2021 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0.0-1
- Creation of the test spec.

