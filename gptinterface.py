import customtkinter as ctk
from PIL import Image
import sys
import os

import FluxoPersonalzado as FluxoPersonalzado
import FluxoSite as FluxoSite

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class RedirectLogger:
    def __init__(self, textbox, root):
        self.textbox = textbox
        self.root = root
        self.terminal = sys.__stdout__  # mantém o terminal original

    def write(self, message):
        if message.strip() != "":
            self.root.after(0, self._write_to_box, message)
        self.terminal.write(message)

    def _write_to_box(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", message)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def flush(self):
        pass


def interface():
    root_tk.configure(fg_color="#ffffff")
    root_tk.grid_columnconfigure(0, weight=1)
    root_tk.grid_columnconfigure(1, weight=0)
    root_tk.grid_columnconfigure(2, weight=1)
    root_tk.grid_rowconfigure(0, weight=1)

    # Frame esquerdo (input e botões)
    left_frame = ctk.CTkFrame(root_tk, fg_color="#ffffff")
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
    caminho_imagem = resource_path("Mitra.jpeg")

    # 2. Use esse caminho para carregar a imagem
    my_image = ctk.CTkImage(dark_image=Image.open(caminho_imagem), size=(130, 130))
    image_label = ctk.CTkLabel(left_frame, image=my_image, text="")
    image_label.pack(pady=(0, 10))

    titulo_label = ctk.CTkLabel(left_frame, text="Automação Mitra",
                                text_color="#000000", font=("Helvetica", 30, "bold"))
    titulo_label.pack(pady=(0, 20))

    usuUrl = ctk.CTkEntry(left_frame, fg_color="#FFFFFF", border_color="#4664B4",
                          placeholder_text="Digite o URL", placeholder_text_color="#000000", width=200)
    usuUrl.pack(pady=(0, 20))

    # Linha de botões
    btn_frame = ctk.CTkFrame(left_frame, fg_color="#ffffff")
    btn_frame.pack(pady=(0, 20))


    import threading

    # Dentro do interface(), troque os botões para isso:

    ctk.CTkButton(
        btn_frame,
        text="Personalizado",
        fg_color="#4664B4",
        hover_color="#314783",
        width=120,
        command=lambda: threading.Thread(
            target=FluxoPersonalzado.main, args=(usuUrl.get(),), daemon=True
        ).start()
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        btn_frame,
        text="Fluxo Site",
        fg_color="#4664B4",
        hover_color="#314783",
        width=120,
        command=lambda: threading.Thread(
            target=FluxoSite.main, daemon=True
        ).start()
    ).pack(side="left", padx=5)


    # Label "Criado por..."
    footer_label = ctk.CTkLabel(left_frame, text="Criado por Luizeras da Bahia",
                                text_color="#444444", font=("Helvetica", 12, "italic"))
    footer_label.pack(side="bottom", anchor="sw", pady=(20, 0), padx=5)

    # Linha divisória
    divider = ctk.CTkFrame(root_tk, fg_color="#000000", width=2)
    divider.grid(row=0, column=1, sticky="ns", pady=20)

    # Frame direito (log)
    right_frame = ctk.CTkFrame(root_tk, fg_color="#ffffff")
    right_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)

    log_label = ctk.CTkLabel(right_frame, text="Log", text_color="#FFFFFF", fg_color="#000000")
    log_label.pack(fill="x")

    log_box = ctk.CTkTextbox(right_frame, fg_color="#000000", text_color="#00FF00", wrap="word")
    log_box.pack(fill="both", expand=True)

    # Redireciona print para o log
    sys.stdout = RedirectLogger(log_box, root_tk)
    sys.stderr = RedirectLogger(log_box, root_tk)  # também captura erros


    # Logs iniciais

# Janela principal
root_tk = ctk.CTk()
ctk.set_appearance_mode("light")
root_tk.geometry("700x450")
root_tk.title("Automação Lipw")

interface()
root_tk.mainloop()
