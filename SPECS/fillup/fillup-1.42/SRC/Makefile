
################################################################################
#									       #
#									       #
# Copyrights to SuSE GmbH (c) 1996, 1997, 1998, 1999, 2000, 2001, 2002         #
# Copyrights to SuSE Linux AG (c) 2002, 2003                                   #
#									       #
# Time-stamp:                                                                  #
# Project:     fillup                                                          #
# Module:                                                                      #
# Filename:    Makefile                                                        #
# Authors:     Martin Scherbaum/Joerg Dippel                                   #
# Description: see also getArguments.c                                         #
#									       #
################################################################################

# VERSION is only used in services.c
VERSION = 1.42

# DUMPFILE is now generated with tmpfile()

# Set "COMPILE_OPTION" to "DEBUG", "OPTIMIZE" or "PROFILE"
COMPILE_OPTION = DEBUG
# COMPILE_OPTION = OPTIMIZE
# COMPILE_OPTION = PROFILE

# the ldb directories
PROJ      = Fillup                      # project name
ROOTDIR   = ..                          # directory where project dir is located
PROJDIR   = ..
SRC	  = ${PROJDIR}/SRC
OBJ	  = ${PROJDIR}/OBJ
BIN	  = ${PROJDIR}/BIN
ARCHIVE   = ${PROJDIR}/ARCHIVE

# Set "WARNINGS" to whatever you want
WARNINGS = -Wall -Wmissing-prototypes -Wmissing-declarations -Wstrict-prototypes
# WARNINGS = -Wunused -Wswitch -Wformat -Wreturn-type -Wimplicit -Wmissing-prototypes -Wmissing-declarations

DEFINES   = 

# LINUX system
OPTISPLUS = 
TM	  = \"LINUX\"
INC       = -I/usr/include
COMPILER  = -DGCC=1

# Set OPTIS to the following values
OPTIS = $(OPTISPLUS) -O2 -fforce-addr -finline-functions -fno-function-cse \
	-fkeep-inline-functions

ifeq ($(COMPILE_OPTION),DEBUG)
  # compile for debugging
  COMPILE  = gcc -fsigned-char -DDEBUG -ansi -g -c ${WARNINGS} -I${SRC} -I${INC} ${COMPILER} ${SYS} ${DEFINES}
  LINK	   = gcc -g
endif

ifeq ($(COMPILE_OPTION),OPTIMIZE)
  # compile with all optimizations
  COMPILE  = gcc -fsigned-char -ansi -c $(OPTIS) $(WARNINGS) -I${SRC} -I${INC} ${COMPILER} ${SYS} ${DEFINES}
  LINK	   = gcc -O -s
endif

ifeq ($(COMPILE_OPTION),PROFILE)
  # compile for use with "gprof"
  COMPILE  = gcc -fsigned-char -ansi -pg -c ${WARNINGS} -I${SRC} -I${INC} ${COMPILER} ${SYS} ${DEFINES}
  LINK	   = gcc -pg
endif

#--------------------------------- targets to build -----------------------------------#

all: $(BIN)/fillup

#---------------------------------- linking files -------------------------------------#

OBJS = $(OBJ)/getArguments.o $(OBJ)/services.o $(OBJ)/parameters.o \
       $(OBJ)/parser.o $(OBJ)/file.o $(OBJ)/variableblock.o \
       $(OBJ)/fillup_cfg.o $(OBJ)/metadata.o $(OBJ)/validate.o \
       $(OBJ)/consume.o $(OBJ)/dump.o

$(BIN)/fillup: $(OBJS)
	$(LINK) $(OBJS) -o $(BIN)/fillup 

#----------------------------------- object files -------------------------------------#

$(OBJ)/getArguments.o: $(SRC)/getArguments.c $(SRC)/portab.h $(SRC)/parameters.h \
                $(SRC)/services.h
	$(COMPILE) -o $(OBJ)/getArguments.o $(SRC)/getArguments.c

$(OBJ)/services.o: $(SRC)/services.c $(SRC)/portab.h $(SRC)/services.h
	$(COMPILE) -DVERSION=${VERSION} -o $(OBJ)/services.o $(SRC)/services.c

$(OBJ)/parameters.o: $(SRC)/parameters.c $(SRC)/portab.h $(SRC)/parameters.h \
                $(SRC)/services.h
	$(COMPILE) -o $(OBJ)/parameters.o $(SRC)/parameters.c

$(OBJ)/parser.o: $(SRC)/parser.c $(SRC)/parser.h
	$(COMPILE) -o $(OBJ)/parser.o $(SRC)/parser.c

$(OBJ)/file.o:  $(SRC)/file.c $(SRC)/file.h 
	$(COMPILE) -o $(OBJ)/file.o $(SRC)/file.c

$(OBJ)/variableblock.o:  $(SRC)/variableblock.c $(SRC)/variableblock.h 
	$(COMPILE) -o $(OBJ)/variableblock.o $(SRC)/variableblock.c

$(OBJ)/fillup_cfg.o: $(SRC)/fillup_cfg.c 
	$(COMPILE) -o $(OBJ)/fillup_cfg.o $(SRC)/fillup_cfg.c

# -DFixedSequenceOfMetadata: no longer necessary: always fixed sequence
$(OBJ)/metadata.o: $(SRC)/metadata.c
	$(COMPILE) -o $(OBJ)/metadata.o $(SRC)/metadata.c

$(OBJ)/validate.o: $(SRC)/validate.c
	$(COMPILE) -o $(OBJ)/validate.o $(SRC)/validate.c

$(OBJ)/consume.o: $(SRC)/consume.c
	$(COMPILE) -o $(OBJ)/consume.o $(SRC)/consume.c

$(OBJ)/dump.o: $(SRC)/dump.c
	$(COMPILE) -o $(OBJ)/dump.o $(SRC)/dump.c

#----------------------------------- any functions ------------------------------------#

install: all
	install -s -o root -m 755 $(BIN)/fillup /bin

clean:
	rm -f $(OBJ)/*.o $(SRC)/\#* $(SRC)/*~ 

distclean: clean
	rm -f $(BIN)/*


