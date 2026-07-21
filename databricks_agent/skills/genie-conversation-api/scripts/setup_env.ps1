<#
.SYNOPSIS
    Set Genie Conversation API environment variables (User scope) without
    exposing secrets.

.DESCRIPTION
    Prompts for the workspace host, the target Genie space id, and (optionally)
    a PAT via HIDDEN input, then stores them as user-scoped environment
    variables. The token is never written to a file, echoed, or placed on the
    command line / in history.

    Prefer OAuth (databricks auth login, or a service principal for automation)
    over a PAT. Use the PAT path only when necessary.

.NOTES
    - Values persist in the Windows per-user environment (registry). Rotate the
      token and delete these variables when done (see bottom of file).
    - Open a NEW terminal after running so the variables load.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\setup_env.ps1
#>

$ErrorActionPreference = 'Stop'

function Set-UserEnv {
    param([string]$Name, [string]$Value)
    [Environment]::SetEnvironmentVariable($Name, $Value, 'User')
    Set-Item -Path ("Env:{0}" -f $Name) -Value $Value
    Write-Host ("  set {0}" -f $Name) -ForegroundColor Green
}

Write-Host "Genie Conversation API environment setup" -ForegroundColor Cyan
Write-Host "----------------------------------------"

$hostUrl = Read-Host 'Workspace host (e.g. https://dbc-xxxx.cloud.databricks.com)'
if ([string]::IsNullOrWhiteSpace($hostUrl)) { throw 'Host is required.' }
if ($hostUrl -notmatch '^https://') { $hostUrl = "https://$hostUrl" }
Set-UserEnv -Name 'DATABRICKS_HOST' -Value $hostUrl

$spaceId = Read-Host 'Genie space id (the Genie Agent id)'
if ([string]::IsNullOrWhiteSpace($spaceId)) { throw 'Space id is required.' }
Set-UserEnv -Name 'GENIE_SPACE_ID' -Value $spaceId

$warehouseId = Read-Host 'SQL warehouse id (optional, press Enter to skip)'
if (-not [string]::IsNullOrWhiteSpace($warehouseId)) {
    Set-UserEnv -Name 'DATABRICKS_WAREHOUSE_ID' -Value $warehouseId
}

$useToken = Read-Host 'Set a PAT now? (y/N)  [choose N if using OAuth]'
if ($useToken -match '^[Yy]') {
    $secure = Read-Host 'Databricks PAT (input hidden)' -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
        if ([string]::IsNullOrWhiteSpace($token)) { throw 'Empty token.' }
        Set-UserEnv -Name 'DATABRICKS_TOKEN' -Value $token
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
        Remove-Variable token -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "  skipped PAT. Use 'databricks auth login --host <host>' (OAuth U2M)" -ForegroundColor Yellow
    Write-Host "  or configure a service principal (OAuth M2M) for automation." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done. Open a NEW terminal, then run:" -ForegroundColor Cyan
Write-Host "  python .\genie_conversation.py --question `"What were total sales last month?`""

# ---------------------------------------------------------------------------
# To remove these later (paste into PowerShell):
#   'DATABRICKS_HOST','DATABRICKS_TOKEN','GENIE_SPACE_ID','DATABRICKS_WAREHOUSE_ID' |
#     ForEach-Object { [Environment]::SetEnvironmentVariable($_, $null, 'User') }
# ---------------------------------------------------------------------------
