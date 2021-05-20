import requests
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

#############       IMPORT DATA     ##############

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
req = requests.get(url)
json = req.json()

###### END ##########

##########      HELPFUL FUNCTIONS       #############

def altair_plot(df, X, Y, tit, col):
    fig = (
        alt.Chart(
            df.reset_index(),
            title=tit,
        )
        .mark_bar()
        .encode(
            x=alt.X(X['col'], title=X['title']),
            y=alt.Y(Y['col'],  title=Y['title']),
        ).configure_mark(
        color=col,
        )
        .interactive()
    )
    return fig

##########      END     ################

################        VISUALIZATION      ##################

st.write('''# FPL Visualization''')

elements = pd.DataFrame(json['elements'])
elements_types = pd.DataFrame(json['element_types'])
teams = pd.DataFrame(json['teams'])


Trim_elements = elements[['second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']]

Trim_elements['position'] = Trim_elements['element_type'].map(elements_types.set_index('id').singular_name)

Trim_elements['team'] = Trim_elements['team'].map(teams.set_index('id').name)



Trim_elements['value'] = Trim_elements.value_season.astype(float)

# st.write('''### Sorting by Value''')

# st.write(Trim_elements.sort_values('value',ascending=False).head(10))

##################      AVERAGE VALUES BY POSITION      #################

Trim_elements.sort_values('total_points',ascending=False).head(10)

Trim_elements = Trim_elements.loc[Trim_elements.value > 0]

pivot = Trim_elements.pivot_table(index='position',values='value',aggfunc=np.mean)

st.write('''## Value by Position''')

X = {"col" : "position", "title": "Positions"}
Y = {"col" : "value", "title": "Value"}

fig = altair_plot(pivot, X, Y, "Positionwise Distribution", '#f5bc42')

st.altair_chart(fig, use_container_width=True)

##################      END     ############################

##############################       Altair Chart For VALUES OF TEAMS       #####################

st.write('''## Best Team in FPL''')

best_team = Trim_elements.pivot_table(index='team', values='value', aggfunc=np.mean)

X = {"col" : "team", "title": "Teams"}
Y = {"col" : "value", "title": "Value"}

fig = altair_plot(best_team, X, Y, "Teamwise Distribution", '#FF4B4B')

# st.bar_chart(best_team.sort_values('value', ascending=False))
st.altair_chart(fig, use_container_width=True)

##################################      END PLOT        ########################################## 


####################        Teamwise and Positionwise VALue      ######################

fwd = Trim_elements.loc[Trim_elements.position == 'Forward']
mid = Trim_elements.loc[Trim_elements.position == 'Midfielder']
defn = Trim_elements.loc[Trim_elements.position == 'Defender']
goal = Trim_elements.loc[Trim_elements.position == 'Goalkeeper']

team_name = st.selectbox('Select a Team',teams.name)

team_seg = Trim_elements.loc[Trim_elements.team == team_name]
position_pivot = team_seg.pivot_table(index='position',values='value',aggfunc=np.mean)

st.write('''## Value by Position for ''' + str(team_name))

X = {"col" : "position", "title": "Positions"}
Y = {"col" : "value", "title": "Value"}

fig = altair_plot(position_pivot, X, Y, "Positionwise Distribution", '#993dba')
st.altair_chart(fig, use_container_width=True)