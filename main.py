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
    "Você é um assistente de classificação de e-mails de uma empresa. "
    "Seu objetivo é analisar o conteúdo de e-mails e classificá-los como Produtivo ou Improdutivo, com base nas regras abaixo:\n\n"
    "Produtivo: E-mails que requerem ação ou resposta, como solicitações de suporte, dúvidas sobre o sistema ou atualizações sobre casos em aberto.\n"
    "Improdutivo: E-mails que não exigem ação imediata, como mensagens de agradecimento, felicitações, spam ou conteúdo pessoal irrelevante.\n\n"
    "Leia o texto abaixo, e responda:\n"
    "1. Classifique o conteúdo como Produtivo ou Improdutivo (escreva apenas uma dessas palavras).\n"
    "2. Em seguida, escreva um breve resumo do conteúdo do e-mail (máximo 200 caracteres).\n\n"
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
