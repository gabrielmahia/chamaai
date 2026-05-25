# SaccoAI — Kenya Chama & SACCO Management

> **Manage** your chama — merry-go-round schedules, table banking, M-Pesa payments, AI advisor.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://saccoai.streamlit.app)
[![Part of East African Decision Infrastructure](https://img.shields.io/badge/Portfolio-East%20African%20Decision%20Infrastructure-orange)](https://gabrielmahia.github.io)

> **Looking to find and compare SACCOs?** Use [SACCO Scout →](https://chaguasacco.streamlit.app) (github.com/gabrielmahia/sacco-scout)

## What it does

SaccoAI is a **management** tool for Kenya's 300,000+ chamas and SACCOs — rotating credit groups, investment clubs, and table banking groups.

| Feature | What it does |
|---------|-------------|
| 🏠 Chama Setup | Configure type, contributions, meeting schedule, registration path |
| 👥 Member Manager | Track members, roles, M-Pesa phones, contribution history |
| 📅 Merry-Go-Round | Auto-generate rotation schedule with monthly payouts |
| 🏦 Table Banking | Loan eligibility (1x–3x savings), repayment, interest, dividends |
| 📊 Contribution Tracker | Monthly board — who's paid, who's pending, collection rate |
| 📱 M-Pesa Integration | STK push commands for contributions, B2C for payouts |
| 🤖 AI Advisor | Gemini-powered guidance: constitution, UWEZO Fund, dispute resolution |

## The gap it fills

Kenya has 300,000+ registered chamas managing an estimated KES 500B+ in rotating credit.
Zero of them have an AI-first management tool. This is that tool.

## Deploy

```
share.streamlit.io → New app → gabrielmahia/saccoai → app.py
Add secret: GOOGLE_API_KEY
```

## Related

- [SACCO Scout](https://github.com/gabrielmahia/sacco-scout) — Find and compare Kenya's licensed SACCOs (chaguasacco.streamlit.app)
- [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) — M-Pesa API for payment automation
- [East African Decision Infrastructure](https://gabrielmahia.github.io)

## License

MIT © Gabriel Mahia | contact@aikungfu.dev
