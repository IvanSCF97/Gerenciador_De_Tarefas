import os
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import csv

# Nome do arquivo onde as tarefas serão salvas
ARQUIVO_TAREFAS = "tarefas.txt"

def carregar_tarefas():
    """Carrega as tarefas do arquivo, se existir."""
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'r') as arquivo:
            return [linha.strip().split("|") for linha in arquivo.readlines()]
    return []

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo."""
    with open(ARQUIVO_TAREFAS, 'w') as arquivo:
        for tarefa in tarefas:
            arquivo.write(f"{'|'.join(tarefa)}\n")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Tarefas")
        self.geometry("700x800")  # Aumentei o tamanho da janela
        self.resizable(False, False)
        self.tarefas = carregar_tarefas()

        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Modo escuro
        ctk.set_default_color_theme("green")  # Tema verde personalizado

        # Cabeçalho com título estilizado
        self.cabecalho = ctk.CTkLabel(self, text="📝 Gerenciador de Tarefas", font=("Arial", 24, "bold"))
        self.cabecalho.pack(pady=10)

        # Frame para entrada de nova tarefa
        self.frame_entrada = ctk.CTkFrame(self, corner_radius=10)
        self.frame_entrada.pack(pady=10, padx=20, fill="x")

        self.entry_tarefa = ctk.CTkEntry(self.frame_entrada, width=350, placeholder_text="Digite sua tarefa aqui...")
        self.entry_tarefa.grid(row=0, column=0, padx=10, pady=10)

        self.prioridade_var = ctk.StringVar(value="Média")
        self.menu_prioridade = ctk.CTkOptionMenu(self.frame_entrada, variable=self.prioridade_var, values=["Alta", "Média", "Baixa"])
        self.menu_prioridade.grid(row=0, column=1, padx=10, pady=10)

        self.entry_data = ctk.CTkEntry(self.frame_entrada, width=120, placeholder_text="DD/MM/AAAA")
        self.entry_data.grid(row=0, column=2, padx=10, pady=10)

        self.botao_adicionar = ctk.CTkButton(self.frame_entrada, text="➕ Adicionar", command=self.adicionar_tarefa, width=100)
        self.botao_adicionar.grid(row=0, column=3, padx=10, pady=10)

        # Lista de tarefas com rolagem
        self.frame_lista = ctk.CTkFrame(self, corner_radius=10)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.lista_tarefas = ctk.CTkTextbox(self.frame_lista, width=650, height=350, corner_radius=10)
        self.lista_tarefas.pack(padx=10, pady=10)

        # Barra de rolagem para a lista de tarefas
        self.scrollbar = ctk.CTkScrollbar(self.frame_lista, orientation="vertical", command=self.lista_tarefas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.lista_tarefas.configure(yscrollcommand=self.scrollbar.set)

        # Botões de ação
        self.frame_botoes = ctk.CTkFrame(self, corner_radius=10)
        self.frame_botoes.pack(pady=10, padx=20, fill="x")

        self.botao_editar = ctk.CTkButton(self.frame_botoes, text="✏️ Editar", command=self.editar_tarefa, fg_color="#FFC300", hover_color="#FFA500")
        self.botao_editar.grid(row=0, column=0, padx=10, pady=10)

        self.botao_remover = ctk.CTkButton(self.frame_botoes, text="❌ Remover", command=self.remover_tarefa, fg_color="#FF5733", hover_color="#C70039")
        self.botao_remover.grid(row=0, column=1, padx=10, pady=10)

        self.botao_exportar = ctk.CTkButton(self.frame_botoes, text="📤 Exportar CSV", command=self.exportar_csv, fg_color="#33CC33", hover_color="#228B22")
        self.botao_exportar.grid(row=0, column=2, padx=10, pady=10)

        self.botao_sair = ctk.CTkButton(self.frame_botoes, text="🚪 Sair", command=self.sair, fg_color="#333333", hover_color="#000000")
        self.botao_sair.grid(row=0, column=3, padx=10, pady=10)

        # Carregar tarefas na lista
        self.atualizar_lista_tarefas()
        self.verificar_notificacoes()

    def atualizar_lista_tarefas(self):
        """Atualiza a lista de tarefas exibida na interface."""
        self.lista_tarefas.delete("1.0", ctk.END)
        for i, tarefa in enumerate(self.tarefas, 1):
            descricao, prioridade, data = tarefa
            cor = {"Alta": "#FF5733", "Média": "#FFC300", "Baixa": "#33CC33"}[prioridade]
            self.lista_tarefas.insert(ctk.END, f"{i}. {descricao} | Prioridade: {prioridade} | Vencimento: {data}\n")
            self.lista_tarefas.tag_add(f"tag{i}", f"{i}.0", f"{i}.end")
            self.lista_tarefas.tag_config(f"tag{i}", foreground=cor)

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa à lista."""
        descricao = self.entry_tarefa.get().strip()
        prioridade = self.prioridade_var.get()
        data = self.entry_data.get().strip()
        if descricao and data:
            try:
                datetime.strptime(data, "%d/%m/%Y")  # Valida a data
                self.tarefas.append([descricao, prioridade, data])
                self.atualizar_lista_tarefas()
                self.entry_tarefa.delete(0, ctk.END)
                self.entry_data.delete(0, ctk.END)
            except ValueError:
                messagebox.showwarning("Aviso", "Data inválida! Use o formato DD/MM/AAAA.")
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def remover_tarefa(self):
        """Remove a tarefa selecionada da lista."""
        try:
            indice = int(self.lista_tarefas.index(ctk.INSERT).split('.')[0]) - 1
            self.tarefas.pop(indice)
            self.atualizar_lista_tarefas()
        except Exception:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")

    def editar_tarefa(self):
        """Edita a tarefa selecionada."""
        try:
            indice = int(self.lista_tarefas.index(ctk.INSERT).split('.')[0]) - 1
            tarefa_atual = self.tarefas[indice]
            self.entry_tarefa.delete(0, ctk.END)
            self.entry_tarefa.insert(0, tarefa_atual[0])
            self.prioridade_var.set(tarefa_atual[1])
            self.entry_data.delete(0, ctk.END)
            self.entry_data.insert(0, tarefa_atual[2])
            self.remover_tarefa()  # Remove a tarefa antiga
        except Exception:
            messagebox.showwarning("Aviso", "Selecione uma tarefa para editar!")

    def verificar_notificacoes(self):
        """Verifica tarefas próximas ao vencimento e exibe notificações."""
        hoje = datetime.now().date()
        for tarefa in self.tarefas:
            descricao, _, data = tarefa
            data_vencimento = datetime.strptime(data, "%d/%m/%Y").date()
            if (data_vencimento - hoje).days <= 1:
                messagebox.showinfo("Notificação", f"A tarefa '{descricao}' está próxima ou já venceu!")

    def exportar_csv(self):
        """Exporta a lista de tarefas para um arquivo CSV."""
        with open("tarefas.csv", "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["Descrição", "Prioridade", "Data de Vencimento"])
            escritor.writerows(self.tarefas)
        messagebox.showinfo("Sucesso", "Tarefas exportadas para 'tarefas.csv'!")

    def sair(self):
        """Salva as tarefas e fecha o aplicativo."""
        salvar_tarefas(self.tarefas)
        self.quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()