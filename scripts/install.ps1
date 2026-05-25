# Zyos Support Agent Installer

$BasePath = 'C:\Zyos\AgentLab\zyos-support-agent-v1'

Write-Host ''
Write-Host '====================================='
Write-Host 'Installing Zyos Support Agent'
Write-Host '====================================='
Write-Host ''

New-Item -ItemType Directory -Force -Path $BasePath | Out-Null

Set-Location $BasePath

if (!(Test-Path '.venv')) {
    py -m venv .venv
}

& '.\.venv\Scripts\Activate.ps1'

python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ''
Write-Host 'Installation complete.' -ForegroundColor Green
Write-Host ''
Write-Host 'Launch with:' -ForegroundColor Yellow
Write-Host 'streamlit run app.py'
Write-Host ''
