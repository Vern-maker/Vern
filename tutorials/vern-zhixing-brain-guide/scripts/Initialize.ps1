param(
    [Parameter(Mandatory=$true)][string]$Root,
    [string]$PythonCommand = 'py',
    [string[]]$PythonArgs = @()
)
$ErrorActionPreference = 'Stop'
Get-Command $PythonCommand -ErrorAction Stop | Out-Null
if ($PythonArgs.Count -eq 0 -and [IO.Path]::GetFileNameWithoutExtension($PythonCommand) -eq 'py') { $PythonArgs = @('-3') }
& $PythonCommand @PythonArgs (Join-Path $PSScriptRoot 'initialize.py') --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Initialization stopped. Check the error and preserve existing files.' }
