[CmdletBinding()]
param(
    [string]$EngineRoot,
    [string]$Configuration = "Development",
    [switch]$SkipValidation,
    [switch]$SkipBuild,
    [switch]$NoLaunch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ProjectPath = Join-Path $RepoRoot "LiminalDominion.uproject"
$ProjectName = [System.IO.Path]::GetFileNameWithoutExtension($ProjectPath)
$SolutionPath = Join-Path $RepoRoot "$ProjectName.sln"
$ContentFolders = @(
    (Join-Path $RepoRoot "Content\Maps"),
    (Join-Path $RepoRoot "Content\Blueprints"),
    (Join-Path $RepoRoot "Content\Data"),
    (Join-Path $RepoRoot "Content\UI")
)

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Invoke-NativeCommand {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

function Get-PythonCommand {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @("py", "-3")
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @("python")
    }

    throw "Python 3 was not found. Install Python 3.9+ first."
}

function Invoke-PythonScript {
    param(
        [string[]]$CommandPrefix,
        [string[]]$Arguments
    )

    Invoke-NativeCommand -FilePath $CommandPrefix[0] -Arguments (@($CommandPrefix | Select-Object -Skip 1) + $Arguments)
}

function Test-WindowsSdkInstalled {
    $WindowsSdkIncludeRoot = "C:\Program Files (x86)\Windows Kits\10\Include"
    if (-not (Test-Path $WindowsSdkIncludeRoot)) {
        return $false
    }

    return (Get-ChildItem -Path $WindowsSdkIncludeRoot -Directory -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
}

function Test-VisualCppToolchainInstalled {
    $VsWhere = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    $KnownToolchainRoot = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
    if (Test-Path $KnownToolchainRoot) {
        return (Get-ChildItem -Path $KnownToolchainRoot -Directory -ErrorAction SilentlyContinue | Measure-Object).Count -gt 0
    }

    if (-not (Test-Path $VsWhere)) {
        return $false
    }

    $InstallPath = & $VsWhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    return -not [string]::IsNullOrWhiteSpace($InstallPath)
}

function Resolve-UnrealVersionSelectorPath {
    $Candidates = @(
        "C:\Program Files (x86)\Epic Games\Launcher\Engine\Binaries\Win64\UnrealVersionSelector.exe",
        "C:\Program Files\Epic Games\Launcher\Engine\Binaries\Win64\UnrealVersionSelector.exe"
    )

    foreach ($Candidate in $Candidates) {
        if (Test-Path $Candidate) {
            return $Candidate
        }
    }

    return $null
}

function Resolve-EngineRoot {
    param([string]$RequestedRoot)

    $Candidates = @()

    if ($RequestedRoot) {
        $Candidates += $RequestedRoot
    }

    if ($env:UE_ROOT) {
        $Candidates += $env:UE_ROOT
    }

    $EpicRoot = "C:\Program Files\Epic Games"
    if (Test-Path $EpicRoot) {
        $Candidates += Get-ChildItem -Path $EpicRoot -Directory -Filter "UE_*" |
            Sort-Object Name -Descending |
            Select-Object -ExpandProperty FullName
    }

    foreach ($Candidate in $Candidates | Select-Object -Unique) {
        $EditorPath = Join-Path $Candidate "Engine\Binaries\Win64\UnrealEditor.exe"
        $BuildPath = Join-Path $Candidate "Engine\Build\BatchFiles\Build.bat"
        $GeneratePath = Join-Path $Candidate "Engine\Build\BatchFiles\GenerateProjectFiles.bat"
        $UnrealBuildToolPath = Join-Path $Candidate "Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe"

        if ((Test-Path $EditorPath) -and (Test-Path $BuildPath)) {
            return [pscustomobject]@{
                Root = $Candidate
                EditorPath = $EditorPath
                BuildPath = $BuildPath
                GeneratePath = $(if (Test-Path $GeneratePath) { $GeneratePath } else { $null })
                UnrealBuildToolPath = $(if (Test-Path $UnrealBuildToolPath) { $UnrealBuildToolPath } else { $null })
            }
        }
    }

    throw "Could not locate a valid Unreal Engine install. Pass -EngineRoot or set UE_ROOT."
}

$PlatformIsWindows = $env:OS -eq "Windows_NT"

if (-not $PlatformIsWindows) {
    throw "This startup script is Windows-only."
}

if (-not (Test-Path $ProjectPath)) {
    throw "Missing Unreal project file: $ProjectPath"
}

$ProjectDescriptor = Get-Content $ProjectPath -Raw | ConvertFrom-Json
$HasProjectModules = ($ProjectDescriptor.PSObject.Properties.Name -contains "Modules") -and $ProjectDescriptor.Modules.Count -gt 0
$PythonCommand = Get-PythonCommand
$Engine = Resolve-EngineRoot -RequestedRoot $EngineRoot
$UnrealVersionSelectorPath = Resolve-UnrealVersionSelectorPath
$WindowsSdkInstalled = Test-WindowsSdkInstalled
$VisualCppToolchainInstalled = Test-VisualCppToolchainInstalled
$ShouldBuild = (-not $SkipBuild) -and $HasProjectModules

Write-Host "Repo: $RepoRoot"
Write-Host "Project: $ProjectPath"
Write-Host "Project has code modules: $HasProjectModules"
Write-Host "Engine: $($Engine.Root)"
Write-Host "Python: $($PythonCommand -join ' ')"
if ($UnrealVersionSelectorPath) {
    Write-Host "UnrealVersionSelector: $UnrealVersionSelectorPath"
}
Write-Host "Windows SDK detected: $WindowsSdkInstalled"
Write-Host "Visual C++ build tools detected: $VisualCppToolchainInstalled"

if (-not $SkipValidation) {
    Write-Step "Validating seed data"
    Invoke-PythonScript -CommandPrefix $PythonCommand -Arguments @("scripts/validate_seed_data.py")

    Write-Step "Exporting Unreal DataTables"
    Invoke-PythonScript -CommandPrefix $PythonCommand -Arguments @("scripts/export_unreal_datatables.py")
}

Write-Step "Ensuring starter content folders exist"
foreach ($Folder in $ContentFolders) {
    if (-not (Test-Path $Folder)) {
        New-Item -ItemType Directory -Path $Folder | Out-Null
    }
}

if ((-not $ShouldBuild) -and (-not $SkipBuild) -and (-not $HasProjectModules)) {
    Write-Step "Skipping native build"
    Write-Host "No project modules are enabled in the .uproject, so the visualization startup path can launch without compiling C++."
}

if ($ShouldBuild -and (-not $WindowsSdkInstalled -or -not $VisualCppToolchainInstalled)) {
    throw @"
Win64 Unreal build prerequisites are missing on this machine.

Recommended install:
  winget install --id Microsoft.VisualStudio.2022.BuildTools --exact --override "--wait --quiet --norestart --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.Windows11SDK.22621"

If you prefer the standalone SDK package:
  winget install --id Microsoft.WindowsSDK.10.0.22621 --exact
"@
}

if ($ShouldBuild -and -not (Test-Path $SolutionPath)) {
    Write-Step "Generating Visual Studio project files"
    if ($UnrealVersionSelectorPath) {
        Invoke-NativeCommand -FilePath $UnrealVersionSelectorPath -Arguments @("/projectfiles", $ProjectPath)
    }
    elseif ($Engine.GeneratePath) {
        Invoke-NativeCommand -FilePath $Engine.GeneratePath -Arguments @("-project=$ProjectPath", "-game", "-rocket")
    }
    elseif ($Engine.UnrealBuildToolPath) {
        Invoke-NativeCommand -FilePath $Engine.UnrealBuildToolPath -Arguments @("-projectfiles", "-project=$ProjectPath", "-game", "-rocket")
    }
    else {
        throw "Could not find GenerateProjectFiles.bat or UnrealBuildTool.exe."
    }
}

if ($ShouldBuild) {
    Write-Step "Building $ProjectName Editor ($Configuration Win64)"
    Invoke-NativeCommand -FilePath $Engine.BuildPath -Arguments @("$($ProjectName)Editor", "Win64", $Configuration, $ProjectPath, "-WaitMutex", "-NoHotReloadFromIDE")
}

if (-not $NoLaunch) {
    Write-Step "Launching Unreal Editor"
    Start-Process -FilePath $Engine.EditorPath -ArgumentList @($ProjectPath) -WorkingDirectory $RepoRoot
}

Write-Host ""
Write-Host "Startup sequence complete." -ForegroundColor Green
