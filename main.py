import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Live Tracker", layout="wide")

# CSS for Win/Lose styling
st.markdown("""
    <style>
    .win { color: #28a745; font-weight: bold; font-size: 24px; }
    .lose { color: #dc3545; font-weight: bold; font-size: 24px; }
    .prediction-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #1f77b4; }
    </style>
    """, unsafe_allow_stdio=True)

st.title("🎯 TRX Live Pattern Tracker & Predictor")

# ၁။ Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv', usecols=['bs'])
        return df['bs'].astype(str).tolist()
    except:
        return []

data_list = load_data()

# ၂။ Session State သုံးပြီး ရိုက်ထားတဲ့ Data တွေကို မှတ်ထားမယ်
if 'my_history' not in st.session_state:
    st.session_state.my_history = []  # User ရိုက်သမျှ သိမ်းထားမယ့်နေရာ
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'score_log' not in st.session_state:
    st.session_state.score_log = []

# ၃။ Input Section
st.subheader("တကယ့်ရလဒ်ကို တစ်ခုချင်းစီ ရိုက်ထည့်ပါ")
col_input, col_reset = st.columns([3, 1])

with col_input:
    new_val = st.radio("အခုထွက်တဲ့ ရလဒ်ကို ရွေးပါ:", ["B", "S"], horizontal=True)

if st.button("ADD RESULT & PREDICT"):
    # ရလဒ်အသစ်ကို List ထဲထည့်
    st.session_state.my_history.append(new_val)
    
    # ၁၀ ခုထက် ကျော်သွားရင် ရှေ့ဆုံးကတစ်ခုကို ဖြုတ် (Queue Logic)
    if len(st.session_state.my_history) > 10:
        st.session_state.my_history.pop(0)

    # Win/Lose စစ်ဆေးခြင်း (အရင်ရှိခဲ့တဲ့ prediction နဲ့ အခုရလဒ် တိုက်စစ်မယ်)
    if st.session_state.last_prediction:
        if st.session_state.last_prediction == new_val:
            st.session_state.score_log.append("WIN ✅")
        else:
            st.session_state.score_log.append("LOSE ❌")

# ၄။ လက်ရှိ Sequence ကို ပြသခြင်း
st.write("---")
st.write(f"**လက်ရှိ Sequence (နောက်ဆုံး {len(st.session_state.my_history)} ခု):**")
st.code(" - ".join(st.session_state.my_history))

# ၅။ Analysis & Prediction Logic (၁၀ ခု ပြည့်မှ လုပ်မယ်)
if len(st.session_state.my_history) == 10:
    m_b, m_s = 0, 0
    current_pattern = st.session_state.my_history
    
    for i in range(len(data_list) - 10):
        if data_list[i : i+10] == current_pattern:
            next_val = data_list[i+10]
            if next_val == 'B': m_b += 1
            elif next_val == 'S': m_s += 1
    
    total = m_b + m_s
    
    if total > 0:
        b_per = (m_b/total)*100
        s_per = (m_s/total)*100
        
        # Next Prediction သတ်မှတ်ခြင်း
        pred = "B" if b_per > s_per else "S"
        st.session_state.last_prediction = pred # နောက်တစ်ကြိမ် တိုက်စစ်ဖို့ သိမ်းထားမယ်
        
        st.markdown('<div class="prediction-box">', unsafe_allow_stdio=True)
        st.subheader("🔮 နောက်တစ်ကြိမ်အတွက် ခန့်မှန်းချက်:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recommended", "BIG (B)" if pred == "B" else "SMALL (S)")
        with col2:
            st.metric("Confidence", f"{round(max(b_per, s_per), 1)}%")
        
        st.write(f"ယခင်မှတ်တမ်းထဲတွင် ဤ Pattern ကို {total} ကြိမ် တွေ့ရှိခဲ့သည်။")
        st.markdown('</div>', unsafe_allow_stdio=True)
    else:
        st.warning("ဒီ ၁၀ ခု Pattern မျိုး Data ထဲမှာ မတွေ့သေးပါ။")
        st.session_state.last_prediction = None
else:
    st.info(f"ခန့်မှန်းချက်ထွက်ရန် နောက်ထပ် {10 - len(st.session_state.my_history)} ခု ရိုက်ထည့်ပေးပါဦး။")

# ၆။ Win/Lose History Log
if st.session_state.score_log:
    st.write("---")
    st.subheader("Result History")
    # နောက်ဆုံး ၅ ကြိမ်စာ ရလဒ်ကို ပြမယ်
    for res in reversed(st.session_state.score_log[-5:]):
        if "WIN" in res:
            st.markdown(f'<span class="win">{res}</span>', unsafe_allow_stdio=True)
        else:
            st.markdown(f'<span class="lose">{res}</span>', unsafe_allow_stdio=True)

# Reset Button
if st.sidebar.button("Reset Everything"):
    st.session_state.my_history = []
    st.session_state.last_prediction = None
    st.session_state.score_log = []
    st.rerun()
