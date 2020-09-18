import plotly.graph_objects as go

lst = ['GGAAACCGAAUCGGAGACUACUAUAGUUGAGUAAUCGUCGACUUUAUGCGAUCGUAUUACUGCUACGA' , 'GGAAAAGCUCUAAUAACAGGAGACUAGGACUACGUAUUUCUAGGUAACUGGAAUAACCCAUACCAGCA']
lst2 = []
fig = go.Figure()
for item in lst:
    lst2 = list(item)
    y = [
            lst2.count('A'),
            lst2.count('C'),
            lst2.count('G'),
            lst2.count('U'),
        ]
    fig.add_trace(go.Bar(
        x = ['A', 'C', 'G', 'U'],
        y = y, 
        name = item
    ))

fig.update_layout(
    title = 'Base Count',
    barmode = 'group',
    bargap = 0.1
)


fig.show()
