// server_win.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <windows.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 4096


int main(){
    WSADATA wsaData;
    SOCKET server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_size = sizeof(client_addr);

    //init winsock
    int wsaStartup = WSAStartup(MAKEWORD(2,2), &wsaData);
    if (wsaStartup != 0){
        printf("Error ao inicializar winsock\n");
        return 1; 
    }

    //create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if(server_socket == INVALID_SOCKET){

        printf("Erro ao criar socket %d\n", WSAGetLastError);
        WSACleanup();
        return 1;
    }

    //config endereco do servidor
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    int server_socket_bind = bind(server_socket, (struct sockaddr*)&server_addr, sizeof(server_addr));

    if (server_socket_bind == SOCKET_ERROR){
        prinf("Erro no server_socket_bind: %d\n", WSAGetLastError());
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    //listen 
    if(listen(server_socket, 10) == SOCKET_ERROR){
        printf("erro no listen");
        closesocket(server_socket);
        WSACleanup();
        return 1;
    }

    printf("servidor rodando:  http://localhost:%d \n", PORT);
    
    while(1){
        client_socket = accept(server_socket, (struct scokaddr*)&client_addr, &client_addr_size);

        if (client_socket == INVALID_SOCKET){
            printf("erro no accept");
            continue;
        }

        handle_client(client_socket);

        /* LIMPEZA 
        closesocket(server_socket);
        WSACleanup();
        return 0;
        */
    }
}

void  send_response(SOCKET client_socket, const char *content, const char *content_type){
    char response[BUFFER_SIZE];
    int content_lenght = strlen(content);

    snprintf(response, sizeof(response), 
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: %s\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s", content_type, content_lenght, content);

    send(client_socket, response, strlen(response), 0);
}