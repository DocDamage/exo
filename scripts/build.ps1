[CmdletBinding()]
param(
    [ValidateSet('dev', 'release', 'test', 'hello', 'snow')]
    [string]$Target = 'dev'
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

New-Item -ItemType Directory -Force -Path 'build/native', 'build/bin' | Out-Null
python scripts/check_repo.py
if ($LASTEXITCODE -ne 0) { throw 'Repository validation failed.' }

$compiler = Get-Command clang, cc -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $compiler) { throw 'clang or cc is required to compile the native image shim.' }
& $compiler.Source -std=c99 -O2 -Isrc -c src/stb_image_shim.c -o build/native/stb_image_shim.o
if ($LASTEXITCODE -ne 0) { throw 'Native shim compilation failed.' }

python scripts/compile_shaders.py --clean
if ($LASTEXITCODE -ne 0) { throw 'Shader compilation failed.' }

spectre build $Target
if ($LASTEXITCODE -ne 0) { throw "Spectre build failed for target '$Target'." }
Write-Host "Exo target '$Target' built successfully."
