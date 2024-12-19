import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('data/skillshare.csv', encoding='latin1')


st.set_page_config(page_title='Skillshare Top 100 Courses Evaluation Dashboard', layout='wide')

st.title('Skillshare Top 100 Courses Evaluation Dashboard')
st.caption('EDUC 5144 final project - Yue Zhao, 2024')

st.write('Skillshare is an online learning environment providing a diverse range of classes in creative areas. The Skillshare Course Evaluation Dashboard is designed to display the basic and feedback information for the Top 100 courses on the Skillshare platform. ')


st.header('Overall Evaluation')
col1, col2 = st.columns(2)

with col1:
    st.subheader('Course Rating Review')
    st.markdown('This section displays the numbers of the overall ratings for the top 100 courses on Skillshare. The ratings range from 1 to 5.')
    
    # The bar chart for 'rating'
    overall_rating_fig = px.bar(
        df['rating'].value_counts().rename_axis('Rating').reset_index(name='Count'),
        x='Rating',
        y='Count',
        labels={'Rating': 'Rating', 'Count': 'Count'},
    )
    st.plotly_chart(overall_rating_fig)


with col2:
    st.subheader('Course Level Review')
    st.markdown('This section displays the proportion of the course levels for the top 100 courses on Skillshare. The levels include Beginner and Senior Level.')
    
    # The pie chart for 'level'
    level_counts = df['level'].value_counts().reset_index()
    level_counts.columns = ['Level', 'Count']
    level_fig = px.pie(
        level_counts,
        names='Level',
        values='Count',
    )
    st.plotly_chart(level_fig)


st.subheader('Course Completion Rate and Time Duration')
st.markdown('This section displays the course completion rate and time duration for the top 100 courses on Skillshare, exploring the relationship between them. Hover over the points to see the course title.')

# The scatterplot for 'course duration' vs 'completion rate'
scatter_fig = px.scatter(
    df,
    x='course duration',
    y='completion rate',
    labels={'course duration': 'Course Duration(min)', 'completion rate': 'Completion Rate(%)'},
    hover_data=['Title']
)
st.plotly_chart(scatter_fig, use_container_width=True)


st.header('Evaluation for Each Course')

course_titles = df['Title'].unique()
selected_course = st.selectbox('Select a course', course_titles)

course_data = df[df['Title'] == selected_course].iloc[0]


col1, col2 = st.columns(2)

with col1:
    st.subheader('Course Details')
    st.write(f"**Title:** {course_data['Title']}")
    st.write(f"**Instructor:** {course_data['instructor']}")
    st.write(f"**Students Count:** {course_data['students count']}")
    st.write(f"**Course Duration:** {course_data['course duration']} minutes")
    st.write(f"**Lessons Count:** {course_data['lessons count']}")
    st.write(f"**Level:** {course_data['level']}")
    st.write(f"**Student Projects:** {course_data['student projects']}")
    st.write(f"**Completion Rate:** {course_data['completion rate'] * 100}%")


with col2:
    st.subheader('Review Metrics')
    st.write('This section displays the review metrics for the selected course. The metrics include Engagement, Clarity, and Quality. Each metric is calculted as (review number/student count)*100%.')
    review_metrics = {
        'Engagement': course_data['engaging'],
        'Clarity': course_data['clarity'],
        'Quality': course_data['quality'],
    }
    review_df = pd.DataFrame(list(review_metrics.items()), columns=['Metric', 'Score'])
    
    #The bar chart for review metrics
    review_fig = px.bar(
        review_df,
        x='Metric',
        y='Score',
        title='Review Metrics',
        labels={'Metric': 'Review Metric', 'Score': 'Score(%)'},
        color='Metric'
    )
    st.plotly_chart(review_fig, use_container_width=True)




st.header('Comparison for Two Courses')

course_titles = df['Title'].unique()
selected_course_1 = st.selectbox('Select the first course', course_titles, key='course1')
selected_course_2 = st.selectbox('Select the second course', course_titles, key='course2')


course_data_1 = df[df['Title'] == selected_course_1].iloc[0]
course_data_2 = df[df['Title'] == selected_course_2].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.subheader('Course 1 Details')
    st.write(f"**Title:** {course_data_1['Title']}")
    st.write(f"**Instructor:** {course_data_1['instructor']}")
    st.write(f"**Students Count:** {course_data_1['students count']}")
    st.write(f"**Course Duration:** {course_data_1['course duration']} minutes")
    st.write(f"**Lessons Count:** {course_data_1['lessons count']}")
    st.write(f"**Level:** {course_data_1['level']}")
    st.write(f"**Student Projects:** {course_data_1['student projects']}")
    st.write(f"**Completion Rate:** {course_data_1['completion rate'] * 100}%")

with col2:
    st.subheader('Course 2 Details')
    st.write(f"**Title:** {course_data_2['Title']}")
    st.write(f"**Instructor:** {course_data_2['instructor']}")
    st.write(f"**Students Count:** {course_data_2['students count']}")
    st.write(f"**Course Duration:** {course_data_2['course duration']} minutes")
    st.write(f"**Lessons Count:** {course_data_2['lessons count']}")
    st.write(f"**Level:** {course_data_2['level']}")
    st.write(f"**Student Projects:** {course_data_2['student projects']}")
    st.write(f"**Completion Rate:** {course_data_2['completion rate'] * 100}%")


review_metrics = {
    'Metric': ['Engagement', 'Clarity', 'Quality'] * 2,
    'Score': [
        course_data_1['engaging'], course_data_1['clarity'], course_data_1['quality'],
        course_data_2['engaging'], course_data_2['clarity'], course_data_2['quality']
    ],
    'Course': [selected_course_1] * 3 + [selected_course_2] * 3
}
review_df = pd.DataFrame(review_metrics)


review_fig = px.bar(
    review_df,
    x='Metric',
    y='Score',
    color='Course',
    barmode='group',
    title='Review Metrics Comparison',
    labels={'Metric': 'Review Metric', 'Score': 'Score'}
)
st.plotly_chart(review_fig, use_container_width=True)
