# Caminho do projeto
$projectPath = "C:\Users\plata\Downloads\Projeto-AutoU-main"
$venvPath = "$projectPath\venv"

# Ir para a pasta do projeto
Set-Location -Path $projectPath

# Remover venv antiga, se existir
if (Test-Path $venvPath) {
    Write-Host "Removendo ambiente virtual antigo..."
    Remove-Item -Recurse -Force $venvPath
}

# Criar novo ambiente virtual
Write-Host "Criando novo ambiente virtual..."
python -m venv venv

# Ativar o ambiente virtual
Write-Host "Ativando ambiente virtual..."
& "$venvPath\Scripts\Activate.ps1"

# Instalar pacotes
Write-Host "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

Write-Host "Ambiente pronto! ✅"
