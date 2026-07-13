#include <mpi.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    int rank, source, dest;
    MPI_Request requests[4];
    const int tag1 = 6;
    const int tag2 = 10;
    char inmsg[64];
    const char outmsg0[] = "Using Tag1";
    const char outmsg1[] = "Again Using Tag1";
    const char outmsg2[] = "Using Tag2";
    const char outmsg3[] = "Again Using Tag2";

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank == 0) {
        dest = 1;
        MPI_Isend(outmsg0, (int)strlen(outmsg0) + 1, MPI_CHAR, dest, tag1, MPI_COMM_WORLD, &requests[0]);
        MPI_Isend(outmsg2, (int)strlen(outmsg2) + 1, MPI_CHAR, dest, tag2, MPI_COMM_WORLD, &requests[1]);
        MPI_Isend(outmsg1, (int)strlen(outmsg1) + 1, MPI_CHAR, dest, tag1, MPI_COMM_WORLD, &requests[2]);
        MPI_Isend(outmsg3, (int)strlen(outmsg3) + 1, MPI_CHAR, dest, tag2, MPI_COMM_WORLD, &requests[3]);
        MPI_Waitall(4, requests, MPI_STATUSES_IGNORE);
        printf("rank0 sent messages\n");
    } else if (rank == 1) {
        source = 0;
        memset(inmsg, 0, sizeof(inmsg));
        MPI_Recv(inmsg, sizeof(inmsg), MPI_CHAR, source, tag2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("tag2:%s\n", inmsg);
        memset(inmsg, 0, sizeof(inmsg));
        MPI_Recv(inmsg, sizeof(inmsg), MPI_CHAR, source, tag2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("tag2:%s\n", inmsg);
        memset(inmsg, 0, sizeof(inmsg));
        MPI_Recv(inmsg, sizeof(inmsg), MPI_CHAR, source, tag1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("tag1:%s\n", inmsg);
        memset(inmsg, 0, sizeof(inmsg));
        MPI_Recv(inmsg, sizeof(inmsg), MPI_CHAR, source, tag1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        printf("tag1:%s\n", inmsg);
    }

    MPI_Finalize();
    return 0;
}