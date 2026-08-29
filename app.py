import streamlit as st
from sahih_al_bukhari import Bukhari

st.set_page_config(page_title="موسوعة صحيح البخاري", page_icon="📖", layout="centered")

st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] { direction: rtl; text-align: right; }
.stTextInput input { direction: rtl; text-align: right; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_bukhari():
    return Bukhari()

with st.spinner("جاري تحميل أحاديث صحيح البخاري..."):
    bukhari = load_bukhari()

st.title("📖 موسوعة صحيح البخاري الرقمية")
st.write("تصفح الأحاديث مصنفة حسب الأبواب الفقهية أو ابحث بشكل مباشر.")

# إنشاء خيارات التصفح (الألبومات / الأبواب الجاهزة)
categories = {
    "اختر باباً للتصفح...": "",
    "🌙 ألبوم الصيام": "الصيام",
    "🕋 ألبوم الصلاة": "الصلاة",
    "💧 ألبوم الوضوء": "الوضوء",
    "🤝 ألبوم الأخلاق والمعاملات": "الأخلاق"
}

selected_category = st.selectbox("اختر فئة جاهزة (الأبواب):", list(categories.keys()))

# تصفح عبر الأبواب الجاهزة إذا تم اختيارها
if categories[selected_category]:
    keyword = categories[selected_category]
    st.subheader(f"أحاديث باب: {selected_category}")
    results = bukhari.search(keyword, limit=15)
    
    if results:
        for h in results:
            st.markdown(f"**حديث رقم:** {h.id} | **الراوي:** {h.arabic.get('narrator', 'غير متوفر')}")
            st.info(h.arabic.get('text', ''))
            st.divider()
    else:
        st.warning("لا توجد أحاديث متاحة لهذا الباب حالياً.")

else:
    # البحث اليدوي العادي
    query = st.text_input("أو ابحث بكلمة مفتاحية حرة:")
    if query:
        results = bukhari.search(query, limit=15)
        st.subheader(f"نتائج البحث عن: '{query}'")
        if results:
            for h in results:
                st.markdown(f"**حديث رقم:** {h.id} | **الراوي:** {h.arabic.get('narrator', 'غير متوفر')}")
                st.info(h.arabic.get('text', ''))
                st.divider()
        else:
            st.warning("لم يتم العثور على نتائج مطابقة لبحثك.")
