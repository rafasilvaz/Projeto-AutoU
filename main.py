#Importando as bibliotecas necessárias
from flask import Flask, render_template, request, redirect
import os
from openai import OpenAI
import json

#Configurar a chave da OpenAI
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

app = Flask(__name__)
app.config['SECRET_KEY'] = "senha123"
app.config['UPLOAD_FOLDER'] = "uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

#Função para ler arquivos .txt
def ler_arquivo_txt(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

#Função para ler PDFs
def ler_arquivo_pdf(caminho):
    try:
        import PyPDF2
        texto = ""
        with open(caminho, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                texto += page.extract_text() or ""
        return texto.strip()
    except:
        return "Erro ao ler o arquivo PDF."

#Função que envia o conteúdo para a IA da OpenAI
def analisar_conteudo(conteudo):
    prompt = (
        "Analise o conteúdo abaixo e respondade forma clara e objetiva (Não coloque as palavras em negrito ou itálico, e na resposta respeite o máximo de 250 tokens)\n"
        " 1. O conteúdo é relevante ou irrelevante para uma empresa que quer classificar e-mails importantes? (Responda apenas com 'O e-mail é Relevante' ou 'O e-mail é Irrelevante'.)\n"        
        "(Textos produtivos, como solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema, etc., são considerados relevantes. Emails que não necessitam de uma ação imediata ou são spam, como mensagens de felicitações, agradecimentos, piadas, ou assuntos pessoais, são irrelevantes.)\n\n"
        
        " 2. Faça um pequeno resumo ou resposta sobre o conteúdo.\n\n"
        f"Texto:\n{conteudo}\n\n"
        "Resposta:")

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        return f"Erro ao processar IA: {str(e)}"
    

#Rota principal
@app.route("/")
def home():
    return render_template("html/index.html")

#Rota que processa o formulário
@app.route("/results", methods=['POST'])
def results():
    text = request.form.get('conteudoemail')
    file = request.files.get('file')

    conteudo = ""

    if file and file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        if file.filename.lower().endswith('.txt'):
            conteudo = ler_arquivo_txt(filepath)
        elif file.filename.lower().endswith('.pdf'):
            conteudo = ler_arquivo_pdf(filepath)

    elif text and text.strip() != "":
        conteudo = text.strip()
    
    else:
        return redirect("/")  #Caso nenhum dado tenha sido enviado

    #Análise com IA
    resultado_ia = analisar_conteudo(conteudo)

    return render_template("html/result.html", resultado=resultado_ia)

if __name__ == '__main__':
    app.run(debug=True)
