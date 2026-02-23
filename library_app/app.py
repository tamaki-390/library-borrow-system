# app.py
import streamlit as st

from pages import book_page
from pages import member_page
from pages import borrow_page

# ✅ เพิ่มเติม: import หน้า admin 
from pages import admin_page

# ✅ เพิ่มเติม: import หน้า login (View) 
from pages import Login_page

from pages import report_page
# =========================
# View helpers (reset form)
# =========================

# ✅ เพิ่มเติม: init session สำหรับ login/logout 
if "is_logged_in" not in st.session_state: 
    st.session_state["is_logged_in"] = False 
if "user" not in st.session_state: 
    st.session_state["user"] = None 

# ซ่อนเมนูอัตโนมัติ (app/book page/...)
# ✅ ซ่อน Multi-page auto nav (Streamlit sidebar pages list) + fallback หลาย selector
st.markdown("""
<style>
/* 1) ตัวหลัก: Sidebar navigation ของ multipage */
section[data-testid="stSidebarNav"] {display: none !important;}


/* 2) fallback: เผื่อ DOM เปลี่ยนชื่อ/โครง */
div[data-testid="stSidebarNav"] {display: none !important;}
nav[data-testid="stSidebarNav"] {display: none !important;}


/* 3) fallback เพิ่มเติม: ซ่อนหัวข้อ Pages / รายการหน้า (บางเวอร์ชัน) */
div[data-testid="stSidebarNavItems"] {display: none !important;}
div[data-testid="stSidebarNavSeparator"] {display: none !important;}


/* 4) fallback สุดท้าย: ถ้า Streamlit render เป็น <ul>/<li> ใน sidebar */
aside ul:has(a[href*="?page="]) {display: none !important;}
aside ul:has(a[href*="/book_page"]) {display: none !important;}
aside ul:has(a[href*="/member_page"]) {display: none !important;}
aside ul:has(a[href*="/borrow_page"]) {display: none !important;}
</style>
""", unsafe_allow_html=True)


# =========================
# UI
# =========================
st.set_page_config(page_title="ระบบยืม-คืนหนังสือ", page_icon="📚")

import model
model.ensure_user_schema()

# ✅ เพิ่มเติม: Login Gate (ถ้ายังไม่ล็อกอินให้ไปหน้า login) 
if not st.session_state["is_logged_in"]: 
    Login_page.render_login() 
    st.stop()

# ✅ แก้ไขใหม่: ให้ส่วนหัวเว็บทำงานหลัง Login เท่านั้น (เพื่อไม่ให้เห็นหน้าอื่นก่อนล็อกอิน) 
st.title("📚 ระบบยืม-คืนหนังสือ (Streamlit + SQLite)")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (ปรับโครงสร้างแบบ MVC เชิงแนวคิด)")

user = st.session_state.get("user")

st.sidebar.markdown("### 👤 ข้อมูลผู้ใช้")
st.sidebar.write("ชื่อ:", user.get("full_name"))
st.sidebar.write("รหัส:", user.get("student_id"))
st.sidebar.write("หมู่เรียน:", user.get("class_group"))

# ✅ เพิ่มเติม: แสดงผู้ใช้ + ปุ่ม Logout 
user = st.session_state.get("user") or {} 
st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{user.get('role','-')}**") 

if st.sidebar.button("🚪 Logout", use_container_width=True): 
    st.session_state["is_logged_in"] = False 
    st.session_state["user"] = None 
    st.session_state["page"] = "books" 
    st.rerun() 

# menu = st.sidebar.radio("เมนู", ["📚 หนังสือ", "👤 สมาชิก", "🔄 ยืม-คืน"])
# if menu == "📚 หนังสือ":
#     book_page.render_book()
# elif menu == "👤 สมาชิก":
#     member_page.render_member()
# else:
#     borrow_page.render_borrow()


# ---------- เมนูแบบคลิกแถบ ----------
if "page" not in st.session_state:
    st.session_state.page = "books"


# --- เมนู ---
# ===== Sidebar Menu Title (Centered & Styled) =====
st.sidebar.markdown("""
<style>
.menu-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>


<div class="menu-title">
    เมนู
</div>
""", unsafe_allow_html=True)


# ฟังก์ชันสำหรับสร้างปุ่มเมนูใน Sidebar
# ใช้ควบคุมการเปลี่ยนหน้าโดยอาศัย session_state
def nav_button(label, key, icon=""):
    # ตรวจสอบว่าหน้าปัจจุบัน (page) ตรงกับปุ่มนี้หรือไม่
    # ถ้าตรง active จะเป็น True
    active = (st.session_state.page == key)


    # สร้างปุ่มใน Sidebar
    # - label คือข้อความที่แสดงบนปุ่ม
    # - icon คือสัญลักษณ์ (emoji) ที่แสดงหน้าข้อความ
    # - use_container_width=True ทำให้ปุ่มกว้างเต็ม Sidebar
    # - key ใช้ระบุเอกลักษณ์ของปุ่ม (จำเป็นเมื่อมีหลายปุ่ม)
    btn = st.sidebar.button(
        f"{icon} {label}",
        use_container_width=True,
        key=f"btn_{key}"
    )


    # หากผู้ใช้คลิกปุ่มนี้
    if btn:
        # กำหนดค่าหน้าปัจจุบัน (page) ให้ตรงกับปุ่มที่กด
        st.session_state.page = key


        # สั่งให้ Streamlit โหลดหน้าใหม่
        # เพื่อให้แสดงผลตามหน้าที่เปลี่ยน
        st.rerun()

# ✅ แก้ไขใหม่: Role-based menu (มี 2 role คือ admin, staff) 
role = user.get("role", "admin") 

# ✅ แก้ไขใหม่: staff ทำได้ทุกอย่าง “ยกเว้นจัดการ user” 
# ดังนั้นเมนูหลักต้องเหมือนกันทั้ง admin และ staff 

    # ทำไฮไลต์แบบง่าย (ตัวหนา/ตัวชี้)
    # if active:
    #     st.sidebar.markdown(f"✅ **{label}**")


# เรียกใช้ฟังก์ชัน nav_button เพื่อสร้างเมนูแต่ละรายการ
# ปุ่มเหล่านี้ทำหน้าที่เป็นเมนูหลักของระบบ
nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")
nav_button("รายงาน", "reports", "📊") 

# ✅ เพิ่มเติม: เมนูจัดการผู้ใช้ เฉพาะ admin เท่านั้น 
if role == "admin": 
    nav_button("จัดการผู้ใช้", "admin", "🛠️") 

# ---------- Routing ----------
# ✅ แก้ไขใหม่: ป้องกัน staff เข้าหน้า admin ด้วยการบังคับ routing 
# ✅ แก้ไขใหม่: เอาการบังคับ staff ไปหน้า borrows ออก (เพราะ staff ทำได้ทุกอย่างแล้ว) 
if st.session_state.page == "books":
    book_page.render_book()

elif st.session_state.page == "members":
    member_page.render_member()

elif st.session_state.page == "borrows": 
    borrow_page.render_borrow()

elif st.session_state.page == "admin": 
    # ✅ เพิ่มเติม: guard กัน staff เข้าหน้า admin แม้พยายามเปลี่ยน state เอง 
    if role != "admin": 
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น") 
    else: 
        admin_page.render_admin() 

elif st.session_state.page == "reports":
    report_page.render_report()

else: 
    # fallback 
    book_page.render_book() 

