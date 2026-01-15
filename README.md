# Work24 MCP Server

Work24(고용24) OPEN API를 MCP 도구로 노출하는 서버입니다.

## 도구 목록

| 도구 | 설명 |
|------|------|
| `find_recruit_notice` | 채용정보 목록 검색 |
| `get_recruit_detail` | 채용정보 상세 조회 |
| `find_training_course` | 내일배움카드 훈련과정 검색 |
| `get_training_course_detail` | 훈련과정 상세 조회 |
| `find_strong_company` | 강소기업/공채기업 검색 |
| `list_youth_programs` | 청년 프로그램 목록 |
| `match_youth_programs` | 청년 프로그램 매칭 |

## 설치

```bash
uv sync
```

## 설정

`.env.example`를 `.env`로 복사 후 API 키 설정:

```bash
cp .env.example .env
# WORK24_AUTH_KEY 설정
```

## 실행

```bash
uv run python server.py
```

## MCP 클라이언트 설정

Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "work24": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "./"
    }
  }
}
```
