import tkinter as tk
from tkinter import ttk, messagebox
from backend import DatabaseManager

class POSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RetailPOS - Рабочее место кассира")
        self.geometry("900x600")
        
        self.db = DatabaseManager()
        self.cart = [] 
        self.total_sum = 0.0
        
        self._setup_ui()

    def _setup_ui(self):
        top_frame = tk.Frame(self, bg="#eee", pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="Штрихкод:", font=("Arial", 12), bg="#eee").pack(side=tk.LEFT, padx=10)
        
        self.entry_code = tk.Entry(top_frame, font=("Arial", 14), width=20)
        self.entry_code.pack(side=tk.LEFT, padx=5)
        self.entry_code.bind('<Return>', self.add_to_cart)
        self.entry_code.focus()
        
        tk.Button(top_frame, text="Найти / Добавить", command=self.add_to_cart, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

        columns = ("name", "price", "qty", "sum")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("name", text="Наименование")
        self.tree.column("name", width=400)
        self.tree.heading("price", text="Цена")
        self.tree.heading("qty", text="Кол-во")
        self.tree.heading("sum", text="Сумма")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        bottom_frame = tk.Frame(self, bg="#333", height=100)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_total = tk.Label(bottom_frame, text="Итого: 0.00 ₽", font=("Arial", 24, "bold"), bg="#333", fg="#fff")
        self.lbl_total.pack(side=tk.LEFT, padx=20, pady=20)
        
        btn_pay = tk.Button(bottom_frame, text="ОПЛАТИТЬ (Пробел)", font=("Arial", 16, "bold"), 
                           bg="#FF5722", fg="white", height=2, command=self.checkout)
        btn_pay.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.bind('<space>', lambda event: self.checkout())

    def add_to_cart(self, event=None):
        code = self.entry_code.get()
        if not code: return
        
        product = self.db.get_product(code)
        
        if product:
            p_id, name, bcode, price, stock, is_service = product
            
            if not is_service and stock <= 0:
                messagebox.showerror("Ошибка", f"Товара '{name}' нет на складе!")
                self.entry_code.delete(0, tk.END)
                return

            qty = 1
            item_total = price * qty
            
            self.cart.append({
                "id": p_id, "name": name, "price": price, 
                "qty": qty, "total": item_total, "is_service": is_service
            })
            
            self.tree.insert("", tk.END, values=(name, f"{price:.2f}", qty, f"{item_total:.2f}"))
            self.update_total()
            self.entry_code.delete(0, tk.END)
        else:
            messagebox.showwarning("Внимание", "Товар не найден!")

    def update_total(self):
        self.total_sum = sum(item['total'] for item in self.cart)
        self.lbl_total.config(text=f"Итого: {self.total_sum:.2f} ₽")

    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Инфо", "Корзина пуста")
            return
            
        if self.db.process_sale(self.cart, self.total_sum):
            messagebox.showinfo("Успех", f"Чек на сумму {self.total_sum:.2f} ₽ закрыт!\nТовары списаны.")
            self.cart = []
            self.update_total()
            for item in self.tree.get_children():
                self.tree.delete(item)
        else:
            messagebox.showerror("Ошибка", "Сбой при сохранении чека")

if __name__ == "__main__":
    app = POSApp()
    app.mainloop()
