import streamlit as st
import os

st.set_page_config(page_title="موسوعة صحيح البخاري", page_icon="📖", layout="centered")

# تنسيق مخصص لتصغير الخطوط وتناسب الجوال
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
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
}
.hadith-text {
    font-size: 13px !important;
    line-height: 1.5;
    color: #222;
}
.hadith-meta {
    font-size: 11px !important;
    color: #00796b;
    font-weight: bold;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("📖 صحيح البخاري المختار")
st.write("الأحاديث النبوية الشريفة المختارة بعناية:")

# قراءة الأحاديث من ملف خارجي لتتحكم بها وحدك
def load_hadiths():
    hadiths = []
    if os.path.exists("hadiths.txt"):
        with open("hadiths.txt", "r", encoding="utf-8") as f:
            content = f.read().split("---") # الفاصل بين كل حديث والآخر
            for block in content:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) >= 3:
                    hadiths.اتھاض={"id": lines[0], "narrator": lines[1], "text": "\n".join(lines[2:])}
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
    st.info("لم يتم إضافة أي أحاديث حتى الآن. قم بإنشاء ملف hadiths.txt لإضافة الأحاديث.")
