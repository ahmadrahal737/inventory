import streamlit as st
import os

st.set_page_config(page_title="موسوعة صحيح البخاري", page_icon="📖", layout="centered")

st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
    font-size: 13px;
}
h1 {
    font-size: 20px !important;
    text-align: center;
    color: #00796b;
}
.hadith-box {
    background-color: #1e1e1e;
    border: 1px solid #333;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 12px;
}
.hadith-text {
    font-size: 13px !important;
    line-height: 1.6;
    color: #e0e0e0;
}
.hadith-meta {
    font-size: 11px !important;
    color: #4db6ac;
    font-weight: bold;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("📖 صحيح البخاري المختار")
st.write("الأحاديث النبوية الشريفة المختارة:")

def load_hadiths():
    hadiths = []
    if os.path.exists("hadiths.txt"):
        with open("hadiths.txt", "r", encoding="utf-8") as f:
            content = f.read().split("---")
            for block in content:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) >= 3:
                    h = {"id": lines[0], "narrator": lines[1], "text": "\n".join(lines[2:])}
                    hadiths.append(h)
    return hadiths

hadiths_list = load_hadiths()

if hadiths_list:
    for h in hadiths_list:
        st.markdown(f"""
        <div class="hadith-box">
            <div class="hadith-meta">حديث رقم: {h['id']} | الراوي: {h['narrator']}</div>
            <div class="hadith-text">{h['text']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("الرجاء إنشاء ملف בשم hadiths.txt في مستودع GitHub وإضافة الأحاديث داخله.")
