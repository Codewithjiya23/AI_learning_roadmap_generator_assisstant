
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Learning Roadmap Generator")

st.title("🎯 AI Learning Roadmap Generator")
st.write("Create your personalized learning plan!")

field = st.text_input("What do you want to learn?")

level = st.selectbox(
    "Your current level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.selectbox(
    "Time available",
    ["1 month", "3 months", "6 months", "1 year"]
)

hours = st.slider("Study hours per week", 1, 40, 10)

if st.button("Generate Roadmap"):
    if not field.strip():
        st.warning("Please enter a learning field.")
    else:
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])

            prompt = f"""
            Create a practical learning roadmap for {field}.
            Skill level: {level}
            Duration: {duration}
            Study time: {hours} hours per week.

            Include weekly topics, free resources, practice,
            hands-on projects, and a final project.
            Make the plan realistic and easy to follow.
            """

            with st.spinner("Generating your roadmap..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert learning mentor."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

            roadmap = response.choices[0].message.content
            st.markdown(roadmap)

            st.download_button(
                "Download Roadmap",
                data=roadmap,
                file_name="my_learning_roadmap.md"
            )

        except Exception as e:
            st.error(f"Error: {e}")
