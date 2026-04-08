# installation paths
SHAREDIR := /usr/share/selinux

AWK ?= gawk
NAME ?= $(strip $(shell $(AWK) -F= '/^SELINUXTYPE/{ print $$2 }' /etc/selinux/config))

ifeq ($(MLSENABLED),)
	MLSENABLED := 1
endif

ifeq ($(MLSENABLED),1)
	NTYPE = mcs
endif

ifeq ($(NAME),mls)
	NTYPE = mls
endif

TYPE ?= $(NTYPE)

HEADERDIR := $(SHAREDIR)/devel/include
include $(HEADERDIR)/Makefile
