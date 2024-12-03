import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Load data with specified encoding
df = pd.read_csv('data/skillshare.csv', encoding='latin1')

# Set page title
st.set_page_config(page_title='Skill Courses Evaluation Dashboard', layout='wide')

st.title('Skill Courses Evaluation Dashboard')

st.write('Final assignment - Yue Zhao, 2024')

# Dashboard A
st.header('Overall Evaluation')
col1, col2 = st.columns(2)

with col1:
    st.subheader('Overall Rating')
    st.markdown('This section displays the numbers of the overall ratings for the top 100 courses on Skillshare.')
    # Create a bar chart for 'overall rating'
    st.bar_chart(df['overall rating'].value_counts())

with col2:
    st.subheader('Course Level')
    st.markdown('This section displays the proportion of the course levels for the top 100 courses on Skillshare.')
    # Create a pie chart for 'level'
    level_counts = df['level'].value_counts()
    level_counts = level_counts.reset_index()
    level_counts.columns = ['Level', 'Count']
    fig, ax = plt.subplots()
    ax.pie(level_counts['Count'], labels=level_counts['Level'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)


# Dashboard B
st.header('Evaluation for Each Course')

# Dropdown menu to select a course
course_titles = df['Title'].unique()
selected_course = st.selectbox('Select a course', course_titles)

# Filter data for the selected course
course_data = df[df['Title'] == selected_course].iloc[0]

# Create two columns
col1, col2 = st.columns(2)

# Display course details in the first column
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

# Display review metrics in the second column
with col2:
    st.subheader('Review Metrics')
    review_metrics = {
        'Engaging': course_data['engaging'],
        'Clarity': course_data['clarity'],
        'Quality': course_data['quality'],
    }
    review_df = pd.DataFrame(list(review_metrics.items()), columns=['Metric', 'Count'])

    # Create a bar chart for review metrics using Altair
    chart = alt.Chart(review_df).mark_bar().encode(
        x=alt.X('Metric', title='Review Metric'),
        y=alt.Y('Count', title='Score')
    ).properties(
        title='Review Metrics'
    )

    st.altair_chart(chart, use_container_width=True)