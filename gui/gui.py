import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import random
import shutil

class SNN_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("SNN FPGA Digit Classifier (Test Mode)")
        self.master.geometry("400x500")
        self.master.configure(bg="#f5f7fa")

        self.image_path = None

       
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Custom.TButton",
                             font=("Segoe UI", 10, "bold"),
                             padding=6,
                             relief="flat",
                             background="#667ce7",
                             foreground="white")
        self.style.map("Custom.TButton",
                       background=[("active", "#5060d0")],
                       foreground=[("disabled", "#ccc")])

        
        self.frame = tk.Frame(master, bg="#ffffff", bd=2, relief="ridge")
        self.frame.pack(padx=20, pady=20, fill="both", expand=True)

        
        self.upload_button = ttk.Button(self.frame, text="Upload Digit Image", command=self.upload_image, style="Custom.TButton")
        self.upload_button.pack(pady=10)

       
        self.canvas = tk.Canvas(self.frame, width=140, height=140, bg="#e9ecef", bd=0, highlightthickness=1, relief="ridge")
        self.canvas.pack(pady=10)

        
        self.send_button = tk.Button(self.frame, text="Send to FPGA (Mock)", command=self.send_to_fpga,
                                     state='disabled', bg="#667ce7", fg="white",
                                     font=("Segoe UI", 10, "bold"), width=24, relief="flat", activebackground="#5060d0")
        self.send_button.pack(pady=8)

        
        self.predict_button = tk.Button(self.frame, text="Predict (Mock)", command=self.predict,
                                        state='disabled', bg="#667ce7", fg="#ffffff",
                                        font=("Segoe UI", 10, "bold"), width=24, relief="flat", activebackground="#5060d0")
        self.predict_button.pack(pady=8)

       
        self.result_label = tk.Label(self.frame, text="", font=("Segoe UI", 14, "bold"),
                                     bg="#ffffff", fg="#333")
        self.result_label.pack(pady=15)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            try:
                img = Image.open(file_path).resize((140, 140))
                self.tk_img = ImageTk.PhotoImage(img)
                self.canvas.create_image(70, 70, image=self.tk_img)
                self.send_button.config(state='normal')
                self.result_label.config(text="")
                print(f"[DEBUG] Uploaded image: {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to load image: {e}")
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def preprocess_image(self, image_path):
        try:
            img = Image.open(image_path).convert("L")  
            img = ImageOps.invert(img)  
            img = img.resize((28, 28))  
            processed_path = "normalized_input.png"
            img.save(processed_path)
            print(f"[DEBUG] Image preprocessed and saved as: {processed_path}")
            return processed_path
        except Exception as e:
            raise RuntimeError(f"Image preprocessing failed: {e}")

    def send_to_fpga(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image uploaded.")
            return

        try:
            print(f"[DEBUG] Starting simulated send for: {self.image_path}")
            processed = self.preprocess_image(self.image_path)
            shutil.copy(processed, "input_simulated.png")
            print("[DEBUG] Simulated image transfer complete.")
            messagebox.showinfo("Success", "Image 'sent' to simulated FPGA.")
            self.predict_button.config(state='normal')
        except Exception as e:
            print(f"[ERROR] Exception in send_to_fpga: {e}")
            messagebox.showerror("Error", f"Simulated send failed: {e}")

    def predict(self):
        try:
            print("[DEBUG] Simulating FPGA prediction...")
            fake_prediction = random.randint(0, 9)
            with open("result.txt", "w") as f:
                f.write(str(fake_prediction))

            self.result_label.config(text=f"Predicted Digit: {fake_prediction}")
            print(f"[DEBUG] Prediction complete: {fake_prediction}")
        except Exception as e:
            print(f"[ERROR] Prediction error: {e}")
            messagebox.showerror("Error", f"Simulated prediction failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SNN_GUI(root)
    root.mainloop()
