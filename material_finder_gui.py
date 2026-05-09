import gradio as gr
from material_finder_agent import get_learning_material, get_word_meaning

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
