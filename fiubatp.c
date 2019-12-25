// Proxy transparente para comunicar corrector.py con fiubatp.
//
// Descripción: Este programa hace forwarding de su entrada y salida
// estándar al socket del nuevo worker de fiubatp, si está presente. En
// caso de no estarlo, simplemente invoca al worker de Docker original.

#define WORKER_DOCKER "/srv/algo2/corrector/bin/worker.docker"
#define FIUBATP_SOCKET "/srv/fiubatp/run/worker.sock"

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    char fdarg[32];
    struct sockaddr_un addr = {0};
    int sock = socket(AF_UNIX, SOCK_STREAM, 0);

    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, FIUBATP_SOCKET, sizeof(addr.sun_path));

    if (connect(sock, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
        close(sock);
        execv(WORKER_DOCKER, argv);
    } else {
        snprintf(fdarg, sizeof(fdarg), "FD:%d", sock);
        execl("/usr/bin/socat", "socat", "STDIO", fdarg, NULL);
    }

    perror("exec");
    return -1;
}
