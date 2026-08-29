import streamlit as st

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
p, .stSelectbox label {
    font-size: 12px !important;
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

# قاعدة بيانات مصغرة ومباشرة للأحاديث لضمان ظهورها فوراً على الجوال
bukhari_data = {
    "الصيام": [
        {"id": 1, "narrator": "أبو هريرة رضي الله عنه", "text": "قال رسول الله صلى الله عليه وسلم: «الصيام جُنَّة، فلا يرفث ولا يجهل، وإن امرؤ قاتله أو شاتمه فليقل: إني صائم مرتين»."},
        {"id": 2, "narrator": "عائشة رضي الله عنها", "text": "كان رسول الله صلى الله عليه وسلم يصوم حتى نقول لا يفطر، ويفطر حتى نقول لا يصوم."}
    ],
    "الصلاة": [
        {"id": 3, "narrator": "عمر بن الخطاب رضي الله عنه", "text": "سمعت رسول الله صلى الله عليه وسلم يقول: «إنما الأعمال بالنيات، وإنما لكل امرئ ما نَوَى»."},
        {"id": 4, "narrator": "أبو هريرة رضي الله عنه", "text": "أتي النبي صلى الله عليه وسلم برجل قد شرب فقال: اضربوه."}
    ],
    "الوضوء": [
        {"id": 5, "narrator": "حمران مولى عثمان", "text": "أن عثمان بن عفان رضي الله عنه دعا بتور ففرغ على كفيكه ثلاث مرار فغسلهما..."}
    ]
}

st.title("📖 صحيح البخاري الشامل")
st.write("اختر الباب لعرض الأحاديث مباشرة:")

selected_cat = st.selectbox("الأبواب الفقهية:", ["اختر الباب..."] + list(bukhari_data.keys()))

if selected_cat in bukhari_data:
    st.subheader(f"أحاديث باب: {selected_cat}")
    for h in bukhari_data[selected_cat]:
        st.markdown(f"""
        <div class="hadith-box">
            <div class="hadith-meta">حديث رقم: {h['id']} | الراوي: {h['narrator']}</div>
            <div class="hadith-text">{h['text']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("يرجى اختيار باب من القائمة أعلاه لعرض الأحاديث.")
