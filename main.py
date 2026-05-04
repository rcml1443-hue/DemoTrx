import streamlit as st
import pandas as pd

# Web App ရဲ့ ခေါင်းစဉ်နှင့် Layout ကို သတ်မှတ်ခြင်း
st.set_page_config(page_title="TRX Predictor", layout="centered")
st.title("📈 TRX Big/Small Analysis")

# ၁။ Data Loading (data.csv ဖိုင်ကို ဖတ်ခြင်း)
@st.cache_data
def load_data():
    try:
        # ကော်လံတွေအများကြီးထဲက 'bs' တစ်ခုတည်းကိုပဲ ရွေးဖတ်ခြင်းဖြင့် speed တက်စေပါတယ်
        df = pd.read_csv('data.csv', usecols=['bs'])
        return df['bs'].astype(str).tolist()
    except Exception as e:
        # ဖိုင်နာမည် မှားနေလျှင် သို့မဟုတ် bs ကော်လံမပါလျှင် Error ပြရန်
        st.error(f"Error: {e}")
        return []

data_list = load_data()

# ၂။ UI အပိုင်း - User က လက်ရှိရလဒ် ၅ ခု ရွေးချယ်ရန်
if not data_list:
    st.info("GitHub တွင် data.csv ဖိုင်ကို အရင်တင်ပေးရန် စောင့်ဆိုင်းနေပါသည်...")
else:
    st.subheader("နောက်ဆုံးထွက်ထားသော ရလဒ် ၅ ခုကို ရွေးပါ")
    
    # ရလဒ် ၅ ခုကို ဘေးတိုက်ပြသရန် Column ၅ ခုခွဲခြင်း
    cols = st.columns(5)
    inputs = []
    for i in range(5):
        with cols[i]:
            val = st.selectbox(f"#{i+1}", ["B", "S"], key=f"in_{i}")
            inputs.append(val)

    # ၃။ Prediction Button - ခန့်မှန်းချက်တွက်ချက်ခြင်း
    if st.button("Predict Next Result", use_container_width=True):
        matches_next_b = 0
        matches_next_s = 0
        
        # Pattern Matching Logic (Data ထဲမှာ လိုက်ရှာမယ်)
        # ဥပမာ- [B, B, S, S, S] ကိုတွေ့ရင် နောက်ကပ်လျက်က ဘာလဲဆိုတာကို မှတ်မယ်
        for i in range(len(data_list) - 5):
            if data_list[i : i+5] == inputs:
                next_val = data_list[i+5]
                if next_val == 'B':
                    matches_next_b += 1
                elif next_val == 'S':
                    matches_next_s += 1
        
        total_matches = matches_next_b + matches_next_s

        if total_matches > 0:
            b_percent = (matches_next_b / total_matches) * 100
            s_percent = (matches_next_s / total_matches) * 100
            
            st.divider()
            st.write(f"သမိုင်းကြောင်းအရ ဤ Pattern ကို **{total_matches}** ကြိမ် တွေ့ရှိခဲ့သည်။")
            
            # ရလဒ်များကို % ဖြင့် ပြသခြင်း
            col_b, col_s = st.columns(2)
            col_b.metric("Big (B) ကျနိုင်ခြေ", f"{round(b_percent, 1)}%")
            col_s.metric("Small (S) ကျနိုင်ခြေ", f"{round(s_percent, 1)}%")
            
            # Progress Bar ပြသခြင်း
            st.progress(int(b_percent))
            st.caption("ဘယ်ဘက် (B) | ညာဘက် (S)")
        else:
            # တူညီတဲ့ Pattern မရှိခဲ့လျှင် Warning ပြရန်
            st.warning("စိတ်မရှိပါနဲ့၊ ဤ Pattern မျိုး ယခင် Data ထဲမှာ မတွေ့ရှိခဲ့ပါ။")
