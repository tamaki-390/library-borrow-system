import streamlit as st
import controller

def render_login():

    # 🔹 แสดงข้อมูลก่อน Login
    st.markdown("## 📚 ระบบยืม-คืนหนังสือ")
    st.markdown("### 👨‍🎓 ข้อมูลผู้จัดทำ")
    st.write("ชื่อ: ชินณชร พงษ์เพชร")
    st.write("รหัสนักศึกษา: 6501234567")
    st.write("หมู่เรียน: IT-01")

    st.divider()

    # 🔐 ฟอร์ม Login
    st.title("🔐 เข้าสู่ระบบ")

    with st.form("login_form"):
        username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น admin")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="เช่น 1234")
        submitted = st.form_submit_button("Login")

    if submitted:
        ok, msgs, user_info = controller.login(username, password)
        if not ok:
            for m in msgs:
                st.error(m)
        else:
            for m in msgs:
                st.success(m)

            st.session_state["is_logged_in"] = True
            st.session_state["user"] = user_info
            st.session_state["page"] = "books"
            st.rerun()
