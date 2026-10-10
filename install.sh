#!/usr/bin/env bash
# r-dataviz-beauty-skill 一键安装脚本
# 用途：把本仓库安装到 WorkBuddy 用户级技能目录（所有 Agent 可用）
set -e

SKILL_NAME="r-dataviz-beauty"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -n "$WORKBUDDY_SKILLS_DIR" ]; then
  DEST_BASE="$WORKBUDDY_SKILLS_DIR"
elif [ -n "$HOME" ]; then
  DEST_BASE="$HOME/.workbuddy/skills"
else
  DEST_BASE="$USERPROFILE/.workbuddy/skills"
fi

DEST_DIR="$DEST_BASE/$SKILL_NAME"

echo "==> 安装到：$DEST_DIR"
mkdir -p "$DEST_DIR/references"

cp "$SRC_DIR/SKILL.md" "$DEST_DIR/SKILL.md"
cp "$SRC_DIR"/references/*.md "$DEST_DIR/references/"

echo "==> 完成。已安装文件："
ls -1 "$DEST_DIR" "$DEST_DIR/references"

echo
echo "验证方式：对 Agent 说"
echo "  「我有 5 个处理组各 20 个重复的株高数据，要放进论文，该画什么图？」"
echo "若回答中出现箱形图 + theme_classic() + 600 dpi + (p.页码)，即为安装成功。"
