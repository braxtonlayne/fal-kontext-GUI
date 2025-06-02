# Fal API GUI Client

## Description
A simple Graphical User Interface (GUI) application built with Python and Tkinter to interact with Fal AI's image generation models. It allows users to easily set parameters, generate images, and view them.

## Features
*   Securely connect to the Fal API using your API key.
*   Select from the following Fal image generation models:
    *   `fal-ai/flux-pro/kontext/max/text-to-image` (Text-to-Image)
    *   `fal-ai/flux-pro/kontext/max/multi` (Multi-modal, can use text and/or image URL)
    *   `fal-ai/flux-pro/kontext` (Context-aware, can use text and/or image URL)
*   Input a text prompt for image generation.
*   Adjust various generation parameters:
    *   Guidance Scale
    *   Number of Images
    *   Safety Tolerance
    *   Output Format (JPEG/PNG)
    *   Aspect Ratio
    *   Seed (optional)
    *   Image URL(s) (for compatible models)
*   View the generated image(s) directly within the application.
*   Settings page to save and load your Fal API key locally (stored in `config.json`).

## Requirements
*   Python 3.7 or newer.
*   Python packages: `requests`, `Pillow`. (Install via `requirements.txt`)
*   A Fal API Key.

## Setup Instructions
1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    (Or download the `fal_gui.py` and `requirements.txt` files directly.)

2.  **Install Dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    Then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Get a Fal API Key:**
    *   You need an API key from Fal AI to use this application.
    *   Visit the [Fal AI website](https://fal.ai/) and sign up or log in to obtain your API key.

## Running the Application
1.  **Run the Script:**
    ```bash
    python fal_gui.py
    ```

2.  **Set API Key:**
    *   On the first run (or if `config.json` is not present), the application will not have your API key.
    *   Click the **"Settings"** button in the GUI.
    *   Enter your Fal API Key in the input field and click **"Save Key"**.
    *   The key will be saved to a `config.json` file in the same directory as the script for future sessions. You can also use "Load Key" if the file already exists.

3.  **Generate Images:**
    *   Select a model from the dropdown.
    *   Enter your prompt.
    *   Adjust parameters as needed.
    *   Click **"Generate Image"**.
    *   The status bar at the bottom will show the progress, and the image will appear in the right-hand panel.

## Parameters Overview
*   **Model:** The Fal AI model to use for generation.
*   **Prompt:** The textual description of the image you want to generate.
*   **Image URL(s):** For models like `fal-ai/flux-pro/kontext/max/multi` and `fal-ai/flux-pro/kontext`, you can provide a URL to an existing image to influence the generation (e.g., for image-to-image tasks or style transfer). If providing multiple URLs, separate them with a comma (though the current GUI version primarily uses the first URL for these models).
*   **Guidance Scale:** Controls how much the model adheres to the prompt (e.g., 3.5). Higher values mean stricter adherence.
*   **Number of Images:** How many images to generate (e.g., 1-4). The GUI currently displays the first image.
*   **Safety Tolerance:** A numeric value (1-6) to control content safety filtering. Default is 2.
*   **Output Format:** Choose "jpeg" or "png" for the generated image.
*   **Aspect Ratio:** The desired aspect ratio of the image (e.g., "1:1", "16:9").
*   **Seed:** An optional integer to control randomness. Using the same seed with the same prompt and parameters should produce similar images.

---
This GUI provides a convenient way to experiment with Fal AI's powerful image models. Enjoy!
