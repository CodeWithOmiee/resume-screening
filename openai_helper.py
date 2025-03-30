from openai import OpenAI
from openai import AuthenticationError, APIConnectionError


def generate_ai_recommendation(resume_text, job_description, match_result, api_key):
    """Generate recommendation using OpenAI API with proper error handling"""
    prompt = f"""
    Analyze this resume against the job description and provide a professional recommendation.
    Current technical match: {match_result['percentage_match']}%
    Missing technical keywords: {', '.join(match_result['missing_keywords'][:5]) or 'None'}

    Job Requirements:
    {job_description[:1000]}

    Candidate Resume:
    {resume_text[:1000]}

    Provide a 2-3 sentence assessment focusing on:
    - Overall suitability
    - Key strengths
    - Major gaps if any
    """

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an experienced HR professional providing concise, objective candidate evaluations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,  # More deterministic output
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except AuthenticationError:
        return "Error: Invalid API key. Please check your OpenAI credentials."
    except APIConnectionError:
        return "Error: Connection failed. Please check your internet connection."
    except Exception as e:
        return f"Error generating recommendation: {str(e)}"