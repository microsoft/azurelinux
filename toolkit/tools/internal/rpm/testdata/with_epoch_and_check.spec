Summary:        Test spec file with with no default package
Name:           with_epoch_and_check
Epoch:          1
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Group:          Test
Vendor:         Microsoft
Distribution:   Mariner

%description
Test spec. Make sure:
- The default package is built.
- The 'Epoch' equals 1!
- The '%check' section is present.

%prep

%build

%install

%check

%files
%defattr(-,root,root)

%changelog
* Wed Jun 21 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Creation of the test spec.
