import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from datetime import datetime

st.set_page_config(
    page_title="Enterprise Multi-Server Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🖥️ نظام مراقبة خوادم الشركة (Multi-Server Cloud Monitor)")
st.markdown("لوحة قيادة مركزية لمراقبة الأداء والاستجابة لعدة سيرفرات في وقت واحد")


# محاكاة شبكة سيرفرات الشركة
@st.cache_data(ttl=5)
def load_company_servers():
    servers = [
        {"name": "App-Server-01", "role": "Application Node"},
        {"name": "DB-Server-Primary", "role": "Database Main"},
        {"name": "Web-Proxy-01", "role": "Load Balancer"},
        {"name": "Backup-Node-02", "role": "Storage & Backup"}
    ]

    data = []
    np.random.seed(int(time.time()))

    for s in servers:
        cpu = round(np.random.uniform(20, 95), 1)
        ram = round(np.random.uniform(35, 90), 1)
        disk = round(np.random.uniform(45, 80), 1)
        latency = round(np.random.uniform(2, 40), 1)
        status = "Critical" if cpu > 85 else ("Warning" if cpu > 70 else "Healthy")

        data.append({
            "اسم السيرفر": s["name"],
            "الوظيفة": s["role"],
            "الحالة": status,
            "استهلاك CPU (%)": cpu,
            "استهلاك RAM (%)": ram,
            "استهلاك التخزين (%)": disk,
            "زمن الاستجابة (ms)": latency,
            "آخر تحديث": datetime.now().strftime("%H:%M:%S")
        })
    return pd.DataFrame(data)


df = load_company_servers()

# الشريط الجانبي للفلترة
st.sidebar.header("⚙️ لوحة التصفية")
selected_server = st.sidebar.selectbox("اختر السيرفر للمعاينة:", ["جميع السيرفرات"] + list(df["اسم السيرفر"]))

if st.sidebar.button("🔄 تحديث البيانات"):
    st.cache_data.clear()
    st.rerun()

# الإحصائيات العامة
total_nodes = len(df)
healthy_nodes = len(df[df["الحالة"] == "Healthy"])
critical_nodes = len(df[df["الحالة"] == "Critical"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي السيرفرات", total_nodes)
c2.metric("السيرفرات السليمة", f"{healthy_nodes} / {total_nodes}")
c3.metric("سيرفرات تحت الضغط", critical_nodes, delta_color="inverse")
c4.metric("متوسط استهلاك الشبكة CPU", f"{df['استهلاك CPU (%)'].mean():.1f}%")

st.divider()

if selected_server == "جميع السيرفرات":
    st.subheader("📊 عرض المقارنة الجماعي لسيرفرات الشركة")
    st.dataframe(df, use_container_width=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_cpu = px.bar(df, x="اسم السيرفر", y="استهلاك CPU (%)", color="الحالة",
                         title="مقارنة ضغط المعالج (CPU) لكل سيرفر",
                         color_discrete_map={"Healthy": "green", "Warning": "orange", "Critical": "red"})
        st.plotly_chart(fig_cpu, use_container_width=True)

    with col_g2:
        fig_ram = px.bar(df, x="اسم السيرفر", y="استهلاك RAM (%)", color="اسم السيرفر",
                         title="مقارنة الذاكرة (RAM)")
        st.plotly_chart(fig_ram, use_container_width=True)
else:
    st.subheader(f"🔍 تفاصيل السيرفر: {selected_server}")
    s_data = df[df["اسم السيرفر"] == selected_server].iloc[0]

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("الوظيفة", s_data["الوظيفة"])
    sc2.metric("الحالة الحالية", s_data["الحالة"])
    sc3.metric("استهلاك CPU", f"{s_data['استهلاك CPU (%)']}%")
    sc4.metric("سرعة الاستجابة", f"{s_data['زمن الاستجابة (ms)']} ms")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=s_data['استهلاك CPU (%)'],
        title={'text': f"مؤشر الضغط الحالي لـ {selected_server}"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "red" if s_data['استهلاك CPU (%)'] > 80 else "green"},
            'threshold': {'line': {'color': "black", 'width': 4}, 'value': 85}
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# زر التقرير
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 تنزيل تقرير السيرفرات (CSV)", csv, "servers_status.csv", "text/csv")