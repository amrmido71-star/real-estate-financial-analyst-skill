#!/bin/bash
# publish_to_github.sh — ارفع المشروع إلى GitHub في دقيقة واحدة
# الاستخدام:
#   chmod +x publish_to_github.sh
#   ./publish_to_github.sh https://github.com/USERNAME/real-estate-financial-analyst-skill.git

set -e

if [ -z "$1" ]; then
  echo "❌ الاستخدام: ./publish_to_github.sh <GITHUB_REPO_URL>"
  echo "   مثال: ./publish_to_github.sh https://github.com/ahmed/real-estate-financial-analyst-skill.git"
  echo ""
  echo "   1) اذهب إلى https://github.com/new"
  echo "   2) اسم المستودع: real-estate-financial-analyst-skill"
  echo "   3) اجعله Public + بدون README (لأن عندنا README جاهز)"
  echo "   4) انسخ رابط المستودع والصقه هنا"
  exit 1
fi

REPO_URL="$1"

echo "🔗 Remote URL: $REPO_URL"
echo "📦 Branch: main"

# تأكد أننا على main
git branch -M main

# أضف الريموت (أو حدثه لو موجود)
if git remote | grep -q origin; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

echo "🚀 رفع إلى GitHub..."
git push -u origin main

echo ""
echo "✅ تم الرفع بنجاح!"
echo "🔍 افتح المستودع: $REPO_URL"
echo ""
echo "للتحديث لاحقاً:"
echo "  git add ."
echo "  git commit -m \"feat: update\""
echo "  git push"
