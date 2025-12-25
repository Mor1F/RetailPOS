import tkinter as tk
from tkinter import ttk, messagebox
from backend import DatabaseManager

class WarehouseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RetailPOS - Склад и Номенклатура")
        self.geometry("400x350")
        
        self.db = DatabaseManager()
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Добавление товара", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = tk.Frame(self, padx=20)
        form_frame.pack(fill=tk.X)

        tk.Label(form_frame, text="Наименование:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = tk.Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Штрихкод:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_code = tk.Entry(form_frame, width=30)
        self.entry_code.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Цена (руб):").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_price = tk.Entry(form_frame, width=30)
        self.entry_price.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Начальный остаток:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_stock = tk.Entry(form_frame, width=30)
        self.entry_stock.grid(row=3, column=1, pady=5)

        self.is_service_var = tk.IntVar()
        chk = tk.Checkbutton(form_frame, text="Это услуга (не вести учет остатков)", variable=self.is_service_var)
        chk.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        btn_save = tk.Button(self, text="Сохранить товар", bg="#2196F3", fg="white", 
                             font=("Arial", 12), command=self.save_product)
        btn_save.pack(pady=20, fill=tk.X, padx=20)

    def save_product(self):
        name = self.entry_name.get()
        code = self.entry_code.get()
        price = self.entry_price.get()
        stock = self.entry_stock.get()
        is_service = self.is_service_var.get()

        if not name or not code or not price:
            messagebox.showwarning("Ошибка", "Заполните основные поля!")
            return

        try:
            success = self.db.add_product(name, code, float(price), int(stock or 0), is_service)
            
            if success:
                messagebox.showinfo("Успех", f"Товар '{name}' добавлен!")
                self.entry_name.delete(0, tk.END)
                self.entry_code.delete(0, tk.END)
                self.entry_price.delete(0, tk.END)
                self.entry_stock.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Товар с таким штрихкодом уже существует!")
        except ValueError:
            messagebox.showerror("Ошибка", "Цена и Остаток должны быть числами!")

if __name__ == "__main__":
    app = WarehouseApp()
    app.mainloop()
