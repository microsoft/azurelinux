<?xml version='1.0'?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output
        doctype-public="-//OASIS//DTD DocBook MathML Module V1.1b1//EN"
        doctype-system="http://www.oasis-open.org/docbook/xml/mathml/1.1CR1/dbmathml.dtd"
        cdata-section-elements="book"
        indent="yes"
        encoding="UTF-8"
    />
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    

    <xsl:template match="refentry/refmeta">
        <xsl:element name="info">
            <xsl:element name="orgname">
                <xsl:attribute name="class">consortium</xsl:attribute>
                <xsl:text>opengl.org</xsl:text>
            </xsl:element>
        </xsl:element>
        <xsl:element name="refmeta">
            <xsl:apply-templates select="@*|node()"/>
            <xsl:element name="refmiscinfo">
                <xsl:attribute name="class">manual</xsl:attribute>
                <xsl:text>OpenGL Manual</xsl:text>
            </xsl:element>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>
