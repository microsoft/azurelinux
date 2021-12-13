#!/bin/sh

XMLFMTOPS="-indentSize 2 -trimText -newlines"

if [ $# -eq 0 ]; then
echo PullParserDemo
echo ./run.sh samples.PullParserDemo $XMLFMTOPS xml/web.xml
echo ./run.sh samples.PullParserDemo $XMLFMTOPS xml/fibo.xml
echo
echo SAXDemo
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/web.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/test/test_schema.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/xhtml/xhtml-basic.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/contents.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/cdata.xml
echo ./run.sh -Dorg.xml.sax.driver=org.apache.xerces.parsers.SAXParser samples.SAXDemo $XMLFMTOPS xml/cdata.xml
echo ./run.sh -Dorg.xml.sax.driver=xml.aelfred2.SAXDriver samples.SAXDemo $XMLFMTOPS xml/cdata.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/testPI.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/namespaces.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/testNamespaces.xml
echo ./run.sh samples.SAXDemo $XMLFMTOPS xml/inline.xml
echo
echo DOMDemo
echo ./run.sh samples.dom.DOMDemo xml/contents.xml
echo
echo SAXDOMDemo
echo ./run.sh samples.dom.SAXDOMDemo xml/contents.xml
echo
echo JTidyDemo
echo ./run.sh samples.JTidyDemo $XMLFMTOPS readme.html
echo
echo VisitorDemo
echo ./run.sh samples.VisitorDemo xml/cdata.xml
echo
echo CountDemo
echo ./run.sh samples.CountDemo xml/fibo.xml
echo
echo CreateXMLDemo
echo ./run.sh samples.CreateXMLDemo
echo
echo HTMLWriterDemo
echo ./run.sh samples.HTMLWriterDemo xml/xhtml.xml
echo
echo PerformanceTest
echo ./run.sh -Xprof samples.performance.PerformanceSupport xml/periodic_table.xml org.dom4j.DocumentFactory 10
echo ./run.sh -Xprof -Dorg.xml.sax.driver=org.apache.xerces.parsers.SAXParser samples.performance.PerformanceSupport xml/periodic_table.xml org.dom4j.DocumentFactory 10
echo ./run.sh -Xprof -Dorg.xml.sax.driver=xml.aelfred2.SAXDriver samples.performance.PerformanceSupport xml/periodic_table.xml org.dom4j.DocumentFactory 10
echo ./run.sh -Xprof samples.performance.PerformanceSupport xml/much_ado.xml org.dom4j.DocumentFactory 10
echo ./run.sh -Xprof -Dorg.xml.sax.driver=org.apache.xerces.parsers.SAXParser samples.performance.PerformanceSupport xml/much_ado.xml org.dom4j.DocumentFactory 10
echo ./run.sh -Xprof -Dorg.xml.sax.driver=xml.aelfred2.SAXDriver samples.performance.PerformanceSupport xml/much_ado.xml org.dom4j.DocumentFactory 10
echo
echo XPathDemo
echo ./run.sh samples.XPathDemo xml/web.xml //servlet/servlet-class
echo ./run.sh samples.XPathDemo xml/much_ado.xml //ACT/TITLE
echo
echo XSLTDemo
echo ./run.sh samples.XSLTDemo xml/nitf/sample.xml xml/nitf/ashtml.xsl
echo
echo XSLTNativeDOMDemo
echo ./run.sh samples.dom.XSLTNativeDOMDemo xml/nitf/sample.xml xml/nitf/ashtml.xsl
echo
echo LargeDocumentDemo
echo ./run.sh samples.LargeDocumentDemo xml/much_ado.xml /PLAY/ACT
echo
echo LargeDocumentDemo2
echo ./run.sh samples.LargeDocumentDemo2 xml/much_ado.xml
echo
echo LinkCheckerDemo
echo ./run.sh samples.LinkChecker xml/xhtml/xhtml-basic.xml
echo
echo BeanDemo
echo ./run.sh samples.bean.BeanDemo xml/bean/gui.xml
echo
echo SAXValidatorDemo
echo ./run.sh samples.validate.SAXValidatorDemo xml/nitf/invalid.xml
echo
echo VisitorDemo
echo ./run.sh -Dorg.dom4j.factory=org.dom4j.datatype.DatatypeDocumentFactory samples.VisitorDemo  xml/schema/personal-schema.xml
echo
echo JTableDemo
echo ./run.sh samples.swing.JTableDemo  xml/web.xml
echo
echo JTableTool
echo ./run.sh samples.swing.JTableTool xml/swing/tableForAtoms.xml xml/periodic_table.xml
echo
echo JTreeDemo
echo ./run.sh samples.swing.JTreeDemo xml/web.xml
exit 0
fi 

if [ -z "$JAVA_HOME" ] ; then
  JAVA=`which java`
  if [ -z "$JAVA" ] ; then
    echo "Cannot find JAVA. Please set your PATH."
    exit 1
  fi
  JAVA_BIN=`dirname $JAVA`
  JAVA_HOME=$JAVA_BIN/..
fi

JAVA=$JAVA_HOME/bin/java

CLASSPATH=`build-classpath \
dom4j \
xpp2 \
jtidy \
fop \
xerces-j2 \
msv-relaxngDatatype \
msv-xsdlib \
msv-isorelax \
msv \
jaxen \
junit \
junitperf \
saxpath \
xalan-j2 \
xml-commons-apis \
avalon-framework \
avalon-logkit \
`:$CLASSPATH

BOOTCLASSPATH=`build-classpath \
xml-commons-apis \
xerces-j2 \
xalan-j2 \
`

CLASSPATH=classes:$CLASSPATH:$JAVA_HOME/lib/tools.jar


$JAVA -Xbootclasspath/p:$BOOTCLASSPATH -classpath $CLASSPATH "$@"
