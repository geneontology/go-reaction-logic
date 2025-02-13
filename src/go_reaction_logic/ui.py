# Instantiate the engine
from typing import List

import gradio as gr
from go_reaction_logic.main import GOReactionEngine

engine = GOReactionEngine()
print(f"Engine instantiated: {engine}")  # Debugging: Print to console


def get_chemicals(go_mf1: str, go_mf2: str) -> str:
    """
    Get the chemicals involved in a reaction between two GO molecular functions.

    Example:

        >>> get_chemicals("GO:0047918", "GO:0008446")
        ['CHEBI:57527: GDP-alpha-D-mannose(2-)']

    :param go_mf1:
    :param go_mf2:
    :return:
    """
    try:
        print(f"Finding chemicals for {go_mf1} and {go_mf2}")  # Debugging: Print to console
        intermediates = engine.compute_intermediates(go_mf1.strip(), go_mf2.strip())
        return "\n".join([f"{chem.id}: {chem.label}" for chem in intermediates])
    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging: Print to console
        return f"Error: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("## Find Intermediate Chemicals in a Reaction")
    with gr.Row():
        go_mf1 = gr.Textbox(label="Enter First GO MF ID", placeholder="e.g., GO:0047918")
        go_mf2 = gr.Textbox(label="Enter Second GO MF ID", placeholder="e.g., GO:0008446")
    submit_button = gr.Button("Find Chemicals")
    output = gr.Textbox(label="Chemicals Involved", lines=5, visible=True, interactive=True)


    submit_button.click(fn=get_chemicals, inputs=[go_mf1, go_mf2], outputs=output)

demo.launch(debug=True)