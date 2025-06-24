# Projeto text-to-sql

## 📋 Sobre o Projeto
Este projeto cria uma conversão de linguagem natural para SQL utilizando LLM. Projeto feito para a matéria de Banco de Dados da UTFPR.

## 🔧 Tecnologias Utilizadas
- Python 3.13+
- MySql
- PostgreSQL
  ###  🐛 Bibliotecas python:
      - psycopg2
      - pandas
      - webbrowser
      - warnings
      - groq
      - MySQLdb 

## 🚀 Como Executar

### Pré-requisitos
- Crie um servidor MySQL e Potsgre dentro do seu computador
- Instale as blibliotecas necessárias com o comando: pip install "bliblioteca aqui".
- No site da groq, crie uma conta e crie sua api aqui:
  <img width="820" alt="image" src="https://github.com/user-attachments/assets/2df5a19b-bed5-4f00-bf18-2fef04d21462" />

- Crie o banco de dados usando os comandos SQL(tanto no MySQL quanto no Postgre) presentes aqui: (https://db-book.com/university-lab-dir/sample_tables-dir/index.html)
- Caso utilize outro banco de dados que não seja o University, coloque um link com o DER novo aqui(ignore essa parte caso seja o mesmo banco de dados do passo anterior):

  <img width="509" alt="image" src="https://github.com/user-attachments/assets/68f3d6be-51cf-427a-8d87-42d6703be4c4" />


- Substitua o arquivo key abaixo com o diretorio do seu txt contendo sua api_key:
  <img width="548" alt="image" src="https://github.com/user-attachments/assets/053adb14-d1ab-4486-95e2-fbc3637ba6ae" />

- Substitua as informações do seu banco de dados nas seguintes linhas de código:
  ```bash
  if(bd==1):
    import MySQLdb as my
    conexao=my.connect(
        "localhost",
        "root", 
        "12345",
        "university"
    )
    banco_de_dados=" o banco é MySql"
    cursor=conexao.cursor()

  elif(bd==2):
    import psycopg2 as psy

    conexao=psy.connect(
        host="localhost",
        database="university",
        user="postgres",
        password="12345"
    )
    banco_de_dados=" o banco é PostgreSQL"
'''
- Agora é só rodar e brincar
### 📖 Schema do banco de dado utilizado (university):
![Diagrama do Banco de Dados](https://raw.githubusercontent.com/Camilamima/text-to-sql/refs/heads/main/banco_de_dados.png)
