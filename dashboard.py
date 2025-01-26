import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('/teamspace/studios/this_studio/fivetwo/final_data_without_embeddings.csv', parse_dates=['date'])
    return df

df = load_data()

st.sidebar.header('Filters')
date_range = st.sidebar.date_input(
    "Date range",
    value=[df['date'].min(), df['date'].max()],
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

users = st.sidebar.multiselect(
    'Select Users',
    options=df['user'].unique(),
    default=df['user'].unique()
)

departments = st.sidebar.multiselect(
    'Select Departments',
    options=df['department'].unique(),
    default=df['department'].unique()
)

filtered_df = df[
    (df['date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))) &
    (df['user'].isin(users)) &
    (df['department'].isin(departments))
]

st.title('Employee Activity Dashboard')

st.header('Filtered Data')
st.dataframe(filtered_df, use_container_width=True)

st.header('Basic Statistics')
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", filtered_df.shape[0])
col2.metric("Unique Users", filtered_df['user'].nunique())
col3.metric("Unique Projects", filtered_df['projects'].nunique())

st.header('Visualizations')

fig = px.line(filtered_df, x='date', y='time_diff', 
             title='Time Difference Over Time',
             labels={'time_diff': 'Time Difference (seconds)'})
st.plotly_chart(fig)

st.subheader('Personality Traits Distribution')
trait = st.selectbox('Select Trait', ['O', 'C', 'E', 'A', 'N'])
fig = px.histogram(filtered_df, x=trait, nbins=20)
st.plotly_chart(fig)

st.subheader('Department Analysis')
dept_stats = filtered_df.groupby('department').agg({
    'user': 'nunique',
    'projects': 'nunique',
    'time_diff': 'mean'
}).reset_index()
st.dataframe(dept_stats, use_container_width=True)

st.subheader('User Activity Breakdown')
user_activity = filtered_df['user'].value_counts().reset_index()
user_activity.columns = ['User', 'Activity Count']
fig = px.bar(user_activity, x='User', y='Activity Count')
st.plotly_chart(fig)

st.subheader('File Operations Analysis')
col1, col2 = st.columns(2)

with col1:
    st.write("### File Extensions Distribution")
    ext_counts = filtered_df['extension'].value_counts()
    st.bar_chart(ext_counts)

with col2:
    st.write("### Drive Letter Usage")
    drive_counts = filtered_df['driveletter'].value_counts()
    st.bar_chart(drive_counts)

st.header('Advanced Statistics')
if st.checkbox('Show detailed statistics'):
    st.write(filtered_df.describe())

if st.button('Export Filtered Data'):
    filtered_df.to_csv('filtered_data.csv', index=False)
    st.success('Data exported successfully!')