import streamlit as st
import os
import json

st.set_page_config(
    page_title="منصة الأحاديث النبوية الشريفة", 
    page_icon="🌿", 
    layout="centered"
)

# تصميم وتنسيق عصري متطور وملون بالكامل مع واجهة راقية
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', sans-serif;
    background: linear-gradient(135deg, #f4f7f6 0%, #eef2f3 100%);
    color: #2b2d42;
}

/* الهيدر الرئيسي */
.main-header {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
    padding: 25px;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 8px 20px rgba(27, 67, 50, 0.15);
}
.main-header h1 {
    font-size: 26px !important;
    font-weight: 900;
    margin-bottom: 5px;
    color: #ffffff;
}
.main-header p {
    font-size: 13px;
    color: #d8f3dc;
    margin: 0;
}

/* بطاقات الأحاديث المزخرفة */
.hadith-card {
    background: #ffffff;
    border: none;
    border-right: 5px solid #52b788;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hadith-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}

.hadith-text {
    font-size: 15px !important;
    line-height: 1.8;
    color: #2b2d42;
    margin-bottom: 12px;
    font-weight: 600;
}

.hadith-meta {
    font-size: 12px !important;
    color: #2d6a4f;
    font-weight: 700;
    background-color: #e8f5e9;
    padding: 4px 10px;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 10px;
}

/* تخصيص الأزرار */
.stButton>button {
    border-radius: 8px !important;
    font-family: 'Cairo', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

/* تذييل الصفحة */
.footer {
    text-align: center;
    font-size: 13px;
    color: #6c757d;
    margin-top: 50px;
    padding: 20px;
    border-top: 2px dashed #dee2e6;
}
</style>
""", unsafe_allow_html=True)

# رأس الصفحة الجميل
st.markdown("""
<div class="main-header">
    <h1>🌿 منارة الأحاديث النبوية الشريفة</h1>
    <p>مرجعك الموثوق لأحاديث وسنة النبي صلى الله عليه وسلم والأذكار الصحيحة</p>
</div>
""", unsafe_allow_html=True)

# ملف حفظ المفضلة الدائمة
FAV_FILE = "favorites.json"

def load_favorites():
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_favorites(favorites):
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)

if 'saved_hadiths' not in st.session_state:
    st.session_state.saved_hadiths = load_favorites()

# دالة لتحميل الأحاديث
def load_hadiths():
    hadiths = []
    filename = "hadith.txt" if os.path.exists("hadith.txt") else "hadiths.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().split("---")
            for block in content:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) >= 4:
                    h = {
                        "category": lines[0],
                        "id": lines[1],
                        "narrator": lines[2],
                        "text": "\n".join(lines[3:])
                    }
                    hadiths.append(h)
    return hadiths

all_hadiths = load_hadiths()

# الشريط الجانبي الذكي (مخفي فيه مدخل المشرف بسرية تامة)
st.sidebar.markdown("### 🧭 خيارات التصفح والتحكم")
categories = [
    "الرئيسية (كل الأحاديث)",
    "🌙 احاديث عن النوم",
    "🍽️ احاديث عن الاكل",
    "🌙 احاديث عن الصوم",
    "🕋 احاديث عن الصلاة",
    "🤲 اذكار الصباح والمساء",
    "⭐ الأحاديث المحفوظة"
]

selected_tab = st.sidebar.selectbox("اختر القسم:", categories)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔐 بوابة الإدارة الخاصة")
# مفتاح سري لا يفتح خانة الإدارة إلا إذا كتبت الكلمة السرية الخاصة بك بدقة
admin_secret_key = st.sidebar.text_input("أدخل مفتاح المشرف:", type="password", placeholder="كلمة المرور الخاصة بك")

# قم بتغيير كلمة المرور الخاصة بك هنا إلى أي كلمة سر قوية تريدها تماماً
MY_ADMIN_PASSWORD = "AhmedRahal@2026_Secure" 

if admin_secret_key == MY_ADMIN_PASSWORD:
    st.sidebar.success("مرحباً بك يا أستاذ أحمد! تم تفعيل وضع المشرف.")
    st.markdown("---")
    st.subheader("🛠️ لوحة تحكم المشرف (إضافة حديث جديد)")
    
    with st.form("admin_add_form"):
        new_category = st.selectbox("اختر القسم للحديث الجديد:", [
            "🌙 احاديث عن النوم",
            "🍽️ احاديث عن الاكل",
            "🌙 احاديث عن الصوم",
            "🕋 احاديث عن الصلاة",
            "🤲 اذكار الصباح والمساء"
        ])
        new_id = st.text_input("رقم الحديث (مثلاً: 04)")
        new_narrator = st.text_input("الراوي أو المرجع (مثلاً: رواه مسلم)")
        new_text = st.text_area("نص الحديث الشريف أو الذكر بطريقة صحيحة")
        
        publish_btn = st.form_submit_button(label="🚀 نشر الحديث فوراً للموقع")
        
        if publish_btn:
            if new_id and new_narrator and new_text:
                block_to_add = f"\n\n---\n{new_category}\n{new_id}\n{new_narrator}\n{new_text}"
                with open("hadith.txt", "a", encoding="utf-8") as f:
                    f.write(block_to_add)
                st.success("تم نشر الحديث بنجاح وسيراه الزوار الآن!")
            else:
                st.error("الرجاء تعبئة كافة الحقول المطلوبة للنشر.")
    st.markdown("---")

# عرض الأحاديث للزوار
filtered_hadiths = []
if selected_tab == "الرئيسية (كل الأحاديث)":
    filtered_hadiths = all_hadiths
elif selected_tab == "⭐ الأحاديث المحفوظة":
    filtered_hadiths = st.session_state.saved_hadiths
else:
    keyword = ""
    if "النوم" in selected_tab: keyword = "النوم"
    elif "الاكل" in selected_tab or "الأكل" in selected_tab: keyword = "الاكل"
    elif "الصوم" in selected_tab: keyword = "الصوم"
    elif "الصلاة" in selected_tab: keyword = "الصلاة"
    elif "اذكار" in selected_tab or "أذكار" in selected_tab: keyword = "اذكار"
    
    filtered_hadiths = [h for h in all_hadiths if keyword in h['category']]

if filtered_hadiths:
    st.markdown(f"**عدد الأحاديث المتاحة في هذا القسم: ({len(filtered_hadiths)})**")
    st.write("")
    
    for i, h in enumerate(filtered_hadiths):
        st.markdown(f"""
        <div class="hadith-card">
            <div class="hadith-meta">📌 {h['category']} | رقم: {h['id']} | الراوي: {h['narrator']}</div>
            <div class="hadith-text">{h['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        save_key = f"save_{h['category']}_{h['id']}_{i}"
        is_saved = h in st.session_state.saved_hadiths
        
        with col1:
            if not is_saved:
                if st.button("💾 حفظ", key=save_key):
                    if h not in st.session_state.saved_hadiths:
                        st.session_state.saved_hadiths.append(h)
                        save_favorites(st.session_state.saved_hadiths)
                        st.success("تم الحفظ!")
                        st.rerun()
            else:
                if st.button("❌ إزالة", key=f"remove_{save_key}"):
                    st.session_state.saved_hadiths.remove(h)
                    save_favorites(st.session_state.saved_hadiths)
                    st.warning("تمت الإزالة.")
                    st.rerun()
        st.write("")
else:
    st.info("لا توجد أحاديث مضافة حالياً في هذا القسم.")

# التذييل
st.markdown("""
<div class="footer">
    تم التصميم والتطوير بعناية بواسطة: <b>أحمد رحال</b> ✨ <br>
    جميع الحقوق محفوظة لنشر السنة النبوية الشريفة.
</div>
""", unsafe_allow_html=True)
