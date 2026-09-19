$ErrorActionPreference = "Stop"

$inbox = $env:STAGE04_PRIVATE_INPUT_INBOX
if (-not $inbox -or -not [IO.Path]::IsPathRooted($inbox)) {
    throw "STAGE04_PRIVATE_INPUT_INBOX must be an absolute local path."
}
$target = Join-Path $env:RUNNER_TEMP "stage04-private-input"

if (Test-Path -LiteralPath $target -PathType Container) {
    Get-ChildItem -LiteralPath $target -File | Remove-Item -Force
}

foreach ($path in @(
    (Join-Path $inbox "aggregate.csv"),
    (Join-Path $inbox "manifest.json")
)) {
    if (Test-Path -LiteralPath $path -PathType Leaf) {
        Remove-Item -LiteralPath $path -Force
    }
}

foreach ($directory in @($target, $inbox)) {
    if ((Test-Path -LiteralPath $directory -PathType Container) -and
        -not (Get-ChildItem -LiteralPath $directory -Force)) {
        Remove-Item -LiteralPath $directory -Force
    }
}

Write-Output "Per-run input copies were removed from runner temp and the local inbox."
