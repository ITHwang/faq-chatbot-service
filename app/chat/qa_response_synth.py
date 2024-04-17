from llama_index.core import ServiceContext
from llama_index.core.prompts import PromptType, PromptTemplate
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.response_synthesizers.base import BaseSynthesizer


def get_custom_response_synth(service_context: ServiceContext) -> BaseSynthesizer:
    refine_template_str = """
사용자가 스마트 스토어 FAQ에 질문을 남겼어.
원래 질문은 다음과 같아: {{query_str}}
기존 답변은 다음과 같아: {{existing_answer}}
우리는 아래의 추가적인 맥락으로 기존 답변을 개선할 수 있어.
------------
{{context_msg}}
------------
새로운 맥락을 고려하여 원래 답변을 개선하여 질문에 더 나은 답변을 제공해줘.
맥락이 유용하지 않다면 원래 답변을 반환해줘.
개선된 답변:
""".strip()
    refine_prompt = PromptTemplate(
        template=refine_template_str,
        prompt_type=PromptType.REFINE,
    )

    qa_template_str = """
사용자가 스마트 스토어 FAQ에 질문을 남겼어.
아래는 맥락 정보입니다.
---------------------
{{context_str}}
---------------------
맥락 정보와 사전 지식을 고려하여 질문에 답변해주세요.
질문: {{query_str}}
답변:
""".strip()
    qa_prompt = PromptTemplate(
        template=qa_template_str,
        prompt_type=PromptType.QUESTION_ANSWER,
    )

    return get_response_synthesizer(
        service_context,
        refine_template=refine_prompt,
        text_qa_template=qa_prompt,
        # only useful for gpt-3.5
        structured_answer_filtering=False,
    )
