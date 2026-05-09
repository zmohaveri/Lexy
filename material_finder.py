from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import gradio as gr
import dotenv

dotenv.load_dotenv()

prompt_template = PromptTemplate.from_template(
  '''
  You are a German learning assistant for a user with a German level **{level}**.
  Generate a **{format}** related to **{concept}** that is appropriate for this level.
  Only output the material. No English text.
  '''
)
model = init_chat_model(model='gpt-4o',model_provider="openai")

def get_learning_material(concept,level,format):
  format_mapping = {
    'Text':'text','Liedtexte':'song lyrics',
    'Kurzgeschichte':'short story','Neuigkeit':'news article'
  }
  format = format_mapping[format] #TODO: enforce keywords within range
  prompt = prompt_template.format(level=level,format=format,concept=concept)
  response = model.invoke(prompt)
  return response.content

dictionary_prompt_template = PromptTemplate.from_template('''
Explain the meaning of **{word}** for Someone with german level of **{level}**.
Only use German. Do not use English.
''')
def get_word_meaning(word,level):
  prompt = dictionary_prompt_template.format(word=word,level=level)
  return model.invoke(prompt).content
  
with gr.Blocks() as demo:
  with gr.Row():
    concept_input= gr.Textbox(label="Concept", lines=1)
    level_input = gr.Radio(['A1','A2','B1','B2','C1','C2'],label="Niveau")
    format_input = gr.Radio(['Text','Liedtexte','Kurzgeschichte','Neuigkeit'],label="Format")
  output = gr.Textbox('Lernmaterial', lines=5)
  for input_component in [concept_input,level_input,format_input]:
    input_component.change(
      fn = get_learning_material,
      inputs = [concept_input,level_input,format_input],
      outputs = output
    )
  with gr.Row():
    #gr.Markdown("Wörterbuch")
    word_input= gr.Textbox(label="Wörterbuch",lines=1)
    word_output = gr.Textbox('Bedeutung', lines=5)
    word_input.change(
      fn = get_word_meaning,
      inputs = [word_input,level_input],
      outputs= word_output
    )
'''
    title="AI Concept Explainer",
    description="Über welches Thema möchtest du heute etwas lernen?"
'''

if __name__ == "__main__":
    demo.launch()