from pyvis.network import Network
import webbrowser
import os

net = Network(
    height="900px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="black"
)

# -----------------------------
# Physics Settings
# -----------------------------

net.barnes_hut(
    gravity=-8000,
    central_gravity=0.2,
    spring_length=240,
    spring_strength=0.02
)

# -----------------------------
# Node Categories
# -----------------------------

node_types = {

    "ADHD":"root",
    "Diagnosis Status":"outcome",

    "Symptom Severity":"mediator",
    "Functional Impairment":"mediator",
    "Teacher Referral Rate":"mediator",

    "Socioeconomic Status":"confounder",
    "Gender":"confounder",

    "Cultural Norms":"latent"
}

colors = {
    "root":"#1f77b4",
    "outcome":"#ff7f0e",
    "mediator":"#2ca02c",
    "confounder":"#9467bd",
    "latent":"#ffd92f",
    "factor":"#dddddd"
}

# -----------------------------
# All Nodes
# -----------------------------

nodes = [

"ADHD","Diagnosis Status","Age","Gender","Genetic Risk",
"Symptom Severity","Symptom Type","Comorbid Conditions",

"Parental Awareness","Parenting Style","Family Stress",
"Household Stability","Teacher Referral Rate","Classroom Size",

"Academic Demands","School Resources","Workplace Accommodations",

"Access to Mental Health Care","Provider Availability",
"Diagnostic Criteria Variability","Waiting Time for Assessment",
"Cost of Evaluation","Stigma","Gender Bias","Cultural Norms",
"Socioeconomic Status","Age at Diagnosis","Misdiagnosis Rate",
"Functional Impairment","Quality of Life"
]

for node in nodes:

    ntype = node_types.get(node,"factor")

    net.add_node(
        node,
        label=node,
        color=colors[ntype],
        size=35 if ntype in ["root","outcome"] else 22,
        title=f"Node Type: {ntype}"
    )

# -----------------------------
# Edges With Weights
# -----------------------------

edges = [

("Genetic Risk","ADHD","+",0.85),

("ADHD","Symptom Severity","+",0.9),
("ADHD","Symptom Type","+",0.65),
("ADHD","Comorbid Conditions","+",0.6),
("ADHD","Functional Impairment","+",0.9),
("ADHD","Quality of Life","-",0.75),
("ADHD","Misdiagnosis Rate","-",0.4),

("Age","Diagnosis Status","+",0.35),
("Gender","Diagnosis Status","+",0.3),

("Symptom Severity","Diagnosis Status","+",0.9),
("Symptom Type","Teacher Referral Rate","+",0.65),
("Teacher Referral Rate","Diagnosis Status","+",0.8),

("Parental Awareness","Diagnosis Status","+",0.65),
("Parenting Style","Symptom Severity","-",0.3),
("Family Stress","Symptom Severity","+",0.55),
("Household Stability","Family Stress","-",0.6),

("Classroom Size","Teacher Referral Rate","+",0.5),
("Academic Demands","Functional Impairment","+",0.55),

("Access to Mental Health Care","Diagnosis Status","+",0.9),
("Provider Availability","Diagnosis Status","+",0.8),
("Waiting Time for Assessment","Diagnosis Status","-",0.6),
("Cost of Evaluation","Diagnosis Status","-",0.55),

("Stigma","Diagnosis Status","-",0.65),
("Socioeconomic Status","Access to Mental Health Care","+",0.75),

("Functional Impairment","Quality of Life","-",0.9),
("Diagnosis Status","Quality of Life","+",0.75)

]
for u, v, sign, power in edges:

    color = "green" if sign == "+" else "red"

    net.add_edge(
        u,
        v,
        color=color,
        width=power * 8,          # thickness reflects power
        value=power,
        arrows="to",
        title=f"""
        Causal Relationship

        Direction: {u} → {v}
        Effect: {"Positive" if sign=="+" else "Negative"}
        Causal Power: {power:.2f}
        """
    )
# -----------------------------
# Enable Node Interaction
# -----------------------------

net.set_options("""
{
  "interaction": {
    "dragNodes": true,
    "dragView": true,
    "zoomView": true
  },
  "physics": {
    "enabled": true
  }
}
""")

# -----------------------------
# Legend
# -----------------------------

net.add_node(
"Legend",
label="""
Legend

Green Edge (+) : Positive Effect
Red Edge (-)   : Negative Effect

Blue Node      : Root Cause
Orange Node    : Outcome
Green Node     : Mediator
Purple Node    : Confounder
Yellow Node    : Latent Factor
""",
shape="box",
physics=False,
color="#f5f5f5"
)

# -----------------------------
# Save Graph
# -----------------------------

filename = "adhd_causal_network_meeting_ready.html"

net.write_html(filename)

print("Graph saved:",filename)

webbrowser.open("file://" + os.path.realpath(filename))