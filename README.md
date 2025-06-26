# Projeto text-to-sql

## 📋 Sobre o Projeto
Este projeto cria uma conversão de linguagem natural para SQL utilizando LLM. Projeto feito para a matéria de Banco de Dados da UTFPR.

## 🔧 Tecnologias Utilizadas
- Python 3.13+
- MySql
- PostgreSQL
- meta-llama/llama-4-scout-17b-16e-instruct (Modelo META llama 4 com 17b)
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
- No site da groq(https://console.groq.com/home), crie uma conta e crie sua api aqui:
  <img width="820" alt="image" src="https://github.com/user-attachments/assets/2df5a19b-bed5-4f00-bf18-2fef04d21462" />

- Crie o banco de dados usando os comandos SQL(tanto no MySQL quanto no Postgre) presentes aqui: (https://db-book.com/university-lab-dir/sample_tables-dir/index.html)
- Caso utilize outro banco de dados que não seja o University, coloque um link com o DER novo aqui(ignore essa parte caso seja o mesmo banco de dados do passo anterior):

  <img width="509" alt="image" src="https://github.com/user-attachments/assets/68f3d6be-51cf-427a-8d87-42d6703be4c4" />


- Substitua o arquivo key abaixo com o diretorio do seu txt contendo sua api_key:
  <img width="548" alt="image" src="https://github.com/user-attachments/assets/053adb14-d1ab-4486-95e2-fbc3637ba6ae" />

- Substitua as informações do seu banco de dados nas seguintes linhas de código:
  ```python
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
###  💻  Como o código fuinciona?
- Primeiramente, dentro do código, são definidas as funções:
   - conectar_bd, a função que recebe um argumento que vai ser usado para conectar ao MySQLdb ou o PostgreSQL:
      ```python
      def conectar_bd(bd):
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
          cursor=conexao.cursor()
      return conexao, cursor, banco_de_dados
      ```
    - Função printa_tabelas, printa atráves de uma consulta e comandos diretos ao banco de dado a tabela e 3 linhas delas dependendo do banco de dados escolido(recebe bd):
        ```python
        def printa_tabelas(cursor,bd,conexao):
          if bd==1:
              query_tabelas="SELECT table_name FROM information_schema.tables WHERE table_schema = 'university';"
          else:
              query_tabelas="SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
          
          cursor.execute(query_tabelas)
      
          tabelas = [t[0] for t in cursor.fetchall()]
      
          #printa todas as tabelas disponíveis   
          for i in tabelas:
              query=f"SELECT * FROM {i} LIMIT 3"
              df=pd.read_sql(query,conexao)
              print("Tabela:",i)
              print(df,"\n")
        ```
  - Função pergunta_groq, nela sera recebida a pergunta em formato string, o link do schema, e a chave api do groq. Dentro da conexão groq são enviadas a role que a inteligencia artifical vai usar(ser um assistente de banco de dados", o schema via url de imagem e a pergunta, além de ser mandado o modelo a ser usado(meta-llama/llama-4-scout-17b-16e-instruct). A função retorna a resposta em string.
      ```python
        def pergunta_groq(pergunta, schema, client):
        chat_resposta = client.chat.completions.create(
          messages=[
            {"role": "system",
             "content": "Você é um assistente de banco de dados, você irá receber perguntas em linguagem natural e deve responder com apenas a query SQL, sem nada a mais, caso a pergunta não seja relacionada ao banco de dados mandado, responda com 1." + banco_de_dados
             },
            {"role": "user",
             "content": [
                 {"type": "text",
                  "text": pergunta
                  },
                 {"type": "image_url",
                  "image_url": {
                    "url": schema
                      }
                    }
                 ]
             },
          ],
          model="meta-llama/llama-4-scout-17b-16e-instruct",  # Modelo utilizado
          )
      return chat_resposta.choices[0].message.content
      ```
   - Função interacao_bd, vai receber a query que foi feita, a conexão e o cursor do banco de dados, nela, dependendo do que tiver na string da query, sera feito uma das interações com o bd:
     ```python
      def interacao_bd(query,conexao,cursor):
        if(query.strip() =="1"):
            print("Pergunta não relacionada ao banco de dados\n")
    
        elif("SELECT" in query.upper()):
            try:
                df=pd.read_sql(query,conexao)
                print(df)
            except Exception as error:
                print("Ocorreu um erro ao executar a query:", error)
    
        elif("DROP" in query.upper()):
            print("A query de drop não é permitida")
    
        elif("DELETE" in query.upper() and "WHERE" not in query.upper()):
            print("Hoje não é dia de delete sem where")
    
        elif("UPDATE" in query.upper() and "WHERE" not in query.upper()):
            print("Hoje não é dia de update sem where")
            
        else:
            try:
                cursor.execute(query)
                conexao.commit()
                print("Query executada com sucesso")
            except Exception as error:
                print("Ocorreu um erro ao executar a query:", error)
                conexao.rollback()
   ```
- Depois, são definidos o schema e a chave api, além de filtrar warnings:
  ```python
     ####Filtra os warnings do pd####
    warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")
    
    ###URL do schema###
    schema="https://github.com/Camilamima/text-to-sql/blob/main/banco_de_dados.png?raw=true"
    
    ####Le a chave API pra não cair mais no github####
    with open(r"C:\Users\admin\Desktop\banco de dados\api_key.txt", "r") as arquivo:
        key = arquivo.read().strip()  # Lê a chave da API do arquivo
    
    ####conexão ao Groq####
    client = Groq(
        api_key=key,
    )
  ```
- Agora, temos a definição do banco de dados pelo usuário e retorno de conexão, cursor e o tipo de bando de dados
  ```python
    ####Escolha de banco de dados####
      bd=0
      
      while(bd!=1 and bd!=2):
          bd=int(input("Selecione o seu banco de dados, digite 1 para MySql, 2 Para Postgre:\n"))
      
      conexao, cursor, banco_de_dados = conectar_bd(bd)
  ```
- Depois, temos o case when, permitindo 1- printar as tabelas(chamando a função printar_tabelas),2-Converter linguagem natural em query(que recebe a pergunta do usuário via imput, depois chama a função conecta groq, trata a string, e chama a interacao_bd), 3- ver Schema(abre o DER do schema no navegador, para o usuário ver), e 4 - Sair(sai do programa).
  Agora, temos a definição do banco de dados pelo usuário e retorno de conexão, cursor e o tipo de bando de dados
  ```python
   while(opcao!=4):
    opcao=int(input("Você deseja:\n1-Ver tabelas disponiveis.\n2-Converter linguagem natural em query\n3-Ver Schema\n4-Sair\n"))

    match opcao:
        case 1:##printa todas as tabelas
            printa_tabelas(cursor,bd,conexao)

        case 2: ##faz a pesquisa via linguagem natural
            
            pergunta=input("Escreva a sua query em formato natural de linguagem:\n")
            
            ##Converte em string e limpa a query##
            query=pergunta_groq(pergunta, schema, client)

            query = query.replace("```sql", "").replace("```", "").strip()#as vezes o modelo retorna com ```sql''' ???

            print("\n",query,"\n")

            interacao_bd(query,conexao,cursor)
            
           
        case 3:#abre imagem com schema
            webbrowser.open(schema)
  ```
- Por fim, a conexõe com o banco de dados é fechada:
    
  ```python
  cursor.close()
  conexao.close()
  ```
    
    
### 📖 Schema do banco de dado utilizado (university):
![Diagrama do Banco de Dados](https://raw.githubusercontent.com/Camilamima/text-to-sql/refs/heads/main/banco_de_dados.png)
