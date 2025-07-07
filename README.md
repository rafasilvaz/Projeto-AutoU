## Projeto AutoU


<h3>Instalação do Ambiente remoto e Bibliotecas</h3>

Para instalar o ambiente remoto e as bibliotecas no seu computador é necessário primeiramente alterar a segunda linha do arquivo "setup.ps1" para o local onde se encontra o projeto no seu computador.

Após isto abra o PowerShell como administrador e execute:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

(caso ainda não tenha feito antes)

E depois execute o script:

.\setup.ps1


<h3>Chave da OpenAI</h3>

Após a instalação do ambiente remoto é necessário que você tenha uma chave da OpenAI para a utilização da IA no projeto.

Após a obtenção da chave da OpenAI, basta inseri-la na linha 9 onde está escrito "sua-chave-aqui" do arquivo "main.py".

Realizando estas breves configurações, o código poderá ser rodado normalmente.

(Vale lembrar apenas que a sua chave OpenAI não pode ser divulgada, então a mantenha em sigilo).

Caso tenha alguma dúvida sobre as linhas do código, é possível verificar suas explicações dentro dos arquivos em forma de comentários.

Obrigado por usar meu projeto, espero que goste!
