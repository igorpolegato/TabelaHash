import tkinter as tk
from tkinter import messagebox

class PhonebookApp:
    def __init__(self, root):
        # Configuração inicial da janela
        root.title("Agenda telefônica com Tabela Hash")
        root.configure(bg='light gray')

        # Dicionário para armazenar os contatos e contato selecionado
        self.contacts = {}
        self.selected_contact = None

        # Frames para organização dos widgets
        entry_frame = tk.Frame(root, bg='light gray')
        entry_frame.grid(row=0, column=0, padx=10, pady=10)

        button_frame = tk.Frame(root, bg='light gray')
        button_frame.grid(row=1, column=0, padx=10, pady=10)

        # Rótulos e campos de entrada
        tk.Label(entry_frame, text="Nome", bg='light gray').grid(row=0, column=0)
        tk.Label(entry_frame, text="Endereço", bg='light gray').grid(row=1, column=0)
        tk.Label(entry_frame, text="Telefone", bg='light gray').grid(row=2, column=0)

        self.name_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()

        tk.Entry(entry_frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(entry_frame, textvariable=self.address_var).grid(row=1, column=1)
        tk.Entry(entry_frame, textvariable=self.phone_var).grid(row=2, column=1)

        # Botões para ações de adicionar, deletar, pesquisar e atualizar contatos
        tk.Button(button_frame, text="Adicionar", command=self.add_contact, bg='sky blue').grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Deletar", command=self.delete_contact, bg='sky blue').grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Pesquisar", command=self.search_contact, bg='sky blue').grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Atualizar", command=self.update_contact, bg='sky blue').grid(row=0, column=3, padx=5)

        # Listbox para exibir a lista de contatos
        self.contacts_listbox = tk.Listbox(root, height=10, width=30)
        self.contacts_listbox.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        self.contacts_listbox.bind("<<ListboxSelect>>", self.on_select_contact)
        self.update_contacts_listbox()

    # Atualiza a listbox com os nomes dos contatos
    def update_contacts_listbox(self):
        self.contacts_listbox.delete(0, tk.END)
        for name in self.contacts:
            self.contacts_listbox.insert(tk.END, name)

    # Formatar telefone para salvar
    def format_phone(self, phone):
        data = {}

        # Lista de elementos para remover do telefone
        phone_replaces = ["-", " ", "(", ")"]

        for rp in phone_replaces:
            phone = phone.replace(rp, "")

        data['clear'] = phone

        has_ddd = len(phone) == 11

        # Formata o telefone com DDD
        if has_ddd:
            data["formated"] = f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"

        # Formata o telefone sem DDD
        else:
            data["formated"] = f"{phone[:5]}-{phone[5:]}"

        return data

    # Verificar se os campos são validos antes de salvar
    def save_form(self, name, address, phone):

        # Verifica se todos os campos foram preenchidos
        if "" in [name, address, phone]:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return False

        # Verifica se o número de telefone já existe
        elif not phone.isdigit() or not len(phone) in [9, 11]:
            messagebox.showerror("Número invalido", "Número de telefone inválido!")
            return False

        # Verifica se o contato já existe
        elif name in self.contacts:
            messagebox.showerror("Erro", "Um contato com este nome já existe.")
            return False

        return True

    # Adiciona um novo contato ao dicionário
    def add_contact(self):

        # Obtem os valores dos campos de entrada
        name = self.name_var.get().strip()
        address = self.address_var.get().strip()
        phone = self.phone_var.get().strip()

        phone = self.format_phone(phone)

        if self.save_form(name, address, phone["clear"]):
            self.contacts[name] = {"address": address, "phone": phone["formated"]}
            messagebox.showinfo("Success", "Contact added successfully.")
            self.update_contacts_listbox()

    # Deleta um contato selecionado
    def delete_contact(self):

        # Obtem o nome do contato a ser deletado
        name = self.name_var.get()
        if name in self.contacts:

            del self.contacts[name]
            messagebox.showinfo("Sucesso", "Contato deletado com sucesso.")
            self.update_contacts_listbox()

        else:
            messagebox.showerror("Erro", "Contato não encontrado.")

    # Seleciona um contato da listbox e preenche os campos de entrada
    def on_select_contact(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.selected_contact = widget.get(index)
            contact = self.contacts[self.selected_contact]

            # Atualiza os campos de entrada com as informações do contato selecionado
            self.name_var.set(self.selected_contact)
            self.address_var.set(contact['address'])
            self.phone_var.set(contact['phone'])

    # Atualiza as informações de um contato existente
    def update_contact(self):
        if not self.selected_contact:
            messagebox.showerror("Erro", "Nenhum contato selecionado")
            return

        new_name = self.name_var.get().strip()
        address = self.address_var.get().strip()
        phone = self.phone_var.get().strip()

        phone = self.format_phone(phone)

        # Atualiza o contato e a listbox
        if self.save_form(None, address, phone["clear"]):
            del self.contacts[self.selected_contact]

            self.contacts[new_name] = {"address": address, "phone": phone["formated"]}
            self.selected_contact = new_name

            messagebox.showinfo("Sucesso", "Contato atualizado com sucesso.")
            self.update_contacts_listbox()

    # Procura por um contato específico
    def search_contact(self):
        search_name = self.name_var.get().strip()

        if search_name in self.contacts:
            contact = self.contacts[search_name]
            info = f"Nome: {search_name}\nEndereço: {contact['address']}\nTelefone: {contact['phone']}"

            messagebox.showinfo("Contato Encontrado", info)

        else:
            messagebox.showerror("Erro", "Contato não encontrado.")

# Inicia a aplicação
def main():
    root = tk.Tk()
    root.geometry("500x300")
    app = PhonebookApp(root)
    root.mainloop()

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
