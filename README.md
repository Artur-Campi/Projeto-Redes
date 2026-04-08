# LAB03 - Socket UDP e TCP 2026

Repositorio da atividade da disciplina de Redes de Computadores.

Este projeto foi desenvolvido para o **LAB03 - Socket UDP e TCP**, contemplando a analise dos exemplos fornecidos pelo professor e o desenvolvimento das aplicacoes solicitadas nas questoes da atividade.

## Integrante

- Lucas Carmo RA:10439830
- Artur Campi RA:10436740

## Objetivo do laboratorio

O laboratorio tem como objetivo praticar os conceitos de comunicacao em rede usando sockets, comparando os protocolos **UDP** e **TCP** e implementando aplicacoes cliente-servidor em Python.

## Estrutura do repositorio

### Arquivos base para estudo e analise

- `ClientTCP.py`
- `ServerTCP.py`
- `ClientUDP.py`
- `ServerUDP.py`

Esses arquivos foram utilizados para observar o funcionamento inicial dos sockets TCP e UDP, conforme solicitado na **Questao 1**.

### Aplicacoes desenvolvidas

- `Q3ServerTCP.py`
- `Q3ClientTCP.py`

## Questao 1

Na Questao 1, foi realizada a execucao e analise dos programas cliente e servidor com TCP e UDP, observando:

- o que acontece quando o cliente TCP e executado antes do servidor;
- a diferenca de comportamento entre TCP e UDP;
- o efeito de usar portas diferentes entre cliente e servidor.

Essa parte foi feita a partir dos arquivos base disponibilizados no laboratorio.

## Questao 2

Na Questao 2, a proposta do laboratorio e desenvolver um chat simples entre cliente e servidor usando UDP ou TCP, com troca de mensagens ate que uma das partes envie o comando `QUIT`.

Essa implementacao faz parte do projeto do laboratorio e deve acompanhar o restante dos codigos no repositorio.

## Questao 3

Para a Questao 3, foi desenvolvida uma aplicacao propria em Python usando **socket TCP** e **threads**.

A aplicacao simula o **controle remoto de uma sala inteligente**, onde varios clientes podem se conectar ao mesmo servidor e controlar dispositivos compartilhados em tempo real.

Os dispositivos controlados sao:

- lampada
- ventilador
- porta
- alarme

Cada cliente conectado pode consultar o estado da sala, visualizar os usuarios conectados e enviar comandos para alterar o ambiente. O servidor trata varias conexoes simultaneamente usando threads e compartilha as atualizacoes com todos os clientes conectados.

## Conceitos utilizados

- socket TCP
- socket UDP
- arquitetura cliente-servidor
- conexao orientada a fluxo
- comunicacao sem conexao
- troca de mensagens em rede
- threads para multiplas conexoes
- controle de estado compartilhado

## Reproducao do projeto

Para que um terceiro consiga reproduzir o funcionamento do laboratorio, este repositorio contem:

- os arquivos base usados nas analises;
- a aplicacao desenvolvida para a Questao 3;
- a documentacao de apoio;
- instrucoes de execucao.

## Links de entrega

- Video 1: adicionar link
- Video 2: adicionar link
- Repositorio GitHub: adicionar link

