"""
SaccoAI — Kenya SACCO & Chama Manager
AI-powered chama, merry-go-round, and table banking management.
"""
import sys, json, math, urllib.request, ssl, datetime
import streamlit as st

st.set_page_config(
    page_title="SaccoAI — Kenya Chama Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini(prompt: str, key: str, max_tokens: int = 1200) -> str:
    """Call Gemini — returns graceful fallback on any error, never raises."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    prompt = prompt[:5000]
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": max_tokens}}
    req_obj = urllib.request.Request(f"{url}?key={key}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    try:
        import ssl, urllib.error
        with urllib.request.urlopen(req_obj, timeout=25,
                                     context=ssl.create_default_context()) as r:
            d = json.loads(r.read())
        candidates = d.get("candidates", [])
        if not candidates:
            return "_No response. Try again._"
        return candidates[0]["content"]["parts"][0]["text"]
    except Exception as e:
        code_val = getattr(e, 'code', '')
        return f"_AI unavailable{f' (HTTP {code_val})' if code_val else ''}: {type(e).__name__}_"

if "members" not in st.session_state:
    st.session_state.members = []
if "contributions" not in st.session_state:
    st.session_state.contributions = {}
if "chama_name" not in st.session_state:
    st.session_state.chama_name = "My Chama"

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=40)
    st.title("SaccoAI 💰")
    st.caption("Kenya Chama Manager")
    st.divider()
    mode = st.radio("Select module", [
        "🏠 Chama Setup",
        "👥 Member Management",
        "📅 Merry-Go-Round Schedule",
        "🏦 Table Banking Calculator",
        "📊 Contribution Tracker",
        "📱 M-Pesa Integration",
        "🤖 AI Advisor"
    ])
    st.divider()
    st.caption("💡 All calculations follow Kenya chama best practices")

key = get_key()
if not key:
    st.warning("Add GOOGLE_API_KEY to Streamlit secrets to enable AI Advisor.")

# ─────────────────────────────────────────────────────────────
# MODULE 1: CHAMA SETUP
# ─────────────────────────────────────────────────────────────
if mode == "🏠 Chama Setup":
    st.title("🏠 Chama Setup")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Chama name", value=st.session_state.chama_name)
        if name:
            st.session_state.chama_name = name

        chama_type = st.selectbox("Chama type", [
            "Merry-go-round (rotating payout)",
            "Table banking (loans + interest)",
            "Investment chama (shares/portfolio)",
            "Hybrid (rotating + loans)"
        ])

        contribution = st.number_input("Monthly contribution per member (KES)", 
                                        min_value=100, max_value=100000, 
                                        value=5000, step=500)
        meeting_day = st.selectbox("Meeting day", 
                                    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        meeting_freq = st.selectbox("Meeting frequency", 
                                     ["Weekly", "Bi-weekly", "Monthly"])

    with col2:
        start_date = st.date_input("Chama start date", value=datetime.date.today())
        reg_status = st.selectbox("Registration status", [
            "Unregistered (informal)",
            "Registered with Registrar of Societies",
            "Registered as SACCO",
            "Registered as Limited Company"
        ])
        bank = st.selectbox("Banking partner", [
            "Equity Bank (Biashara account)",
            "KCB (Chama account)",
            "Co-operative Bank (Chama account)",
            "NCBA", "Family Bank", "M-Pesa Savings",
            "No bank account yet"
        ])
        welfare = st.number_input("Monthly welfare fund (KES)", 
                                   min_value=0, max_value=10000, value=500, step=100)

    if st.button("💾 Save Chama Setup", type="primary"):
        st.session_state.chama_config = {
            "name": name, "type": chama_type,
            "contribution": contribution, "welfare": welfare,
            "meeting_day": meeting_day, "frequency": meeting_freq,
            "start_date": str(start_date), "bank": bank,
            "registration": reg_status
        }
        st.success(f"✅ Chama '{name}' configured!")

    # Registration guide
    st.divider()
    st.subheader("📋 Registration Guide")
    st.info("""
**Why register your chama?**
Registered chamas can: open a joint bank account, apply for government grants (UWEZO Fund, Youth Fund, Women Fund), 
access SACCO loans, sign contracts, and have legal protection for disputes.

**Registrar of Societies (cheapest, ~KES 1,000):**
- Min. 10 members
- Fill Form 1 (available at Attorney General's office)
- Attach: signed constitution, minutes of inaugural meeting, member list + IDs, passport photos
- Processing: 4-6 weeks

**SACCO registration (KES 3,000 + shares capital):**
- Min. 30 members OR KES 1M share capital
- Apply to SASRA (Sacco Societies Regulatory Authority)
- Access to DT-SACCO lending (up to 3x deposits)

**UWEZO Fund eligibility:**
- Registered, youth/women-led chama
- Max KES 500,000 at 0% interest, 3-year repayment
- Apply via eCitizen under Youth Fund portal
""")

# ─────────────────────────────────────────────────────────────
# MODULE 2: MEMBER MANAGEMENT
# ─────────────────────────────────────────────────────────────
elif mode == "👥 Member Management":
    st.title("👥 Member Management")

    col1, col2 = st.columns([2, 1])
    with col2:
        st.subheader("Add Member")
        name = st.text_input("Full name")
        phone = st.text_input("Phone (254XXXXXXXXX)")
        role = st.selectbox("Role", ["Member", "Chairperson", "Secretary", "Treasurer", "Assistant Treasurer"])
        join_date = st.date_input("Join date")
        if st.button("➕ Add Member", type="primary"):
            if name and phone:
                member = {"name": name, "phone": phone, "role": role, 
                          "join_date": str(join_date), "active": True,
                          "total_contributed": 0, "loans_outstanding": 0}
                st.session_state.members.append(member)
                st.success(f"✅ Added {name}")
            else:
                st.error("Name and phone required")

    with col1:
        st.subheader(f"Members ({len(st.session_state.members)})")
        if not st.session_state.members:
            st.info("No members yet. Add members using the form →")
            # Demo data
            if st.button("Load demo chama (12 members)"):
                demo = [
                    {"name":"Grace Wanjiku","phone":"254712001001","role":"Chairperson","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":0},
                    {"name":"Peter Otieno","phone":"254723002002","role":"Secretary","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":15000},
                    {"name":"Mary Njeri","phone":"254734003003","role":"Treasurer","join_date":"2024-01-01","active":True,"total_contributed":55000,"loans_outstanding":0},
                    {"name":"John Kamau","phone":"254745004004","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":0},
                    {"name":"Fatuma Hassan","phone":"254756005005","role":"Member","join_date":"2024-02-01","active":True,"total_contributed":55000,"loans_outstanding":20000},
                    {"name":"David Ochieng","phone":"254767006006","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":0},
                    {"name":"Ann Chebet","phone":"254778007007","role":"Member","join_date":"2024-03-01","active":True,"total_contributed":50000,"loans_outstanding":0},
                    {"name":"James Mwangi","phone":"254789008008","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":30000},
                    {"name":"Rose Auma","phone":"254701009009","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":0},
                    {"name":"Samuel Kiprop","phone":"254712010010","role":"Member","join_date":"2024-04-01","active":True,"total_contributed":45000,"loans_outstanding":0},
                    {"name":"Esther Muthoni","phone":"254723011011","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":10000},
                    {"name":"Daniel Gitonga","phone":"254734012012","role":"Member","join_date":"2024-01-01","active":True,"total_contributed":60000,"loans_outstanding":0},
                ]
                st.session_state.members = demo
                st.rerun()
        else:
            total_contrib = sum(m["total_contributed"] for m in st.session_state.members)
            total_loans = sum(m["loans_outstanding"] for m in st.session_state.members)
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Members", len(st.session_state.members))
            c2.metric("Total Contributions (KES)", f"{total_contrib:,.0f}")
            c3.metric("Loans Outstanding (KES)", f"{total_loans:,.0f}")

            st.divider()
            for i, m in enumerate(st.session_state.members):
                col_a, col_b, col_c = st.columns([3, 1, 1])
                with col_a:
                    st.markdown(f"**{m['name']}** — {m['role']}")
                    st.caption(f"📱 {m['phone']} | Joined: {m['join_date']}")
                with col_b:
                    st.markdown(f"KES {m['total_contributed']:,.0f}")
                    st.caption("contributed")
                with col_c:
                    if m["loans_outstanding"] > 0:
                        st.markdown(f"🔴 KES {m['loans_outstanding']:,.0f}")
                        st.caption("loan out")
                    else:
                        st.markdown("✅ Clear")
                st.divider()

# ─────────────────────────────────────────────────────────────
# MODULE 3: MERRY-GO-ROUND SCHEDULE
# ─────────────────────────────────────────────────────────────
elif mode == "📅 Merry-Go-Round Schedule":
    st.title("📅 Merry-Go-Round Schedule")

    if not st.session_state.members:
        st.warning("Add members first in the Member Management module.")
    else:
        st.subheader("Configure the Rotation")
        col1, col2 = st.columns(2)
        with col1:
            contribution = st.number_input("Monthly contribution per member (KES)",
                                           min_value=500, value=5000, step=500)
            start_month = st.selectbox("Start month", 
                ["January","February","March","April","May","June",
                 "July","August","September","October","November","December"])
            start_year = st.number_input("Start year", min_value=2024, max_value=2030, value=2026)
        with col2:
            welfare_per_month = st.number_input("Welfare deduction (KES/month)", 
                                                 min_value=0, value=500, step=100)
            order = st.selectbox("Rotation order", [
                "Random draw (fair randomisation)",
                "Seniority (longest member first)",
                "Alphabetical",
                "Custom (entered below)"
            ])

        members = st.session_state.members
        n = len(members)
        monthly_pool = contribution * n
        payout = monthly_pool - (welfare_per_month * n)

        st.metric("Monthly pool", f"KES {monthly_pool:,.0f}")
        st.metric("Payout per month (after welfare)", f"KES {payout:,.0f}")
        st.metric("Welfare fund / month", f"KES {welfare_per_month * n:,.0f}")
        st.metric("Full cycle duration", f"{n} months ({n/12:.1f} years)")

        st.divider()
        st.subheader("📋 Rotation Schedule")

        months_list = ["January","February","March","April","May","June",
                       "July","August","September","October","November","December"]
        start_idx = months_list.index(start_month)

        member_names = [m["name"] for m in members]

        schedule_data = []
        for i, member in enumerate(member_names):
            month_offset = (start_idx + i) % 12
            year_offset = start_year + (start_idx + i) // 12
            schedule_data.append({
                "Month": f"{months_list[month_offset]} {year_offset}",
                "Recipient": member,
                "Payout (KES)": f"{payout:,.0f}",
                "Pool (KES)": f"{monthly_pool:,.0f}",
                "Welfare (KES)": f"{welfare_per_month * n:,.0f}",
                "Round": i + 1
            })

        import pandas as pd
        df = pd.DataFrame(schedule_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Export as text
        if st.button("📋 Copy schedule as text"):
            text = f"MERRY-GO-ROUND SCHEDULE — {st.session_state.chama_name}\n"
            text += "=" * 50 + "\n"
            for row in schedule_data:
                text += f"{row['Round']}. {row['Month']}: {row['Recipient']} receives KES {payout:,.0f}\n"
            st.code(text)

# ─────────────────────────────────────────────────────────────
# MODULE 4: TABLE BANKING CALCULATOR
# ─────────────────────────────────────────────────────────────
elif mode == "🏦 Table Banking Calculator":
    st.title("🏦 Table Banking Calculator")
    st.markdown("*Calculate loan eligibility, interest earned, and dividend distribution*")

    tab1, tab2, tab3 = st.tabs(["Loan Calculator", "Interest & Dividends", "Fund Projections"])

    with tab1:
        st.subheader("Loan Eligibility & Repayment")
        col1, col2 = st.columns(2)
        with col1:
            member_savings = st.number_input("Member's total savings in chama (KES)", 
                                              min_value=0, value=60000, step=1000)
            loan_multiplier = st.selectbox("Loan multiplier (chama policy)", 
                [("1x savings", 1), ("2x savings", 2), ("3x savings", 3)],
                format_func=lambda x: x[0])
            interest_rate = st.number_input("Monthly interest rate (%)", 
                                             min_value=1.0, max_value=20.0, value=10.0, step=0.5)
            repayment_months = st.number_input("Repayment period (months)", 
                                                min_value=1, max_value=24, value=3)

        with col2:
            max_loan = member_savings * loan_multiplier[1]
            st.metric("Maximum loan eligible", f"KES {max_loan:,.0f}")

            loan_amount = st.number_input("Loan amount requested (KES)", 
                                           min_value=1000, max_value=int(max_loan), 
                                           value=min(30000, int(max_loan)), step=1000)

            # Simple interest calculation
            total_interest = loan_amount * (interest_rate / 100) * repayment_months
            monthly_payment = (loan_amount + total_interest) / repayment_months
            total_repayment = loan_amount + total_interest

            st.metric("Monthly repayment", f"KES {monthly_payment:,.0f}")
            st.metric("Total interest", f"KES {total_interest:,.0f}")
            st.metric("Total repayment", f"KES {total_repayment:,.0f}")

        st.divider()
        st.subheader("Repayment Schedule")
        repayment_data = []
        balance = loan_amount
        for month in range(1, repayment_months + 1):
            interest_this_month = loan_amount * (interest_rate / 100)
            principal_this_month = loan_amount / repayment_months
            payment_this_month = principal_this_month + interest_this_month
            balance -= principal_this_month
            repayment_data.append({
                "Month": month,
                "Principal (KES)": f"{principal_this_month:,.0f}",
                "Interest (KES)": f"{interest_this_month:,.0f}",
                "Total Payment (KES)": f"{payment_this_month:,.0f}",
                "Balance (KES)": f"{max(0, balance):,.0f}"
            })
        import pandas as pd
        st.dataframe(pd.DataFrame(repayment_data), use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Interest Earnings & Dividend Distribution")
        col1, col2 = st.columns(2)
        with col1:
            total_fund = st.number_input("Total chama fund (KES)", 
                                          min_value=10000, value=720000, step=10000)
            loans_out = st.number_input("Total loans disbursed (KES)", 
                                         min_value=0, value=250000, step=5000)
            avg_interest = st.number_input("Average monthly interest rate (%)", 
                                            value=10.0, step=0.5)
            period_months = st.number_input("Period (months)", min_value=1, value=12)
        with col2:
            interest_earned = loans_out * (avg_interest / 100) * period_months
            st.metric("Interest earned", f"KES {interest_earned:,.0f}")
            st.metric("Return on fund", f"{(interest_earned/total_fund*100):.1f}%")

            if st.session_state.members:
                per_member = interest_earned / len(st.session_state.members)
                st.metric("Dividend per member", f"KES {per_member:,.0f}")

        st.info("""
**Distribution formula (proportional to savings):**
Each member receives: (their savings ÷ total savings) × total interest earned

This rewards members who save more, which is the standard Kenya chama practice.
Members who take loans pay the interest; members who save receive the dividends.
""")

    with tab3:
        st.subheader("Fund Growth Projection")
        col1, col2 = st.columns(2)
        with col1:
            num_members = st.number_input("Number of members", 
                                           min_value=2, value=max(12, len(st.session_state.members)), step=1)
            monthly_contribution = st.number_input("Monthly contribution/member (KES)", 
                                                    value=5000, step=500)
            loan_rate = st.number_input("Loan interest rate (%/month)", value=10.0, step=0.5)
            loan_utilization = st.slider("% of fund lent out as loans", 0, 100, 60)
            proj_months = st.number_input("Projection period (months)", min_value=6, value=24, step=6)

        with col2:
            monthly_inflow = num_members * monthly_contribution
            months_data = []
            fund = 0
            for m in range(1, int(proj_months) + 1):
                fund += monthly_inflow
                interest = fund * (loan_utilization / 100) * (loan_rate / 100)
                fund += interest
                months_data.append({"Month": m, "Fund (KES)": round(fund), "Monthly Growth": round(interest)})

            final_fund = months_data[-1]["Fund (KES)"]
            st.metric(f"Fund after {proj_months} months", f"KES {final_fund:,.0f}")
            st.metric("Per-member share", f"KES {final_fund/num_members:,.0f}")

        import pandas as pd
        df = pd.DataFrame(months_data)
        st.line_chart(df.set_index("Month")["Fund (KES)"])

# ─────────────────────────────────────────────────────────────
# MODULE 5: CONTRIBUTION TRACKER
# ─────────────────────────────────────────────────────────────
elif mode == "📊 Contribution Tracker":
    st.title("📊 Contribution Tracker")

    if not st.session_state.members:
        st.warning("Add members first in Member Management module.")
    else:
        months = ["Jan 2026","Feb 2026","Mar 2026","Apr 2026","May 2026","Jun 2026"]
        current_month = "May 2026"

        st.subheader(f"Contributions — {current_month}")
        expected = st.number_input("Expected contribution per member (KES)", value=5000, step=500)

        col1, col2, col3 = st.columns(3)
        paid_count = sum(1 for m in st.session_state.members if m.get("total_contributed", 0) >= expected)
        col1.metric("Paid", paid_count)
        col2.metric("Pending", len(st.session_state.members) - paid_count)
        col3.metric("Collection rate", f"{(paid_count/len(st.session_state.members)*100):.0f}%")

        st.divider()
        import pandas as pd
        tracker_data = []
        for m in st.session_state.members:
            tracker_data.append({
                "Member": m["name"],
                "Status": "✅ Paid" if m.get("total_contributed", 0) >= expected else "⏳ Pending",
                "Amount (KES)": f"{expected:,.0f}",
                "M-Pesa": m["phone"]
            })
        st.dataframe(pd.DataFrame(tracker_data), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────
# MODULE 6: M-PESA INTEGRATION
# ─────────────────────────────────────────────────────────────
elif mode == "📱 M-Pesa Integration":
    st.title("📱 M-Pesa Integration")
    st.info("""
**This module shows how to use mpesa-mcp with your chama.**
For live M-Pesa payments, connect [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp).
""")

    tab1, tab2 = st.tabs(["Collect Contributions", "Send Payouts"])

    with tab1:
        st.subheader("Collect Monthly Contributions via M-Pesa STK Push")
        st.markdown("*Send STK push requests to all members at once*")

        contribution = st.number_input("Contribution amount (KES)", value=5000)
        chama_ref = st.text_input("M-Pesa account reference", 
                                   value=f"{st.session_state.chama_name.replace(' ','_')}_MAY26")

        if st.session_state.members and st.button("📤 Generate STK Push requests"):
            st.subheader("STK Push Commands (paste into mpesa-mcp)")
            for m in st.session_state.members:
                st.code(f"""mpesa_stk_push(
    phone_number="{m['phone']}",
    amount={contribution},
    account_reference="{chama_ref}",
    transaction_desc="Chama contribution {st.session_state.chama_name}"
)""")
                st.caption(f"→ {m['name']}")

    with tab2:
        st.subheader("Pay Merry-Go-Round Recipient via B2C")

        if st.session_state.members:
            recipient = st.selectbox("Select payout recipient",
                options=[m["name"] for m in st.session_state.members])
            payout = st.number_input("Payout amount (KES)", value=60000)
            recipient_data = next(m for m in st.session_state.members if m["name"] == recipient)

            if st.button("💸 Generate B2C payment"):
                st.code(f"""mpesa_b2c_payment(
    phone_number="{recipient_data['phone']}",
    amount={payout},
    occasion="{st.session_state.chama_name} merry-go-round payout",
    remarks="Monthly payout to {recipient}"
)""")
                st.success(f"B2C command generated for {recipient} — KES {payout:,}")

# ─────────────────────────────────────────────────────────────
# MODULE 7: AI ADVISOR
# ─────────────────────────────────────────────────────────────
else:
    st.title("🤖 SaccoAI Advisor")
    st.markdown("*AI-powered guidance for your chama's financial health*")

    if "chama_chat" not in st.session_state:
        st.session_state.chama_chat = []

    # Quick prompts
    st.subheader("Quick questions")
    quick = st.selectbox("Select a common question or type your own below", [
        "—",
        "How do we handle a member who defaults on a loan?",
        "What is the best interest rate for our table banking?",
        "How do we invest our surplus funds safely?",
        "What are the tax implications of our chama?",
        "How do we expand from 12 to 20 members?",
        "What government funds can our chama apply for?",
        "How do we create a chama constitution?",
        "What should our loan policy include?"
    ])

    for msg in st.session_state.chama_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_q = st.chat_input("Ask SaccoAI...")
    if quick != "—":
        user_q = quick
        st.session_state.chama_chat = []

    if user_q and key:
        # Build context from session state
        members_summary = f"{len(st.session_state.members)} members" if st.session_state.members else "no members yet"
        config = st.session_state.get("chama_config", {})
        context = f"Chama name: {st.session_state.chama_name}, {members_summary}, type: {config.get('type', 'merry-go-round')}"

        st.session_state.chama_chat.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.markdown(user_q)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                prompt = f"""You are SaccoAI, an expert in Kenya chama management, rotating credit groups, table banking, and informal financial systems.

Context: {context}

Question: {user_q}

Provide practical, Kenya-specific guidance covering:
- Legal framework (if relevant): Societies Act, SACCO Act, Co-operatives Act
- Financial best practices for Kenya informal sector
- M-Pesa integration possibilities
- Government support programs (UWEZO Fund, Youth Fund, Women Enterprise Fund)
- Risk management and dispute resolution

Be practical, concise, and use Kenya Shilling (KES) for all amounts.
Format with clear headings and bullet points."""

                try:
                    resp = gemini(prompt, key)
                    st.markdown(resp)
                    st.session_state.chama_chat.append({"role": "assistant", "content": resp})
                except Exception as e:
                    st.error(f"AI error: {e}")

st.divider()
st.caption("SaccoAI © 2026 | [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) | [East African Decision Infrastructure](https://gabrielmahia.github.io) | contact@aikungfu.dev")
