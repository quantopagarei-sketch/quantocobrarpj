# Copia a pasta do WhatsApp Business do Samsung S22 para o PC (só copia, não apaga nada no celular).
$ErrorActionPreference = 'Stop'
$base  = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'WhatsApp-S22'
$tools = Join-Path $base 'platform-tools'
$adb   = Join-Path $tools 'adb.exe'
New-Item -ItemType Directory -Force $base | Out-Null

function Fim($msg) { Write-Host ""; Write-Host $msg; Read-Host "Aperte Enter para fechar" | Out-Null; exit }

try {
  if (-not (Test-Path $adb)) {
    Write-Host "Baixando a ferramenta oficial do Google (adb), uma vez só..."
    $zip = Join-Path $base 'platform-tools.zip'
    Invoke-WebRequest 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile $zip
    Expand-Archive $zip -DestinationPath $base -Force
    Remove-Item $zip
  }
  & $adb start-server | Out-Null

  Write-Host ""
  Write-Host "No S22: ligue o cabo USB, escolha 'Transferindo arquivos' e toque em PERMITIR se aparecer 'Permitir depuração USB'."
  Write-Host "(Se não aparecer: Configurações > Sobre o telefone > Informações do software > toque 7 vezes em 'Número da versão';"
  Write-Host " depois Configurações > Opções do desenvolvedor > ative 'Depuração USB'.)"
  Write-Host ""
  $ok = $false
  for ($i = 0; $i -lt 60 -and -not $ok; $i++) {
    $lines = (& $adb devices) -split "`r?`n" | Where-Object { $_ -match "`t" }
    if ($lines | Where-Object { $_ -match "`tdevice$" }) { $ok = $true }
    elseif ($lines | Where-Object { $_ -match "unauthorized" }) { Write-Host "Aguardando você tocar em PERMITIR no celular..."; Start-Sleep 3 }
    else { Write-Host "Aguardando o S22 aparecer..."; Start-Sleep 3 }
  }
  if (-not $ok) { Fim "Não encontrei o S22. Confira o cabo e a depuração USB e rode de novo." }

  $src = '/sdcard/Android/media/com.whatsapp.w4b/WhatsApp Business'
  $chk = & $adb shell "ls '/sdcard/Android/media/com.whatsapp.w4b/WhatsApp Business/Databases' 2>&1"
  Write-Host "Backups encontrados no celular:"; $chk | ForEach-Object { Write-Host "  $_" }
  if (-not ($chk -match 'msgstore')) { Fim "Não achei os backups no S22. Abra o WhatsApp Business no S22 e faça um backup (Configurações > Conversas > Backup de conversas)." }
  if ($chk -match 'crypt14' -and -not ($chk -match 'crypt15')) { Write-Host "ATENÇÃO: só há backup .crypt14. Ative o backup com chave de 64 dígitos no S22 e faça um backup novo antes (veja o guia)." }

  $dest = Join-Path $base ("copia-" + (Get-Date -Format 'yyyy-MM-dd-HHmm'))
  New-Item -ItemType Directory -Force $dest | Out-Null
  Write-Host ""; Write-Host "Copiando para $dest (pode demorar)..."
  & $adb pull $src $dest
  $n = (Get-ChildItem $dest -Recurse -File | Measure-Object).Count
  $gb = [math]::Round(((Get-ChildItem $dest -Recurse -File | Measure-Object Length -Sum).Sum) / 1MB)
  Fim "Pronto: $n arquivos ($gb MB) em $dest`nAgora abra o Arquivo de Clientes > Importar e escolha o arquivo msgstore.db.crypt15 (pasta Databases) e a pasta Media."
} catch { Fim "Erro: $($_.Exception.Message)" }
