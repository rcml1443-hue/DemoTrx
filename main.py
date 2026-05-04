import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="TRX Live Tracker", layout="wide")

# CSS for Win/Lose styling (ပြင်ဆင်ပြီးသား)
st.markdown("""
    <style>
    .win { color: #28a745; font-weight: bold; font-size: 24px; }
    .lose { color: #dc3545; font-weight: bold; font-size: 24px; }
    .prediction-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border: 2px solid #1f77b4; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 TRX Live Pattern Tracker & Predictor")

# ၁။ Data Loading
@st.cache_data
def load_data():
    try:
        # data.csv ဖိုင်ကို ဖတ်မယ်
        df = pd.read_csv('data.csv', usecols=['bs'])
        return df['bs'].astype(str).tolist()
    except:
        return []

data_list = load_data()

# ၂။ Session State
if 'my_history' not in st.session_state:
    st.session_state.my_history = []
if 'last_prediction' not in st.session_state:
    st.session_state.last_prediction = None
if 'score_log' not in st.session_state:
    st.session_state.score_log = []

# ၃။ Input Section
st.subheader("တကယ့်ရလဒ်ကို တစ်ခုချင်းစီ ရိုက်ထည့်ပါ")
new_val = st.radio("အခုထွက်တဲ့ ရလဒ်ကို ရွေးပါ:", ["B", "S"], horizontal=True)

if st.button("ADD RESULT & PREDICT"):
    # Win/Lose စစ်ဆေးခြင်း
    if st.session_state.last_prediction:
        if st.session_state.last_prediction == new_val:
            st.session_state.score_log.append("WIN ✅")
        else:
            st.session_state.score_log.append("LOSE ❌")
            
    # ရလဒ်အသစ်ထည့်
    st.session_state.my_history.append(new_val)
    if len(st.session_state.my_history) > 10:
        st.session_state.my_history.pop(0)

# ၄။ လက်ရှိ Sequence
st.write("---")
st.write(f"**လက်ရှိ Sequence (နောက်ဆုံး {len(st.session_state.my_history)} ခု):**")
st.code(" - ".join(st.session_state.my_history))

# ၅။ Analysis & Prediction
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
        pred = "B" if b_per > s_per else "S"
        st.session_state.last_prediction = pred
        
        st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
        st.subheader("🔮 နောက်တစ်ကြိမ်အတွက် ခန့်မှန်းချက်:")
        col1, col2 = st.columns(2)
        col1.metric("Recommended", "BIG (B)" if pred == "B" else "SMALL (S)")
        col2.metric("Confidence", f"{round(max(b_per, s_per), 1)}%")
        st.write(f"သမိုင်းကြောင်းအရ ဤ Pattern ကို {total} ကြိမ် တွေ့ရှိခဲ့သည်။")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("ဒီ ၁၀ ခု Pattern မျိုး Data ထဲမှာ မတွေ့သေးပါ။")
        st.session_state.last_prediction = None
else:
    st.info(f"ခန့်မှန်းချက်ထွက်ရန် နောက်ထပ် {10 - len(st.session_state.my_history)} ခု ရိုက်ထည့်ပေးပါ။")

# ၆။ History Log
if st.session_state.score_log:
    st.write("---")
    st.subheader("Win/Lose History")
    for res in reversed(st.session_state.score_log[-10:]):
        if "WIN" in res:
            st.markdown(f'<span class="win">{res}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="lose">{res}</span>', unsafe_allow_html=True)

if st.sidebar.button("Reset All"):
    st.session_state.my_history = []
    st.session_state.last_prediction = None
    st.session_state.score_log = []
    st.rerun()
