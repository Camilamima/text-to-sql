import pandas as pd
import webbrowser
import warnings
from groq import Groq
import psycopg2 as psy

####Filtra os warnings do pd####
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

###URL do schema###
schema="https://github.com/Camilamima/text-to-sql/blob/main/banco_de_dados.jpg?raw=true"

####conexão ao Groq####
client = Groq(
    api_key="-----",
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
    opcao=int(input("Você deseja:\n1-Ver tabelas disponiveis.\n2-Fazer uma consulta em linguagem natural\n3-Ver Schema\n4-Sair\n"))

    match opcao:
        case 1: #Printra todas as tabelas atrávez de um looping

            tabelas = [
            "prereq",
            "time_slot",
            "advisor",
            "takes",
            "student",
            "teaches",
            "section",
            "instructor",
            "course",
            "department",
            "classroom"
            ]
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
                    "content": "Você é um assistente de banco de dados, você irá receber perguntas em linguagem natural e deve responder com apenas a query SQL, sem nada a mais, caso a pergunta não seja relacionada ao banco de dados University, responda com 1." + banco_de_dados
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
            
            
            ##Printa a query##
            query=chat_resposta.choices[0].message.content
            print("\n",query)

            if(query.strip() =="1"):
                print("\nPergunta não relacionada ao banco de dados\n")

            elif("SELECT" in query.upper()):
                try:
                    df=pd.read_sql(query,conexao)
                    print(df)
                except Exception as error:
                    print("Ocorreu um erro,query errada")

            elif("DELETE" in query.upper()):
                print("A query de exclusão não é permitida")

            elif("UPDATE" in query.upper() and "WHERE" not in query.upper()):
                print("Hoje não é dia de update sem where")
            else:
                try:
                    cursor.execute(query)
                    conexao.commit()
                    print("Query executada com sucesso")
                except Exception as error:
                    print("Ocorreu um erro, query errada")
            
           


        case 3:#abre imagem com schema
            webbrowser.open(schema)

conexao.close()






