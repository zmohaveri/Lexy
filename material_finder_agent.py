from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import dotenv

dotenv.load_dotenv()

# Initialize model once
model = init_chat_model(model='gpt-4o', model_provider="openai")

prompt_template = PromptTemplate.from_template(
    '''
    You are a German learning assistant for a user with a German level **{level}**.
    Generate a **{format}** related to **{concept}** that is appropriate for this level.
    Only output the material. No English text.
    '''
)

dictionary_prompt_template = PromptTemplate.from_template(
    '''
    Explain the meaning of **{word}** for Someone with german level of **{level}**.
    Only use German. Do not use English.
    '''
)


def get_learning_material(concept, level, format):
    format_mapping = {
        'Text': 'text',
        'Liedtexte': 'song lyrics',
        'Kurzgeschichte': 'short story',
        'Neuigkeit': 'news article',
    }

    mapped_format = format_mapping.get(format)
    if not mapped_format:
        raise ValueError(f"Unsupported format: {format}")

    prompt = prompt_template.format(level=level, format=mapped_format, concept=concept)
    response = model.invoke(prompt)
    return response.content


def get_word_meaning(word, level):
    prompt = dictionary_prompt_template.format(word=word, level=level)
    return model.invoke(prompt).content
