<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="1.1">
    <xsl:param name="distro"/>

    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="node()|@*"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match="rhel_only">
        <xsl:if test="$distro='rhel'">
            <xsl:apply-templates/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="rhel_or_centos">
        <xsl:if test="$distro='rhel'">
            <xsl:apply-templates/>
        </xsl:if>
        <xsl:if test="$distro='centos'">
            <xsl:apply-templates/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="centos_only">
        <xsl:if test="$distro='centos'">
            <xsl:apply-templates/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="eln_only">
        <xsl:if test="$distro='eln'">
            <xsl:apply-templates/>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>
