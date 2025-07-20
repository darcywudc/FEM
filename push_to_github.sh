#!/bin/bash

echo "=== FEM Analysis Environment - GitHub推送脚本 ==="
echo ""

# 🔧 请修改以下变量为您的GitHub信息
GITHUB_USERNAME="darcywudc"               # 您的GitHub用户名
REPO_NAME="fem-analysis-env"              # 仓库名

# 🔗 构建仓库URL
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "📋 推送信息:"
echo "GitHub用户名: ${GITHUB_USERNAME}"
echo "仓库名称: ${REPO_NAME}"
echo "仓库URL: ${REPO_URL}"
echo ""

# ❓ 确认信息
read -p "⚠️  请确认以上信息是否正确？(y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 已取消推送"
    exit 1
fi

echo ""
echo "🚀 开始推送到GitHub..."

# 🔗 添加远程仓库
echo "1️⃣ 添加远程仓库..."
git remote add origin ${REPO_URL}

# 📤 推送到远程仓库
echo "2️⃣ 推送代码..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 推送完成！"
echo "🔗 访问您的仓库: ${REPO_URL}"
echo ""
echo "📊 推送内容:"
echo "- README.md (项目文档)"
echo "- continuous_bridge_analysis.py (FEM分析脚本)"
echo "- anastruct_bridge_analysis.png (分析结果图)"
echo "- requirements.txt (依赖列表)"
echo "- .gitignore (Git忽略文件)" 