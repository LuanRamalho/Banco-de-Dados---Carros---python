import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class CarRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Carro")
        self.root.geometry("600x600")
        
        # Carregar dados se o arquivo existir
        if os.path.exists('cars.json'):
            with open('cars.json', 'r') as f:
                self.cars = json.load(f)
        else:
            self.cars = []

        self.selected_car_index = None

        self.create_widgets()
        self.load_table()

    def create_widgets(self):
        # Frame para o formulário de cadastro
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Ano de Fabricação:").grid(row=0, column=0, padx=10, pady=5)
        self.year_entry = tk.Entry(frame)
        self.year_entry.grid(row=0, column=1)

        tk.Label(frame, text="Fabricante:").grid(row=1, column=0, padx=10, pady=5)
        self.manufacturer_entry = tk.Entry(frame)
        self.manufacturer_entry.grid(row=1, column=1)

        tk.Label(frame, text="Tipo de Combustível:").grid(row=2, column=0, padx=10, pady=5)
        self.type_combobox = ttk.Combobox(frame, values=["Gasolina", "Etanol", "Flex", "Híbrido", "Elétrico", "GNV"])
        self.type_combobox.grid(row=2, column=1)

        tk.Label(frame, text="Placa do Carro:").grid(row=3, column=0, padx=10, pady=5)
        self.plate_entry = tk.Entry(frame)
        self.plate_entry.grid(row=3, column=1)

        tk.Label(frame, text="Cor do Carro:").grid(row=4, column=0, padx=10, pady=5)
        self.color_combobox = ttk.Combobox(frame, values=["Branco", "Cinza", "Preto", "Azul", "Amarelo", "Rosa", "Verde", "Vermelho", "Roxo", "Bege", "Laranja", "Ciano", "Marrom"])
        self.color_combobox.grid(row=4, column=1)

        self.save_button = tk.Button(frame, text="Salvar Dados", command=self.save_data)
        self.save_button.grid(row=5, columnspan=2, pady=10)

        # Frame para busca
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(search_frame, text="Buscar", command=self.search_data)
        self.search_button.grid(row=0, column=2, padx=5)

        self.table = ttk.Treeview(self.root, columns=("year", "manufacturer", "type", "plate", "color"), show='headings')
        self.table.heading("year", text="Ano")
        self.table.heading("manufacturer", text="Fabricante")
        self.table.heading("type", text="Tipo de Combustível")
        self.table.heading("plate", text="Placa")
        self.table.heading("color", text="Cor")

        self.table.bind('<ButtonRelease-1>', self.select_car)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Botões de editar, salvar e excluir
        self.edit_button = tk.Button(self.root, text="Editar", command=self.edit_data)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Excluir", command=self.delete_data)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    def load_table(self, cars=None):
        for row in self.table.get_children():
            self.table.delete(row)
        cars_to_display = cars if cars is not None else self.cars
        for car in cars_to_display:
            self.table.insert("", tk.END, values=(car['year'], car['manufacturer'], car['type'], car['plate'], car['color']))

    def save_data(self):
        car = {
            'year': self.year_entry.get(),
            'manufacturer': self.manufacturer_entry.get(),
            'type': self.type_combobox.get(),
            'plate': self.plate_entry.get(),
            'color': self.color_combobox.get()
        }

        self.cars.append(car)

        with open('cars.json', 'w') as f:
            json.dump(self.cars, f)

        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        self.year_entry.delete(0, tk.END)
        self.manufacturer_entry.delete(0, tk.END)
        self.type_combobox.set('')
        self.plate_entry.delete(0, tk.END)
        self.color_combobox.set('')
        self.load_table()

    def select_car(self, event):
        selected_item = self.table.selection()[0]
        self.selected_car_index = self.table.index(selected_item)
        car = self.cars[self.selected_car_index]

        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, car['year'])
        self.manufacturer_entry.delete(0, tk.END)
        self.manufacturer_entry.insert(0, car['manufacturer'])
        self.type_combobox.set(car['type'])
        self.plate_entry.delete(0, tk.END)
        self.plate_entry.insert(0, car['plate'])
        self.color_combobox.set(car['color'])

    def edit_data(self):
        if self.selected_car_index is not None:
            car = self.cars[self.selected_car_index]
            car['year'] = self.year_entry.get()
            car['manufacturer'] = self.manufacturer_entry.get()
            car['type'] = self.type_combobox.get()
            car['plate'] = self.plate_entry.get()
            car['color'] = self.color_combobox.get()

            with open('cars.json', 'w') as f:
                json.dump(self.cars, f)

            messagebox.showinfo("Sucesso", "Dados editados com sucesso!")
            self.load_table()
        else:
            messagebox.showwarning("Seleção", "Por favor, selecione um carro para editar.")

    def delete_data(self):
        if self.selected_car_index is not None:
            del self.cars[self.selected_car_index]
            with open('cars.json', 'w') as f:
                json.dump(self.cars, f)

            messagebox.showinfo("Sucesso", "Carro excluído com sucesso!")
            self.load_table()
            self.selected_car_index = None
        else:
            messagebox.showwarning("Seleção", "Por favor, selecione um carro para excluir.")

    def search_data(self):
        query = self.search_entry.get().lower()
        filtered_cars = [car for car in self.cars if (query in car['year'].lower() or
                                                        query in car['manufacturer'].lower() or
                                                        query in car['plate'].lower() or
                                                        query in car['type'].lower())]
        self.load_table(filtered_cars)

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRegistrationApp(root)
    root.mainloop()
