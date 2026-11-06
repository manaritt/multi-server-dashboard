import streamlit as st
import time
import pandas as pd
import plotly.express as px
from agent import generate_server_metrics, trigger_auto_healing

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Multi-Server Infrastructure Dashboard",
    page_icon="🖥️",
    layout="wide"
)

st.title("🖥️ Enterprise Multi-Server Monitoring Dashboard")
st.markdown("نظام مراقبة تجميعي لعدة خوادم مع خاصية التحديث التلقائي والتعافي الذاتي.")

# 2. القائمة الجانبية - التحكم بالزمن وإصلاح الأعطال
st.sidebar.header("⚙️ إعدادات النظام")

# أداة السحب للتحكم بزمن التحديث بالثواني
refresh_rate = st.sidebar.slider(
    "⏱️ معدل تحديث البيانات (بالثواني):",
    min_value=2,
    max_value=30,
    value=5,
    step=1
)

st.sidebar.markdown("---")
st.sidebar.header("🛠️ إجراءات التعافي الذاتي (Auto-Healing)")
selected_server = st.sidebar.selectbox("اختر السيرفر للإصلاح:", ["Server-01", "Server-02", "Server-03", "Server-04"])

if st.sidebar.button("🧹 تفريغ الذاكرة (Clear Cache)"):
    result = trigger_auto_healing(selected_server, "clear_cache")
    st.sidebar.success(result)

if st.sidebar.button("🔄 إعادة تشغيل السيرفر (Restart)"):
    result = trigger_auto_healing(selected_server, "restart")
    st.sidebar.warning(result)

# 3. جلب بيانات السيرفرات الأربعة من المحاكي agent.py
servers_data = generate_server_metrics()

# 4. ملخص مؤشرات الأداء العليا (Top-level Metrics)
col1, col2, col3, col4 = st.columns(4)
avg_cpu = sum(s['cpu'] for s in servers_data) / len(servers_data)
avg_ram = sum(s['ram'] for s in servers_data) / len(servers_data)
unhealthy_count = sum(1 for s in servers_data if s['status'] != 'Healthy')

col1.metric("إجمالي السيرفرات", f"{len(servers_data)} Nodes")
col2.metric("متوسط الـ CPU", f"{avg_cpu:.1f}%")
col3.metric("متوسط الـ RAM", f"{avg_ram:.1f}%")
col4.metric("السيرفرات الحرجة", f"{unhealthy_count} Alert", delta_color="inverse")

st.markdown("---")

# 5. عرض كروت السيرفرات التفصيلية
st.subheader("📊 حالة الخوادم الحالية")
cols = st.columns(4)

for idx, server in enumerate(servers_data):
    with cols[idx]:
        st.markdown(f"### {server['name']}")
        st.caption(f"الوظيفة: {server['role']}")
        
        # لون الحالة
        if server['status'] == 'Healthy':
            st.success(f"الحالة: {server['status']}")
        elif server['status'] == 'Warning':
            st.warning(f"الحالة: {server['status']}")
        else:
            st.error(f"الحالة: {server['status']}")
            
        st.write(f"CPU استهلاك: {server['cpu']:.1f}%")
        st.progress(int(server['cpu']))
        
        st.write(f"RAM استهلاك: {server['ram']:.1f}%")
        st.progress(int(server['ram']))
        
        st.write(f"سرعة الاستجابة: {server['response_time']:.1f} ms")

st.markdown("---")

# 6. الرسم البياني للمقارنة اللحظية
st.subheader("📈 مقارنة أداء السيرفرات")
df = pd.DataFrame(servers_data)
fig = px.bar(
    df,
    x='name',
    y=['cpu', 'ram'],
    barmode='group',
    title="نسب الاستهلاك الحية (CPU vs RAM)",
    labels={'value': 'النسبة المئوية %', 'name': 'السيرفر', 'variable': 'المورد'}
)
st.plotly_chart(fig, use_container_width=True)

# 7. التحديث التلقائي بناءً على الثواني المحددة في الـ Slider
time.sleep(refresh_rate)
st.rerun()
