import streamlit as st
from sahih_al_bukhari import Bukhari

st.set_page_config(page_title="موسوعة صحيح البخاري", page_icon="📖", layout="centered")

# تنسيق مخصص لتصغير الخطوط وتناسب الهاتف المحمول (RTL)
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
    font-size: 14px;
}
h1 {
    font-size: 22px !important;
    text-align: center;
    color: #00796b;
}
p, .stTextInput label, .stSelectbox label {
    font-size: 13px !important;
}
.hadith-box {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.hadith-text {
    font-size: 14px !important;
    line-height: 1.5;
    color: #333;
}
.hadith-meta {
    font-size: 11px !important;
    color: #00796b;
    font-weight: bold;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_bukhari():
    return Bukhari()

with st.spinner("جاري تحميل قاعدة بيانات الأحاديث..."):
    bukhari = load_bukhari()

st.title("📖 صحيح البخاري الشامل")
st.write("تصفح الأحاديث أو ابحث مباشرة:")

# قائمة الأبواب مع مصطلحات بحث مضمونة النتائج داخل المكتبة
categories = {
    "اختر الباب الفقهي...": "",
    "الصلاة": "الصلاة",
    "الصيام": "الصيام",
    "الوضوء": "الوضوء",
    "الإيمان": "الإيمان",
    "العلم": "العلم",
    "الزكاة": "الزكاة"
}

selected_cat = st.selectbox("الأبواب الجاهزة:", list(categories.keys()))

results = []

if categories[selected_cat]:
    keyword = categories[selected_cat]
    results = bukhari.search(keyword, limit=20)
else:
    query = st.text_input("أو بحث حر (مثال: صلاة، صوم، حج):")
    if query:
        results = bukhari.search(query, limit=20)

if results:
    st.write(f"**عدد النتائج الظاهرة:** {len(results)}")
    for h in results:
        narrator = h.arabic.get('narrator', 'غير متوفر')
        text = h.arabic.get('text', '')
        st.markdown(f"""
        <div class="hadith-box">
            <div class="hadith-meta">حديث رقم: {h.id} | الراوي: {narrator}</div>
            <div class="hadith-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)
elif selected_cat != "اختر الباب الفقهي..." or 'query' in locals() and locals().get('query'):
    st.warning("لم يتم العثور على نتائج مطابقة.")
