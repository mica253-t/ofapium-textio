#!/usr/bin/env python3
"""
Éditeur de Texte Graphique en Python (tkinter)
Fonctionne sur tous les OS (macOS, Windows, Linux)
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Éditeur de Texte (Python Tkinter)")
        self.root.geometry("900x700")
        
        self.current_file = "sans_titre.txt"
        
        # Créer la zone de texte D'ABORD
        self.text_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Courier New", 11),
            undo=True,
            maxundo=-1
        )
        
        # Créer le menu APRÈS
        self.create_menu()
        
        # Créer la barre d'outils
        self.create_toolbar()
        
        # Empiler la zone de texte
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Créer la barre de statut
        self.status_bar = tk.Label(
            root,
            text="Prêt",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind pour les raccourcis clavier
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Ouvrir", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Sauvegarder", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Sauvegarder Sous", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Statistiques", command=self.show_statistics)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Édition
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Annuler", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Rétablir", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Couper", command=lambda: self.cut_text(), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copier", command=lambda: self.copy_text(), accelerator="Ctrl+C")
        edit_menu.add_command(label="Coller", command=lambda: self.paste_text(), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Sélectionner tout", command=lambda: self.select_all(), accelerator="Ctrl+A")
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)
    
    def create_toolbar(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        buttons = [
            ("Nouveau", self.new_file),
            ("Ouvrir", self.open_file),
            ("Sauvegarder", self.save_file),
            ("Sauvegarder Sous", self.save_as_file),
        ]
        
        for text, command in buttons:
            btn = tk.Button(toolbar, text=text, command=command, width=15)
            btn.pack(side=tk.LEFT, padx=2)
    
    def new_file(self):
        if self.text_area.get(1.0, tk.END).strip():
            result = messagebox.askyesno(
                "Nouveau fichier",
                "Êtes-vous sûr de vouloir créer un nouveau fichier?"
            )
            if not result:
                return
        
        self.text_area.delete(1.0, tk.END)
        self.current_file = "sans_titre.txt"
        self.root.title(f"Éditeur de Texte - {self.current_file}")
        self.status_bar.config(text="Nouveau fichier créé")
    
    def open_file(self):
        # Forcer la fenêtre au premier plan sur macOS
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        file_path = filedialog.askopenfilename(
            parent=self.root,
            title="Ouvrir un fichier",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        
        if file_path and len(file_path) > 0:
            try:
                # Lire le fichier
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Effacer et insérer le contenu
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert("1.0", content)
                
                # Mettre à jour les infos
                self.current_file = file_path
                self.root.title(f"Éditeur de Texte - {os.path.basename(file_path)}")
                self.status_bar.config(text=f"Fichier ouvert: {file_path}")
                messagebox.showinfo("Succès", f"Fichier ouvert:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier:\n{str(e)}")
        else:
            self.status_bar.config(text="Ouverture annulée")
    
    def save_file(self):
        if self.current_file == "sans_titre.txt":
            self.save_as_file()
            return
        
        try:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(content)
            
            self.status_bar.config(text=f"Fichier sauvegardé: {self.current_file}")
            messagebox.showinfo("Succès", f"Fichier sauvegardé: {self.current_file}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier: {e}")
    
    def save_as_file(self):
        # Forcer la fenêtre au premier plan sur macOS
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        
        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Sauvegarder sous",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")],
            initialfile="document.txt",
            initialdir=os.path.expanduser("~")
        )
        
        if file_path and len(file_path) > 0:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                
                self.current_file = file_path
                self.root.title(f"Éditeur de Texte - {os.path.basename(file_path)}")
                self.status_bar.config(text=f"Fichier sauvegardé: {file_path}")
                messagebox.showinfo("Succès", f"Fichier sauvegardé:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder le fichier:\n{str(e)}")
        else:
            self.status_bar.config(text="Sauvegarde annulée")
    
    def cut_text(self):
        try:
            self.text_area.event_generate("<<Cut>>")
        except:
            pass
    
    def copy_text(self):
        try:
            self.text_area.event_generate("<<Copy>>")
        except:
            pass
    
    def paste_text(self):
        try:
            self.text_area.event_generate("<<Paste>>")
        except:
            pass
    
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return "break"
    
    def show_statistics(self):
        content = self.text_area.get(1.0, tk.END)
        
        char_count = len(content) - 1  # Exclure le dernière newline
        line_count = len(content.split("\n")) - 1
        word_count = len(content.split())
        
        stats = f"""
Statistiques:
━━━━━━━━━━━━━━━━━
Caractères: {char_count}
Lignes: {line_count}
Mots: {word_count}
"""
        messagebox.showinfo("Statistiques", stats)
    
    def show_about(self):
        messagebox.showinfo(
            "À propos",
            "Éditeur de Texte (Python Tkinter)\n\n"
            "Un éditeur de texte simple et efficace\n"
            "Sauvegarde au format .txt\n\n"
            "© 2024"
        )

def main():
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
