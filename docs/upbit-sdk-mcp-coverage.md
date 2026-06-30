# Upbit SDK ↔ MCP 기능 커버리지

[upbit-sdk-python](https://github.com/upbit-official/upbit-sdk-python) `v0.9.0` 기준으로, SDK가 제공하는 API와 이 MCP 서버에서 노출하는 기능을 대조한 체크리스트입니다.

**범례**

| 기호 | 의미 |
|------|------|
| ✅ | MCP로 제공 중 (`main.py`에 등록됨) |
| 🔶 | 구현은 되어 있으나 MCP에 미등록 |
| ❌ | 미구현 |
| ➖ | REST API 아님 (WebSocket 등) |

**MCP 노출 유형**

- **Tool** — 에이전트가 호출하는 함수
- **Resource** — 읽기 전용 데이터 URI
- **Prompt** — SDK API와 무관한 프롬프트 템플릿
- **Composite** — SDK 메서드 여러 개를 조합한 상위 기능

---

## 요약

| 구분 | SDK 메서드 수 | MCP 제공 | 구현만 됨 | 미구현 |
|------|--------------|----------|-----------|--------|
| REST API | 48 | 14 | 3 | 31 |
| WebSocket | 2 | 0 | 0 | 2 |

> SDK 메서드 48개 + WebSocket 2개 = 총 50개 항목 기준

---

## Accounts

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.accounts.list` | `GET /v1/accounts` | ✅ | `get_accounts` | 인증 필요 |

---

## TravelRule

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.travel_rule.list_vasps` | `GET /v1/travel_rule/vasps` | ❌ | — | |
| `client.travel_rule.verify_deposit_by_txid` | `POST /v1/travel_rule/deposit/txid` | ❌ | — | |
| `client.travel_rule.verify_deposit_by_uuid` | `POST /v1/travel_rule/deposit/uuid` | ❌ | — | |

---

## WalletStatus

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.wallet_status.list` | `GET /v1/status/wallet` | ❌ | — | |

---

## APIKeys

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.api_keys.list` | `GET /v1/api_keys` | ❌ | — | |

---

## Orders

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.orders.create` | `POST /v1/orders` | ✅ | `create_order` | 인증 필요 |
| `client.orders.retrieve` | `GET /v1/order` | ✅ | `get_order` | 인증 필요 |
| `client.orders.cancel` | `DELETE /v1/order` | ✅ | `cancel_order` | 인증 필요 |
| `client.orders.list_open` | `GET /v1/orders/open` | ✅ | `get_orders` | `state=wait` 시 사용 |
| `client.orders.list_closed` | `GET /v1/orders/closed` | ✅ | `get_orders` | `state=done\|cancel` 시 사용 |
| `client.orders.cancel_and_new` | `POST /v1/orders/cancel_and_new` | ❌ | — | |
| `client.orders.cancel_by_uuids` | `DELETE /v1/orders/uuids` | ❌ | — | |
| `client.orders.cancel_open` | `DELETE /v1/orders/open` | ❌ | — | |
| `client.orders.list_by_uuids` | `GET /v1/orders/uuids` | ❌ | — | |
| `client.orders.retrieve_chance` | `GET /v1/orders/chance` | ❌ | — | |
| `client.orders.test_create` | `POST /v1/orders/test` | ❌ | — | |

---

## Withdraws

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.withdraws.retrieve` | `GET /v1/withdraw` | ❌ | — | |
| `client.withdraws.list` | `GET /v1/withdraws` | ✅ | `get_deposits_withdrawals` | `transaction_type=withdraw` |
| `client.withdraws.cancel_withdrawal` | `DELETE /v1/withdraws/coin` | ❌ | — | |
| `client.withdraws.create_krw_withdrawal` | `POST /v1/withdraws/krw` | 🔶 | `create_withdraw` | 미등록 |
| `client.withdraws.create_withdrawal` | `POST /v1/withdraws/coin` | 🔶 | `create_withdraw` | 미등록 |
| `client.withdraws.list_coin_addresses` | `GET /v1/withdraws/coin_addresses` | ❌ | — | |
| `client.withdraws.retrieve_chance` | `GET /v1/withdraws/chance` | ❌ | — | |

---

## Deposits

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.deposits.retrieve` | `GET /v1/deposit` | ❌ | — | |
| `client.deposits.list` | `GET /v1/deposits` | ✅ | `get_deposits_withdrawals` | `transaction_type=deposit` |
| `client.deposits.create_coin_address` | `POST /v1/deposits/generate_coin_address` | ❌ | — | |
| `client.deposits.deposit_krw` | `POST /v1/deposits/krw` | ❌ | — | |
| `client.deposits.list_coin_addresses` | `GET /v1/deposits/coin_addresses` | ❌ | — | |
| `client.deposits.retrieve_chance` | `GET /v1/deposits/chance/coin` | ❌ | — | |
| `client.deposits.retrieve_coin_address` | `GET /v1/deposits/coin_address` | ❌ | — | |

---

## TradingPairs

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.trading_pairs.list` | `GET /v1/market/all` | ✅ | `get_market_list` (Resource) | `market://list` |
| `client.trading_pairs.list` | `GET /v1/market/all` | ✅ | `get_market_summary` (Composite) | KRW 마켓 수 집계에 사용 |

---

## Tickers

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.tickers.list_by_trading_pairs` | `GET /v1/ticker` | ✅ | `get_ticker` | 단일/복수 마켓 |
| `client.tickers.list_by_quote_currencies` | `GET /v1/ticker/all` | ✅ | `get_market_summary` (Composite) | KRW 전체 티커 조회 |

---

## Orderbooks

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.orderbooks.list` | `GET /v1/orderbook` | ✅ | `get_orderbook` | |
| `client.orderbooks.list_instruments` | `GET /v1/orderbook/instruments` | ❌ | — | |

---

## Trades

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.trades.list` | `GET /v1/trades/ticks` | ✅ | `get_trades` | |

---

## Candles

| SDK 메서드 | HTTP | MCP | MCP 이름 | 비고 |
|------------|------|-----|----------|------|
| `client.candles.list_minutes` | `GET /v1/candles/minutes/{unit}` | 🔶 | `get_candles` | minute1~240 지원, 미등록 |
| `client.candles.list_days` | `GET /v1/candles/days` | 🔶 | `get_candles` | 미등록 |
| `client.candles.list_weeks` | `GET /v1/candles/weeks` | 🔶 | `get_candles` | 미등록 |
| `client.candles.list_months` | `GET /v1/candles/months` | 🔶 | `get_candles` | 미등록 |
| `client.candles.list_seconds` | `GET /v1/candles/seconds` | ❌ | — | |
| `client.candles.list_years` | `GET /v1/candles/years` | ❌ | — | |
| `client.candles.*` | — | 🔶 | `technical_analysis` (Composite) | `list_minutes` / `list_days` 사용, 미등록 |

---

## WebSocket

| SDK 영역 | MCP | 비고 |
|----------|-----|------|
| `WsPublic` | ➖ | 실시간 공개 시세 스트림, REST MCP와 별개 |
| `WsPrivate` | ➖ | 실시간 개인 주문/잔고 스트림, REST MCP와 별개 |

---

## MCP 전용 기능 (SDK에 직접 대응 없음)

| 유형 | 이름 | 설명 |
|------|------|------|
| Tool (Composite) | `get_market_summary` | 주요 코인·거래량·등락률 상위 종목 요약 |
| Tool (Composite) | `technical_analysis` | 캔들 데이터 기반 기술적 지표 계산 |
| Prompt | `explain_ticker` | 티커 해석 프롬프트 |
| Prompt | `analyze_portfolio` | 포트폴리오 분석 프롬프트 |
| Prompt | `order_help` | 주문 도움말 프롬프트 |
| Prompt | `trading_strategy` | 매매 전략 프롬프트 |

---

## `main.py` 등록 현황

### 등록된 Tool (10개)

- [x] `get_ticker`
- [x] `get_orderbook`
- [x] `get_trades`
- [x] `get_accounts`
- [x] `create_order`
- [x] `get_orders`
- [x] `get_order`
- [x] `cancel_order`
- [x] `get_market_summary`
- [x] `get_deposits_withdrawals`

### 구현됐으나 미등록 Tool (3개)

- [ ] `get_candles` — `tools/get_candles.py`
- [ ] `create_withdraw` — `tools/create_withdraw.py`
- [ ] `technical_analysis` — `tools/technical_analysis.py`

### 등록된 Resource (1개)

- [x] `get_market_list` — URI: `market://list`

### 등록된 Prompt (4개)

- [x] `explain_ticker`
- [x] `analyze_portfolio`
- [x] `order_help`
- [x] `trading_strategy`

---

## 우선 추가 후보

SDK는 지원하지만 MCP에 아직 없는 기능 중, 기존 도구와 연관이 높은 항목입니다.

1. `get_candles`, `technical_analysis` — `main.py` 등록
2. `create_withdraw` — `main.py` 등록
3. `client.orders.retrieve_chance` — 주문 가능 수량/수수료 사전 확인
4. `client.orders.cancel_open` — 미체결 주문 일괄 취소
5. `client.deposits.retrieve_coin_address` / `client.withdraws.list_coin_addresses` — 입출금 주소 조회
6. `client.wallet_status.list` — 지갑 점검 상태 확인

---

*마지막 업데이트: upbit-sdk `0.9.0`, MCP 서버 `main.py` 기준*
