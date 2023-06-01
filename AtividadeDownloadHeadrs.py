#Atividade para armazenar o Hearder da imagem de uma URL em um arquivo
#autor: Jesue Lucas Diogo
#data: 17/05/2023
# URL de teste HTTP: http://www.httpbin.org/image/png
# URL de teste HTTPS: https://www.httpbin.org/image/png
import socket, ssl, sys
from wsgiref import headers
import xml.etree.ElementTree as ET


#Criação de variáveis e separação dos campos da URL
url_completa = input ()
lista_completa = url_completa.split("/", 3)
url_imagem = '/'+lista_completa[3]
url_host = lista_completa[2].split('.', 1)
url_host = url_host[1]
lista_nomeImage = url_completa.split('/', -1)
nome_imagem = lista_nomeImage[-1]
lista_sem_extensao = nome_imagem.split ('.')
imagem_sem_extensao = lista_sem_extensao[0]
headers_txt = imagem_sem_extensao + '.txt'
protocolo_site = lista_completa[0]
host_port = 0
imagem_dados = ''
buffer_size = 1024
code_page = 'UTF-8'
retorno_imagem_dados = ' '

#host_port verificando qual o protocolo da conexão
if protocolo_site == 'http:':
    host_port = 80
elif protocolo_site == 'https:':
    host_port = 443
else:
    print(' FTP em implementação')

#Tratamento da porta
if  host_port == 443:
#construindo requisição
    request  = f'HEARD {url_imagem} HTTP/1.1\r\n'#trocar get por header
    request += f'Host: {url_host}\r\n'
    request += 'User-Agent: Python\r\n'
    request += 'Connection: close\r\n\r\n'
#conexão com o servidor
    context = ssl.create_default_context()
    socket_rss  = socket.create_connection((url_host, host_port))
    socket_rss_wrap = context.wrap_socket(socket_rss, server_hostname=url_host)
#enviando requisição
    socket_rss_wrap.send(request.encode(code_page))
#recebendo dados
    while True:
        resposta = socket_rss_wrap.recv(buffer_size).decode(code_page)
        if not resposta: break
        retorno_imagem_dados += resposta
#gravando em um arquivo
    
    imagem_dados = retorno_imagem_dados
    #print(imagem_dados)
    file_output = open(headers_txt, 'wb')
    file_output.write(imagem_dados)
    file_output.close()
else:
#Construindo requisição HTTP
    url_request = f'HEAD /{url_imagem} HTTP/1.1\r\nHOST: {url_host}\r\n\r\n' 
# criação do socket
    print('cheguei no socket HTTP')
    print(url_host)
    print(url_imagem)
    print(host_port)
    sock_img = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_img.connect((url_host, host_port))
    sock_img.sendall(url_request.encode())

#Gravando em um arquivo
    imagem_dados = sock_img.recv(buffer_size)
    print(imagem_dados)
    file_output = open(headers_txt, 'wb')
    file_output.write(imagem_dados)
    file_output.close()
    
    sock_img.close()
print ('FIM')

print('--------------------------------------')
#print('url completa = ', url_completa)
#print('lista completa =', lista_completa)
print('Protocolo do site = ', protocolo_site)
print('URL do host', url_host)
print('url da imagem', url_imagem )
print('nome da imagem = ', nome_imagem)
print('nome do arquivo a ser salvo = ', headers_txt)
print('teste de variavel  = ',  host_port)