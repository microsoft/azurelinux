Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname suds

Summary: A python SOAP client
Name:  python-suds
Version: 1.0.0
Release: 2%{?dist}
Source0: https://github.com/suds-community/suds/archive/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
License: LGPLv3+
BuildArch: noarch
URL: https://github.com/suds-community/suds

BuildRequires: python3-devel
BuildRequires: python3-six

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

%global _description %{expand:
The suds project is a python soap web services client lib.  Suds leverages
python meta programming to provide an intuitive API for consuming web
services.  Objectification of types defined in the WSDL is provided
without class generation.  Programmers rarely need to read the WSDL since
services and WSDL based objects can be easily inspected.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} -m pip install pytest==7.1.2
%pytest

%files -n python3-%{srcname}
%{python3_sitelib}/%{srcname}*/
%doc README.md
%license LICENSE.txt

%changelog
* Fri Aug 26 2022 Muhammad Falak <mwani@microsoft.com> - 1.0.0-2
- Add BR on `python3-pip` & drop `python3-pytest` to enable ptest

* Fri Feb 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Updating to version 1.0.0 using Fedora 36 specs (license: MIT) for guidance.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.17.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 13 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-0.16.94664ddd46a6
- Subpackage python2-suds has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-0.15.94664ddd46a6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-0.14.94664ddd46a6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.13.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Scott Talbert <swt@techie.net> - 0.7-0.12.94664ddd46a6
- Fix FTBFS with Python 3.8 (#1719145)

* Tue Jun 11 2019 Scott Talbert <swt@techie.net> - 0.7-0.11.94664ddd46a6
- Adapt to support pytest4 (#1706285)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.10.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.9.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-0.8.94664ddd46a6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.7.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 08 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.7-0.6.94664ddd46a6
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.5.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-0.4.94664ddd46a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7-0.3.94664ddd46a6
- Rebuild for Python 3.6

* Sat Feb 06 2016 Scott Talbert <swt@techie.net> - 0.7-0.2.94664ddd46a6
- Applied patch from Haikel Guemar to support building on CentOS w/o Python 3
- Move BRs to subpackages, support python- vs python2- BRs on non-Fedora

* Fri Jan 01 2016 Scott Talbert <swt@techie.net> - 0.7-0.1.94664ddd46a6
- Switched to Jurko fork of suds
- Modernize python packaging, build python3 package
- Fixed bogus changelog dates

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.1-7
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 15 2010 jortel <jortel@redhat.com> - 0.4.1-1
- 0.4.1

* Wed Sep 8 2010 jortel <jortel@redhat.com> - 0.4-1
- Fix spelling errors in spec description.
- Fix source0 URL warning.
- Updated caching to not cache intermediate wsdls.
- Added DocumentCache which caches verified XML documents as text. User can choose.
- Added cachingpolicy option to allow user to specify whether to cache XML documents or the WSDL object.
- Provided for repeating values in reply for message parts consistent with way handled in nested objects.
- Added charset=utf-8 to stock content-type http header.
- Added <?xml version="1.0" encoding="UTF-8"?> to outgoing SOAP messages.
- Detection of faults in successful (http=200) replies and raise WebFault. Search for <soapenv:Fault/>.
- Add plugins facility. 
- Fixed Tickets: #251, #313, #314, #334

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Dec 17 2009 jortel <jortel@redhat.com> - 0.3.9-1
- Bumped python requires to 2.4
- Replaced stream-based caching in the transport package with document-based caching.
- Caches pickled Document objects instead of XML text. 2x Faster!
- No more SAX parsing exceptions on damaged or incomplete cached files. 
- Cached WSDL objects. Entire Definitions object including contained Schema object cached via pickle.
- Copy of soap encoding schema packaged with suds.
- Refactor Transports to use ProxyHandler instead of urllib2.Request.set_proxy().
- Added WSSE enhancements <Timestamp/> and <Expires/> support. See: Timestamp token. 
- Fixed Tickets: #256, #291, #294, #295, #296

* Wed Dec 9 2009 jortel <jortel@redhat.com> - 0.3.8-1
- Includeds Windows NTLM Transport.
- Add missing self.messages in Client.clone().
- Changed default behavior for WSDL PartElement to be optional.
- Add support for services/ports defined without <address/> element in WSDL.
- Fix sax.attribute.Element.attrib() to find by name only when ns is not specified; renamed to Element.getAttribute().
- Update HttpTransport to pass timeout parameter to urllib2 open() methods when supported by urllib2.
- Add null class to pass explicit NULL values for parameters and optional elements.
- Soap encoded array (soap-enc:Array) enhancement for rpc/encoded.
  Arrays passed as python arrays - works like document/literal now.
  No more using the factory to create the Array.
  Automatically includes arrayType attribute.  Eg: soap-enc:arrayType="Array[2]".
  Reintroduced ability to pass complex (objects) using python dict instead of suds object via factory.
- Fixed tickets: #84, #261, #262, #263, #265, #266, #278, #280, #282.

* Fri Oct 16 2009 jortel <jortel@redhat.com> - 0.3.7-1
- Better soap header support
- Added new transport HttpAuthenticated for active (not passive) basic authentication.
- New options (prefixes, timeout, retxml)
- WSDL processing enhancements.
- Expanded builtin XSD type support.
- Fixed <xs:iniclude/>
- Better XML date/datetime conversion.
- Client.clone() method added for lightweight copy of client object.
- XSD processing fixes/enhancements.
- Better <simpleType/> by <xs:restriction/> support.
- Performance enhancements. 
- Fixed tickets: #65, #232, #233, #235, #241, #242, #244, #247, #254, #254, #256, #257, #258

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 1 2009 jortel <jortel@redhat.com> - 0.3.6-1
- Change hard coded /tmp/suds to tempfile.gettempdir() and create suds/ on demand.
- Fix return type for Any.get_attribute().
- Update http caching to ignore file:// urls.
- Better logging of messages when only the reply is injected.
- Fix XInteger and XFloat types to translate returned arrays properly.
- Fix xs:import schema with same namespace.
- Update parser to not load external references and add Import.bind() for XMLSchema.xsd location.
- Add schema doctor - used to patch XSDs at runtime.  (See Options.doctor)
- Fix deprecation warnings in python 2.6.
- Add behavior for @default defined on <element/>.
- Change @xsi:type value to always be qualified for doc/literal.
- Add Option.xstq option to control when @xsi:type is qualified.
- Fixed Tickets: #64, #129, #205, #206, #217, #221, #222, #224, #225, #228, #229, #230

* Wed Feb 25 2009 jortel <jortel@redhat.com> - 0.3.5-1
- Adds http caching.  Default is (1) day.
- Removed checking fc version in spec since no longer building < fc9.
- Updated makefile to roll tarball with tar.sh.
- Moved bare/wrapped determination to wsdl for document/literal.
- Refactored Transport to provide better visibility into http headers.
- Fixed Tickets: #207, #207, #209, #210, #212, #214, #215

* Mon Dec 08 2008 jortel <jortel@redhat.com> - 0.3.4-1
- Static (automatic) Import.bind('https://schemas.xmlsoap.org/soap/encoding/')
- Basic ws-security with {{{UsernameToken}}} and clear-text password only.
- Add support for ''sparse'' soap headers via passing dictionary
- Add support for arbitrary user defined soap headers
- Fixes service operations with multiple soap header entries.
- Schema loading and dereferencing algorithm enhancements.
- Nested soap multirefs fixed.
- Better (true) support for elementFormDefault="unqualified" provides more accurate namespaing.
- WSDL part types no longer default to WSDL targetNamespace.
- Fixed Tickets: #4, #6, #21, #32, #62, #66, #71, #72, #114, #155, #201.

* Thu Dec 04 2008 jortel <jortel@redhat.com> - 0.3.3-2
- Rebuild for Python 2.6

* Thu Dec 04 2008 jortel <jortel@redhat.com> - 0.3.3-1
- No longer installs (tests) package.
- Implements API-3 proposal
    Pluggable transport
    Keyword method arguments
    Baisc http authentication in default transport
- Add namespace prefix normalization in soap message.
- Better soap message pruning of empty nodes.
- Fixed Tickets: #51 - #60.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.2-2
- Rebuild for Python 2.6

* Thu Nov 06 2008 jortel <jortel@redhat.com> - 0.3.2-1
- Add SOAP MultiRef support
- Add support for new schema tags:
    <xs:include/>
    <xs:simpleContent/>
    <xs:group/>
    <xs:attributeGroup/>
- Added support for new xs <--> python type conversions:
    xs:int
    xs:long
    xs:float
    xs:double
- Revise marshaller and binding to further sharpen the namespacing of nodes produced.
- Infinite recursion fixed in ''xsd'' package dereference() during schema loading.
- Add support for <wsdl:import/> of schema files into the wsdl root <definitions/>.
- Fix double encoding of (&)
- Add Client API:
    setheaders()  - Same as keyword but works for all invocations.
    addprefix()   - Mapping of namespace prefixes.
    setlocation() - Override the location in the wsdl.
    setproxy()    - Same as proxy keyword but for all invocations.
- Add proper namespace prefix for soap headers.
- Fixed Tickets: #5, #12, #34, #37, #40, #44, #45, #46, #48, #49, #50, #51

* Mon Nov 03 2008 jortel <jortel@redhat.com> - 0.3.1-5
- Add LICENSE to %%doc.

* Tue Oct 28 2008 jortel <jortel@redhat.com> - 0.3.1-4
- Changes acc. #466496 Comment #8

* Mon Oct 27 2008 jortel <jortel@redhat.com> - 0.3.1-3
- Add "rm -rf $RPM_BUILD_ROOT" to install

* Thu Oct 16 2008 jortel <jortel@redhat.com> - 0.3.1-2
- Changes acc. #466496 Comment #1

* Fri Oct 10 2008 jortel <jortel@redhat.com> - 0.3.1-1
- Extends the support for multi-port services introduced earlier. This addition, 
  provides for multiple services to define the *same* method and suds will
  handle it properly.  See section 'SERVICES WITH MULTIPLE PORTS:'
- Add support for multi-document document/literal soap binding style.
  See section 'MULTI-DOCUMENT Docuemnt/Literal:'
- Add support for (xs:group, xs:attributeGroup) tags.
- Add Client.last_sent() and Client.last_received().
