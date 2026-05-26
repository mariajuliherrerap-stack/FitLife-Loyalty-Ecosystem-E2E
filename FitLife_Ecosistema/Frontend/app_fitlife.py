import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sqlite3

class AppFitLife:
    def __init__(self, root):
        self.root = root
        self.root.title("FitLife - Sistema de Fidelización")
        self.root.geometry("450x600")
        self.root.configure(bg="#f4f6f7")
        self.root.resizable(False, False)
        
        # Identidad Visual
        try:
            ruta_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
            img = Image.open(ruta_logo).convert("RGB").resize((120, 120), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.logo_img, bg="#f4f6f7").pack(pady=10)
        except Exception:
            tk.Label(self.root, text="💪 FITLIFE REWARDS", font=("Arial", 18, "bold"), bg="#f4f6f7", fg="#1a252f").pack(pady=10)
        
        # Módulos CRUD
        frame_crud = tk.Frame(self.root, bg="#f4f6f7")
        frame_crud.pack(pady=10)
        
        tk.Button(frame_crud, text="➕ Registrar Compra", bg="#0984e3", fg="white", width=25, font=("Arial", 11, "bold"), command=self.crear).pack(pady=5)
        tk.Button(frame_crud, text="📖 Auditar Puntos", bg="#e17055", fg="white", width=25, font=("Arial", 11, "bold"), command=self.leer).pack(pady=5)
        tk.Button(frame_crud, text="✏️ Modificar Factura", bg="#f39c12", fg="white", width=25, font=("Arial", 11, "bold"), command=self.actualizar).pack(pady=5)
        tk.Button(frame_crud, text="🗑️ Eliminar Transacción", bg="#d63031", fg="white", width=25, font=("Arial", 11, "bold"), command=self.eliminar).pack(pady=5)
        
        tk.Label(self.root, text="Panel de Dirección Comercial", font=("Arial", 10, "italic"), bg="#f4f6f7", fg="#7f8c8d").pack(pady=15)
        tk.Button(self.root, text="📊 ABRIR POWER BI", bg="#2c3e50", fg="white", font=("Arial", 12, "bold"), width=25, command=self.abrir_pbi).pack(pady=5)

    def ruta_db(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend", "fitlife_fidelizacion.db")

    def crear(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("300x320")
        ventana.title("Registro de Compras")
        ventana.grab_set()
        
        tk.Label(ventana, text="ID Cliente (1-5):").pack(pady=2)
        e_cli = tk.Entry(ventana, justify="center")
        e_cli.pack(pady=2)
        
        tk.Label(ventana, text="ID Sede (101-103):").pack(pady=2)
        e_sede = tk.Entry(ventana, justify="center")
        e_sede.pack(pady=2)
        
        tk.Label(ventana, text="Monto de la Compra ($):").pack(pady=2)
        e_monto = tk.Entry(ventana, justify="center")
        e_monto.pack(pady=2)
        
        tk.Label(ventana, text="Fecha (YYYY-MM-DD):").pack(pady=2)
        e_fec = tk.Entry(ventana, justify="center")
        e_fec.pack(pady=2)
        
        def guardar():
            try:
                monto = float(e_monto.get())
                # Lógica del Reto 4: Bono del 10% si es Oro (>10M), 5% si Plata (>5M)
                bono = monto * 0.10 if monto >= 10000000 else (monto * 0.05 if monto >= 5000000 else 0)
                
                with sqlite3.connect(self.ruta_db()) as conn:
                    conn.cursor().execute("INSERT INTO fact_transacciones (id_cliente, id_sede, monto_compra, bono_entregado, fecha) VALUES (?, ?, ?, ?, ?)",
                                          (int(e_cli.get()), int(e_sede.get()), monto, bono, e_fec.get()))
                    conn.commit()
                messagebox.showinfo("Éxito", f"Compra registrada.\nBono generado: ${bono:,.2f}", parent=ventana)
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=ventana)
                
        tk.Button(ventana, text="💾 Guardar Compra", command=guardar, bg="#0984e3", fg="white").pack(pady=15)

    def leer(self):
        ventana = tk.Toplevel(self.root)
        ventana.geometry("650x300")
        ventana.title("Auditoría de Lealtad")
        ventana.grab_set()
        
        tabla = ttk.Treeview(ventana, columns=("ID", "Cliente", "Sede", "Compra ($)", "Bono ($)"), show="headings")
        for col in tabla["columns"]: tabla.heading(col, text=col)
        tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            with sqlite3.connect(self.ruta_db()) as conn:
                registros = conn.cursor().execute('''SELECT f.id_transaccion, c.nombre, s.nombre_sede, f.monto_compra, f.bono_entregado 
                                                     FROM fact_transacciones f JOIN dim_clientes c ON f.id_cliente = c.id_cliente 
                                                     JOIN dim_sedes s ON f.id_sede = s.id_sede''').fetchall()
                for r in registros: tabla.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        v = tk.Toplevel(self.root)
        v.geometry("300x200")
        tk.Label(v, text="ID Transacción a corregir:").pack(pady=5)
        e_id = tk.Entry(v, justify="center")
        e_id.pack(pady=5)
        tk.Label(v, text="Nuevo Monto de Compra ($):").pack(pady=5)
        e_monto = tk.Entry(v, justify="center")
        e_monto.pack(pady=5)
        
        def exec_act():
            try:
                monto = float(e_monto.get())
                bono = monto * 0.10 if monto >= 10000000 else (monto * 0.05 if monto >= 5000000 else 0)
                with sqlite3.connect(self.ruta_db()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE fact_transacciones SET monto_compra=?, bono_entregado=? WHERE id_transaccion=?", (monto, bono, int(e_id.get())))
                    if cursor.rowcount == 0: raise ValueError("ID no existe.")
                    conn.commit()
                messagebox.showinfo("Éxito", "Factura y bono recalculados.", parent=v)
                v.destroy()
            except Exception as e: messagebox.showerror("Error", str(e), parent=v)
        tk.Button(v, text="Actualizar", command=exec_act, bg="#f39c12", fg="white").pack(pady=10)

    def eliminar(self):
        v = tk.Toplevel(self.root)
        v.geometry("300x150")
        tk.Label(v, text="ID Transacción a ELIMINAR:").pack(pady=10)
        e_id = tk.Entry(v, justify="center")
        e_id.pack(pady=5)
        def exec_del():
            try:
                with sqlite3.connect(self.ruta_db()) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM fact_transacciones WHERE id_transaccion=?", (int(e_id.get()),))
                    if cursor.rowcount == 0: raise ValueError("ID no existe.")
                    conn.commit()
                messagebox.showinfo("Borrado", "Registro eliminado permanentemente.", parent=v)
                v.destroy()
            except Exception as e: messagebox.showerror("Error", str(e), parent=v)
        tk.Button(v, text="🗑️ Eliminar", command=exec_del, bg="#d63031", fg="white").pack(pady=10)

    def abrir_pbi(self):
        try:
            os.startfile(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "FitLife_Dashboard.pbix"))
        except Exception as e:
            messagebox.showerror("Error", "Asegúrese de guardar Power BI como 'FitLife_Dashboard.pbix'.")