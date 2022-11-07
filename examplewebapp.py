import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px
from sklearn.metrics import r2_score
from scipy.stats import pearsonr

# Style of plots
matplotlib.style.use('seaborn')

st.title('Headstarter Student Analysis')

df = pd.read_csv('HackathonDataset.csv')

st.write('#')

hs_students = df['Education'].value_counts()['High School']
college_students = df['Education'].value_counts()['In-College']
bs_degree = df['Education'].value_counts()['Bachelors']
masters_degree = df['Education'].value_counts()['Masters']
phd_degree = df['Education'].value_counts()['PhD']

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("High-School Students", hs_students, f"{round((hs_students / df.shape[0]), 2) * 100}%")
col2.metric("College Students", college_students, f"{round((college_students / df.shape[0]), 2) * 100}%")
col3.metric("Bachelors Degree", bs_degree, f"{round((bs_degree / df.shape[0]), 2) * 100}%")
col4.metric("Masters Degree", masters_degree, f"{round((masters_degree / df.shape[0]), 2) * 100}%")
col5.metric("PhD Degree", phd_degree, f"{round((phd_degree / df.shape[0]), 2) * 100}%")

st.write('#')

valid_cols = ['Income',
            'Days_Since_Last_Cohort', 'Amount_Spent_On_Courses',
            'Amount_Spent_on_Books', 'Minutes_Spent_on_Headstarter',
            'Questions_Completed', 'Videos_Watched', 'Minutes_Spent_Coding',
            'Email_Opens', 'Num_Courses_Purchased', 'Number_of_Students_Referred',
            'Site_Visits_Per_Month', 'Average_Teammate_Rating',
            'Cohorts_Participated_In', 'Highest_Leaderboard_Rank', 'Headstarter_Rating', 'Probability_Of_Getting_Offer']


categories = ['Education', 'Major']

category = st.selectbox(
    'Pick a category to compare',
    categories)


metric = st.selectbox(
    'Pick a metric to compare',
    valid_cols)


fig = px.box(df, x=category, y=metric, title=f"{metric} Distrubution by {category}", height=600)
fig.update_layout(template='plotly_white',xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
st.plotly_chart(fig, use_container_width=True)



df_ = df.groupby([category])[metric].median().reset_index().sort_values(metric, ascending=False)

fig2 = plt.figure(figsize=(10,6))
ax = sns.barplot(x=category, y=metric, data=df_, estimator=np.median, ci=0)
ax.set(title=f"Median {metric} across {category}")
ax.bar_label(ax.containers[0])
#ax.legend(loc='best', fontsize=25)
st.pyplot(fig2)


st.write('#')

lp_col1, lp_col2 = st.columns(2)

with lp_col1:
    lp_col1= st.selectbox('X-Axis', valid_cols)
with lp_col2:
    lp_col2 = st.selectbox('Y-Axis', valid_cols[1:])


line_plot = px.scatter(df, x=lp_col1, y=lp_col2, title=f"{lp_col1} vs {lp_col2}", trendline="ols", trendline_color_override='red')
line_plot.update_layout(template='plotly_white',xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
st.plotly_chart(line_plot, use_container_width=True)

st.subheader(f"Pearson Correlation: {round(pearsonr(df[lp_col1], df[lp_col2])[0], 2)}")


st.write('#')


metric_slider = st.selectbox('Select a metric for the slider', valid_cols)

metric_to_compare = st.selectbox('Select a metric to compare', valid_cols)


slider = st.slider(metric_slider, int(min(df[metric_slider])), int(max(df[metric_slider])), 10)

radio = st.radio(
    f"Find students with atleast {slider} {metric_slider} or atmost?",
    ('Atleast', 'Atmost'))

new_df = df[df[metric_slider] >= slider] if radio == 'Atleast' else df[df[metric_slider] <= slider] 

fig3 = plt.figure(figsize=(10,6))
ax2 = sns.barplot(x='Education', y=metric_to_compare, data=new_df, estimator=np.median, ci=0)
ax2.set(title=f"Median {metric_to_compare} across Education Levels")
ax2.bar_label(ax2.containers[0])
#ax.legend(loc='best', fontsize=25)
st.pyplot(fig3)

st.dataframe(new_df)
