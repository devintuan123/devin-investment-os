$SecretsFile = "secrets/api_keys.local.env"
$Vps = "root@45.32.52.205"
$RemotePath = "/root/devin-investment-os/.env"

if (!(Test-Path $SecretsFile)) {
    Write-Error "Missing $SecretsFile. Copy secrets/api_keys.template.env to secrets/api_keys.local.env first."
    exit 1
}

git check-ignore $SecretsFile | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "$SecretsFile is not ignored by git. Fix .gitignore before uploading."
    exit 1
}

scp $SecretsFile "${Vps}:${RemotePath}"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Upload failed."
    exit 1
}

ssh $Vps "chmod 600 /root/devin-investment-os/.env; chown root:root /root/devin-investment-os/.env; systemctl restart devin-investment-os; sleep 3; systemctl status devin-investment-os --no-pager"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Remote restart or status check failed."
    exit 1
}

Write-Host "Secrets uploaded and service restarted."
