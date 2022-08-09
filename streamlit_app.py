from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import openai


"""
### Welcome Back to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

openai.api_key = st.secrets["api_key"]
fine_tuned_model = st.secrets["finetune_id"]

"You can get the Id but not the Key"
st.write("Model Id:", st.secrets["finetune_id"])

def check_worthiness(tweet):
    tweet = tweet + "\n\n###\n\n"
    result = openai.Completion.create(model = fine_tuned_model, prompt=str(tweet), max_tokens=10, temperature=0)['choices'][0]['text'] 
    print('- ', tweet, ': ', result)
    return result


input = st.text_input('Input:')
if st.button('Submit'):
    st.write('**Output**')
    st.write(f"""---""")
        with st.spinner(text='In progress'):
            report_text = check_worthiness(input)
            st.markdown(report_text)

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
