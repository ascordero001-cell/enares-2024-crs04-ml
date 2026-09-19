$ErrorActionPreference = "Stop"

$inbox = $env:STAGE04_PRIVATE_INPUT_INBOX
if (-not $inbox -or -not [IO.Path]::IsPathRooted($inbox)) {
    throw "STAGE04_PRIVATE_INPUT_INBOX must be an absolute local path."
}
$target = Join-Path $env:RUNNER_TEMP "stage04-private-input"
$aggregate = Join-Path $inbox "aggregate.csv"
$manifest = Join-Path $inbox "manifest.json"

if (-not (Test-Path -LiteralPath $aggregate -PathType Leaf)) {
    throw "The authorized per-run aggregate copy is missing from the local inbox."
}
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) {
    throw "The matching per-run manifest copy is missing from the local inbox."
}

$manifestPayload = Get-Content -LiteralPath $manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$fileName = [string]$manifestPayload.file_name
if (-not $fileName.EndsWith(".csv", [StringComparison]::OrdinalIgnoreCase) -or
    [IO.Path]::GetFileName($fileName) -ne $fileName) {
    throw "The manifest file_name must be a safe CSV basename."
}

New-Item -ItemType Directory -Path $target -Force | Out-Null
Copy-Item -LiteralPath $aggregate -Destination (Join-Path $target $fileName)
Copy-Item -LiteralPath $manifest -Destination (Join-Path $target "manifest.json")
Write-Output "Authorized per-run input was staged after RUNNER_TEMP cleanup."
