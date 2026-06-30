# MCP 도구 소개

Upbit MCP Server가 제공하는 Tool, Resource, Prompt 목록입니다.

**인증 안내**

- 🔓 공개 API — API 키 없이 사용 가능
- 🔐 인증 필요 — `.env`에 `UPBIT_ACCESS_KEY`, `UPBIT_SECRET_KEY` 설정 필요

---

## Tool (18개)

### 시장 데이터

| 이름 | 설명 | 인증 |
|------|------|------|
| `get_ticker` | 단일 또는 복수 마켓의 현재 시세 조회 | 🔓 |
| `get_orderbook` | 호가창(매수·매도 호가) 스냅샷 조회 | 🔓 |
| `get_trades` | 최근 체결 내역 조회 | 🔓 |
| `get_candles` | 캔들(차트) 데이터 조회 — second, minute1~240, day, week, month, year | 🔓 |
| `get_market_summary` | KRW 마켓 주요 코인·거래량·등락률 상위 종목 요약 | 🔓 |
| `technical_analysis` | 캔들 데이터 기반 기술적 지표 계산 (RSI, MACD, 이동평균 등) | 🔓 |

### 계정·주문

| 이름 | 설명 | 인증 |
|------|------|------|
| `get_accounts` | 보유 자산 목록 및 잔고 조회 | 🔐 |
| `get_orders` | 주문 목록 조회 (대기·완료·취소) | 🔐 |
| `get_order` | 특정 주문 상세 정보 조회 | 🔐 |
| `get_order_chance` | 마켓별 주문 가능 정보 조회 | 🔐 |
| `create_order` | 지정가·시장가 매수/매도 주문 생성 | 🔐 |
| `cancel_order` | 특정 주문 취소 | 🔐 |
| `cancel_open_orders` | 미체결 주문 일괄 취소 | 🔐 |

### 입출금·지갑

| 이름 | 설명 | 인증 |
|------|------|------|
| `get_deposits_withdrawals` | 입금·출금 내역 조회 | 🔐 |
| `create_withdraw` | 원화 또는 디지털 자산 출금 요청 | 🔐 |
| `get_deposit_coin_address` | 디지털 자산 입금 주소 조회 | 🔐 |
| `list_withdraw_coin_addresses` | 등록된 출금 주소 목록 조회 | 🔐 |
| `get_wallet_status` | 지갑 상태(입출금 가능 여부) 조회 | 🔓 |

---

## Resource (1개)

| URI | 이름 | 설명 |
|-----|------|------|
| `market://list` | `get_market_list` | 업비트에서 거래 가능한 마켓 코드 목록 |

---

## Prompt (4개)

SDK API와 무관한 프롬프트 템플릿입니다. 에이전트가 분석·설명 시 참고할 수 있습니다.

| 이름 | 설명 |
|------|------|
| `explain_ticker` | 티커 데이터 해석 가이드 |
| `analyze_portfolio` | 포트폴리오 분석 프롬프트 |
| `order_help` | 주문 유형·파라미터 도움말 |
| `trading_strategy` | 매매 전략 수립 프롬프트 |

---

## 관련 문서

- [Upbit SDK ↔ MCP 구현 현황](./upbit-sdk-mcp-coverage.md) — SDK 대비 커버리지 및 미구현 항목
