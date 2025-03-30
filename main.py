import streamlit as st
import json
import time  # Import time for simulating delay
from matcher import calculate_match, generate_recommendation
from openai_helper import generate_ai_recommendation


def main():
    """Main Streamlit application with secure API key input"""
    st.set_page_config(page_title="Resume Screening System", layout="wide")
    st.title("🔍 Resume Screening System")
    st.write("Upload or paste resume and job description to evaluate match")

    # Sidebar for input method and AI options
    st.sidebar.header("Settings")
    input_method = st.sidebar.radio("Input Method:", ("Paste text", "Upload files"))
    use_ai = st.sidebar.checkbox("Enable AI-powered recommendations")

    openai_key = ""
    if use_ai:
        openai_key = st.sidebar.text_input("Enter your OpenAI API key:",
                                           type="password",
                                           help="Your key is used only for this session and not stored")
        st.sidebar.markdown("[Get your OpenAI API key](https://platform.openai.com/api-keys)")

    resume_text = ""
    job_description = ""

    # Handle text input or file upload
    if input_method == "Paste text":
        resume_text = st.text_area("Paste Resume Text:", height=200)
        job_description = st.text_area("Paste Job Description:", height=200)
    else:
        resume_file = st.file_uploader("Upload Resume (txt)", type=["txt"])
        jd_file = st.file_uploader("Upload Job Description (txt)", type=["txt"])

        if resume_file:
            resume_text = resume_file.read().decode("utf-8")
        if jd_file:
            job_description = jd_file.read().decode("utf-8")

    if st.button("Evaluate"):
        if not resume_text or not job_description:
            st.error("⚠️ Please provide both resume and job description")
            return

        if use_ai and not openai_key:
            st.error("⚠️ Please provide an OpenAI API key for AI recommendations")
            return

        # Show spinner
        with st.spinner("🔄 Analyzing documents... Please wait."):
            time.sleep(1)  # Simulating a delay for better UX
            match_result = calculate_match(resume_text, job_description)
            recommendation, thoughts = generate_recommendation(match_result)

            # Prepare output
            output = {
                "percentage_match": match_result["percentage_match"],
                "missing_keywords": match_result["missing_keywords"],
                "final_thoughts": thoughts,
                "recommendation": recommendation
            }

            # Generate AI recommendation if requested
            if use_ai and openai_key:
                try:
                    ai_thoughts = generate_ai_recommendation(
                        resume_text,
                        job_description,
                        match_result,
                        openai_key
                    )
                    output["ai_recommendation"] = ai_thoughts
                    output["final_thoughts"] = ai_thoughts
                except Exception as e:
                    output["ai_error"] = str(e)
                    st.warning(f"⚠️ AI recommendation failed: {e}")

        st.success("✅ Analysis complete!")

        # Display results
        st.subheader("Results")
        st.metric("Match Percentage", f"{output['percentage_match']}%")
        st.metric("Recommendation", output['recommendation'])

        with st.expander("📌 Detailed Analysis"):
            st.write(output['final_thoughts'])

            if output['missing_keywords']:
                st.write("**🔴 Missing Keywords:**")
                st.write(", ".join(output['missing_keywords']))
            else:
                st.write("✅ No missing keywords found!")

        # Show JSON output
        st.subheader("📝 JSON Output")
        st.code(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()