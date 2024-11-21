from system_ui.ui import UI
from datasets.data import ResumeFeaturesDataset, JobResumeMatchesDataset, LocationValidationDataset, ResumeValidationDataset

model = "gpt-4o"

ui = UI()
def handle_pdf_location_input(pdf_file, location_filter):
    pdf_file_path = pdf_file.name
    # Put integration logic here
    # Whatever you return here will be shown on the UI
    pass

ui.process_inputs = handle_pdf_location_input
ui.run()
