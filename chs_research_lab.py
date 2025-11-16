# chs_research_lab.py
# Centauri Health Solutions – Strategy & Research Lab (visual, with sample data)

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# --- Branding & config ---
PRIMARY_GREEN = "#78BE20"
DARK_GREY = "#2E2E2E"
LIGHT_GREY = "#F7F8F9"

st.set_page_config(
    page_title="Centauri Health Solutions – Strategy & Research Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Header (no logo, branded) ---
st.markdown(
    f"""
    <div style="margin-bottom:20px; padding:10px 15px; border-radius:8px;
                background-color:{LIGHT_GREY}; border-left:6px solid {PRIMARY_GREEN};">
        <h1 style="color:{DARK_GREY}; margin:0; font-size:26px;">
            Centauri Health Solutions – Strategy & Research Lab
        </h1>
        <p style="color:{DARK_GREY}; margin:4px 0 0; font-size:14px;">
            Market research, platform strategy, and validation cockpit
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Core sample data & helpers ---

DEFAULT_SEGMENTS = [
    {
        "Segment": "Wellness & Fitness App Developers",
        "Short Name": "Fitness Apps",
        "TAM_2024_USD_B": 3.8,
        "Adoption_Speed_1_5": 4,
        "Compliance_Burden_1_5": 2,
        "CHS_Fit_1_5": 4,
    },
    {
        "Segment": "AI Health Coaching Startups",
        "Short Name": "AI Health Coaches",
        "TAM_2024_USD_B": 11.0,
        "Adoption_Speed_1_5": 5,
        "Compliance_Burden_1_5": 3,
        "CHS_Fit_1_5": 5,
    },
    {
        "Segment": "Chronic Condition Management Apps",
        "Short Name": "Chronic Apps",
        "TAM_2024_USD_B": 1.6,
        "Adoption_Speed_1_5": 3,
        "Compliance_Burden_1_5": 5,
        "CHS_Fit_1_5": 5,
    },
    {
        "Segment": "Wearable Data Aggregators & API Platforms",
        "Short Name": "Aggregators",
        "TAM_2024_USD_B": 0.212,
        "Adoption_Speed_1_5": 3,
        "Compliance_Burden_1_5": 5,
        "CHS_Fit_1_5": 4,
    },
    {
        "Segment": "Digital Therapeutics & Rx Wellness Startups",
        "Short Name": "DTx",
        "TAM_2024_USD_B": 7.8,
        "Adoption_Speed_1_5": 2,
        "Compliance_Burden_1_5": 5,
        "CHS_Fit_1_5": 4,
    },
    {
        "Segment": "Consumer Wearable Hardware Startups",
        "Short Name": "Hardware",
        "TAM_2024_USD_B": 22.0,
        "Adoption_Speed_1_5": 3,
        "Compliance_Burden_1_5": 3,
        "CHS_Fit_1_5": 3,
    },
]

# Platform architecture sample
ARCH_DATA = [
    ["Experience", "Developer Console", "Project config, API keys, dashboards", "Planned"],
    ["Experience", "Compliance Dashboard", "BAA center, audit logs, cert view", "Planned"],
    ["Platform", "Explainability Service", "Model cards, decision logs, feature importance", "Planned"],
    ["Platform", "Model Hosting", "Healthcare-tuned models (stress, risk, etc.)", "Future"],
    ["Data", "Unified Wearable APIs", "Apple/Google/Fitbit/Oura connectors", "MVP"],
    ["Data", "Consent & Audit Layer", "PHI tagging, event logs, consent artifacts", "MVP"],
    ["Infra", "Security & Residency", "KMS, region routing, retention policies", "MVP"],
]

# Roadmap sample
ROADMAP_DATA = [
    ["MVP", "Q1", "Data & Compliance", "Unified wearable APIs + audit logging"],
    ["MVP", "Q1", "Experience", "Developer console + basic dashboard"],
    ["V1", "Q2", "AI & Explainability", "Stress model + explainability views"],
    ["V1", "Q2", "Partnerships", "AI health-coach design partners (5–8)"],
    ["V2", "Q3", "Enterprise", "SOC 2, SSO/SCIM, DTx pilots"],
    ["V2", "Q3", "Ecosystem", "Aggregator integrations (Validic/Terra-style)"],
]

# Pricing sample
PRICING_DATA = [
    ["Sandbox", 0, "1 project, 50k events/month, no BAAs, community support"],
    ["Growth", 499, "Up to 3 projects, 5M events/month, BAAs, email support"],
    ["Enterprise", 2500, "Unlimited projects, 50M+ events, BAAs, SSO, dedicated CSM"],
]

# Funnel sample
FUNNEL_DATA = [
    ["Site Visitors", 5000],
    ["Signup (Dev Accounts)", 800],
    ["Activated (First API Call)", 300],
    ["Pilots (Design Partners)", 40],
    ["Paying Customers", 10],
]

# Competitor sample
COMPETITORS_DATA = [
    ["AWS Health AI", "Hyperscaler", 5, 3, 3],
    ["Google Healthcare API", "Hyperscaler", 5, 3, 3],
    ["Azure Health Data Services", "Hyperscaler", 4, 3, 3],
    ["Niche AI Vendor A", "Niche", 2, 4, 2],
    ["Niche AI Vendor B", "Niche", 2, 3, 3],
    ["CentauriHS", "CHS", 3, 5, 5],
]


def compute_priority_score(row, w_tam=0.3, w_adoption=0.3, w_fit=0.4):
    # Rough TAM -> 1–5 scale
    tam_norm = min(max(row["TAM_2024_USD_B"] / 5.0, 1.0), 5.0)
    return round(
        tam_norm * w_tam
        + row["Adoption_Speed_1_5"] * w_adoption
        + row["CHS_Fit_1_5"] * w_fit,
        2,
    )


def init_state():
    if "segments_df" not in st.session_state:
        df = pd.DataFrame(DEFAULT_SEGMENTS)
        df["Priority_Score"] = df.apply(compute_priority_score, axis=1)
        st.session_state["segments_df"] = df

    if "interviews_df" not in st.session_state:
        st.session_state["interviews_df"] = pd.DataFrame(
            columns=[
                "Segment",
                "Persona",
                "Company Type",
                "Priority_1_5",
                "Key_Question",
                "Status",
            ]
        )

    if "hypotheses_df" not in st.session_state:
        st.session_state["hypotheses_df"] = pd.DataFrame(
            columns=[
                "Segment",
                "Hypothesis",
                "Metric_to_Move",
                "Impact_1_5",
                "Confidence_1_5",
                "Effort_1_5",
                "ICE_Score",
                "Next_Experiment",
            ]
        )


def refresh_priority_scores():
    df = st.session_state["segments_df"].copy()
    for idx, row in df.iterrows():
        df.loc[idx, "Priority_Score"] = compute_priority_score(row)
    st.session_state["segments_df"] = df


init_state()

# --- Sidebar navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select view",
    [
        "Segment Explorer",
        "Prioritization Canvas",
        "Interview Planner",
        "Hypothesis & Experiment Tracker",
        "Platform Architecture Map",
        "Feature Stack by Segment",
        "Roadmap",
        "Pricing Strategy",
        "Developer Adoption Funnel",
        "Competitor Landscape",
    ],
)
st.sidebar.markdown("---")
st.sidebar.caption(f"© {datetime.now().year} Centauri Health Solutions")

segments_df = st.session_state["segments_df"]

# =========================
# 1. Segment Explorer
# =========================
if page == "Segment Explorer":
    st.subheader("Segment Explorer")
    st.caption("Tweak segment assumptions and see how it affects overall priority.")

    editable_df = st.data_editor(
        segments_df,
        column_config={
            "TAM_2024_USD_B": st.column_config.NumberColumn(
                "TAM 2024 ($B)", min_value=0.0
            ),
            "Adoption_Speed_1_5": st.column_config.NumberColumn(
                "Adoption Speed (1–5)", min_value=1, max_value=5
            ),
            "Compliance_Burden_1_5": st.column_config.NumberColumn(
                "Compliance Burden (1–5)", min_value=1, max_value=5
            ),
            "CHS_Fit_1_5": st.column_config.NumberColumn(
                "CHS Fit (1–5)", min_value=1, max_value=5
            ),
        },
        hide_index=True,
        use_container_width=True,
    )

    st.session_state["segments_df"] = editable_df
    refresh_priority_scores()
    seg = st.session_state["segments_df"]

    st.markdown("#### Priority Scores")
    st.dataframe(
        seg[
            [
                "Segment",
                "TAM_2024_USD_B",
                "Adoption_Speed_1_5",
                "CHS_Fit_1_5",
                "Priority_Score",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("#### Visual: Adoption vs Compliance (bubble size = TAM, color = CHS Fit)")
    chart_df = seg.copy()
    chart_df["TAM_scaled"] = chart_df["TAM_2024_USD_B"].clip(lower=0.1)
    scatter = (
        alt.Chart(chart_df)
        .mark_circle()
        .encode(
            x=alt.X("Adoption_Speed_1_5", title="Adoption Speed (1–5)"),
            y=alt.Y("Compliance_Burden_1_5", title="Compliance Burden (1–5)"),
            size=alt.Size("TAM_scaled", title="TAM 2024 ($B)", legend=None),
            color=alt.Color(
                "CHS_Fit_1_5",
                scale=alt.Scale(scheme="greens"),
                title="CHS Fit (1–5)",
            ),
            tooltip=[
                "Segment",
                "TAM_2024_USD_B",
                "Adoption_Speed_1_5",
                "Compliance_Burden_1_5",
                "CHS_Fit_1_5",
            ],
        )
        .properties(height=400)
    )

    st.altair_chart(scatter, use_container_width=True)

# =========================
# 2. Prioritization Canvas
# =========================
elif page == "Prioritization Canvas":
    st.subheader("Prioritization Canvas")
    st.caption("Visual focus: which segments are best for CHS to tackle first?")

    seg = segments_df.copy()

    col1, col2, col3 = st.columns(3)
    with col1:
        w_tam = st.slider("Weight: TAM", 0.0, 1.0, 0.3, 0.05)
    with col2:
        w_adopt = st.slider("Weight: Adoption Speed", 0.0, 1.0, 0.3, 0.05)
    with col3:
        w_fit = st.slider("Weight: CHS Fit", 0.0, 1.0, 0.4, 0.05)

    total = max(w_tam + w_adopt + w_fit, 0.0001)
    w_tam, w_adopt, w_fit = w_tam / total, w_adopt / total, w_fit / total

    seg["Priority_Score"] = seg.apply(
        lambda r: compute_priority_score(r, w_tam, w_adopt, w_fit), axis=1
    )
    ranked = seg.sort_values("Priority_Score", ascending=False)

    st.markdown("#### Ranked Segments")
    st.dataframe(
        ranked[
            [
                "Segment",
                "Short Name",
                "TAM_2024_USD_B",
                "Adoption_Speed_1_5",
                "CHS_Fit_1_5",
                "Priority_Score",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("#### Focus Map (Adoption vs CHS Fit)")
    focus_chart = (
        alt.Chart(ranked)
        .mark_circle()
        .encode(
            x=alt.X("Adoption_Speed_1_5", title="Adoption Speed"),
            y=alt.Y("CHS_Fit_1_5", title="CHS Strategic Fit"),
            size=alt.Size("TAM_2024_USD_B", title="TAM 2024 ($B)", legend=None),
            color=alt.Color(
                "Priority_Score",
                title="Priority Score",
                scale=alt.Scale(scheme="viridis"),
            ),
            tooltip=["Segment", "Priority_Score"],
        )
        .properties(height=400)
    )
    st.altair_chart(focus_chart, use_container_width=True)

# =========================
# 3. Interview Planner
# =========================
elif page == "Interview Planner":
    st.subheader("Interview Planner")
    st.caption("Plan and track discovery interviews across segments & personas.")

    seg_names = segments_df["Segment"].tolist()
    interviews_df = st.session_state["interviews_df"]

    st.markdown("#### Add Interview Plan")
    with st.form("add_interview"):
        col1, col2 = st.columns(2)
        with col1:
            segment = st.selectbox("Segment", seg_names)
            persona = st.text_input("Persona (e.g., Wearables ML Engineer)")
            company_type = st.text_input("Company Type (e.g., Seed AI health coach)")
        with col2:
            priority = st.slider("Priority (1–5)", 1, 5, 3)
            status = st.selectbox(
                "Status", ["Planned", "Invited", "Scheduled", "Completed"]
            )
        key_question = st.text_area(
            "Key Question / Learning Goal",
            "What stops you from adopting a compliance-first AI platform today?",
        )

        submit = st.form_submit_button("Add Interview")
        if submit:
            new_row = {
                "Segment": segment,
                "Persona": persona,
                "Company Type": company_type,
                "Priority_1_5": priority,
                "Key_Question": key_question,
                "Status": status,
            }
            st.session_state["interviews_df"] = pd.concat(
                [interviews_df, pd.DataFrame([new_row])], ignore_index=True
            )
            st.success("Interview added.")

    st.markdown("#### Interview Backlog")
    interviews_df = st.session_state["interviews_df"]
    if interviews_df.empty:
        st.info("No interviews yet. Use the form above to add some.")
    else:
        st.dataframe(interviews_df, use_container_width=True)

        st.markdown("##### Summary by Segment & Status")
        summary = (
            interviews_df.groupby(["Segment", "Status"])["Priority_1_5"]
            .count()
            .reset_index()
            .rename(columns={"Priority_1_5": "# Interviews"})
        )
        st.dataframe(summary, use_container_width=True)

# =========================
# 4. Hypothesis & Experiment Tracker
# =========================
elif page == "Hypothesis & Experiment Tracker":
    st.subheader("Hypothesis & Experiment Tracker")
    st.caption("Capture strategy hypotheses and decide what to test next.")

    seg_names = segments_df["Segment"].tolist()
    hypotheses_df = st.session_state["hypotheses_df"]

    st.markdown("#### Add Hypothesis")
    with st.form("add_hypothesis"):
        col1, col2 = st.columns([1, 2])
        with col1:
            segment = st.selectbox("Segment", seg_names)
            impact = st.slider("Impact (1–5)", 1, 5, 4)
            confidence = st.slider("Confidence (1–5)", 1, 5, 3)
            effort = st.slider("Effort (1–5, higher = harder)", 1, 5, 3)
        with col2:
            hypo = st.text_area(
                "Hypothesis",
                "If we offer built-in HIPAA/SOC2 compliance dashboards, AI health-coach startups will adopt CHS as their main infra.",
            )
            metric = st.text_input(
                "Metric to Move",
                "Number of AI health-coach teams integrating CHS within 3 months",
            )
            experiment = st.text_area(
                "Next Experiment",
                "Run 5 design-partner calls with AI health-coach startups and offer them a pilot sandbox.",
            )

        submit = st.form_submit_button("Add Hypothesis")
        if submit:
            ice = round((impact * confidence) / max(effort, 1), 2)
            new_row = {
                "Segment": segment,
                "Hypothesis": hypo,
                "Metric_to_Move": metric,
                "Impact_1_5": impact,
                "Confidence_1_5": confidence,
                "Effort_1_5": effort,
                "ICE_Score": ice,
                "Next_Experiment": experiment,
            }
            st.session_state["hypotheses_df"] = pd.concat(
                [hypotheses_df, pd.DataFrame([new_row])], ignore_index=True
            )
            st.success("Hypothesis added.")

    st.markdown("#### Hypothesis Backlog (ranked by ICE score)")
    hypotheses_df = st.session_state["hypotheses_df"]
    if hypotheses_df.empty:
        st.info("No hypotheses yet. Add one with the form above.")
    else:
        ranked_h = hypotheses_df.sort_values("ICE_Score", ascending=False)
        st.dataframe(ranked_h, use_container_width=True)

# =========================
# 5. Platform Architecture Map
# =========================
elif page == "Platform Architecture Map":
    st.subheader("Platform Architecture Map (V1)")
    st.caption("Visual view of CHS layers: Data → Platform → Experience.")

    arch_df = pd.DataFrame(
        ARCH_DATA, columns=["Layer", "Component", "Description", "Status"]
    )
    st.markdown("#### Architecture Components")
    st.dataframe(arch_df, use_container_width=True)

    st.markdown("#### Layer Mix")
    layer_counts = arch_df.groupby("Layer")["Component"].count().reset_index()
    layer_chart = (
        alt.Chart(layer_counts)
        .mark_bar()
        .encode(
            x=alt.X("Layer", sort=["Infra", "Data", "Platform", "Experience"]),
            y=alt.Y("Component", title="# Components"),
            color=alt.Color("Layer", legend=None, scale=alt.Scale(scheme="greens")),
            tooltip=["Layer", "Component"],
        )
        .properties(height=300)
    )
    st.altair_chart(layer_chart, use_container_width=True)

    st.markdown("#### Simple Architecture Diagram (conceptual)")
    dot = """
    digraph CHS {
        rankdir=TB;
        node [shape=box, style="rounded,filled", color="#78BE20", fillcolor="#E9F5DB"];

        subgraph cluster_infra {
            label="Infra";
            style="rounded";
            SecurityResidency [label="Security & Residency"];
        }

        subgraph cluster_data {
            label="Data Layer";
            style="rounded";
            UnifiedAPIs [label="Unified Wearable APIs"];
            ConsentAudit [label="Consent & Audit Layer"];
        }

        subgraph cluster_platform {
            label="Platform Services";
            style="rounded";
            Explainability [label="Explainability Service"];
            ModelHosting [label="Model Hosting"];
        }

        subgraph cluster_experience {
            label="Developer Experience";
            style="rounded";
            DevConsole [label="Developer Console"];
            ComplianceDash [label="Compliance Dashboard"];
        }

        SecurityResidency -> UnifiedAPIs -> ConsentAudit -> Explainability -> ModelHosting -> DevConsole -> ComplianceDash;
    }
    """
    st.graphviz_chart(dot)

# =========================
# 6. Feature Stack by Segment
# =========================
elif page == "Feature Stack by Segment":
    st.subheader("Feature Stack by Segment")
    st.caption("Which features matter most for which developer segment?")

    features = [
        "Unified Wearable APIs",
        "Consent & Audit Trails",
        "Explainability Dashboards",
        "HIPAA/SOC2 Compliance Pack",
        "Data Residency Controls",
        "DTx / FDA Support",
    ]
    seg_names = [s["Short Name"] for s in DEFAULT_SEGMENTS]
    # Simple 1–5 importance matrix (sample)
    importance_matrix = pd.DataFrame(
        [
            [5, 3, 3, 2, 2, 1],  # Fitness Apps
            [4, 4, 5, 4, 3, 2],  # AI Health Coaches
            [4, 5, 4, 5, 4, 3],  # Chronic Apps
            [3, 5, 4, 4, 4, 2],  # Aggregators
            [3, 5, 5, 5, 4, 5],  # DTx
            [5, 3, 2, 2, 2, 1],  # Hardware
        ],
        columns=features,
        index=seg_names,
    ).reset_index(names="Segment")

    st.markdown("#### Importance Heatmap (1–5)")
    st.dataframe(importance_matrix, use_container_width=True)

    # Melt for heatmap
    melt_df = importance_matrix.melt(
        id_vars=["Segment"], var_name="Feature", value_name="Importance"
    )
    heatmap = (
        alt.Chart(melt_df)
        .mark_rect()
        .encode(
            x=alt.X("Feature:N", sort=features),
            y=alt.Y("Segment:N", sort=seg_names),
            color=alt.Color(
                "Importance:Q",
                scale=alt.Scale(scheme="greens", domain=[1, 5]),
                title="Importance",
            ),
            tooltip=["Segment", "Feature", "Importance"],
        )
        .properties(height=250)
    )
    st.altair_chart(heatmap, use_container_width=True)

# =========================
# 7. Roadmap
# =========================
elif page == "Roadmap":
    st.subheader("Roadmap (MVP → V1 → V2)")
    st.caption("Timeline view of CHS platform evolution.")

    roadmap_df = pd.DataFrame(
        ROADMAP_DATA, columns=["Phase", "Quarter", "Area", "Item"]
    )
    st.markdown("#### Roadmap Items")
    st.dataframe(roadmap_df, use_container_width=True)

    # Map quarter to numeric for a simple Gantt-ish chart
    quarter_order = ["Q1", "Q2", "Q3", "Q4"]
    roadmap_df["QuarterIdx"] = roadmap_df["Quarter"].apply(
        lambda q: quarter_order.index(q) + 1 if q in quarter_order else 1
    )

    gantt = (
        alt.Chart(roadmap_df)
        .mark_bar()
        .encode(
            x=alt.X("QuarterIdx:Q", title="Quarter", scale=alt.Scale(domain=[1, 4])),
            y=alt.Y("Item:N", title="Feature / Initiative"),
            color=alt.Color("Phase:N", scale=alt.Scale(scheme="set2")),
            tooltip=["Phase", "Quarter", "Area", "Item"],
        )
        .properties(height=350)
    )

    # Custom x-axis labels
    text_labels = alt.Chart(
        pd.DataFrame({"QuarterIdx": [1, 2, 3, 4], "QuarterLabel": ["Q1", "Q2", "Q3", "Q4"]})
    ).mark_text(
        dy=20  # offset
    ).encode(
        x="QuarterIdx:Q",
        text="QuarterLabel:N"
    )

    st.altair_chart(gantt + text_labels, use_container_width=True)

# =========================
# 8. Pricing Strategy
# =========================
elif page == "Pricing Strategy":
    st.subheader("Pricing Strategy")
    st.caption("Sample tiers for Sandbox, Growth, and Enterprise customers.")

    pricing_df = pd.DataFrame(
        PRICING_DATA, columns=["Tier", "Price_USD_per_month", "Includes"]
    )

    cols = st.columns(3)
    for col, (_, row) in zip(cols, pricing_df.iterrows()):
        with col:
            st.markdown(
                f"""
                <div style="border-radius:10px; border:1px solid #ddd; padding:15px; background-color:white;">
                    <h3 style="margin:0; color:{DARK_GREY};">{row['Tier']}</h3>
                    <p style="font-size:24px; margin:4px 0; color:{PRIMARY_GREEN};">
                        ${row['Price_USD_per_month']}/mo
                    </p>
                    <p style="font-size:13px; color:{DARK_GREY};">{row['Includes']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Price Comparison")
    st.dataframe(pricing_df, use_container_width=True)

    price_chart = (
        alt.Chart(pricing_df)
        .mark_bar()
        .encode(
            x=alt.X("Tier:N"),
            y=alt.Y("Price_USD_per_month:Q", title="Price ($/month)"),
            color=alt.Color("Tier:N", legend=None, scale=alt.Scale(scheme="greens")),
            tooltip=["Tier", "Price_USD_per_month"],
        )
        .properties(height=300)
    )
    st.altair_chart(price_chart, use_container_width=True)

# =========================
# 9. Developer Adoption Funnel
# =========================
elif page == "Developer Adoption Funnel":
    st.subheader("Developer Adoption Funnel")
    st.caption("Sample funnel from awareness → signup → activation → pilots → paid.")

    funnel_df = pd.DataFrame(FUNNEL_DATA, columns=["Stage", "Count"])

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("#### Funnel Stages (Editable)")
        editable_funnel = st.data_editor(
            funnel_df,
            column_config={
                "Stage": st.column_config.TextColumn("Stage"),
                "Count": st.column_config.NumberColumn("Count", min_value=0),
            },
            hide_index=True,
            use_container_width=True,
        )
    with col2:
        st.markdown("#### Conversion Rates")
        # compute conversion percentages
        ef = editable_funnel.copy()
        ef["PrevCount"] = ef["Count"].shift(1)
        ef["Conversion_from_prev_%"] = (
            ef["Count"] / ef["PrevCount"] * 100
        ).replace([np.inf, -np.inf], np.nan).round(1)
        st.dataframe(
            ef[["Stage", "Count", "Conversion_from_prev_%"]],
            use_container_width=True,
        )

    st.markdown("#### Funnel Chart")
    funnel_chart = (
        alt.Chart(editable_funnel)
        .mark_bar()
        .encode(
            x=alt.X("Stage:N"),
            y=alt.Y("Count:Q"),
            color=alt.Color(
                "Stage:N",
                legend=None,
                scale=alt.Scale(scheme="greens"),
            ),
            tooltip=["Stage", "Count"],
        )
        .properties(height=300)
    )
    st.altair_chart(funnel_chart, use_container_width=True)

# =========================
# 10. Competitor Landscape
# =========================
elif page == "Competitor Landscape":
    st.subheader("Competitor Landscape")
    st.caption("Position CHS vs hyperscalers and niche AI vendors.")

    comp_df = pd.DataFrame(
        COMPETITORS_DATA,
        columns=[
            "Vendor",
            "Type",
            "Breadth_1_5",
            "Compliance_1_5",
            "Explainability_1_5",
        ],
    )

    st.markdown("#### Competitive Metrics")
    st.dataframe(comp_df, use_container_width=True)

    st.markdown("#### Visual: Breadth vs Explainability")
    comp_chart = (
        alt.Chart(comp_df)
        .mark_circle(size=200)
        .encode(
            x=alt.X("Breadth_1_5:Q", title="Platform Breadth"),
            y=alt.Y("Explainability_1_5:Q", title="Explainability Depth"),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(scheme="set2"),
                title="Vendor Type",
            ),
            tooltip=["Vendor", "Type", "Breadth_1_5", "Compliance_1_5", "Explainability_1_5"],
        )
        .properties(height=350)
    )
    st.altair_chart(comp_chart, use_container_width=True)

    st.markdown("#### Visual: Compliance vs Explainability (where CHS should win)")
    comp_chart2 = (
        alt.Chart(comp_df)
        .mark_circle(size=200)
        .encode(
            x=alt.X("Compliance_1_5:Q", title="Compliance Strength"),
            y=alt.Y("Explainability_1_5:Q", title="Explainability Depth"),
            color=alt.Color("Vendor:N", legend=None),
            tooltip=["Vendor", "Compliance_1_5", "Explainability_1_5"],
        )
        .properties(height=350)
    )
    st.altair_chart(comp_chart2, use_container_width=True)

# --- Footer ---
st.markdown(
    f"""
    <hr/>
    <div style="color:{DARK_GREY}; font-size:11px; margin-top:4px;">
        Prototype only – data not persisted between runs. Use as an internal tool for CHS strategy & validation.
    </div>
    """,
    unsafe_allow_html=True,
)
