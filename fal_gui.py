import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import requests
import threading
import time
import io
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"
# Define constants for API interaction
BASE_API_URL = "https://api.fal.ai/queues/"
POLLING_INTERVAL_SECONDS = 3
POLLING_TIMEOUT_SECONDS = 300 # 5 minutes

class FalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fal GUI")
        self.root.geometry("800x600")

        self.api_key_var = tk.StringVar()

        # Attempt to load API key on startup
        self.load_api_key(silent=True)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Button to open settings
        settings_button = ttk.Button(main_frame, text="Settings", command=self.open_settings_window)
        settings_button.pack(pady=5, anchor="ne") # Anchor to top right

        # Main interaction area
        self.create_main_interaction_widgets(main_frame)

        # Status Bar
        self.status_var = tk.StringVar(value="Idle")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding="2 5")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)


    def _update_status_label(self, status_text):
        self.status_var.set(status_text)
        # Force update, useful if called from a thread via root.after
        self.root.update_idletasks()

    def create_main_interaction_widgets(self, parent_frame):
        interaction_frame = ttk.Frame(parent_frame, padding="10")
        interaction_frame.pack(fill="both", expand=True)

        # Left panel for controls
        controls_frame = ttk.Frame(interaction_frame)
        controls_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Right panel for image display
        self.image_display_frame = ttk.Frame(interaction_frame, width=400, height=400) # Initial size
        self.image_display_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.image_display_frame.pack_propagate(False) # Prevent children from shrinking frame

        # Model Selection
        model_frame = ttk.Labelframe(controls_frame, text="Model", padding="5")
        model_frame.pack(fill="x", pady=5)
        self.model_ids = [
            "fal-ai/flux-pro/kontext/max/text-to-image",
            "fal-ai/flux-pro/kontext/max/multi",
            "fal-ai/flux-pro/kontext"
        ]
        self.model_var = tk.StringVar()
        self.model_combobox = ttk.Combobox(model_frame, textvariable=self.model_var, values=self.model_ids, state="readonly", width=45)
        self.model_combobox.pack(fill="x")
        self.model_combobox.set(self.model_ids[0]) # Default selection

        # Prompt Input
        prompt_frame = ttk.Labelframe(controls_frame, text="Prompt", padding="5")
        prompt_frame.pack(fill="both", expand=True, pady=5)
        self.prompt_text = tk.Text(prompt_frame, height=10, width=50, wrap=tk.WORD)
        prompt_scrollbar = ttk.Scrollbar(prompt_frame, command=self.prompt_text.yview)
        self.prompt_text.configure(yscrollcommand=prompt_scrollbar.set)
        self.prompt_text.pack(side="left", fill="both", expand=True)
        prompt_scrollbar.pack(side="right", fill="y")

        # Image URL Input
        image_url_frame = ttk.Labelframe(controls_frame, text="Image URL(s) (comma-separated)", padding="5")
        image_url_frame.pack(fill="x", pady=5)
        self.image_url_var = tk.StringVar()
        self.image_url_entry = ttk.Entry(image_url_frame, textvariable=self.image_url_var, width=48)
        self.image_url_entry.pack(fill="x")

        # API Parameters
        params_frame = ttk.Labelframe(controls_frame, text="API Parameters", padding="10")
        params_frame.pack(fill="x", pady=5)

        # Guidance Scale
        ttk.Label(params_frame, text="Guidance Scale:").grid(row=0, column=0, sticky="w", pady=2)
        self.guidance_scale_var = tk.DoubleVar(value=3.5)
        self.guidance_scale_entry = ttk.Entry(params_frame, textvariable=self.guidance_scale_var, width=5)
        self.guidance_scale_entry.grid(row=0, column=1, sticky="w", pady=2)
        # ttk.Scale(params_frame, from_=0, to=20, variable=self.guidance_scale_var, orient=tk.HORIZONTAL).grid(row=0, column=1, sticky="ew", pady=2)


        # Num Images
        ttk.Label(params_frame, text="Number of Images:").grid(row=1, column=0, sticky="w", pady=2)
        self.num_images_var = tk.IntVar(value=1)
        self.num_images_spinbox = ttk.Spinbox(params_frame, from_=1, to=10, textvariable=self.num_images_var, width=3)
        self.num_images_spinbox.grid(row=1, column=1, sticky="w", pady=2)

        # Safety Tolerance
        ttk.Label(params_frame, text="Safety Tolerance:").grid(row=2, column=0, sticky="w", pady=2)
        self.safety_tolerance_var = tk.StringVar(value="2")
        self.safety_tolerance_combobox = ttk.Combobox(params_frame, textvariable=self.safety_tolerance_var, values=[str(i) for i in range(1, 7)], state="readonly", width=3)
        self.safety_tolerance_combobox.grid(row=2, column=1, sticky="w", pady=2)

        # Output Format
        ttk.Label(params_frame, text="Output Format:").grid(row=3, column=0, sticky="w", pady=2)
        self.output_format_var = tk.StringVar(value="jpeg")
        self.output_format_combobox = ttk.Combobox(params_frame, textvariable=self.output_format_var, values=["jpeg", "png"], state="readonly", width=6)
        self.output_format_combobox.grid(row=3, column=1, sticky="w", pady=2)

        # Aspect Ratio
        ttk.Label(params_frame, text="Aspect Ratio:").grid(row=4, column=0, sticky="w", pady=2)
        self.aspect_ratio_values = ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"]
        self.aspect_ratio_var = tk.StringVar(value="1:1")
        self.aspect_ratio_combobox = ttk.Combobox(params_frame, textvariable=self.aspect_ratio_var, values=self.aspect_ratio_values, state="readonly", width=6)
        self.aspect_ratio_combobox.grid(row=4, column=1, sticky="w", pady=2)

        # Seed
        ttk.Label(params_frame, text="Seed (optional):").grid(row=5, column=0, sticky="w", pady=2)
        self.seed_var = tk.StringVar() # Optional, so can be empty
        self.seed_entry = ttk.Entry(params_frame, textvariable=self.seed_var, width=10)
        self.seed_entry.grid(row=5, column=1, sticky="w", pady=2)

        params_frame.columnconfigure(1, weight=1) # Allow entry/combobox to expand a bit if needed

        # Submit Button
        self.submit_button = ttk.Button(controls_frame, text="Generate Image", command=self.on_submit) # command to be defined
        self.submit_button.pack(pady=10, fill="x")

        # Image Display Area
        self.image_display_label = ttk.Label(self.image_display_frame, text="Generated image will appear here", relief="solid", anchor="center")
        self.image_display_label.pack(fill="both", expand=True)

        self.generated_image_urls = [] # To store results
        self.current_display_photo = None # To keep a reference to the PhotoImage

    def on_submit(self):
        api_key = self.api_key_var.get()
        if not api_key:
            messagebox.showerror("Error", "API Key is not set. Please set it in Settings.")
            return

        model_id = self.model_var.get()
        prompt = self.prompt_text.get("1.0", tk.END).strip()

        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty.")
            return

        payload_input = {"prompt": prompt}

        try:
            # Guidance Scale
            g_scale = self.guidance_scale_var.get() # This is DoubleVar
            payload_input["guidance_scale"] = g_scale

            # Num Images
            num_imgs = self.num_images_var.get() # This is IntVar
            payload_input["num_images"] = num_imgs

            # Safety Tolerance - already string, ensure it's passed as expected by API (float or int?)
            # Assuming API expects float for safety_tolerance
            safety_tol_str = self.safety_tolerance_var.get()
            if not safety_tol_str: # Should not happen with combobox, but good for future proofing
                 messagebox.showerror("Validation Error", "Safety Tolerance must be selected.")
                 return
            payload_input["safety_tolerance"] = float(safety_tol_str)

        except tk.TclError as e: # Catches errors if DoubleVar/IntVar get() fails due to invalid content
            messagebox.showerror("Validation Error", f"Invalid numeric input: {e}. Please check Guidance Scale and Number of Images.")
            return
        except ValueError as e: # More specific for float conversion if safety_tolerance were an Entry
            messagebox.showerror("Validation Error", f"Invalid value for Safety Tolerance: {e}")
            return

        payload_input["output_format"] = self.output_format_var.get()
        if not payload_input["output_format"]: # Should not happen with combobox
            messagebox.showerror("Validation Error", "Output Format must be selected.")
            return

        payload_input["aspect_ratio"] = self.aspect_ratio_var.get()
        if not payload_input["aspect_ratio"]: # Should not happen with combobox
            messagebox.showerror("Validation Error", "Aspect Ratio must be selected.")
            return

        seed_str = self.seed_var.get().strip()
        if seed_str:
            try:
                payload_input["seed"] = int(seed_str)
            except ValueError:
                messagebox.showerror("Validation Error", "Seed must be a whole number (integer).")
                return

        image_urls_str = self.image_url_var.get().strip()
        if image_urls_str:
            # Assuming models requiring image_url expect a list of strings or a single string.
            # For "multi" model, it might be `image_url` (singular) or `image_urls` (plural).
            # Let's assume `image_url` for now if it's a single URL, or handle based on model.
            # For simplicity, if model is multi or kontext, pass it.
            if "multi" in model_id or "kontext" in model_id and model_id != "fal-ai/flux-pro/kontext/max/text-to-image":
                 # Split by comma and strip spaces if multiple URLs are intended
                urls = [url.strip() for url in image_urls_str.split(',') if url.strip()]
                if urls:
                    # The specific key for image URLs might vary. `image_url` is common.
                    # If the model expects a list, assign `urls`. If a single one, `urls[0]`.
                    # The flux-pro/kontext model docs state `image_url` (string)
                    # The flux-pro/kontext/max/multi docs state `image_url` (string)
                    # So we should probably only pass one, or the API might only use the first.
                    # For this generic client, we'll pass the first one if multiple are entered.
                    payload_input["image_url"] = urls[0]
                    if len(urls) > 1:
                         messagebox.showwarning("Multiple URLs", "Multiple image URLs provided. Only the first will be used for this model type.")


        self.submit_button.config(state=tk.DISABLED)
        self._update_status_label(f"Submitting to {model_id}...")

        # Start API call in a new thread
        thread = threading.Thread(target=self._execute_api_call, args=(api_key, model_id, payload_input))
        thread.daemon = True # Allow main program to exit even if threads are running
        thread.start()

    def _execute_api_call(self, api_key, model_id, payload_input):
        try:
            submit_url = f"{BASE_API_URL}{model_id}/submit"
            headers = {
                "Authorization": f"Key {api_key}",
                "Content-Type": "application/json"
            }

            # Initial POST request to submit the job
            self.root.after(0, self._update_status_label, "Submitting job to queue...")
            response = requests.post(submit_url, headers=headers, json={"input": payload_input}, timeout=20) # Added timeout for submit
            response.raise_for_status()

            submit_response_data = response.json()
            request_id = submit_response_data.get("request_id")
            if not request_id:
                self.root.after(0, messagebox.showerror, "API Error", "Submission successful but no Request ID received.")
                raise ValueError("Request ID not found in submission response.")

            status_url = f"{BASE_API_URL}{model_id}/requests/{request_id}/status"
            result_url = f"{BASE_API_URL}{model_id}/requests/{request_id}"

            self.root.after(0, self._update_status_label, f"Submitted (ID: {request_id[:8]}...). Polling...")

            start_time = time.time()
            while True:
                if time.time() - start_time > POLLING_TIMEOUT_SECONDS:
                    raise TimeoutError("Polling timed out.")

                time.sleep(POLLING_INTERVAL_SECONDS)
                status_response = requests.get(status_url, headers=headers, timeout=10) # Added timeout for status poll
                status_response.raise_for_status()
                status_data = status_response.json()

                current_status = status_data.get("status", "UNKNOWN") # Default if key missing
                progress = status_data.get("progress") # New: check for progress if available
                eta_ms = status_data.get("eta_ms")
                queue_pos = status_data.get("queue_position")

                status_msg_parts = [f"Status: {current_status}"]
                if progress and isinstance(progress, dict):
                    percentage = progress.get("percentage")
                    if percentage is not None:
                        status_msg_parts.append(f"{percentage:.1f}%")
                if eta_ms is not None: # eta_ms can be 0
                    status_msg_parts.append(f"ETA: {eta_ms / 1000.0:.1f}s")
                if queue_pos is not None: # queue_pos can be 0
                    status_msg_parts.append(f"Queue: {queue_pos}")

                self.root.after(0, self._update_status_label, " | ".join(status_msg_parts))

                if current_status == "COMPLETED":
                    break
                elif current_status == "FAILED":
                    error_info = status_data.get("error", {})
                    error_detail = error_info.get("message", "Unknown error during processing.")
                    # Attempt to get logs if available
                    logs = status_data.get("logs", []) # Fal structure for logs
                    if not logs and "fal_logs" in status_data: # Alternative structure
                        logs = status_data.get("fal_logs", [])

                    log_messages = "\n".join([log.get("message", "") for log in logs if log.get("message")])
                    if log_messages:
                         error_detail += f"\n\nLogs:\n{log_messages}"
                    raise Exception(f"Job failed: {error_detail}") # This will be caught by general Exception handler

            # Fetch the final result
            self.root.after(0, self._update_status_label, "Fetching final result...")
            result_response = requests.get(result_url, headers=headers, timeout=20) # Added timeout for result fetch
            result_response.raise_for_status()
            final_result = result_response.json()

            # Process result - expecting structure like {"images": [{"url": ...}]}
            # Or the direct model output based on `DOCS FOR THE MODEL.md`
            self.generated_image_urls = []
            if "images" in final_result and isinstance(final_result["images"], list):
                for img_data in final_result["images"]:
                    if "url" in img_data:
                        self.generated_image_urls.append(img_data["url"])
            elif "image_url" in final_result and isinstance(final_result["image_url"], str) : # some models might return a single image_url
                 self.generated_image_urls.append(final_result["image_url"])
            elif isinstance(final_result, dict) and "url" in final_result and final_result.get("type") == "image": # Adapting to potential single image output
                 self.generated_image_urls.append(final_result["url"])


            if self.generated_image_urls:
                self.root.after(0, self._update_status_label, f"Success! {len(self.generated_image_urls)} image(s) ready. Displaying first image...")
                # Schedule the image processing and display
                self.root.after(0, self._process_and_display_images, self.generated_image_urls)
            else:
                self.root.after(0, self._update_status_label, "Completed, but no image URLs found in result.")
                self.root.after(0, self._clear_image_display) # Clear any old image
                print("Result received, but no image URLs found:", final_result)


        except requests.exceptions.HTTPError as e:
            error_msg = f"API Error ({e.response.status_code}): "
            try:
                error_json = e.response.json()
                error_detail = error_json.get('detail') or error_json.get('message') or error_json.get('error',{}).get('message') or json.dumps(error_json)
                error_msg += error_detail
            except json.JSONDecodeError:
                error_msg += e.response.text or "Could not retrieve error details."

            if e.response.status_code == 401 or e.response.status_code == 403:
                error_msg = "API Key invalid or unauthorized. Please check your API Key in Settings."

            self.root.after(0, self._update_status_label, f"Failed: {error_msg[:100]}...") # Truncate for status bar
            self.root.after(0, messagebox.showerror, "API Error", error_msg)
        except requests.exceptions.Timeout as e:
            err_str = f"Network request timed out: {e}"
            self.root.after(0, self._update_status_label, "Error: Request timed out.")
            self.root.after(0, messagebox.showerror, "Network Timeout", err_str)
        except requests.exceptions.ConnectionError as e:
            err_str = f"Network connection error: {e}. Check your internet connection."
            self.root.after(0, self._update_status_label, "Error: Connection error.")
            self.root.after(0, messagebox.showerror, "Connection Error", err_str)
        except requests.exceptions.RequestException as e: # Catch other request exceptions
            err_str = f"Network Error: {e}"
            self.root.after(0, self._update_status_label, "Error: Network issue.")
            self.root.after(0, messagebox.showerror, "Network Error", err_str)
        except json.JSONDecodeError as e:
            err_str = f"Error parsing server response (JSON): {e}. The response may not be valid JSON."
            self.root.after(0, self._update_status_label, "Error: Invalid server response.")
            self.root.after(0, messagebox.showerror, "Data Error", err_str)
        except ValueError as e: # Catch other JSON parsing errors or missing keys
            err_str = f"Data Error: {e}"
            self.root.after(0, self._update_status_label, "Error: Data handling issue.")
            self.root.after(0, messagebox.showerror, "Data Error", err_str)
        except TimeoutError as e: # This is our custom polling timeout
            err_str = f"Operation timed out after {POLLING_TIMEOUT_SECONDS}s: {e}"
            self.root.after(0, self._update_status_label, "Error: Operation timed out.")
            self.root.after(0, messagebox.showerror, "Timeout", err_str)
        except Exception as e: # Catch any other errors during the process
            err_str = f"An unexpected error occurred: {e}"
            self.root.after(0, self._update_status_label, "Error: Unexpected issue.")
            self.root.after(0, messagebox.showerror, "Unexpected Error", err_str)
        finally:
            # Re-enable submit button from the main thread
            self.root.after(0, lambda: self.submit_button.config(state=tk.NORMAL))

    def _clear_image_display(self, message="Generated image will appear here"):
        self.image_display_label.config(image=None, text=message)
        self.image_display_label.image = None # Clear reference
        self.current_display_photo = None

    def _process_and_display_images(self, image_urls):
        if not image_urls:
            self._clear_image_display("No image URLs provided.")
            return

        first_image_url = image_urls[0] # Displaying only the first image for now
        self._update_status_label(f"Downloading image from {first_image_url[:50]}...")

        # Start image download and preparation in a new thread
        # Pass the URL and a callback for when the PhotoImage is ready
        thread = threading.Thread(target=self._download_and_prepare_image_threaded, args=(first_image_url,))
        thread.daemon = True
        thread.start()

    def _download_and_prepare_image_threaded(self, image_url):
        try:
            response = requests.get(image_url, stream=True, timeout=30)
            response.raise_for_status()

            image_bytes = response.content
            if not image_bytes:
                raise IOError("Downloaded image data is empty.")

            img = Image.open(io.BytesIO(image_bytes))

            max_width = self.image_display_frame.winfo_width() if self.image_display_frame.winfo_width() > 10 else 400
            max_height = self.image_display_frame.winfo_height() if self.image_display_frame.winfo_height() > 10 else 400
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            self.root.after(0, self._update_image_label_final, photo, "Image displayed successfully.")

        except requests.exceptions.HTTPError as e:
            error_msg = f"Image download failed (HTTP {e.response.status_code}): {image_url[:100]}"
            print(f"{error_msg} - {e}")
            self.root.after(0, self._clear_image_display, "Error: Could not download image.")
            self.root.after(0, self._update_status_label, "Error: Image download failed.")
        except requests.exceptions.Timeout as e:
            error_msg = f"Image download timed out: {image_url[:100]}"
            print(f"{error_msg} - {e}")
            self.root.after(0, self._clear_image_display, "Error: Image download timed out.")
            self.root.after(0, self._update_status_label, "Error: Image download timeout.")
        except requests.exceptions.RequestException as e:
            error_msg = f"Image download error: {e}"
            print(error_msg)
            self.root.after(0, self._clear_image_display, "Error: Could not download image.")
            self.root.after(0, self._update_status_label, "Error: Image download issue.")
        except (IOError, Image.UnidentifiedImageError) as e: # Catches PIL errors more specifically
            error_msg = f"Image processing error: {e}. The image may be corrupted or in an unsupported format."
            print(error_msg)
            self.root.after(0, self._clear_image_display, "Error: Could not process image.")
            self.root.after(0, self._update_status_label, "Error: Image processing failed.")
        except Exception as e: # Catch-all for other unexpected errors
            error_msg = f"Unexpected error displaying image: {e}"
            print(error_msg)
            self.root.after(0, self._clear_image_display, "Error: Could not display image.")
            self.root.after(0, self._update_status_label, "Error: Image display failed.")


    def _update_image_label_final(self, photo_object, success_message="Image displayed."):
        if photo_object:
            self.image_display_label.config(image=photo_object, text="") # Clear text when image is shown
            self.image_display_label.image = photo_object # Keep reference!
            self.current_display_photo = photo_object # Also store here if needed for other ops
        else:
            self._clear_image_display("Failed to display image.")


    def open_settings_window(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x250")
        settings_window.transient(self.root) # Keep settings window on top of main
        settings_window.grab_set() # Modal behavior

        frame = ttk.Frame(settings_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Fal API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.api_key_entry = ttk.Entry(frame, textvariable=self.api_key_var, width=40)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(button_frame, text="Save Key", command=self.save_api_key)
        save_button.pack(side="left", padx=5)

        load_button = ttk.Button(button_frame, text="Load Key", command=self.load_api_key)
        load_button.pack(side="left", padx=5)

        self.settings_status_label = ttk.Label(frame, text="")
        self.settings_status_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Load key into entry when settings window opens
        self.load_api_key(silent=True, update_entry=True)
        if not self.api_key_var.get(): # If still empty after load attempt
             self.settings_status_label.config(text="API key not found. Please enter and save.")


    def save_api_key(self):
        api_key = self.api_key_var.get()
        if not api_key:
            if hasattr(self, 'settings_status_label'):
                self.settings_status_label.config(text="API key cannot be empty.", foreground="red")
            else: # Fallback if settings window not fully initialized
                messagebox.showerror("Error", "API key cannot be empty.")
            return

        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"api_key": api_key}, f)
            if hasattr(self, 'settings_status_label'):
                self.settings_status_label.config(text="API key saved successfully.", foreground="green")
            # Update the main app's understanding of the current key if needed immediately
        except IOError as e:
            if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                self.settings_status_label.config(text=f"Error saving key: {type(e).__name__} - {e}", foreground="red")
            else:
                messagebox.showerror("File Error", f"Error saving API key to {CONFIG_FILE}: {e}")

    def load_api_key(self, silent=False, update_entry=False):
        config_file_exists = os.path.exists(CONFIG_FILE)
        loaded_successfully = False
        try:
            if config_file_exists:
                with open(CONFIG_FILE, "r") as f:
                    # Check if file is empty
                    if os.path.getsize(CONFIG_FILE) == 0:
                        if not silent and hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                            self.settings_status_label.config(text="Config file is empty.", foreground="orange")
                        self.api_key_var.set("") # Ensure key is cleared if file is empty
                        return False # Indicate key not loaded

                    config = json.load(f)
                    loaded_key = config.get("api_key", "")
                    self.api_key_var.set(loaded_key)
                    loaded_successfully = True

                    if loaded_key and not silent:
                        if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                            self.settings_status_label.config(text="API key loaded successfully.", foreground="green")
                    elif not loaded_key and not silent : # Key is empty string in config
                        if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                           self.settings_status_label.config(text="API key is empty in config file.", foreground="orange")
            elif not silent: # Config file does not exist
                if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                    self.settings_status_label.config(text="Config file not found. Enter and save a key.", foreground="orange")

            if update_entry and hasattr(self, 'api_key_entry'): # Ensure entry is updated even if key is empty
                self.api_key_entry.delete(0, tk.END)
                if loaded_successfully:
                    self.api_key_entry.insert(0, self.api_key_var.get())

            return loaded_successfully and bool(self.api_key_var.get())

        except json.JSONDecodeError as e:
            error_msg = f"Error: Config file '{CONFIG_FILE}' is malformed and cannot be read: {e}"
            print(error_msg) # Log to console for debugging
            self.api_key_var.set("") # Clear any potentially partially loaded key
            if not silent:
                if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                    self.settings_status_label.config(text="Config file is corrupted.", foreground="red")
                else:
                    messagebox.showerror("Config Error", error_msg) # Show critical error if settings window not open
            return False
        except IOError as e: # Covers file not found if os.path.exists failed, or permission issues
            error_msg = f"Error reading config file '{CONFIG_FILE}': {e}"
            print(error_msg)
            self.api_key_var.set("")
            if not silent:
                if hasattr(self, 'settings_status_label') and self.settings_status_label.winfo_exists():
                    self.settings_status_label.config(text=f"Error reading config: {e}", foreground="red")
                else:
                    messagebox.showerror("File Error", error_msg)
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = FalGUI(root)
    root.mainloop()
