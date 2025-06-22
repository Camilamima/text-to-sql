# Projeto text-to-sql

## 📋 Sobre o Projeto
Este projeto cria uma conversão de linguagem natural para SQL utilizando LLM.

## 🔧 Tecnologias Utilizadas
- Python 3.8+
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
- Instale as blibliotecas necessárias com o comando: pip install "bliblioteca aqui".
- No site da groq, crie uma conta e baixe uma API:
- Substitua a api_key pela sua api
- Instale os bancos de dados (PostgreSQL e MySQL) e substitua as informações aqui:
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
- Crie o banco de dados usando os comandos SQL presentes aqui: (https://db-book.com/university-lab-dir/sample_tables-dir/index.html)
### 📖 Schema do banco de dado utilizado (university):
![Diagrama do Banco de Dados](https://raw.githubusercontent.com/Camilamima/text-to-sql/refs/heads/main/banco_de_dados.jpg)
