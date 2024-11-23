import gradio as gr

class UI:
    def __init__(self) -> None:
        self.demo = None

    def process_inputs(self, pdf_file, location_filter):
        if (pdf_file is not None) and (location_filter is not None):
            return {
                'resume_pdf_path': pdf_file.name,
                'location_filter': location_filter,
            }    
        
        return f"Location filter or Resume Not Provided."

    def run(self):
        with gr.Blocks() as demo:
            gr.Markdown("# Resumatch")
            
            pdf_file_input = gr.File(label="Upload PDF File", file_types=[".pdf"])
            location_input = gr.Textbox(label="Enter Your Desired Location")
            
            output = gr.HTML(label="Job Matches")
            
            submit_button = gr.Button("Submit")
            submit_button.click(
                fn=self.process_inputs,
                inputs=[pdf_file_input, location_input],
                outputs=output
            )

            demo.launch(share=True)

if __name__ == "__main__":
    ui = UI()
    ui.run()
