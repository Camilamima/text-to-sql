import pandas as pd
import webbrowser
import warnings
from groq import Groq
import psycopg2 as psy

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

####Escolha de banco de dados####
bd=0

while(bd!=1 and bd!=2):
    bd=int(input("Selecione o seu banco de dados, digite 1 para MySql, 2 Para Postgre:\n"))

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


##Caso when para opções do usuário##

opcao=0

while(opcao!=4):
    opcao=int(input("Você deseja:\n1-Ver tabelas disponiveis.\n2-Converter linguagem natural em query\n3-Ver Schema\n4-Sair\n"))

    match opcao:
        case 1: #Printra todas as tabelas atrávez de um looping

            ###Dependendo do banco de dados, faz uma lista com as tabelas disponíveis###
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

        case 2: ##faz a pesquisa via linguagem natural
            
            pergunta=input("Escreva a sua query em formato natural de linguagem:\n")

            ##Conexão com o Groq, envio de pergunta e schema do banco de dados para o modelo LLM##
            chat_resposta=client.chat.completions.create(
               messages=[
                    {"role": "system",
                    "content": "Você é um assistente de banco de dados, você irá receber perguntas em linguagem natural e deve responder com apenas a query SQL, sem nada a mais, caso a pergunta não seja relacionada ao banco de dados mandado, responda com 1." + banco_de_dados
                   },##Aqui foi dito ao sistema qual é o seu papel##
                   {"role": "user",
                        "content": [
                            {"type":"text",
                            "text": pergunta ##Manda a pergunta do usuário##
                            },
                            {"type":"image_url",
                            "image_url":{
                                "url": schema##Manda url com o schema"
                                }
                            }
                        ]
                    },
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct", ##Modelo utilizado, foi utilizado o Llama 4 Scout 17B, permitia imagens##
            )
            
            
            ##Converte em string e limpa a query##
            query=chat_resposta.choices[0].message.content
            query = query.replace("```sql", "").replace("```", "").strip()#as vezes o modelo retorna com ```sql''' ???
            print("\n",query,"\n")

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
            
           
        case 3:#abre imagem com schema
            webbrowser.open(schema)
            
cursor.close()
conexao.close()
