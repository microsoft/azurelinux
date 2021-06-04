%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Docutils -- Python Documentation Utilities.
Name:           python-docutils
Version:        0.14
Release:        4%{?dist}
License:        Public Domain, PSF-2.0, BSD, GPLv3
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/docutils
Source0:        https://files.pythonhosted.org/packages/source/d/docutils/docutils-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Docutils is a modular system for processing documentation into useful formats, such as HTML, XML, and LaTeX. For input Docutils supports reStructuredText, an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax.

%package -n     python3-docutils
Summary:        python-docutils
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-docutils
Python 3 version.

%prep
%setup -q -n docutils-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install

pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
for BINARY in rstpep2html rst2xml rst2xetex rst2s5 rst2pseudoxml rst2odt_prepstyles rst2odt rst2man rst2latex rst2html5 rst2html rst2html4
do
  mv %{buildroot}/%{_bindir}/$(echo $BINARY).py %{buildroot}%{_bindir}/$(echo $BINARY)3.py
  ln -sfv $(echo $BINARY)3.py %{buildroot}/%{_bindir}/$(echo $BINARY)3
done
popd

python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
for BINARY in rstpep2html rst2xml rst2xetex rst2s5 rst2pseudoxml rst2odt_prepstyles rst2odt rst2man rst2latex rst2html5 rst2html rst2html4
do
  ln -sfv $(echo $BINARY).py %{buildroot}%{_bindir}/$(echo $BINARY)
done


%check
PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python2_sitelib}
python2 test/alltests.py
pushd ../p3dir
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 test3/alltests.py
popd

%files
%defattr(-,root,root)
%license licenses
%{python2_sitelib}/*
%{_bindir}/rstpep2html
%{_bindir}/rst2xml
%{_bindir}/rst2xetex
%{_bindir}/rst2s5
%{_bindir}/rst2pseudoxml
%{_bindir}/rst2odt_prepstyles
%{_bindir}/rst2odt
%{_bindir}/rst2man
%{_bindir}/rst2latex
%{_bindir}/rst2html5
%{_bindir}/rst2html
%{_bindir}/rst2html4
%{_bindir}/rstpep2html.py
%{_bindir}/rst2xml.py
%{_bindir}/rst2xetex.py
%{_bindir}/rst2s5.py
%{_bindir}/rst2pseudoxml.py
%{_bindir}/rst2odt_prepstyles.py
%{_bindir}/rst2odt.py
%{_bindir}/rst2man.py
%{_bindir}/rst2latex.py
%{_bindir}/rst2html5.py
%{_bindir}/rst2html.py
%{_bindir}/rst2html4.py

%files -n python3-docutils
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/rstpep2html3
%{_bindir}/rst2xml3
%{_bindir}/rst2xetex3
%{_bindir}/rst2s53
%{_bindir}/rst2pseudoxml3
%{_bindir}/rst2odt_prepstyles3
%{_bindir}/rst2odt3
%{_bindir}/rst2man3
%{_bindir}/rst2latex3
%{_bindir}/rst2html53
%{_bindir}/rst2html3
%{_bindir}/rst2html43
%{_bindir}/rstpep2html3.py
%{_bindir}/rst2xml3.py
%{_bindir}/rst2xetex3.py
%{_bindir}/rst2s53.py
%{_bindir}/rst2pseudoxml3.py
%{_bindir}/rst2odt_prepstyles3.py
%{_bindir}/rst2odt3.py
%{_bindir}/rst2man3.py
%{_bindir}/rst2latex3.py
%{_bindir}/rst2html53.py
%{_bindir}/rst2html3.py
%{_bindir}/rst2html43.py

%changelog
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.14-4
- Follow the Fedora convention of providing a suffix-less binary name
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.14-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.14-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.14-1
- Update to version 0.14

* Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-3
- Add BuildRequires python-xml and python3-xml for the tests to pass

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13.1-2
- Create separate packages for python2 and python3 in the bin directory

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13.1-1
- Initial packaging for Photon
