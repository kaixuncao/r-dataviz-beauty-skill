# r-dataviz-beauty-skill 一键安装脚本（Windows PowerShell）
# 用途：把本仓库安装到 WorkBuddy 用户级技能目录（所有 Agent 可用）

$ErrorActionPreference = "Stop"

$SkillName = "r-dataviz-beauty"
$SrcDir    = Split-Path -Parent $MyInvocation.MyCommand.Path
$DestBase  = Join-Path $env:USERPROFILE ".workbuddy\skills"
$DestDir   = Join-Path $DestBase $SkillName

Write-Host "==> 安装到：$DestDir"

New-Item -ItemType Directory -Force -Path (Join-Path $DestDir "references") | Out-Null

Copy-Item (Join-Path $SrcDir "SKILL.md") -Destination $DestDir -Force
Copy-Item (Join-Path $SrcDir "references\*.md") -Destination (Join-Path $DestDir "references") -Force

Write-Host "==> 完成。已安装文件："
Get-ChildItem $DestDir, (Join-Path $DestDir "references") | Select-Object -ExpandProperty Name

Write-Host ""
Write-Host "验证方式：对 Agent 说"
Write-Host "  「我有 5 个处理组各 20 个重复的株高数据，要放进论文，该画什么图？」"
Write-Host "若回答中出现箱形图 + theme_classic() + 600 dpi + (p.页码)，即为安装成功。"
