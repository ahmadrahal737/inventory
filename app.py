import streamlit as st
import os
import json

st.set_page_config(
    page_title="منصة الأحاديث النبوية الشريفة", 
    page_icon="🌿", 
    layout="centered"
)

# تنسيق واجهة حديثة، مرتبة، وخالية من أي تداخل
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', sans-serif;
    background: #f8f9fa;
    color: #2b2d42;
}

.main-header {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
    padding: 22px;
    border-radius: 14px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(27, 67, 50, 0.1);
}
.main-header h1 {
    font-size: 22px !important;
    font-weight: 900;
    margin-bottom: 5px;
    color: #ffffff;
}
.main-header p {
    font-size: 12px;
    color: #d8f3dc;
    margin: 0;
}

.hadith-card {
    background: #ffffff;
    border: 1px solid #e9ecef;
    border-right: 5px solid #52b788;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.hadith-text {
    font-size: 14px !important;
    line-height: 1.7;
    color: #212529;
    margin-bottom: 10px;
    font-weight: 600;
}

.hadith-meta {
    font-size: 11px !important;
    color: #2d6a4f;
    font-weight: 700;
    background-color: #e8f5e9;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 8px;
}

.footer {
    text-align: center;
    font-size: 12px;
    color: #6c757d;
    margin-top: 30px;
    padding: 15px;
    border-top: 1px solid #dee2e6;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🌿 منارة الأحاديث النبوية الشريفة</h1>
    <p>مرجعك الموثوق لأحاديث وسنة النبي صلى الله عليه وسلم والأذكار</p>
</div>
""", unsafe_allow_html=True)

FAV_FILE = "favorites.json"
HADITH_FILE = "hadith.txt"

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

def load_hadiths():
    hadiths = []
    filename = HADITH_FILE if os.path.exists(HADITH_FILE) else "hadiths.txt"
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

def save_all_hadiths(hadiths):
    with open(HADITH_FILE, "w", encoding="utf-8") as f:
        blocks = []
        for h in hadiths:
            block = f"{h['category']}\n{h['id']}\n{h['narrator']}\n{h['text']}"
            blocks.append(block)
        f.write("\n\n---\n".join(blocks))

all_hadiths = load_hadiths()

# الشريط الجانبي للتنقل
st.sidebar.markdown("### 🧭 لوحة التحكم والتصفح")
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
st.sidebar.markdown("#### 🔐 إعدادات المشرف")
admin_secret_key = st.sidebar.text_input("مفتاح المشرف السري:", type="password")
MY_ADMIN_PASSWORD = "AhmedRahal@2026_Secure"
is_admin = (admin_secret_key == MY_ADMIN_PASSWORD)

if is_admin:
    st.sidebar.success("تم تفعيل صلاحيات المشرف ✅")
    st.markdown("---")
    st.subheader("🛠️ إضافة حديث جديد للموقع")
    
    with st.form("admin_add_form"):
        new_category = st.selectbox("القسم:", [
            "🌙 احاديث عن النوم",
            "🍽️ احاديث عن الاكل",
            "🌙 احاديث عن الصوم",
            "🕋 احاديث عن الصلاة",
            "🤲 اذكار الصباح والمساء"
        ])
        new_id = st.text_input("رقم الحديث (مثلاً: 01)")
        new_narrator = st.text_input("الراوي / المصدر (مثلاً: رواه البخاري)")
        new_text = st.text_area("نص الحديث الشريف أو الذكر")
        
        publish_btn = st.form_submit_button(label="نشر الحديث")
        
        if publish_btn:
            if new_id and new_narrator and new_text:
                new_h = {"category": new_category, "id": new_id, "narrator": new_narrator, "text": new_text}
                all_hadiths.append(new_h)
                save_all_hadiths(all_hadiths)
                st.success("تم نشر الحديث بنجاح!")
                st.rerun()
            else:
                st.error("الرجاء تعبئة كافة الحقول.")
    st.markdown("---")

# فلترة الأحاديث بناءً على القسم المختاره
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
    st.markdown(f"**عدد الأحاديث المعروضة: ({len(filtered_hadiths)})**")
    st.write("")
    
    for i, h in enumerate(filtered_hadiths):
        st.markdown(f"""
        <div class="hadith-card">
            <div class="hadith-meta">📌 {h['category']} | رقم: {h['id']} | الراوي: {h['narrator']}</div>
            <div class="hadith-text">{h['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # أزرار التفاعل (حفظ / إزالة / حذف نهائي للأدمن)
        cols = st.columns([1, 1, 3] if is_admin else [1, 3])
        is_saved = h in st.session_state.saved_hadiths
        
        with cols[0]:
            if not is_saved:
                if st.button("💾 حفظ", key=f"s_{i}_{h['id']}_{h['category'][:3]}"):
                    if h not in st.session_state.saved_hadiths:
                        st.session_state.saved_hadiths.append(h)
                        save_favorites(st.session_state.saved_hadiths)
                        st.success("تم الحفظ!")
                        st.rerun()
            else:
                if st.button("❌ إزالة", key=f"r_{i}_{h['id']}_{h['category'][:3]}"):
                    st.session_state.saved_hadiths.remove(h)
                    save_favorites(st.session_state.saved_hadiths)
                    st.warning("تمت الإزالة.")
                    st.rerun()
        
        if is_admin:
            with cols[1]:
                if st.button("🗑️ حذف نهائي", key=f"del_{i}_{h['id']}_{h['category'][:3]}"):
                    if h in all_hadiths:
                        all_hadiths.remove(h)
                        save_all_hadiths(all_hadiths)
                    if h in st.session_state.saved_hadiths:
                        st.session_state.saved_hadiths.remove(h)
                        save_favorites(st.session_state.saved_hadiths)
                    st.error("تم حذف الحديث نهائياً من الموقع!")
                    st.rerun()
        st.write("")
else:
    st.info("لا توجد أحاديث مضافة حالياً في هذا القسم.")

st.markdown("""
<div class="footer">
    تم التصميم والتطوير بعناية بواسطة: <b>أحمد رحال</b> ✨
</div>
""", unsafe_allow_html=True)
