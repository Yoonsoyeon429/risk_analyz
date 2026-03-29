#!/bin/bash
# GitHub: soyeonyoooon / risk_analyzer
# 터미널에서 실행:  bash push_github.sh
# 또는:  chmod +x push_github.sh && ./push_github.sh

set -e
cd "$(dirname "$0")"

echo "→ 저장소: https://github.com/soyeonyoooon/risk_analyzer"
echo "→ 계정 아이디: soyeonyoooon"
echo ""

git remote set-url origin https://github.com/soyeonyoooon/risk_analyzer.git 2>/dev/null \
  || git remote add origin https://github.com/soyeonyoooon/risk_analyzer.git

git branch -M main

# 비밀번호 대신 Personal Access Token 입력 (https://github.com/settings/tokens)
export GIT_TERMINAL_PROMPT=1

echo "→ git push 실행 중..."
git push -u origin main

echo ""
echo "완료. 브라우저에서 확인: https://github.com/soyeonyoooon/risk_analyzer"
