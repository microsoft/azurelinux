Summary:        Test package B
Name:           B
Epoch:          1
Version:        1.0.0
Release:        1%{?dist}
License:        MIT
URL:            https://test.com
Source0:        macros.B
Group:          Test
Vendor:         Microsoft
Distribution:   Azure Linux

%description
Test spec B.

%prep

%build

%install
install -Dp -m644 %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.B

%check

%files
%defattr(-,root,root)
%{_rpmconfigdir}/macros.d/macros.B

%changelog
* Tue Aug 20 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Spec created.
