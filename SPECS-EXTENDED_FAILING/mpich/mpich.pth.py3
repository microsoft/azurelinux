import sys, os; s = os.getenv('MPI_PYTHON3_SITEARCH'); s and (s in sys.path or sys.path.append(s))
