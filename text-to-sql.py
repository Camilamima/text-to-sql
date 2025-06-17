import pandas as pd
from PIL import Image
import warnings
from groq import Groq

#filtra os warnings do pd
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

#conexão ao Groq
client = Groq(
    api_key="",
)

#escolha de banco de dados
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
        case 2: 

            with open("C:/Users/admin/Desktop/banco de dados/dicionario.txt", 'r', encoding='utf-8') as f:
              conteudo = f.read()
            
            pergunta=input("Escreva a sua query em formato natural de linguagem:\n")

            conteudo_final = conteudo + "\n\n" + pergunta + "\n" + "+Caso não tenha como fazer isso em linguagem natural, retorne apenas o numero 1"
            
            chat_resposta=client.chat.completions.create(
               messages=[
                    {
                    "role": "user",
                    "content": conteudo_final
                    }
                ],
                model="gemma2-9b-it",
             )

            
            query=chat_resposta.choices[0].message.content

            query=query.removesuffix("```")
            query=query.removeprefix("```sql\n")

            print("\n",query)
            if (query.strip() =="1"):
                print("\nPergunta não relacionada ao banco de dados University\n")

            else:
                try:
                    df=pd.read_sql(query,conexao)
                    print(df)
                except Exception as error:
                    print("Ocorreu um erro!,query errada!")



        case 3:#abre imagem com schema
            imagem = Image.open("C:/Users/admin/Desktop/banco de dados/banco_de_dados.jpg")
            imagem.show()  







"""
pergunta=input("digite a pergunta:")

resposta: ChatResponse = chat(model='gemma3',
                              messages=[{
                                  'role':'user',
                                  'content':pergunta
                              },]
)

print(resposta['message']['content'])


"""

