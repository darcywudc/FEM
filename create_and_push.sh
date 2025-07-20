#!/bin/bash

echo "🚀 FEM Analysis Environment - 一键创建并推送到GitHub"
echo ""

# 检查GitHub CLI登录状态
if ! gh auth status > /dev/null 2>&1; then
    echo "⚠️  需要先登录GitHub CLI"
    echo "执行: gh auth login"
    echo "然后重新运行此脚本"
    exit 1
fi

echo "✅ GitHub CLI已登录"
echo ""

# 创建GitHub仓库
echo "📁 创建GitHub仓库..."
gh repo create FEM \
  --public \
  --description "FEM Analysis Environment for Apple Silicon Mac - Continuous Bridge Analysis" \
  --confirm

if [ $? -eq 0 ]; then
    echo "✅ 仓库创建成功！"
else
    echo "❌ 仓库创建失败，可能已存在"
fi

echo ""

# 添加远程仓库并推送
echo "📤 推送代码到GitHub..."
git remote add origin https://github.com/darcywudc/FEM.git 2>/dev/null || echo "远程仓库已存在"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 推送成功！"
    echo "🔗 仓库地址: https://github.com/darcywudc/fem-analysis-env"
    echo ""
    echo "📋 已推送的文件:"
    echo "  ✅ README.md - 项目文档"
    echo "  ✅ continuous_bridge_analysis.py - FEM分析脚本"
    echo "  ✅ anastruct_bridge_analysis.png - 分析结果图"
    echo "  ✅ requirements.txt - 依赖列表"
    echo "  ✅ .gitignore - Git配置"
else
    echo "❌ 推送失败，请检查网络连接"
fi 