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
st.write("ابحث في آلاف الأحاديث النبوية الشريفة بسهولة ويسر.")

query = st.text_input("أدخل كلمة للبحث عنها (مثل: الإيمان، الصلاة):")

if query:
    results = bukhari.search(query, limit=10)
    st.subheader(f"نتائج البحث عن: '{query}'")
    if results:
        for h in results:
            st.markdown(f"**حديث رقم:** {h.id} | **الراوي:** {h.arabic.get('narrator', 'غير متوفر')}")
            st.info(h.arabic.get('text', ''))
            st.divider()
    else:
        st.warning("لم يتم العثور على نتائج مطابقة لبحثك.")
