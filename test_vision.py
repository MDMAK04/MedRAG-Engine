from backend.services.vision_agent import extract_images_from_pdf, analyze_image
from pathlib import Path

pdf_path = str(Path("Data/uploads/Book.pdf"))

print("Extracting high-res images and text...")
images = extract_images_from_pdf(pdf_path, max_images_per_page=5)

if len(images) == 0:
    print("No images found.")
else:
    target_page = 5
    target_image = None
    
    for img in images:
        if img["page"] == target_page:
            target_image = img
            break
    
    if target_image is None:
        target_image = images[-1]
    
    print(f"Analyzing page {target_image['page']} with text context...")
    
    question = "What does this graph show? Describe the X-axis, Y-axis, and the trends."
    answer = analyze_image(question, target_image["image"], target_image.get("text", ""))
    
    print("\n--- VISION MODEL RESPONSE ---")
    print(answer)