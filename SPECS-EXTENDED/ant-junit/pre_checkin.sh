#!/bin/sh
EDIT_WARNING="##### WARNING: please do not edit this auto generated spec file. Use the ant.spec! #####\n"
sed "s/^%bcond_without bootstrap$/${EDIT_WARNING}%bcond_with bootstrap/;
     s/^%bcond_with antlr/%bcond_without antlr/;
     s/^\(Name:.*\)$/\1-antlr/;
     0,/^Summary:.*/{s/^Summary:.*/Summary:        Antlr Task for ant/};
    " < ant.spec > ant-antlr.spec
cp ant.changes ant-antlr.changes
sed "s/^%bcond_without bootstrap$/${EDIT_WARNING}%bcond_with bootstrap/;
     s/^%bcond_with junit/%bcond_without junit/;
     s/^%bcond_without junit5/%bcond_with junit5/;
     s/^\(Name:.*\)$/\1-junit/;
     0,/^Summary:.*/{s/^Summary:.*/Summary:        Optional junit tasks for ant/};
    " < ant.spec > ant-junit.spec
cp ant.changes ant-junit.changes
sed "s/^%bcond_without bootstrap$/${EDIT_WARNING}%bcond_with bootstrap/;
     s/^%bcond_with junit5/%bcond_without junit5/;
     s/^\(Name:.*\)$/\1-junit5/;
     0,/^Summary:.*/{s/^Summary:.*/Summary:        Optional junit tasks for ant/};
    " < ant.spec > ant-junit5.spec
cp ant.changes ant-junit5.changes

