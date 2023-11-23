import tkinter as tk
from tkinter import messagebox

class PhonebookApp:
    # Explicação das principais variaveis de classe

    """
    :contacts: {"name": index}

    :addresses: {"index": address}

    :phones: {"index": phone}
    """

    # Dicionarios para armazenamento das informações (as informações foram separadas para incrementar indexação)
    contacts = {}
    addresses = {}
    phones = {}

    # Index para adicionar informações evitando conflitos
    current_index = 0
    selected_contact = None

    # Função de inicialização da classe
    def __init__(self, root:tk.Tk):

        # Configuração da janela do programa
        root.title("Agenda Telefonica Com Tabela Hash")
        root.configure(bg="light gray")

        self.root = root

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
        self.update_listbox()

    # Atualizar contatos exibidos na lista
    def update_listbox(self):
        self.contacts_listbox.delete(0, tk.END)

        # self.contacts = sorted(self.contacts)

        for name in sorted(self.contacts):
           self.contacts_listbox.insert(tk.END, name)

    # Adicionar contato à lista
    def add_contact(self):

        # Valores dos campos
        name = self.name_var.get().strip()
        address = self.address_var.get().strip()
        phone = self.phone_var.get().strip()

        # Formatação do telefone para verificar tamanho e manter padronização
        phone = self.format_phone(phone)

        # Validar campos
        if self.save_form(name, address, phone["clear"]):
            # Adicionar informações do contato a lista
            self.contacts[name] = self.current_index
            self.addresses[self.current_index] = address
            self.phones[self.current_index] = phone["formated"]

            # Preencher campo com telefone formatado
            self.phone_var.set(phone["formated"])

            # Incrementar index
            self.current_index += 1

            # Atualizar lista de contatos
            self.update_listbox()

    # Apagar contato da lista
    def delete_contact(self):

        # Index do contato selecionado
        contact_index = self.contacts[self.selected_contact]

        # Remover informações antigas do contato
        del self.contacts[self.selected_contact]
        del self.addresses[contact_index]
        del self.phones[contact_index]

        # Atualizar lista de contatos
        self.update_listbox()

    def search_contact(self):

        # Nome para ser usado na busca
        name = self.name_var.get().strip()

        # Verificar se o usuário está na lista
        if name in self.contacts:
            contact_index = self.contacts[name] # Index do contato

            # Texto com as informações da busca
            infos = (f"Nome: {name}\n" +
                    f"Endereço: {self.addresses[contact_index]}\n" +
                    f"Telefone: {self.phones[contact_index]}")

            # Mostrar informações na tela
            messagebox.showinfo("Usuário encontrado", infos)

        else:
            # Alertar que o usuário não foi encontrar / não existe na lista
            messagebox.showerror("Usuário não encontrado", "Não foi possível encontrar o usuário!")

    # Atualizar contato já existente
    def update_contact(self):

        # Valores dos campos
        name = self.name_var.get().strip()
        address = self.address_var.get().strip()
        phone = self.phone_var.get().strip()

        # Formatação do telefone para verificar tamanho e manter padronização
        phone = self.format_phone(phone)

        # Validar campos
        if self.update_form(name, address, phone["clear"]):
            contact_index = self.contacts[self.selected_contact] # Index do contato a ser editado

            # Remover informações antigas do contato
            del self.contacts[self.selected_contact]
            del self.addresses[contact_index]
            del self.phones[contact_index]

            # Adicionar informações atualizadas a lista
            self.contacts[name] = self.current_index
            self.addresses[self.current_index] = address
            self.phones[self.current_index] = phone["formated"]

            # Preencher campo com telefone formatado
            self.phone_var.set(phone["formated"])

            # Incrementar index
            self.current_index += 1

            # Atualizar lista de contatos
            self.update_listbox()

    #### EVENTOS #####

    # Evento de selecionar um contato na lista
    def on_select_contact(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection:
            index = selection[0] # Index do elemento selecionado

            # Posição e contato que foi selecionado
            self.selected_contact = widget.get(index)
            contact_index = self.contacts[self.selected_contact]

            # Atualiza os campos de entrada com as informações do contato selecionado
            self.name_var.set(self.selected_contact)
            self.address_var.set(self.addresses[contact_index])
            self.phone_var.set(self.phones[contact_index])

    #### UTILS ####

    # Limpar pontuações e espaços e formatar telefone
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


    #### VALIDADORES ####

    # Validar os campos antes de salvar um contato
    def save_form(self, name, address, phone):

        # Verificar se todos os campos foram preenchidos
        if not (name and address and phone):
            messagebox.showerror("Erro", "Campo(s) inválidos!")
            return False

        # Verificar se o novo nome já existe na lista
        if name in self.contacts:
            messagebox.showerror("Erro", "Contato já existe!")
            return False

        # Verificar se o telefone é valido
        if not phone.isdigit() or not len(phone) in [9, 11]:
            messagebox.showerror("Erro", "Número invalido!")
            return False

        return True

    # Validar os campos antes de atualizar um contato
    def update_form(self, new_name, address, phone):

        # Verificar se todos os campos foram preenchidos
        if not (new_name and address and phone):
            messagebox.showerror("Erro", "Campo(s) inválidos!")
            return False

        # Verificar se o novo nome já existe na lista (se não for o mesmo do contato selecionado)
        if new_name in self.contacts and new_name != self.selected_contact:
            messagebox.showerror("Erro", "Contato já existe!")
            return False

        # Verificar se o telefone é valido
        if not phone.isdigit() or not len(phone) in [9, 11]:
            messagebox.showerror("Erro", "Número invalido!")
            return False

        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300")
    app = PhonebookApp(root)
    root.mainloop()
