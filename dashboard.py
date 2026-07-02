import streamlit as st
import requests
import pandas as pd

# App Configuration
st.set_page_config(page_title="Supply Chain Disruption Dashboard", layout="wide")
st.title("📦 Supply Chain Disruption Monitoring Agent")
st.markdown("Analyze supplier bottlenecks, blast radiuses, and discover alternative sourcing recommendations live.")

BASE_URL = "http://127.0.0.1:8000"

# Fetch Supplier List from API
try:
    suppliers_res = requests.get(f"{BASE_URL}/suppliers").json()
    supplier_list = suppliers_res.get("suppliers", [])
except Exception:
    st.error("❌ Could not connect to FastAPI server. Make sure your backend server is running on port 8000!")
    st.stop()

# Layout Columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 Disruption Analyzer")
    
    # 1. Select Supplier
    selected_supplier = st.selectbox("Select Affected Supplier:", supplier_list)
    
    # 2. Select Disruption Reason
    issue_type = st.selectbox("Select Disruption Reason:", [
        "Port Strike / Logistics Halt",
        "Extreme Weather Event",
        "Geopolitical Dispute",
        "Factory Fire / Infrastructure Damage",
        "Financial Insolvency"
    ])
    
    analyze_btn = st.button("Run Disruption Analysis", type="primary")

with col2:
    if analyze_btn:
        st.subheader(f"📊 Impact Analysis for {selected_supplier}")
        st.info(f"🚨 Reason: {issue_type}")
        
        # Fetch Blast Radius
        blast_res = requests.get(f"{BASE_URL}/blast-radius/{selected_supplier}").json()
        affected_count = blast_res.get("count", 0)
        affected_list = blast_res.get("affected_suppliers", [])
        
        # Fetch Backup Recommendations
        backup_res = requests.get(f"{BASE_URL}/backup-suppliers/{selected_supplier}").json()
        backups = backup_res.get("backup_recommendations", [])
        
        # Display Metrics
        m1, m2 = st.columns(2)
        m1.metric("Direct Blast Radius Tiers", f"{affected_count} Vendors")
        m2.metric("Alternative Options Found", f"{len(backups)} Suppliers")
        
        # Display Affected Network Nodes
        with st.expander("⚠️ View Impacted Secondary Tiers"):
            if affected_list:
                st.write(affected_list)
            else:
                st.write("No secondary tiers directly disrupted.")
                
        # Display Alternative Solutions Table
        st.subheader("💡 Recommended Alternative Solutions")
        if backups:
            # Check if backups list is objects or strings, convert to DataFrame cleanly
            if isinstance(backups, list) and len(backups) > 0 and isinstance(backups[0], dict):
                df_backups = pd.DataFrame(backups)
            else:
                df_backups = pd.DataFrame({"Recommended Alternative Supplier ID": backups})
            st.dataframe(df_backups, use_container_width=True)
        else:
            st.warning("No pre-vetted fallback suppliers found in database for this tier tier sequence.")
    else:
        st.write("⬅️ Select a supplier and click 'Run Disruption Analysis' to calculate alternative sourcing solutions.")
