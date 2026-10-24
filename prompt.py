
import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="PromptLab AI",
    page_icon="🧪",
    layout="wide"
)

st.title("PromptLab AI")
st.subheader("Prompt Engineering Experimentation")

st.write(
    "Experiment with different prompt engineering techniques "
    "and observe how they influence AI-generated responses."
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Set it in the terminal and restart the app.")
    st.stop()

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"

techniques = {
    "Zero-Shot Prompting": (
        "Answer the user's request directly without examples.\n\n"
    ),
    "Few-Shot Prompting": (
        "Learn from these examples and follow the same pattern.\n"
        "Example 1: Input: Happy | Sentiment: Positive\n"
        "Example 2: Input: Terrible | Sentiment: Negative\n"
        "Example 3: Input: Wonderful | Sentiment: Positive\n"
        "Now respond to the user's request using the pattern above.\n\n"
    ),
    "Role-Based Prompting": (
        "Act as an experienced, friendly teacher. "
        "Explain clearly using beginner-friendly language and examples.\n\n"
    ),
    "Structured Prompting": (
        "Organize your response using these sections:\n"
        "1. Definition\n"
        "2. Key Points\n"
        "3. Example\n"
        "4. Conclusion\n\n"
    ),
    "Step-by-Step Prompting": (
        "Explain the important steps in a clear numbered sequence. "
        "Provide the final answer at the end.\n\n"
    )
}

prompt = st.text_area(
    "Enter your prompt",
    placeholder="Example: Explain artificial intelligence to a beginner.",
    height=130
)

technique = st.selectbox(
    "Choose Prompt Engineering Technique",
    list(techniques.keys())
)

col1, col2 = st.columns(2)

with col1:
    generate = st.button(
        "Generate Response",
        use_container_width=True
    )

with col2:
    compare = st.button(
        "Compare All Techniques",
        use_container_width=True
    )


def generate_response(instruction, user_prompt):
    result = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Follow the supplied instructions carefully."
                )
            },
            {
                "role": "user",
                "content": instruction + user_prompt
            }
        ],
        temperature=0.7,
        max_tokens=400
    )

    return result.choices[0].message.content


if generate:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            with st.spinner("Generating AI response..."):
                response = generate_response(
                    techniques[technique],
                    prompt
                )

            st.subheader("Selected Technique")
            st.write(technique)

            st.subheader("Prompt Instructions")
            st.code(techniques[technique] + prompt)

            st.subheader("AI-Generated Response")
            st.write(response)

        except Exception as error:
            st.error("Unable to generate a response. Please try again.")
            st.caption(str(error))


if compare:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        st.subheader("Comparison of Prompting Techniques")

        for name, instruction in techniques.items():
            with st.expander(name, expanded=True):
                st.caption("Prompt Instructions")
                st.code(instruction + prompt)

                try:
                    with st.spinner(f"Testing {name}..."):
                        response = generate_response(
                            instruction,
                            prompt
                        )

                    st.markdown("**AI-Generated Response**")
                    st.write(response)

                except Exception as error:
                    st.error(f"Could not generate response for {name}.")
                    st.caption(str(error))