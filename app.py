import streamlit as st
import os

st.set_page_config(
    page_title="أحاديث نبوية شريفة", 
    page_icon="✨", 
    layout="centered"
)

# تنسيق CSS احترافي وألوان أنيقة تناسب الجوال
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', sans-serif;
    background-color: #f8f9fa;
    color: #2c3e50;
}

h1 {
    font-size: 22px !important;
    text-align: center;
    color: #1b4332;
    font-weight: 700;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 13px;
    color: #52796f;
    margin-bottom: 20px;
}

.hadith-card {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-right: 4px solid #2d6a4f;
    padding: 14px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}

.hadith-text {
    font-size: 14px !important;
    line-height: 1.6;
    color: #212529;
    margin-bottom: 8px;
}

.hadith-meta {
    font-size: 11px !important;
    color: #40916c;
    font-weight: 600;
    margin-bottom: 8px;
}

.footer {
    text-align: center;
    font-size: 12px;
    color: #6c757d;
    margin-top: 40px;
    padding: 15px;
    border-top: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# رأس الصفحة
st.markdown("<h1>✨ أحاديث عن النبي عليه افضل الصلاة والسلام</h1>", unsafe_allow_html=True)
st.markdown('<div class="sub-title">منصة جامعة للأحاديث النبوية الصحيحة والأذكار</div>', unsafe_allow_html=True)

# قراءة الأحاديث من ملف hadith.txt (أو hadiths.txt)
def load_hadiths():
    hadiths = []
    # البحث عن أي من الاسمين لضمان عدم حدوث خطأ
    filename = "hadith.txt" if os.path.exists("hadith.txt") else "hadiths.txt"
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().split("---")
            for block in content:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) >= 4:  # [القسم، الرقم، الراوي، النص]
                    h = {
                        "category": lines[0],
                        "id": lines[1],
                        "narrator": lines[2],
                        "text": "\n".join(lines[3:])
                    }
                    hadiths.append(h)
    return hadiths

all_hadiths = load_hadiths()

# تهيئة قائمة المحفوظات في الذاكرة المؤقتة للجلسة
if 'saved_hadiths' not in st.session_state:
    st.session_state.saved_hadiths = []

# الأقسام الرئيسية
categories = [
    "الرئيسية (كل الأحاديث)",
    "🌙 احاديث عن النوم",
    "🍽️ احاديث عن الاكل",
    "🌙 احاديث عن الصوم",
    "🕋 احاديث عن الصلاة",
    "🤲 اذكار الصباح والمساء",
    "⭐ الأحاديث المحفوظة"
]

selected_tab = st.selectbox("📂 اختر القسم للتصفح:", categories)

# الفلترة حسب القسم المختاره
filtered_hadiths = []
if selected_tab == "الرئيسية (كل الأحاديث)":
    filtered_hadiths = all_hadiths
elif selected_tab == "⭐ الأحاديث المحفوظة":
    filtered_hadiths = st.session_state.saved_hadiths
else:
    # استخراج اسم القسم بدون الرموز التعبيرية للمطابقة
    cat_name = selected_tab.split(" ")[1] if " " in selected_tab else selected_tab
    filtered_hadiths = [h for h in all_hadiths if cat_name in h['category']]

# عرض الأحاديث
if filtered_hadiths:
    st.write(f"عدد الأحاديث المعروضة: **{len(filtered_hadiths)}**")
    for i, h in enumerate(filtered_hadiths):
        st.markdown(f"""
        <div class="hadith-card">
            <div class="hadith-meta">📌 القسم: {h['category']} | حديث رقم: {h['id']} | الراوي: {h['narrator']}</div>
            <div class="hadith-text">{h['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # زر حفظ الحديث
        save_key = f"save_{h['category']}_{h['id']}_{i}"
        is_saved = h in st.session_state.saved_hadiths
        
        if not is_saved:
            if st.button("💾 حفظ هذا الحديث", key=save_key):
                if h not in st.session_state.saved_hadiths:
                    st.session_state.saved_hadiths.append(h)
                    st.success("تم حفظ الحديث بنجاح!")
                    st.rerun()
        else:
            if st.button("❌ إزالة من المحفوظات", key=f"remove_{save_key}"):
                st.session_state.saved_hadiths.remove(h)
                st.warning("تمت إزالة الحديث من المحفوظات.")
                st.rerun()
else:
    if selected_tab == "⭐ الأحاديث المحفوظة":
        st.info("لم تقم بحفظ أي حديث حتى الآن. اضغط على زر 'حفظ هذا الحديث' ليظهر هنا.")
    else:
        st.info("لا توجد أحاديث مضافة في هذا القسم حالياً. قم بإضافتها عبر ملف النصوص في GitHub.")

# التوقيع في الأسفل
st.markdown("""
<div class="footer">
    تم التصميم والطباعة بواسطة: <b>أحمد رحال</b> ✨
</div>
""", unsafe_allow_html=True)
