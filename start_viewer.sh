#!/bin/bash
# study_viewer_v2.html을 로컬 HTTP 서버로 띄우고 브라우저 자동 열기
# 사용: ./start_viewer.sh  (또는 bash start_viewer.sh)

cd "$(dirname "$0")"

PORT=8765
URL="http://localhost:${PORT}/study_viewer_v2.html"

echo "🚀 IDM Viewer v2 서버 시작 중..."
echo "   포트: ${PORT}"
echo "   URL:  ${URL}"
echo ""

# 브라우저 자동 열기 (백그라운드)
sleep 1 && (
    if command -v xdg-open &> /dev/null; then xdg-open "$URL"
    elif command -v open &> /dev/null; then open "$URL"
    elif command -v cmd.exe &> /dev/null; then cmd.exe /c start "" "$URL"
    else echo "브라우저에서 직접 열어주세요: $URL"
    fi
) &

# 서버 실행 (Ctrl+C로 종료)
echo "(서버 종료: Ctrl+C)"
python3 -m http.server $PORT 2>/dev/null
