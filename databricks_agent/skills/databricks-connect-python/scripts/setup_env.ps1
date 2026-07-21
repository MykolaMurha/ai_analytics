<#
.SYNOPSIS
    Set Databricks Connect environment variables (User scope) for THIS Windows
    account, without exposing secrets.

.DESCRIPTION
    Prompts for the workspace host, compute target, and (if using a PAT) the
    token via HIDDEN input, then stores them as user-scoped environment
    variables. The token is never written to a file, never echoed, and never
    placed on the command line or in shell history.

    Prefer OAuth or a ~/.databrickscfg profile over a PAT when you can. Use this
    script only for the environment-variable PAT path.

.NOTES
    - Values are stored in the Windows per-user environment (registry). Anyone
      with access to your user profile can read them. Rotate the token
      regularly and delete these variables when done (see the bottom of this
      file).
    - Open a NEW terminal after running this so the variables are loaded.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\setup_env.ps1
#>

$ErrorActionPreference = 'Stop'

function Set-UserEnv {
    param([string]$Name, [string]$Value)
    [Environment]::SetEnvironmentVariable($Name, $Value, 'User')
    # also set in the current process so this session can use it immediately
    Set-Item -Path ("Env:{0}" -f $Name) -Value $Value
    Write-Host ("  set {0}" -f $Name) -ForegroundColor Green
}

Write-Host "Databricks Connect environment setup" -ForegroundColor Cyan
Write-Host "------------------------------------"

# --- Workspace host ---------------------------------------------------------
$hostUrl = Read-Host 'Workspace host (e.g. https://dbc-xxxx.cloud.databricks.com)'
if ([string]::IsNullOrWhiteSpace($hostUrl)) { throw 'Host is required.' }
if ($hostUrl -notmatch '^https://') { $hostUrl = "https://$hostUrl" }
Set-UserEnv -Name 'DATABRICKS_HOST' -Value $hostUrl

# --- Compute target ---------------------------------------------------------
$mode = Read-Host 'Compute: [S]erverless or [C]luster? (default S)'
if ([string]::IsNullOrWhiteSpace($mode)) { $mode = 'S' }

if ($mode -match '^[Cc]') {
    $clusterId = Read-Host 'Cluster ID'
    if ([string]::IsNullOrWhiteSpace($clusterId)) { throw 'Cluster ID is required for cluster mode.' }
    Set-UserEnv -Name 'DATABRICKS_CLUSTER_ID' -Value $clusterId
    # clear any serverless override so it does not take precedence
    [Environment]::SetEnvironmentVariable('DATABRICKS_SERVERLESS_COMPUTE_ID', $null, 'User')
} else {
    Set-UserEnv -Name 'DATABRICKS_SERVERLESS_COMPUTE_ID' -Value 'auto'
    [Environment]::SetEnvironmentVariable('DATABRICKS_CLUSTER_ID', $null, 'User')
}

# --- Auth: PAT (hidden) or skip for OAuth/profile ---------------------------
$useToken = Read-Host 'Set a PAT now? (y/N)  [choose N if using OAuth or a profile]'
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
    Write-Host "  or a named profile in ~/.databrickscfg instead." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done. Open a NEW terminal so the variables load, then run:" -ForegroundColor Cyan
Write-Host "  python .\verify_connection.py"

# ---------------------------------------------------------------------------
# To remove these later (paste into PowerShell):
#   'DATABRICKS_HOST','DATABRICKS_TOKEN','DATABRICKS_CLUSTER_ID','DATABRICKS_SERVERLESS_COMPUTE_ID' |
#     ForEach-Object { [Environment]::SetEnvironmentVariable($_, $null, 'User') }
# ---------------------------------------------------------------------------
