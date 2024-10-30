import streamlit as st
from openai import OpenAI

# Show title and description
st.set_page_config(page_title="Document Translation", page_icon="📖", layout="wide")
st.title('''Luke's AI Doc. 파일 번역 프로그램''')
st.subheader('※ 배포금지. 개인용 유료 API key 사용 (해외시장 공통셀 전용)')    
st.text('''Instruction - txt 형식의 불량 증상 파일을 업로드하면 한국어로 번역된 txt 파일을 다운로드할 수 있습니다.''')    
st.markdown('---')

apikey = st.secrets["openai"]["apikey"]  # 환경변수나 Streamlit secrets에서 가져오기

# OpenAI Client 초기화 (api_key를 설정)
client = OpenAI(api_key=apikey)

# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt or .md)", type=("txt", "md")
)

if uploaded_file:
    # Process the uploaded file
    document = uploaded_file.read().decode()

    # Generate a translation request to the OpenAI API
    messages = [
        {
            "role": "user",
            "content": f"다음 제시된 제품 불량 증상을 전문적으로 한 줄씩 한국어로 번역해줘. 그리고 불량 증상을 카테고리화 하여 분류할 수 있게 간략히 요약한 내용도 생성해줘: 출력 양식은 제시된 제품 불량 증상 --- 한국어 번역결과 --- 카테고리화된 요약 증상으로 한 줄씩 출력해줘.  \n\n{document}",
        }
    ]

    # Generate an answer using the OpenAI API.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=16384,  # 필요에 따라 조정
    )

    # Choose the content of the first choice
    translated_text = response.choices[0].message.content  # 속성으로 접근하기

    # 다운로드 버튼
    st.download_button(
        label="Download Translated Document",
        data=translated_text,
        file_name="translated_document.txt",
        mime="text/plain"
    )

    # 번역된 내용 화면에 표시
    st.subheader("Translated Content")
    st.text(translated_text)