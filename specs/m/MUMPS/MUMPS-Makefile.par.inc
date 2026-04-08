##
##  This file derives by that original in MUMPS 4.10.0.
##  Adapted by Antonio Trande from Make.inc/Makefile.gfortran.PAR for RPM packaging for Fedora.
##

#Begin orderings

# NOTE that PORD is distributed within MUMPS by default. If you would like to
# use other orderings, you need to obtain the corresponding package and modify
# the variables below accordingly.
# For example, to have Metis available within MUMPS:
#          1/ download Metis and compile it
#          2/ uncomment (suppress # in first column) lines
#             starting with LMETISDIR,  LMETIS
#          3/ add -Dmetis in line ORDERINGSF
#             ORDERINGSF  = -Dpord -Dmetis
#          4/ Compile and install MUMPS
#             make clean; make   (to clean up previous installation)
#
#          Metis/ParMetis and SCOTCH/PT-SCOTCH (ver 5.1 and later) orderings are now available for MUMPS.
#

SCOTCHDIR  = /usr
# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dscotch in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second 
# line (remember to add -Dptscotch in the ORDERINGSF variable below)

LSCOTCH    = -L$(SCOTCHDIR)/lib -lesmumps -lscotch -lscotcherr
LSCOTCH    = -L$(SCOTCHDIR)/lib -lptesmumps -lptscotch -lptscotcherr


LPORDDIR = $(topdir)/PORD/lib/
IPORD    = -I$(topdir)/PORD/include/
LPORD    = -L$(LPORDDIR) -lpord$(PLAT)

# You have to choose one among the following two lines depending on
# the type of analysis you want to perform. If you want to perform only
# sequential analysis choose the first (remember to add -Dmetis in the ORDERINGSF
# variable below); for both parallel and sequential analysis choose the second 
# line (remember to add -Dparmetis in the ORDERINGSF variable below)

LMETIS    = -L$(LMETISDIR) -lmetis

# The following variables will be used in the compilation process.
# Please note that -Dptscotch and -Dparmetis imply -Dscotch and -Dmetis respectively.

ORDERINGSF  = -Dpord
ORDERINGSC  = $(ORDERINGSF)

LORDERINGS = $(LMETIS) $(LPORD) $(LSCOTCH)
IORDERINGSF = $(ISCOTCH)
IORDERINGSC = $(IMETIS) $(IPORD) $(ISCOTCH)

#End orderings
########################################################################
################################################################################

PLAT    =
LIBEXT  = .so
OUTC    = -o 
OUTF    = -o 
RM = /bin/rm -f
CC = gcc
FC = gfortran
FL = gfortran
AR = ar vr
RANLIB  = echo
SCALAP  = -lscalapack
INCPAR = $(MUMPS_INCDIR)
MPIFLIB = @@MPIFORTRANLIB@@
MPICLIB = @@MPICLIB@@
METISLIB = -lmetis
LIBPAR = $(SCALAP) $(MPIFLIB) 
# See point 17 in the FAQ to have more details on the compilation of mpich with gfortran
INCSEQ = -I$(topdir)/libseq
LIBSEQ  =  -L$(topdir)/libseq -lmpiseq$(PLAT)
LIBOTHERS = -lpthread
#Preprocessor defs for calling Fortran from C (-DAdd_ or -DAdd__ or -DUPPER)
CDEFS   = -DAdd_

#Begin Optimized options
OPTF    = @@FFLAGS@@ -Dintel_ -Wno-unused-dummy-argument -Wno-maybe-uninitialized
OPTL    = @@LDFLAGS@@
OPTC    = @@CFLAGS@@
#End Optimized options
INCS = $(INCPAR)
LIBSEQNEEDED =
